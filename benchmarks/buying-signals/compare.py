"""Make a compact leaderboard from complete Gong test reports."""

from __future__ import annotations

import argparse
import json
from pathlib import Path

from questions import TASKS


def leaderboard(output_dir: Path) -> str:
    reports = [json.loads(path.read_text(encoding="utf-8")) for path in output_dir.rglob("*-test-report.json")]
    if not reports:
        raise ValueError("No complete test reports found")
    revisions = {report["dataset_revision"] for report in reports}
    if len(revisions) != 1 or any(report["split"] != "test" or report["pooled"]["n"] != 1000 for report in reports):
        raise ValueError("Reports do not share one complete test cohort")
    cohorts = {report["prediction_run"]["dataset_manifest_sha256"] for report in reports}
    if len(cohorts) != 1:
        raise ValueError("Reports do not share one manifest")
    reports.sort(key=lambda report: report["macro"]["accuracy"], reverse=True)
    lines = ["# Gong Call Playbook buying-signal benchmark", "", "Test only: 200 examples per signal; 1,000 decisions per model. Primary display metric: macro accuracy at p ≥ 0.5.", "", "| Model | Model ID | Backend | Workers | Macro accuracy | Macro precision | Macro F1 | Min F1 | Macro recall | Macro AUROC | Macro ECE | p50 ms | p95 ms | p99 ms |", "|---|---|---|---:|---:|---:|---:|---:|---:|---:|---:|---:|---:|---:|---:|---:|---:|"]
    for report in reports:
        run = report["prediction_run"]
        macro = report["macro"]
        latency = report["latency"]
        values = [run["name"], run["model"], run["backend"], str(latency["workers"]), *(f"{macro[name]:.3f}" for name in ("accuracy", "precision", "f1")),
                  f"{report['min_task_f1']:.3f}", *(f"{macro[name]:.3f}" for name in ("recall", "auroc", "ece")),
                  *(f"{latency[name]:.0f}" for name in ("p50_ms", "p95_ms", "p99_ms"))]
        lines.append("| " + " | ".join(values) + " |")
    lines += ["", "## Per-signal F1", "", "| Model | " + " | ".join(TASKS) + " |", "|---|" + "---:|" * len(TASKS)]
    for report in reports:
        lines.append("| " + report["prediction_run"]["name"] + " | " + " | ".join(f"{report['by_task'][task]['f1']:.3f}" for task in TASKS) + " |")
    lines += ["", "Latency excludes retries and backoff. Worker count is in each report's provenance; runs with multiple workers measure latency under concurrent load. GPT chat JSON and native Noul probabilities have distinct backends.", ""]
    return "\n".join(lines)


def main() -> None:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--output-dir", type=Path, default=Path("outputs"))
    parser.add_argument("--output", type=Path)
    args = parser.parse_args()
    result = leaderboard(args.output_dir)
    if args.output:
        args.output.parent.mkdir(parents=True, exist_ok=True)
        args.output.write_text(result, encoding="utf-8")
    print(result)


if __name__ == "__main__":
    main()
