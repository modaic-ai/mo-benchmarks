# Access Recommendation — Validation

## Task

Recommend whether to keep or remove existing access from a review snapshot. This folder represents the held-out **validation** split.

## Task shape

`review item, assignment, governance history, profile changes, usage evidence, and separation-of-duties status → approve or revoke`.

```json
{"benchmark": "access_recommendation", "split": "validation", "decision": {"state": {"…": "…"}, "questions": {"…": {"type": "choice", "criteria": {"…": "…"}}}}, "target": {"kind": "hard", "answer": "…"}}
```

Three representative rows for the Security suite are visible in
[`../examples.jsonl`](../examples.jsonl). The complete dataset is private:
[`modaic/security-decision-benchmarks`](https://huggingface.co/datasets/modaic/security-decision-benchmarks/tree/f1617a20780cef96be15eb6e345e003e976cf292).

## Results

| Model | Accuracy | Rows |
| --- | ---: | ---: |
| Mo 1.3.1 | 97.05% | 2,437 |
| Mo 1.3.2 | 87.53% | 2,437 |
| Jev 1.13 | 70.99% | 2,437 |
| Jev 1.14 | 76.36% | 2,437 |
| Luna Decisions | 71.89% | 2,437 |
| PPLX | 88.39% | 2,437 |
| GPT-6.1 | 95.77% | 2,437 |
| Mo Fast | 89.08% | 2,437 |
| Clef | 69.02% | 2,437 |

Headline values are exact-answer accuracy on hard-target rows. ECE and MCE use
15 equal-width bins; complete calibration metrics are in
[`data/benchmark-results.json`](../../../data/benchmark-results.json).
