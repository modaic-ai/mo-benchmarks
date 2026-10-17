"""Preselect and score a CFPB test cohort without near-duplicate train text.

This is a text-only audit of the published splits. It must be run before the
aligned checkpoint is scored; no model predictions are consulted in selection.
"""

from __future__ import annotations

import argparse
import collections
import hashlib
import json
import os
import random
import re

from modaic import Modaic

from prepare import content_key, raw_rows
from run import DATA, OUTPUTS, evaluate, get_or_create, read_json, read_jsonl, save_json, score
from tasks import SEED, TASKS

TASK = TASKS["cfpb-routing"]
THRESHOLD = 0.8
MANIFEST = DATA / "cfpb-routing.clean-eval.json"


def shingles(text: str) -> set[tuple[str, ...]]:
    tokens = re.findall(r"[a-z0-9]+", text.casefold())
    return {tuple(tokens[i:i + 5]) for i in range(max(0, len(tokens) - 4))}


def max_similarity(grams: set, corpus: list[set], index: dict) -> float:
    overlaps = collections.Counter(j for gram in grams for j in index.get(gram, ()))
    return max((count / (len(grams) + len(corpus[j]) - count)
                for j, count in overlaps.items()), default=0.0)


def balanced_diverse_sample(rows: list[dict]) -> list[dict]:
    groups = {label: [] for label in TASK.criteria}
    for row in rows:
        groups[row["truth"]].append(row)
    rng = random.Random(SEED)
    for group in groups.values():
        rng.shuffle(group)
    selected = []
    selected_grams = []
    index = collections.defaultdict(list)
    counts = collections.Counter()
    while len(selected) < 200:
        advanced = False
        for label in sorted(groups):
            if counts[label] >= 20:
                continue
            while groups[label]:
                row = groups[label].pop()
                grams = shingles(row["state"]["record"])
                if max_similarity(grams, selected_grams, index) >= THRESHOLD:
                    continue
                j = len(selected)
                selected.append(row)
                selected_grams.append(grams)
                for gram in grams:
                    index[gram].append(j)
                counts[label] += 1
                advanced = True
                break
        if not advanced:
            raise RuntimeError("not enough distinct CFPB test rows per label")
    return selected


def prepare() -> dict:
    original = read_json(DATA / f"{TASK.slug}.json")
    train_rows = original["train_rows"]
    if len(train_rows) != 200:
        raise RuntimeError("CFPB train cohort is incomplete")
    train_grams = [shingles(r["state"]["record"]) for r in train_rows]
    index = collections.defaultdict(list)
    for j, grams in enumerate(train_grams):
        for gram in grams:
            index[gram].append(j)

    all_test = raw_rows(TASK, TASK.eval_file, TASK.eval_split)
    seen = set()
    exact_unique = []
    for row in all_test:
        key = content_key(row)
        if key not in seen:
            seen.add(key)
            exact_unique.append(row)
    candidates = []
    near_duplicate_count = 0
    for row in exact_unique:
        grams = shingles(row["state"]["record"])
        if max_similarity(grams, train_grams, index) >= THRESHOLD:
            near_duplicate_count += 1
            continue
        candidates.append(row)
    selected = balanced_diverse_sample(candidates)
    if len(selected) != 200 or len({content_key(r) for r in selected}) != 200:
        raise RuntimeError("clean CFPB test cohort could not be selected")
    if collections.Counter(r["truth"] for r in selected) != {label: 20 for label in TASK.criteria}:
        raise RuntimeError("clean CFPB test cohort is not balanced")
    manifest = {
        "task": TASK.slug, "source": TASK.repo, "revision": TASK.revision,
        "source_split": TASK.eval_split, "selection_seed": SEED,
        "train_cohort_sha256": original["sha256"],
        "min_5gram_jaccard_exclusion": THRESHOLD,
        "source_test_rows": len(all_test), "exact_unique_test_rows": len(exact_unique),
        "near_duplicate_test_rows_excluded": near_duplicate_count,
        "eval_rows": selected,
    }
    manifest["sha256"] = hashlib.sha256(json.dumps(manifest, sort_keys=True, ensure_ascii=False).encode()).hexdigest()
    save_json(MANIFEST, manifest)
    return manifest


def main() -> None:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--phase", required=True, choices=["prepare", "baseline", "final"])
    parser.add_argument("--workspace", default=os.environ.get("MODAIC_WORKSPACE", "modaic_labs"))
    parser.add_argument("--workers", type=int, default=4)
    args = parser.parse_args()
    if args.phase == "prepare":
        m = prepare()
        print(json.dumps({k: v for k, v in m.items() if k != "eval_rows"}, indent=2))
        return
    if not os.environ.get("MODAIC_API_KEY"):
        parser.error("MODAIC_API_KEY is required")
    manifest = read_json(MANIFEST)
    state = read_json(OUTPUTS / f"{TASK.slug}.state.json")
    original = read_json(DATA / f"{TASK.slug}.json")
    if not manifest or manifest["train_cohort_sha256"] != original["sha256"] or state["cohort_sha256"] != original["sha256"]:
        raise RuntimeError("clean evaluation or model identity changed")
    with Modaic(timeout=180) as client:
        model = get_or_create(client, TASK, original, args.workspace)
        if model.id != state["model_id"]:
            raise RuntimeError("model identity changed")
        if args.phase == "baseline":
            evaluate(model, TASK, manifest, "clean-baseline", state["baseline_revision"], args.workers)
            return
        if state.get("alignment_status") != "completed" or state.get("batch_status") not in {"completed", "not_applicable"}:
            raise RuntimeError("wait for alignment and automatic batch first")
        baseline = read_jsonl(OUTPUTS / f"{TASK.slug}.clean-baseline.jsonl")
        if len(baseline) != 200:
            raise RuntimeError("clean baseline must be complete before final")
        final = evaluate(model, TASK, manifest, "clean-final", state["result_revision"], args.workers)
        report = score(TASK, baseline, final, manifest["eval_rows"])
        report.update({
            "model_path": state["model_path"], "cohort_sha256": manifest["sha256"],
            "source_train_cohort_sha256": original["sha256"],
            "baseline_revision": state["baseline_revision"],
            "aligned_revision": state["result_revision"],
            "alignment_id": state["alignment_id"], "batch_id": state.get("batch_id"),
            "batch_status": state["batch_status"], "training_labels": 200,
            "near_duplicate_test_rows_excluded": manifest["near_duplicate_test_rows_excluded"],
            "test_similarity_exclusion": "5-token Jaccard >= 0.8 against any selected training complaint",
        })
        save_json(OUTPUTS / f"{TASK.slug}.report.json", report)
        print(json.dumps(report, indent=2))


if __name__ == "__main__":
    main()
