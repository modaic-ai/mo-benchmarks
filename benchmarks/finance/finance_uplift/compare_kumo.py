"""Run local Kumo Tabular Large on the fixed German credit evaluation cohort.

The default gives Kumo the same 200 training labels used for Mo alignment.
Use ``--balanced-full-train`` for 206 rows of each class or ``--full-train``
for all 700 published training rows.
Weights are downloaded on first use and every prediction is computed locally.
"""

from __future__ import annotations

import argparse
import hashlib
import json
import re
from collections import Counter
from importlib.metadata import version
from pathlib import Path

import pandas as pd
import sdm
import torch

from german_credit_training import balanced_training_rows, published_training_rows


COHORT = Path(__file__).resolve().parent / "data" / "german-credit.json"
NUMERIC_FIELDS = {2, 5, 8, 11, 13, 16, 18}
FIELD_PATTERN = re.compile(r"\bX(\d+):\s*([^,.\n]+)")


def fields(row: dict) -> dict[str, str | int]:
    record = row["state"]["customer"].split("Customer record:\n", 1)[1]
    values = {int(index): value.strip() for index, value in FIELD_PATTERN.findall(record)}
    if set(values) != set(range(1, 21)):
        raise ValueError(f"Expected 20 customer fields in {row['id']}: {sorted(values)}")
    return {
        f"X{index}": int(values[index]) if index in NUMERIC_FIELDS else values[index]
        for index in range(1, 21)
    }


def main() -> None:
    parser = argparse.ArgumentParser(description=__doc__)
    training = parser.add_mutually_exclusive_group()
    training.add_argument("--full-train", action="store_true")
    training.add_argument("--balanced-full-train", action="store_true")
    parser.add_argument("--num-estimators", type=int, default=16)
    parser.add_argument("--eval-limit", type=int, default=200, help="For a smoke run only")
    args = parser.parse_args()

    cohort = json.loads(COHORT.read_text())
    train, test = cohort["train_rows"], cohort["eval_rows"][:args.eval_limit]
    if args.full_train:
        train = published_training_rows(cohort)
    elif args.balanced_full_train:
        train = balanced_training_rows(cohort)
    assert len(train) in {200, 412, 700} and 0 < len(test) <= 200
    assert not ({tuple(fields(row).items()) for row in train} &
                {tuple(fields(row).items()) for row in test})

    feature_rows = [fields(row) for row in train + test]
    frame = pd.DataFrame(feature_rows)
    stypes = {
        column: "numerical" if int(column[1:]) in NUMERIC_FIELDS else "categorical"
        for column in frame.columns
    }
    features = sdm.TableTensor.from_pandas(frame, stypes=stypes, device="cpu")
    labels = sdm.TableTensor.from_pandas(
        pd.DataFrame({"target": [row["truth"] for row in train]}),
        stypes={"target": "categorical"}, device="cpu",
    )

    torch.set_num_threads(min(torch.get_num_threads(), 8))
    model = sdm.models.KumoTabular(task="classification", size="large", device="cpu")
    with torch.inference_mode():
        probabilities = model(
            x_context=features[:len(train)],
            y_context=labels,
            x_query=features[len(train):],
            num_estimators=args.num_estimators,
        ).to_pandas()
    truth = pd.Series([row["truth"] for row in test], name="truth")
    predicted = probabilities.idxmax(axis=1).rename("predicted")
    if set(predicted) - set(truth):
        raise ValueError(f"Unexpected predicted labels: {set(predicted) - set(truth)}")

    result = {
        "dataset": cohort["repo"],
        "revision": cohort["revision"],
        "cohort_sha256": cohort["sha256"],
        "model": "nvidia/Kumo-Tabular large",
        "model_weight_revision": "v1.0.1",
        "structured_data_models_version": version("structured-data-models"),
        "inference": "local CPU",
        "num_estimators": args.num_estimators,
        "training_rows": len(train),
        "training_source_indices_sha256": hashlib.sha256(
            ",".join(str(row["source_index"]) for row in train).encode()
        ).hexdigest(),
        "held_out_rows": len(test),
        "training_labels": dict(Counter(row["truth"] for row in train)),
        "held_out_labels": dict(Counter(truth)),
        "correct": int((predicted == truth).sum()),
        "accuracy": float((predicted == truth).mean()),
        "balanced_accuracy": float(sum(
            (predicted[truth == label] == label).mean() for label in sorted(set(truth))
        ) / len(set(truth))),
        "confusion": {
            label: dict(Counter(predicted[truth == label])) for label in sorted(set(truth))
        },
    }
    print(json.dumps(result, indent=2))


if __name__ == "__main__":
    main()
