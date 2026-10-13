"""Run a captured Mo alignment pilot and score an independent held-out cohort.

Usage (from this directory):
    python prepare.py
    python run.py --task multifin --phase baseline
    python run.py --task multifin --phase train
    python run.py --task multifin --phase align
    python run.py --task multifin --phase final

Phases can be resumed. Evaluation decisions never capture examples. During
training, each worker annotates its captured example before taking another row.
"""

from __future__ import annotations

import argparse
import hashlib
import json
import os
import random
import statistics
import time
from concurrent.futures import ThreadPoolExecutor, as_completed
from pathlib import Path
from typing import Any

from modaic import Modaic, ModaicAPIError, ModaicError, ModaicTimeoutError

from tasks import BASE_MODEL, TASKS, Task

ROOT = Path(__file__).resolve().parent
DATA = ROOT / "data"
OUTPUTS = ROOT / "outputs"
TERMINAL = {"completed", "failed", "cancelled"}


def read_json(path: Path, default: Any = None) -> Any:
    return json.loads(path.read_text()) if path.exists() else default


def save_json(path: Path, value: Any) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    temp = path.with_suffix(path.suffix + ".tmp")
    temp.write_text(json.dumps(value, indent=2, ensure_ascii=False, default=str) + "\n")
    temp.replace(path)


def read_jsonl(path: Path) -> dict[str, dict]:
    if not path.exists():
        return {}
    return {row["id"]: row for line in path.read_text().splitlines() if line.strip() for row in [json.loads(line)]}


def append_jsonl(path: Path, value: dict) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    with path.open("a") as out:
        out.write(json.dumps(value, ensure_ascii=False, default=str) + "\n")


def key(task: Task, cohort: dict, phase: str, row: dict) -> str:
    body = f"{task.slug}|{cohort['sha256']}|{phase}|{row['id']}"
    return "finance-uplift-" + hashlib.sha256(body.encode()).hexdigest()[:48]


def get_or_create(client: Modaic, task: Task, cohort: dict, workspace: str):
    slug = f"finance-{task.slug}-mo-{cohort['sha256'][:8]}"
    try:
        model = client.models.get(workspace=workspace, model=slug)
    except ModaicAPIError as error:
        if error.status_code != 404:
            raise
        created = client.models.create(
            workspace=workspace, slug=slug,
            description=f"Finance uplift pilot: {task.slug}; test rows excluded from alignment",
            model=BASE_MODEL, questions={task.question_id: task.question},
        )
        print(f"created {workspace}/{slug}: {created.id}", flush=True)
        model = client.models.get(workspace=workspace, model=slug)
    if model.configuration.model != BASE_MODEL:
        raise RuntimeError(f"unexpected base model: {model.configuration.model}")
    return model


def decision_record(model, task: Task, cohort: dict, row: dict, phase: str, revision: str) -> dict:
    started = time.perf_counter()
    try:
        result = model.decisions.create(
            state=row["state"], revision=revision, capture=False,
            idempotency_key=key(task, cohort, phase, row),
        )
        answer = result.answers[task.question_id]
        return {
            "id": row["id"], "truth": row["truth"], "prediction": answer.choice,
            "confidence": answer.confidence, "probabilities": answer.probabilities,
            "latency_s": round(time.perf_counter() - started, 4),
            "revision": revision,
        }
    except ModaicError as error:
        return {"id": row["id"], "error": f"{type(error).__name__}: {error}"}


def evaluate(model, task: Task, cohort: dict, phase: str, revision: str, workers: int) -> dict[str, dict]:
    rows = cohort["eval_rows"]
    path = OUTPUTS / f"{task.slug}.{phase}.jsonl"
    existing = read_jsonl(path)
    pending = [row for row in rows if existing.get(row["id"], {}).get("revision") != revision or "error" in existing.get(row["id"], {})]
    print(f"{task.slug} {phase}: {len(rows) - len(pending)} done, {len(pending)} pending", flush=True)
    with ThreadPoolExecutor(max_workers=workers) as pool:
        futures = [pool.submit(decision_record, model, task, cohort, row, phase, revision) for row in pending]
        for index, future in enumerate(as_completed(futures), 1):
            record = future.result()
            append_jsonl(path, record)
            existing[record["id"]] = record
            if index % 25 == 0 or index == len(pending):
                errors = sum("error" in r for r in existing.values())
                print(f"  {index}/{len(pending)} new decisions; {errors} errors", flush=True)
    if any("error" in existing.get(row["id"], {}) for row in rows):
        raise RuntimeError(f"{task.slug} {phase} has failed decisions; rerun this phase")
    return existing


def annotate_captured(model, task: Task, example_id: str, truth: str) -> str:
    for attempt in range(8):
        try:
            example = model.examples.annotate(example_id, ground_truth={task.question_id: truth})
            if not example.annotation or example.annotation.split not in {"train", "test"}:
                raise RuntimeError(f"annotation missing split for {example_id}")
            return example.annotation.split
        except ModaicAPIError as error:
            if error.status_code != 404 or attempt == 7:
                raise
            time.sleep(min(0.5 * 2 ** attempt, 5))
    raise RuntimeError("annotation visibility retries exhausted")


def training_record(model, task: Task, cohort: dict, row: dict, revision: str) -> dict:
    try:
        result = model.decisions.create(
            state=row["state"], revision=revision, capture=True,
            idempotency_key=key(task, cohort, "train", row),
        )
        if not result.example_id or not result.captured:
            raise RuntimeError("decision was not captured")
        answer = result.answers[task.question_id]
        # Capture creates the example without a label. Add the source label as
        # soon as this decision returns, while other rows are still running.
        split = annotate_captured(model, task, result.example_id, row["truth"])
        return {
            "id": row["id"], "example_id": result.example_id,
            "decision_id": result.decision_id, "truth": row["truth"],
            "prediction": answer.choice, "confidence": answer.confidence,
            "split": split, "revision": revision,
        }
    except Exception as error:
        return {"id": row["id"], "error": f"{type(error).__name__}: {error}"}


def train(model, task: Task, cohort: dict, revision: str, workers: int) -> dict[str, dict]:
    rows = cohort["train_rows"]
    if len(rows) > 200:
        raise RuntimeError("label cap exceeded")
    path = OUTPUTS / f"{task.slug}.train.jsonl"
    existing = read_jsonl(path)
    pending = [row for row in rows if not existing.get(row["id"], {}).get("split")]
    print(f"{task.slug} train: {len(rows) - len(pending)} labeled, {len(pending)} pending", flush=True)
    with ThreadPoolExecutor(max_workers=workers) as pool:
        futures = [pool.submit(training_record, model, task, cohort, row, revision) for row in pending]
        for index, future in enumerate(as_completed(futures), 1):
            record = future.result()
            append_jsonl(path, record)
            existing[record["id"]] = record
            if index % 25 == 0 or index == len(pending):
                errors = sum("error" in r for r in existing.values())
                print(f"  {index}/{len(pending)} captured and labeled; {errors} errors", flush=True)
    if any(not existing.get(row["id"], {}).get("split") for row in rows):
        raise RuntimeError(f"{task.slug} has unlabeled training examples; rerun train")
    print(f"  Platform splits: train={sum(r['split']=='train' for r in existing.values())}, test={sum(r['split']=='test' for r in existing.values())}", flush=True)
    return existing


def wait_alignment_and_batch(client: Modaic, model, task: Task, state: dict, state_path: Path, max_metric_calls: int) -> dict:
    if not state.get("alignment_id"):
        job = model.jobs.alignments.create(
            branch="main", source_commit_sha=state["baseline_revision"],
            max_metric_calls=max_metric_calls,
            idempotency_key=f"finance-uplift-align-{task.slug}-{state['cohort_sha256'][:16]}",
        )
        state["alignment_id"] = job.id
        save_json(state_path, state)
        print(f"{task.slug} alignment queued: {job.id}", flush=True)
    while True:
        try:
            job = client.alignments.wait(state["alignment_id"], timeout=300, poll_interval=10)
        except ModaicTimeoutError:
            print(f"{task.slug} alignment still running", flush=True)
            continue
        if job.status in TERMINAL:
            break
    state["alignment_status"] = job.status
    state["result_revision"] = job.result_commit_sha or state["baseline_revision"]
    state["alignment_result"] = job.result
    save_json(state_path, state)
    if job.status != "completed":
        raise RuntimeError(f"{task.slug} alignment {job.status}: {job.error}")
    if not job.result_commit_sha:
        print(f"{task.slug} alignment completed without a new checkpoint", flush=True)
        state["batch_status"] = "not_applicable"
        return state
    print(f"{task.slug} alignment completed at {job.result_commit_sha[:10]}; waiting for follow-up batch", flush=True)
    batch_id = state.get("batch_id")
    while not batch_id:
        batches = model.jobs.batch_decisions.list(limit=20).batch_decisions
        matched = [b for b in batches if b.source_commit_sha == job.result_commit_sha]
        if matched:
            batch_id = matched[0].id
            state["batch_id"] = batch_id
            save_json(state_path, state)
            break
        time.sleep(10)
    while True:
        try:
            batch = client.batch_decisions.wait(batch_id, timeout=300, poll_interval=10)
        except ModaicTimeoutError:
            print(f"{task.slug} follow-up batch still running", flush=True)
            continue
        if batch.status in TERMINAL:
            break
    state["batch_status"] = batch.status
    state["batch_progress"] = batch.progress.model_dump() if batch.progress else None
    save_json(state_path, state)
    if batch.status != "completed" or (batch.progress and batch.progress.failed):
        raise RuntimeError(f"{task.slug} follow-up batch {batch.status}: {batch.progress}")
    print(f"{task.slug} follow-up batch completed", flush=True)
    return state


def score(task: Task, baseline: dict[str, dict], final: dict[str, dict], rows: list[dict]) -> dict:
    ids = [row["id"] for row in rows]
    if any(i not in baseline or i not in final for i in ids):
        raise RuntimeError("paired evaluation is incomplete")
    before = [baseline[i]["prediction"] == baseline[i]["truth"] for i in ids]
    after = [final[i]["prediction"] == final[i]["truth"] for i in ids]
    n = len(ids)
    deltas = [int(y) - int(x) for x, y in zip(before, after, strict=True)]
    rng = random.Random(20261013)
    bootstraps = sorted(
        100 * sum(deltas[rng.randrange(n)] for _ in range(n)) / n
        for _ in range(5000)
    )
    return {
        "n": n, "base_model": BASE_MODEL,
        "baseline_accuracy": sum(before) / n,
        "aligned_accuracy": sum(after) / n,
        "uplift_pp": (sum(after) - sum(before)) * 100 / n,
        "uplift_95pct_bootstrap_ci_pp": [bootstraps[124], bootstraps[4874]],
        "fixed_to_correct": sum(not x and y for x, y in zip(before, after, strict=True)),
        "regressed_to_wrong": sum(x and not y for x, y in zip(before, after, strict=True)),
        "baseline_p50_ms": 1000 * statistics.median(baseline[i]["latency_s"] for i in ids),
        "aligned_p50_ms": 1000 * statistics.median(final[i]["latency_s"] for i in ids),
        "task": task.slug,
    }


def main() -> None:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--task", choices=TASKS, required=True)
    parser.add_argument("--phase", choices=["baseline", "train", "align", "final"], required=True)
    parser.add_argument("--workspace", default=os.environ.get("MODAIC_WORKSPACE", "modaic_labs"))
    parser.add_argument("--workers", type=int, default=4)
    parser.add_argument("--max-metric-calls", type=int, default=200)
    args = parser.parse_args()
    if not os.environ.get("MODAIC_API_KEY"):
        parser.error("MODAIC_API_KEY is required")
    task = TASKS[args.task]
    cohort = read_json(DATA / f"{task.slug}.json")
    if not cohort or len(cohort["train_rows"]) > 200:
        raise RuntimeError("prepare the fixed cohorts first; training labels must be <=200")
    state_path = OUTPUTS / f"{task.slug}.state.json"
    state = read_json(state_path, {})
    if state and state["cohort_sha256"] != cohort["sha256"]:
        raise RuntimeError("cohort changed after this model was started")
    with Modaic(timeout=180) as client:
        model = get_or_create(client, task, cohort, args.workspace)
        state.setdefault("cohort_sha256", cohort["sha256"])
        state.setdefault("model_id", model.id)
        state.setdefault("model_path", f"{args.workspace}/{model.slug}")
        if model.id != state["model_id"]:
            raise RuntimeError("model identity changed")
        if args.phase == "baseline":
            if model.configuration.checkpoint != 0 and not state.get("baseline_revision"):
                raise RuntimeError("model already aligned before baseline")
            state.setdefault("baseline_revision", model.commit.commit_sha)
            save_json(state_path, state)
            evaluate(model, task, cohort, "baseline", state["baseline_revision"], args.workers)
        elif args.phase == "train":
            if not state.get("baseline_revision"):
                raise RuntimeError("run baseline first")
            train(model, task, cohort, state["baseline_revision"], args.workers)
        elif args.phase == "align":
            training = read_jsonl(OUTPUTS / f"{task.slug}.train.jsonl")
            if len(training) != len(cohort["train_rows"]) or any("split" not in r for r in training.values()):
                raise RuntimeError("every captured training example must be labeled before alignment")
            if not read_jsonl(OUTPUTS / f"{task.slug}.baseline.jsonl"):
                raise RuntimeError("baseline evaluation is missing")
            try:
                wait_alignment_and_batch(client, model, task, state, state_path, args.max_metric_calls)
            finally:
                save_json(state_path, state)
        else:
            if state.get("alignment_status") != "completed" or state.get("batch_status") not in {"completed", "not_applicable"}:
                raise RuntimeError("wait for alignment and follow-up batch first")
            final = evaluate(model, task, cohort, "final", state["result_revision"], args.workers)
            baseline = read_jsonl(OUTPUTS / f"{task.slug}.baseline.jsonl")
            report = score(task, baseline, final, cohort["eval_rows"])
            report.update({
                "model_path": state["model_path"], "cohort_sha256": cohort["sha256"],
                "baseline_revision": state["baseline_revision"],
                "aligned_revision": state["result_revision"],
                "alignment_id": state["alignment_id"], "batch_id": state.get("batch_id"),
                "batch_status": state["batch_status"], "training_labels": len(cohort["train_rows"]),
            })
            save_json(OUTPUTS / f"{task.slug}.report.json", report)
            print(json.dumps(report, indent=2), flush=True)
        save_json(state_path, state)


if __name__ == "__main__":
    main()
