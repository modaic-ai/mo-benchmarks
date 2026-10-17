"""Evaluate TabPFN-2 or TabPFN-3.5 on the saved German credit cohort.

Install ``tabpfn`` and run this file from anywhere. The default uses the exact
training and held-out cohorts used for the Modaic comparison. Use
``--balanced-full-train`` for 206 good and 206 bad training rows, or
``--full-train`` for all 700 published training rows.
"""

from __future__ import annotations

import argparse
import hashlib
import json
import re
from collections import Counter
from importlib.metadata import version
from pathlib import Path

import numpy as np
from tabpfn import TabPFNClassifier
from tabpfn.constants import ModelVersion

from german_credit_training import balanced_training_rows, published_training_rows


COHORT = Path(__file__).resolve().parent / "data" / "german-credit.json"
NUMERIC_FIELDS = {2, 5, 8, 11, 13, 16, 18}
CATEGORICAL_INDICES = [i - 1 for i in range(1, 21) if i not in NUMERIC_FIELDS]
FIELD_PATTERN = re.compile(r"\bX(\d+):\s*([^,.\n]+)")


def fields(row: dict) -> list[str]:
    record = row["state"]["customer"].split("Customer record:\n", 1)[1]
    matches = FIELD_PATTERN.findall(record)
    values = {int(index): value.strip() for index, value in matches}
    if set(values) != set(range(1, 21)):
        raise ValueError(f"Expected 20 customer fields in {row['id']}: {sorted(values)}")
    return [values[i] for i in range(1, 21)]


def features(train: list[dict], test: list[dict]) -> tuple[np.ndarray, np.ndarray]:
    train_fields = [fields(row) for row in train]
    test_fields = [fields(row) for row in test]
    category_maps = {
        index: {value: code for code, value in enumerate(sorted({row[index] for row in train_fields}))}
        for index in CATEGORICAL_INDICES
    }

    def encode(rows: list[list[str]]) -> np.ndarray:
        return np.asarray([
            [float(value) if index not in category_maps else float(category_maps[index].get(value, -1))
             for index, value in enumerate(row)]
            for row in rows
        ], dtype=np.float32)

    return encode(train_fields), encode(test_fields)


def main() -> None:
    parser = argparse.ArgumentParser(description=__doc__)
    training = parser.add_mutually_exclusive_group()
    training.add_argument("--full-train", action="store_true")
    training.add_argument("--balanced-full-train", action="store_true")
    parser.add_argument("--model-version", choices=("v2", "v3.5"), default="v2")
    args = parser.parse_args()
    cohort = json.loads(COHORT.read_text())
    train, test = cohort["train_rows"], cohort["eval_rows"]
    if args.full_train:
        train = published_training_rows(cohort)
    elif args.balanced_full_train:
        train = balanced_training_rows(cohort)
    assert len(test) == 200
    assert {row["id"] for row in train}.isdisjoint({row["id"] for row in test})
    assert not ({tuple(fields(row)) for row in train} & {tuple(fields(row)) for row in test})
    x_train, x_test = features(train, test)
    y_train = np.asarray([row["truth"] for row in train])
    y_test = np.asarray([row["truth"] for row in test])

    model = TabPFNClassifier.create_default_for_version(
        ModelVersion.V3_5 if args.model_version == "v3.5" else ModelVersion.V2,
        device="cpu",
        categorical_features_indices=CATEGORICAL_INDICES,
        random_state=20261002,
    )
    model.fit(x_train, y_train)
    predictions = model.predict(x_test)
    result = {
        "dataset": cohort["repo"],
        "revision": cohort["revision"],
        "cohort_sha256": cohort["sha256"],
        "model": "TabPFN-3.5" if args.model_version == "v3.5" else "TabPFN-2",
        "tabpfn_version": version("tabpfn"),
        "training_rows": len(train),
        "training_source_indices_sha256": hashlib.sha256(
            ",".join(str(row["source_index"]) for row in train).encode()
        ).hexdigest(),
        "held_out_rows": len(test),
        "training_labels": dict(Counter(y_train)),
        "held_out_labels": dict(Counter(y_test)),
        "correct": int(np.sum(predictions == y_test)),
        "accuracy": float(np.mean(predictions == y_test)),
        "majority_class_accuracy": max(Counter(y_test).values()) / len(y_test),
        "balanced_accuracy": float(np.mean([
            np.mean(predictions[y_test == truth] == truth) for truth in sorted(set(y_test))
        ])),
        "confusion": {
            truth: dict(Counter(predictions[y_test == truth])) for truth in sorted(set(y_test))
        },
    }
    print(json.dumps(result, indent=2))


if __name__ == "__main__":
    main()
