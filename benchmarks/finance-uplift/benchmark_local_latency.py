"""Measure warm local CPU latency on the balanced German credit cohort.

The model weights must already be downloaded. Imports, model setup, one-row
inference, and 200-row inference are timed separately. This uses the same
prediction paths and model settings as compare_tabpfn.py and compare_kumo.py.
"""

from __future__ import annotations

import argparse
import json
import platform
import statistics
import time
from pathlib import Path

from german_credit_training import balanced_training_rows


COHORT = Path(__file__).resolve().parent / "data" / "german-credit.json"


def measure(predict_one, predict_batch, repeats: int) -> tuple[list[float], list[float]]:
    predict_one()
    predict_batch()
    one_times = []
    batch_times = []
    for _ in range(repeats):
        start = time.perf_counter()
        predict_one()
        one_times.append(time.perf_counter() - start)
        start = time.perf_counter()
        predict_batch()
        batch_times.append(time.perf_counter() - start)
    return one_times, batch_times


def tabpfn_run(model_version: str, train: list[dict], test: list[dict], repeats: int):
    import numpy as np
    from tabpfn import TabPFNClassifier
    from tabpfn.constants import ModelVersion

    from compare_tabpfn import CATEGORICAL_INDICES, features

    x_train, x_test = features(train, test)
    y_train = np.asarray([row["truth"] for row in train])
    start = time.perf_counter()
    model = TabPFNClassifier.create_default_for_version(
        ModelVersion.V3_5 if model_version == "tabpfn-3.5" else ModelVersion.V2,
        device="cpu", categorical_features_indices=CATEGORICAL_INDICES,
        random_state=20261002,
    )
    model.fit(x_train, y_train)
    setup_seconds = time.perf_counter() - start
    one, batch = measure(
        lambda: model.predict(x_test[:1]),
        lambda: model.predict(x_test),
        repeats,
    )
    return setup_seconds, one, batch


def kumo_run(train: list[dict], test: list[dict], repeats: int, *, cached: bool):
    import pandas as pd
    import sdm
    import torch

    from compare_kumo import NUMERIC_FIELDS, fields

    frame = pd.DataFrame([fields(row) for row in train + test])
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
    start = time.perf_counter()
    model = sdm.models.KumoTabular(task="classification", size="large", device="cpu")
    if cached:
        with torch.inference_mode():
            model.fit(x=features[:len(train)], y=labels, num_estimators=16)
    setup_seconds = time.perf_counter() - start

    def predict(count: int) -> None:
        with torch.inference_mode():
            if cached:
                model.predict(features[len(train):len(train) + count]).to_pandas()
            else:
                model(
                    x_context=features[:len(train)], y_context=labels,
                    x_query=features[len(train):len(train) + count],
                    num_estimators=16,
                ).to_pandas()

    one, batch = measure(lambda: predict(1), lambda: predict(len(test)), repeats)
    return setup_seconds, one, batch


def summary(seconds: list[float]) -> dict[str, float]:
    return {
        "p50_ms": round(statistics.median(seconds) * 1000, 2),
        "min_ms": round(min(seconds) * 1000, 2),
        "max_ms": round(max(seconds) * 1000, 2),
    }


def main() -> None:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("model", choices=("tabpfn-2", "tabpfn-3.5", "kumo-large", "kumo-large-cached"))
    parser.add_argument("--repeats", type=int, default=10)
    args = parser.parse_args()
    if args.repeats < 1:
        parser.error("--repeats must be positive")
    cohort = json.loads(COHORT.read_text())
    train = balanced_training_rows(cohort)
    test = cohort["eval_rows"]
    if args.model.startswith("kumo-large"):
        setup, one, batch = kumo_run(
            train, test, args.repeats, cached=args.model == "kumo-large-cached"
        )
    else:
        setup, one, batch = tabpfn_run(args.model, train, test, args.repeats)
    print(json.dumps({
        "model": args.model,
        "device": "cpu",
        "machine": platform.machine(),
        "training_rows": len(train),
        "query_rows": len(test),
        "repeats": args.repeats,
        "model_setup_seconds": round(setup, 3),
        "warm_one_row": summary(one),
        "warm_200_rows": summary(batch),
        "warm_200_rows_per_second": round(len(test) / statistics.median(batch), 1),
    }, indent=2))


if __name__ == "__main__":
    main()
