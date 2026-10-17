"""Select reproducible training rows for the German credit comparisons."""

from __future__ import annotations

import random

import pyarrow.parquet as pq
from huggingface_hub import hf_hub_download


def published_training_rows(cohort: dict) -> list[dict]:
    source = hf_hub_download(
        repo_id=cohort["repo"], repo_type="dataset",
        revision=cohort["revision"], filename=cohort["train_file"],
    )
    return [
        {
            "id": f"full-train-{index}",
            "source_index": index,
            "state": {"customer": f"Customer record:\n{row['text']}"},
            "truth": row["answer"],
        }
        for index, row in enumerate(pq.read_table(source).to_pylist())
    ]


def balanced_training_rows(cohort: dict) -> list[dict]:
    """Keep every bad-risk row and sample good-risk rows without replacement.

    The sampled good rows include every good row in the original 200-label
    cohort, so this larger balanced set contains all 200 original examples.
    """
    full = published_training_rows(cohort)
    bad = [row for row in full if row["truth"] == "bad"]
    good = [row for row in full if row["truth"] == "good"]
    original_indices = {row["source_index"] for row in cohort["train_rows"]}
    original_good = {row["source_index"] for row in cohort["train_rows"] if row["truth"] == "good"}
    remaining_good = [row for row in good if row["source_index"] not in original_good]
    rng = random.Random(cohort["seed"])
    selected_good = original_good | {
        row["source_index"]
        for row in rng.sample(remaining_good, len(bad) - len(original_good))
    }
    selected = [
        row for row in full
        if row["truth"] == "bad" or row["source_index"] in selected_good
    ]
    assert len(bad) == len(selected_good) == 206
    assert len(selected) == 412
    assert original_indices <= {row["source_index"] for row in selected}
    rng.shuffle(selected)
    return selected
