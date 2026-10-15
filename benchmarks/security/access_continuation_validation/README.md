# Access Continuation — Validation

## Task

Decide whether an exact access grant or group membership should continue at the review time. This folder represents the held-out **validation** split.

## Task shape

`identity, grants, memberships, event timeline, catalog, controls, and review target → retain or revoke`.

```json
{"benchmark": "access_continuation", "split": "validation", "decision": {"state": {"…": "…"}, "questions": {"…": {"type": "choice", "criteria": {"…": "…"}}}}, "target": {"kind": "hard", "answer": "…"}}
```

Three representative rows for the Security suite are visible in
[`../examples.jsonl`](../examples.jsonl). The complete dataset is private:
[`modaic/security-decision-benchmarks`](https://huggingface.co/datasets/modaic/security-decision-benchmarks/tree/f1617a20780cef96be15eb6e345e003e976cf292).

## Results

| Model | Accuracy | Rows |
| --- | ---: | ---: |
| Mo 1.3.1 | 93.46% | 964 |
| Mo 1.3.2 | 86.72% | 964 |
| Jev 1.13 | 49.17% | 964 |
| Jev 1.14 | 54.25% | 964 |
| Luna Decisions | 49.27% | 964 |
| PPLX | 86.62% | 964 |
| GPT-6.1 | 100.00% | 964 |
| Mo Fast | 68.36% | 964 |
| Clef | 50.83% | 964 |

Headline values are exact-answer accuracy on hard-target rows. ECE and MCE use
15 equal-width bins; complete calibration metrics are in
[`data/benchmark-results.json`](../../../data/benchmark-results.json).
