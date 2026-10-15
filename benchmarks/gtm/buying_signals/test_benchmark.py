"""Local synthetic checks; never use licensed call excerpts in tests."""

from __future__ import annotations

import csv
import json
import tempfile
import unittest
from pathlib import Path
from types import SimpleNamespace

from metrics import auroc, summarize
from prepare import prepare
from questions import TASKS
from report import build_report
from run_models import MODELS, request_state, run_model, score_row


def synthetic_source(root: Path, size: int) -> None:
    for task in TASKS:
        folder = root / task
        folder.mkdir(parents=True)
        with (folder / "test.csv").open("w", encoding="utf-8", newline="") as handle:
            writer = csv.DictWriter(handle, fieldnames=("id", "text", "label"))
            writer.writeheader()
            for index in range(size):
                writer.writerow({"id": index, "text": f"Buyer: Invented {task} excerpt {index}.", "label": index % 2})


class FakeModaic:
    def __init__(self) -> None:
        self.requests = []
        self.decisions = self

    def create(self, **request):
        self.requests.append(request)
        return SimpleNamespace(answers={"signal_present": SimpleNamespace(noul=0.7)})


class BenchmarkTests(unittest.TestCase):
    def test_metrics_include_calibration_and_ties(self) -> None:
        result = summarize([0, 1, 0, 1], [0.1, 0.9, 0.2, 0.8])
        self.assertEqual(result["f1"], 1)
        self.assertEqual(result["auroc"], 1)
        self.assertAlmostEqual(result["ece"], 0.15)
        self.assertEqual(auroc([0, 1], [0.5, 0.5]), 0.5)

    def test_preparation_has_test_only_and_separate_labels(self) -> None:
        with tempfile.TemporaryDirectory() as temporary:
            root = Path(temporary)
            synthetic_source(root / "source", 2)
            manifest = prepare(root / "data", root / "source", expected_per_split=2)
            inputs = [json.loads(line) for line in (root / "data/inputs.jsonl").read_text().splitlines()]
            labels = [json.loads(line) for line in (root / "data/labels.jsonl").read_text().splitlines()]
            self.assertEqual(len(inputs), 10)
            self.assertTrue(all(row["split"] == "test" and "label" not in row for row in inputs))
            self.assertTrue(all("text" not in row for row in labels))
            self.assertEqual(len({row["id"] for row in inputs}), 10)
            self.assertEqual(set(manifest["counts"]), set(TASKS))

    def test_pilot_request_is_label_blind_and_resume_is_stable(self) -> None:
        with tempfile.TemporaryDirectory() as temporary:
            root = Path(temporary)
            synthetic_source(root / "source", 200)
            manifest = prepare(root / "data", root / "source")
            first = json.loads((root / "data/inputs.jsonl").read_text().splitlines()[0])
            self.assertEqual(set(request_state(first)), {"conversation_excerpt"})
            fake = FakeModaic()
            result = score_row(MODELS["mo-fast"], first, "synthetic", fake, None)
            self.assertEqual(result["p_signal"], 0.7)
            self.assertEqual(set(fake.requests[0]["state"]), {"conversation_excerpt"})
            self.assertFalse(fake.requests[0]["capture"])
            new, total = run_model(MODELS["mo-fast"], root / "data", root / "outputs", manifest, 5, fake, None)
            self.assertEqual((new, total), (5, 5))
            predictions = [json.loads(line) for line in (root / "outputs/mo-fast-test.jsonl").read_text().splitlines()]
            self.assertEqual({row["id"].split(":")[1] for row in predictions}, set(TASKS))
            self.assertTrue(all("text" not in row and "label" not in row for row in predictions))
            new, total = run_model(MODELS["mo-fast"], root / "data", root / "outputs", manifest, 5, fake, None)
            self.assertEqual((new, total), (5, 10))
            with self.assertRaisesRegex(ValueError, "Prediction IDs mismatch"):
                build_report(root / "data", root / "outputs/mo-fast-test.jsonl")
            run_model(MODELS["mo-fast"], root / "data", root / "outputs", manifest, None, fake, None)
            report = build_report(root / "data", root / "outputs/mo-fast-test.jsonl")
            self.assertEqual(report["pooled"]["n"], 1000)
            self.assertEqual(set(report["by_task"]), set(TASKS))


if __name__ == "__main__":
    unittest.main()
