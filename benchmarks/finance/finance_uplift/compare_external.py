"""Score Jev and GPT-6.1 Sol on the finance chart's fixed held-out cohorts.

Examples:
    python compare_external.py --plan
    python compare_external.py --models jev --limit 7
    python compare_external.py --models jev,gpt

Each request contains the task question and the row state, never the gold label.
Completed predictions are saved after every call, so an interrupted run resumes.
"""

from __future__ import annotations

import argparse
import hashlib
import json
import os
import time
from concurrent.futures import FIRST_COMPLETED, ThreadPoolExecutor, wait
from dataclasses import dataclass
from pathlib import Path
from typing import Any

import httpx

from tasks import TASKS, Task


ROOT = Path(__file__).resolve().parent
DATA = ROOT / "data"
OUTPUTS = ROOT / "outputs" / "external-comparison"
PUBLIC_REPORT = ROOT.parents[2] / "data" / "finance-external-comparison.json"
DECISIONS_URL = "https://openrouter.ai/api/alpha/decisions"
CHAT_URL = "https://openrouter.ai/api/v1/chat/completions"
CHART_TASKS = (
    "modernfinbert-sentiment",
    "fomc",
    "german-credit",
    "gold-headlines",
    "multifin",
    "sentivent-event",
    "twitter-financial-news-topic",
)
REQUEST_VERSION = "choice-v1"


@dataclass(frozen=True)
class ModelSpec:
    name: str
    model_id: str
    backend: str
    reasoning_effort: str | None = None


MODELS = {
    "jev": ModelSpec("jev", "~typesafe/jev-latest", "openrouter_decisions"),
    "gpt": ModelSpec("gpt", "openai/gpt-6.1-sol", "openrouter_chat", "medium"),
}


def read_cohorts() -> dict[str, dict[str, Any]]:
    cohorts = {}
    for slug in CHART_TASKS:
        cohort = json.loads((DATA / f"{slug}.json").read_text())
        expected_hash = cohort.pop("sha256")
        actual_hash = hashlib.sha256(
            json.dumps(cohort, sort_keys=True, ensure_ascii=False).encode()
        ).hexdigest()
        if actual_hash != expected_hash:
            raise ValueError(f"{slug}: cohort fingerprint changed")
        cohort["sha256"] = expected_hash
        task = TASKS[slug]
        rows = cohort["eval_rows"]
        if (
            cohort["task"] != slug
            or cohort["repo"] != task.repo
            or cohort["revision"] != task.revision
            or len(rows) != 200
            or len({row["id"] for row in rows}) != 200
            or any(row["truth"] not in task.criteria for row in rows)
            or any(not row["id"].startswith(task.eval_split + "-") for row in rows)
        ):
            raise ValueError(f"{slug}: evaluation cohort does not match its pinned task")
        cohorts[slug] = cohort
    return cohorts


def decision_body(spec: ModelSpec, task: Task, state: dict[str, Any]) -> dict[str, Any]:
    question = task.question
    return {
        "model": spec.model_id,
        "state": state,
        "questions": {
            task.question_id: {"type": question.type, **question.model_dump(exclude_unset=True)}
        },
    }


def chat_body(spec: ModelSpec, task: Task, state: dict[str, Any]) -> dict[str, Any]:
    labels = list(task.criteria)
    return {
        "model": spec.model_id,
        "messages": [
            {
                "role": "system",
                "content": (
                    "Choose exactly one label for the decision question. Use only the supplied "
                    "state. Return only the requested JSON object.\n"
                    + json.dumps({"instructions": task.instructions, "criteria": task.criteria}, ensure_ascii=False)
                ),
            },
            {"role": "user", "content": json.dumps({"state": state}, ensure_ascii=False)},
        ],
        "response_format": {
            "type": "json_schema",
            "json_schema": {
                "name": "finance_choice",
                "strict": True,
                "schema": {
                    "type": "object",
                    "properties": {"choice": {"type": "string", "enum": labels}},
                    "required": ["choice"],
                    "additionalProperties": False,
                },
            },
        },
        "provider": {"require_parameters": True},
        "reasoning": {"effort": spec.reasoning_effort},
        "max_completion_tokens": 2048,
    }


def parse_prediction(spec: ModelSpec, task: Task, response: dict[str, Any]) -> str:
    if spec.backend == "openrouter_decisions":
        answer = response.get("answers", {}).get(task.question_id)
        if not isinstance(answer, dict) or answer.get("type") != "choice":
            raise ValueError("OpenRouter returned no Choice answer")
        prediction = answer.get("choice")
    else:
        choices = response.get("choices")
        if not isinstance(choices, list) or not choices:
            raise ValueError("OpenRouter returned no chat choice")
        content = choices[0].get("message", {}).get("content")
        answer = json.loads(content)
        if not isinstance(answer, dict) or set(answer) != {"choice"}:
            raise ValueError("GPT did not return the required JSON object")
        prediction = answer["choice"]
    if prediction not in task.criteria:
        raise ValueError(f"invalid predicted label: {prediction!r}")
    return prediction


def score_row(client: httpx.Client, spec: ModelSpec, task: Task, row: dict[str, Any]) -> dict[str, Any]:
    # The request builders only receive the state, never row['truth'].
    body = (decision_body(spec, task, row["state"]) if spec.backend == "openrouter_decisions"
            else chat_body(spec, task, row["state"]))
    url = DECISIONS_URL if spec.backend == "openrouter_decisions" else CHAT_URL
    for attempt in range(4):
        started = time.perf_counter()
        try:
            response = client.post(url, json=body)
            latency_ms = (time.perf_counter() - started) * 1000
            if response.status_code in {429, 502, 503, 504}:
                if attempt == 3:
                    response.raise_for_status()
                time.sleep(2 ** attempt)
                continue
            response.raise_for_status()
            payload = response.json()
            if not isinstance(payload, dict):
                raise ValueError("OpenRouter returned a non-object response")
            prediction = parse_prediction(spec, task, payload)
            result = {
                "task": task.slug,
                "id": row["id"],
                "prediction": prediction,
                "latency_ms": round(latency_ms, 2),
            }
            for key in ("model", "provider"):
                if isinstance(payload.get(key), str):
                    result["served_model" if key == "model" else key] = payload[key]
            return result
        except (httpx.TransportError, json.JSONDecodeError, ValueError):
            if attempt == 3:
                raise
            time.sleep(2 ** attempt)
    raise AssertionError("unreachable retry state")


def run_model(
    client: httpx.Client,
    spec: ModelSpec,
    cohorts: dict[str, dict[str, Any]],
    output_dir: Path,
    workers: int,
    limit: int | None,
) -> None:
    output_dir.mkdir(parents=True, exist_ok=True)
    path = output_dir / f"{spec.name}.jsonl"
    metadata_path = output_dir / f"{spec.name}.run.json"
    metadata = {
        "model_id": spec.model_id,
        "backend": spec.backend,
        "reasoning_effort": spec.reasoning_effort,
        "request_version": REQUEST_VERSION,
        "workers": workers,
        "cohort_sha256": {slug: cohort["sha256"] for slug, cohort in cohorts.items()},
        "questions": {
            slug: {"instructions": TASKS[slug].instructions, "criteria": TASKS[slug].criteria}
            for slug in CHART_TASKS
        },
    }
    if metadata_path.exists():
        if json.loads(metadata_path.read_text()) != metadata:
            raise ValueError(f"{spec.name}: run metadata changed; use a new output directory")
    elif path.exists():
        raise ValueError(f"{spec.name}: predictions lack run metadata")
    else:
        metadata_path.write_text(json.dumps(metadata, indent=2, ensure_ascii=False) + "\n")

    known = {(slug, row["id"]) for slug, cohort in cohorts.items() for row in cohort["eval_rows"]}
    completed = {}
    if path.exists():
        for line in path.read_text().splitlines():
            if not line.strip():
                continue
            record = json.loads(line)
            row_key = record["task"], record["id"]
            if row_key not in known or row_key in completed or record["prediction"] not in TASKS[row_key[0]].criteria:
                raise ValueError(f"{spec.name}: duplicate or invalid existing prediction")
            completed[row_key] = record

    remaining = [
        (TASKS[slug], cohorts[slug]["eval_rows"][index])
        for index in range(200)
        for slug in CHART_TASKS
        if (slug, cohorts[slug]["eval_rows"][index]["id"]) not in completed
    ]
    if limit is not None:
        remaining = remaining[:limit]
    print(f"{spec.name}: {len(completed)}/{len(known)} saved; {len(remaining)} new calls", flush=True)
    if not remaining:
        return
    with path.open("a") as sink, ThreadPoolExecutor(max_workers=workers) as pool:
        rows_to_run = iter(remaining)
        pending = {}

        def submit_next() -> None:
            try:
                task, row = next(rows_to_run)
            except StopIteration:
                return
            pending[pool.submit(score_row, client, spec, task, row)] = (task.slug, row["id"])

        for _ in range(workers):
            submit_next()
        saved = 0
        while pending:
            done, _ = wait(pending, return_when=FIRST_COMPLETED)
            for future in done:
                row_key = pending.pop(future)
                try:
                    record = future.result()
                except Exception as error:
                    for unfinished in pending:
                        unfinished.cancel()
                    raise RuntimeError(f"{spec.name} failed on {row_key}") from error
                sink.write(json.dumps(record, ensure_ascii=False) + "\n")
                sink.flush()
                saved += 1
                if saved % 50 == 0:
                    print(f"{spec.name}: {len(completed) + saved}/{len(known)} saved", flush=True)
                submit_next()
    print(f"{spec.name}: {len(completed) + saved}/{len(known)} saved", flush=True)


def build_report(cohorts: dict[str, dict[str, Any]], output_dir: Path) -> dict[str, Any]:
    models = {}
    for name, spec in MODELS.items():
        path = output_dir / f"{name}.jsonl"
        if not path.exists():
            raise ValueError(f"{name}: no predictions")
        metadata = json.loads((output_dir / f"{name}.run.json").read_text())
        if (
            metadata.get("model_id") != spec.model_id
            or metadata.get("reasoning_effort") != spec.reasoning_effort
            or metadata.get("request_version") != REQUEST_VERSION
            or metadata.get("cohort_sha256") != {
                slug: cohort["sha256"] for slug, cohort in cohorts.items()
            }
        ):
            raise ValueError(f"{name}: run metadata does not match this comparison")
        predictions = {}
        served_models = set()
        providers = set()
        for line in path.read_text().splitlines():
            if line.strip():
                record = json.loads(line)
                row_key = record["task"], record["id"]
                if row_key in predictions:
                    raise ValueError(f"{name}: duplicate prediction {row_key}")
                predictions[row_key] = record["prediction"]
                if record.get("served_model"):
                    served_models.add(record["served_model"])
                if record.get("provider"):
                    providers.add(record["provider"])
        task_results = {}
        for slug in CHART_TASKS:
            rows = cohorts[slug]["eval_rows"]
            expected = {(slug, row["id"]) for row in rows}
            if not expected <= predictions.keys():
                raise ValueError(f"{name}/{slug}: incomplete predictions")
            correct = sum(predictions[(slug, row["id"])] == row["truth"] for row in rows)
            task_results[slug] = {"n": len(rows), "correct": correct, "accuracy": correct / len(rows)}
        if len(predictions) != 200 * len(CHART_TASKS):
            raise ValueError(f"{name}: unexpected prediction count")
        models[name] = {
            "model_id": spec.model_id,
            "backend": spec.backend,
            "reasoning_effort": spec.reasoning_effort,
            "workers": metadata["workers"],
            "served_models": sorted(served_models),
            "providers": sorted(providers),
            "tasks": task_results,
        }
    return {
        "method": "Exact fixed 200-row held-out cohorts from the finance uplift pilot; same question instructions and label criteria; zero-shot external models; no evaluation labels in requests.",
        "cohort_sha256": {slug: cohort["sha256"] for slug, cohort in cohorts.items()},
        "models": models,
    }


def read_api_key(env_file: Path | None) -> str:
    key = os.getenv("OPENROUTER_API_KEY")
    if key:
        return key
    if env_file:
        for raw in env_file.read_text().splitlines():
            name, separator, value = raw.partition("=")
            if separator and name.removeprefix("export ").strip() == "OPENROUTER_API_KEY":
                key = value.strip().strip('"\'')
                if key:
                    return key
    raise ValueError("Set OPENROUTER_API_KEY or provide --env-file")


def main() -> None:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--models", default="jev,gpt", help="Comma-separated names: jev,gpt")
    parser.add_argument("--workers", type=int, default=8)
    parser.add_argument("--limit", type=int, help="New calls per selected model")
    parser.add_argument("--timeout", type=float, default=120.0)
    parser.add_argument("--env-file", type=Path)
    parser.add_argument("--output-dir", type=Path, default=OUTPUTS)
    parser.add_argument("--plan", action="store_true")
    parser.add_argument("--report-only", action="store_true")
    args = parser.parse_args()
    names = [name.strip() for name in args.models.split(",")]
    if not names or len(set(names)) != len(names) or any(name not in MODELS for name in names):
        parser.error("--models must be jev, gpt, or jev,gpt")
    if args.workers < 1 or args.timeout <= 0 or (args.limit is not None and args.limit < 1):
        parser.error("--workers, --timeout, and --limit must be positive")
    cohorts = read_cohorts()
    if args.plan:
        print(json.dumps({
            "models": {name: MODELS[name].__dict__ for name in names},
            "eval_counts": {slug: len(cohort["eval_rows"]) for slug, cohort in cohorts.items()},
            "cohort_sha256": {slug: cohort["sha256"] for slug, cohort in cohorts.items()},
        }, indent=2))
        return
    if args.report_only:
        report = build_report(cohorts, args.output_dir)
        PUBLIC_REPORT.write_text(json.dumps(report, indent=2, ensure_ascii=False) + "\n")
        print(f"wrote {PUBLIC_REPORT}", flush=True)
        return
    api_key = read_api_key(args.env_file)
    with httpx.Client(timeout=args.timeout, headers={"Authorization": f"Bearer {api_key}"}) as client:
        for name in names:
            run_model(client, MODELS[name], cohorts, args.output_dir, args.workers, args.limit)
    if args.limit is None and set(names) == set(MODELS):
        report = build_report(cohorts, args.output_dir)
        PUBLIC_REPORT.write_text(json.dumps(report, indent=2, ensure_ascii=False) + "\n")
        print(f"wrote {PUBLIC_REPORT}", flush=True)


if __name__ == "__main__":
    main()
