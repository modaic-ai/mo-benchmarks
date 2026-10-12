"""Build label-separated inputs from Gong Call Playbook at a pinned revision."""

from __future__ import annotations

import argparse
import csv
import hashlib
import json
from collections import Counter
from pathlib import Path
from typing import Any

from questions import DATASET_ID, DATASET_REVISION, TASKS


def source_rows(source_dir: Path | None, task: str, split: str) -> list[dict[str, Any]]:
    if source_dir is None:
        from huggingface_hub import hf_hub_download

        path = Path(hf_hub_download(
            repo_id=DATASET_ID, filename=f"{task}/{split}.csv",
            repo_type="dataset", revision=DATASET_REVISION,
        ))
    else:
        path = source_dir / task / f"{split}.csv"
    with path.open(newline="", encoding="utf-8") as handle:
        return list(csv.DictReader(handle))


def prepare(out_dir: Path, source_dir: Path | None = None, expected_per_split: int = 200) -> dict[str, Any]:
    inputs: list[dict[str, Any]] = []
    labels: list[dict[str, Any]] = []
    counts: dict[str, dict[str, dict[str, int]]] = {}
    for task in TASKS:
        counts[task] = {}
        for split in ("test",):
            rows = source_rows(source_dir, task, split)
            if len(rows) != expected_per_split:
                raise ValueError(f"{task}/{split}: expected {expected_per_split} rows, got {len(rows)}")
            seen_ids: set[str] = set()
            label_counts: Counter[int] = Counter()
            for row in rows:
                source_id = str(row["id"])
                if source_id in seen_ids:
                    raise ValueError(f"{task}/{split}: duplicate source ID {source_id}")
                seen_ids.add(source_id)
                excerpt = row["text"]
                if not isinstance(excerpt, str) or not excerpt.strip():
                    raise ValueError(f"{task}/{split}/{source_id}: empty text")
                label = int(row["label"])
                if label not in (0, 1) or str(row["label"]) not in ("0", "1"):
                    raise ValueError(f"{task}/{split}/{source_id}: label must be 0 or 1")
                item_id = f"{split}:{task}:{source_id}"
                inputs.append({"id": item_id, "split": split, "task": task, "text": excerpt})
                labels.append({"id": item_id, "split": split, "task": task, "label": label})
                label_counts[label] += 1
            counts[task][split] = {"n": len(rows), "positive": label_counts[1], "negative": label_counts[0]}
    input_text = "".join(json.dumps(row, ensure_ascii=False) + "\n" for row in inputs)
    label_text = "".join(json.dumps(row, ensure_ascii=False) + "\n" for row in labels)
    manifest = {
        "source": DATASET_ID,
        "revision": DATASET_REVISION,
        "tasks": list(TASKS),
        "counts": counts,
        "inputs_sha256": hashlib.sha256(input_text.encode()).hexdigest(),
        "labels_sha256": hashlib.sha256(label_text.encode()).hexdigest(),
    }
    out_dir.mkdir(parents=True, exist_ok=True)
    (out_dir / "inputs.jsonl").write_text(input_text, encoding="utf-8")
    (out_dir / "labels.jsonl").write_text(label_text, encoding="utf-8")
    (out_dir / "manifest.json").write_text(json.dumps(manifest, indent=2) + "\n", encoding="utf-8")
    return manifest


def main() -> None:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--source-dir", type=Path, help="Local task/test.csv files; omit to load from HF")
    parser.add_argument("--out-dir", type=Path, default=Path("data/gong"))
    args = parser.parse_args()
    manifest = prepare(args.out_dir, args.source_dir)
    print(json.dumps({"revision": manifest["revision"], "counts": manifest["counts"]}, indent=2))


if __name__ == "__main__":
    main()
