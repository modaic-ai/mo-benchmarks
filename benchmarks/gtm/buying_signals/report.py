"""Score complete buying-signal predictions against one frozen split."""

from __future__ import annotations

import argparse
import hashlib
import json
import math
from collections import Counter
from pathlib import Path
from typing import Any

from metrics import percentile, summarize
from questions import DATASET_ID, DATASET_REVISION, TASKS


def read_jsonl(path: Path) -> list[dict[str, Any]]:
    with path.open(encoding="utf-8") as handle:
        return [json.loads(line) for line in handle if line.strip()]


def manifest_hash(manifest: dict[str, Any]) -> str:
    return hashlib.sha256(json.dumps(manifest, sort_keys=True).encode()).hexdigest()


def load_predictions(path: Path) -> dict[str, dict[str, Any]]:
    result = {}
    for row in read_jsonl(path):
        item_id = row.get("id")
        if not isinstance(item_id, str) or item_id in result:
            raise ValueError(f"Missing or duplicate prediction ID: {item_id}")
        score = row.get("p_signal")
        if isinstance(score, bool) or not isinstance(score, (int, float)) or not math.isfinite(score) or not 0 <= score <= 1:
            raise ValueError(f"{item_id}: p_signal must be a finite probability")
        latency = row.get("latency_ms")
        if isinstance(latency, bool) or not isinstance(latency, (int, float)) or not math.isfinite(latency) or latency < 0:
            raise ValueError(f"{item_id}: latency_ms must be nonnegative and finite")
        result[item_id] = row
    return result


def build_report(data_dir: Path, predictions_path: Path) -> dict[str, Any]:
    split = "test"
    manifest = json.loads((data_dir / "manifest.json").read_text(encoding="utf-8"))
    if manifest.get("source") != DATASET_ID or manifest.get("revision") != DATASET_REVISION:
        raise ValueError("Unexpected dataset source or revision")
    inputs_text = (data_dir / "inputs.jsonl").read_bytes()
    labels_text = (data_dir / "labels.jsonl").read_bytes()
    if hashlib.sha256(inputs_text).hexdigest() != manifest["inputs_sha256"] or hashlib.sha256(labels_text).hexdigest() != manifest["labels_sha256"]:
        raise ValueError("Dataset files do not match the manifest")
    metadata_path = predictions_path.with_suffix(predictions_path.suffix + ".run.json")
    if not metadata_path.exists():
        raise ValueError("Predictions need matching .run.json provenance")
    metadata = json.loads(metadata_path.read_text(encoding="utf-8"))
    if metadata.get("dataset_manifest_sha256") != manifest_hash(manifest) or metadata.get("split") != split:
        raise ValueError("Prediction run belongs to a different cohort or split")
    all_labels = read_jsonl(data_dir / "labels.jsonl")
    if any(row["split"] != split for row in all_labels):
        raise ValueError("This benchmark permits test labels only")
    labels = all_labels
    expected = {row["id"] for row in labels}
    if len(expected) != len(labels) or len(labels) != 200 * len(TASKS):
        raise ValueError("Incomplete or duplicated benchmark labels")
    predictions = load_predictions(predictions_path)
    missing, extra = expected - predictions.keys(), predictions.keys() - expected
    if missing or extra:
        raise ValueError(f"Prediction IDs mismatch: {len(missing)} missing, {len(extra)} extra")
    by_task = {}
    for task in TASKS:
        task_labels = [row for row in labels if row["task"] == task]
        if len(task_labels) != 200:
            raise ValueError(f"{task}: expected 200 {split} labels")
        by_task[task] = summarize(
            [row["label"] for row in task_labels],
            [predictions[row["id"]]["p_signal"] for row in task_labels],
        )
    pooled = summarize([row["label"] for row in labels], [predictions[row["id"]]["p_signal"] for row in labels])
    metric_names = ("f1", "precision", "recall", "accuracy", "auroc", "ece")
    macro = {metric: sum(by_task[task][metric] for task in TASKS) / len(TASKS) for metric in metric_names}
    baseline_f1 = {}
    for name, score in (("always_present", 1.0), ("always_absent", 0.0)):
        baseline_f1[name] = sum(
            summarize([row["label"] for row in labels if row["task"] == task], [score] * 200)["f1"]
            for task in TASKS
        ) / len(TASKS)
    latencies = [float(predictions[row["id"]]["latency_ms"]) for row in labels]
    return {
        "benchmark": "Gong Call Playbook buying-signal identification",
        "split": split,
        "dataset_revision": manifest["revision"],
        "prediction_run": metadata,
        "threshold": 0.5,
        "primary_metric": "macro_accuracy",
        "macro": macro,
        "min_task_f1": min(by_task[task]["f1"] for task in TASKS),
        "baseline_macro_f1": baseline_f1,
        "pooled": pooled,
        "by_task": by_task,
        "latency": {
            "method": metadata["timing_method"], "n": len(latencies),
            "workers": metadata.get("workers", 1),
            "p50_ms": percentile(latencies, 0.50),
            "p95_ms": percentile(latencies, 0.95),
            "p99_ms": percentile(latencies, 0.99),
        },
        "served_models": dict(Counter(str(row["served_model"]) for row in predictions.values() if row.get("served_model"))),
        "providers": dict(Counter(str(row["provider"]) for row in predictions.values() if row.get("provider"))),
        "reported_cost_usd": sum(float(row.get("cost_usd", 0)) for row in predictions.values()),
    }


def main() -> None:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--data-dir", type=Path, default=Path("data/gong"))
    parser.add_argument("--predictions", required=True, type=Path)
    parser.add_argument("--output", type=Path)
    args = parser.parse_args()
    report = build_report(args.data_dir, args.predictions)
    result = json.dumps(report, indent=2, allow_nan=False) + "\n"
    if args.output:
        args.output.parent.mkdir(parents=True, exist_ok=True)
        args.output.write_text(result, encoding="utf-8")
    print(result, end="")


if __name__ == "__main__":
    main()
