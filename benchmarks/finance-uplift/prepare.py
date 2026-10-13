"""Prepare pinned, disjoint training and held-out evaluation cohorts."""

from __future__ import annotations

import argparse
import csv
import hashlib
import json
import random
import re
from pathlib import Path

import pyarrow.parquet as pq
from huggingface_hub import hf_hub_download

from tasks import BANKING77_LABELS, SEED, TASKS, Task

ROOT = Path(__file__).resolve().parent
DATA = ROOT / "data"


def source_path(task: Task, filename: str) -> Path:
    cached = Path.home() / ".cache/huggingface/hub" / f"datasets--{task.repo.replace('/', '--')}" / "snapshots" / task.revision / filename
    if cached.exists():
        return cached
    return Path(hf_hub_download(
        repo_id=task.repo, filename=filename, repo_type="dataset", revision=task.revision,
        local_dir=DATA / "source" / task.slug,
    ))


def raw_rows(task: Task, filename: str, split: str) -> list[dict]:
    rows = []
    path = source_path(task, filename)
    items = (map(json.loads, path.open()) if path.suffix == ".jsonl"
             else csv.DictReader(path.open(newline="", encoding="utf-8")) if path.suffix == ".csv"
             else pq.read_table(path).to_pylist())
    for index, item in enumerate(items):
        if task.slug == "multifin":
            value, label = item["text"], item["label"]
            state = {"text": value.strip()} if value else None
        elif task.slug == "banking77-routing":
            value, label = item["utterance"], BANKING77_LABELS[int(item["label"])]
            state = {
                "conversation": value.strip(),
                "account_context": "No account-specific facts are supplied. Route the customer's stated banking-support intent.",
            } if value else None
        elif task.slug == "fincalc-nli":
            label = {0: "contradiction", 1: "entailment", 2: "neutral"}[int(item["label"])]
            state = {"financial_evidence": item["premise"].strip(), "claim": item["hypothesis"].strip()}
        else:
            label = item["subissue"]
            value = item["consumer_complaint_narrative"]
            state = {"record": value.strip()} if value else None
        if state and label in task.criteria:
            row = {"id": f"{split}-{index}", "source_index": index, "state": state, "truth": label}
            if task.slug == "fincalc-nli":
                row["stratum"] = f"{label}|{item['metric']}"
            rows.append(row)
    return rows


def content_key(row: dict) -> str:
    text = (json.dumps(row["state"], sort_keys=True, ensure_ascii=False)
            if "financial_evidence" in row["state"]
            else next(v for k, v in row["state"].items() if k in {"text", "conversation", "record"}))
    normalized = re.sub(r"\s+", " ", text).strip().casefold()
    return hashlib.sha256(normalized.encode()).hexdigest()


def sample(rows: list[dict], limit: int, seed: int) -> list[dict]:
    if limit <= 0 or limit >= len(rows):
        return rows
    groups: dict[str, list[dict]] = {}
    for row in rows:
        groups.setdefault(row.get("stratum", row["truth"]), []).append(row)
    rng = random.Random(seed)
    for group in groups.values():
        rng.shuffle(group)
    selected = []
    while len(selected) < limit and any(groups.values()):
        for label in sorted(groups):
            if groups[label] and len(selected) < limit:
                selected.append(groups[label].pop())
    return selected


def prepare(task: Task, max_labels: int = 200, eval_limit: int = 200) -> dict:
    if max_labels > 200:
        raise ValueError("this pilot is capped at 200 labels per task")
    train_all = raw_rows(task, task.train_file, "train")
    eval_all = raw_rows(task, task.eval_file, task.eval_split)
    eval_keys = {content_key(row) for row in eval_all}
    train_distinct = [row for row in train_all if content_key(row) not in eval_keys]
    # Keep one example per distinct input so a duplicate cannot consume labels.
    seen = set()
    train_unique = []
    for row in train_distinct:
        key = content_key(row)
        if key not in seen:
            seen.add(key)
            train_unique.append(row)
    training = sample(train_unique, max_labels, SEED)
    if task.slug == "cfpb-routing":
        # This source's published train and test CSVs contain many duplicate
        # narratives. Do not let duplicates inflate held-out accuracy.
        eval_seen = set()
        eval_unique = []
        for row in eval_all:
            key = content_key(row)
            if key not in eval_seen:
                eval_seen.add(key)
                eval_unique.append(row)
    else:
        eval_unique = eval_all
    evaluation = sample(eval_unique, eval_limit, SEED)
    if len(training) != max_labels or len(evaluation) != eval_limit:
        raise RuntimeError(f"insufficient rows for {task.slug}")
    if {content_key(r) for r in training} & {content_key(r) for r in evaluation}:
        raise RuntimeError(f"train/evaluation overlap for {task.slug}")
    cohort = {
        "task": task.slug, "repo": task.repo, "revision": task.revision,
        "train_file": task.train_file, "eval_file": task.eval_file,
        "seed": SEED, "train_rows": training, "eval_rows": evaluation,
    }
    fingerprint = hashlib.sha256(json.dumps(cohort, sort_keys=True, ensure_ascii=False).encode()).hexdigest()
    cohort["sha256"] = fingerprint
    DATA.mkdir(parents=True, exist_ok=True)
    (DATA / f"{task.slug}.json").write_text(json.dumps(cohort, ensure_ascii=False, indent=2) + "\n")
    return {
        "task": task.slug, "source_train": len(train_all), "source_eval": len(eval_all),
        "excluded_train_overlap": len(train_all) - len(train_distinct),
        "train_unique": len(train_unique), "eval_unique": len(eval_unique),
        "labels": len(training), "eval": len(evaluation),
        "sha256": fingerprint,
    }


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--task", choices=TASKS)
    args = parser.parse_args()
    tasks = [TASKS[args.task]] if args.task else TASKS.values()
    for task in tasks:
        print(json.dumps(prepare(task), sort_keys=True))
