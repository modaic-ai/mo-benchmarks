# Modaic Access Continuation

## Task

Decide whether an exact access grant or group membership should continue at the review time. This folder represents the held-out **test** split.

## Task shape

`identity, grants, memberships, event timeline, catalog, controls, and review target → retain or revoke`.

```json
{"benchmark": "access_continuation", "split": "test", "decision": {"state": {"…": "…"}, "questions": {"…": {"type": "choice", "criteria": {"…": "…"}}}}, "target": {"kind": "hard", "answer": "…"}}
```

Three representative rows for the Security suite are visible in
[`../examples.jsonl`](../examples.jsonl). The complete dataset is private:
[`modaic/security-decision-benchmarks`](https://huggingface.co/datasets/modaic/security-decision-benchmarks/tree/f1617a20780cef96be15eb6e345e003e976cf292).

## Results

| Model | Accuracy | Rows |
| --- | ---: | ---: |
| Mo 1.3.1 | 88.74% | 382 |
| Mo 1.3.2 | 84.03% | 382 |
| Jev 1.13 | 49.74% | 382 |
| Jev 1.14 | 53.14% | 382 |
| Luna Decisions | 49.48% | 382 |
| PPLX | 83.77% | 382 |
| GPT-6.1 | 100.00% | 382 |
| Mo Fast | 65.45% | 382 |
| Clef | 49.48% | 382 |

Headline values are exact-answer accuracy on hard-target rows. ECE and MCE use
15 equal-width bins; complete calibration metrics are in
[`data/benchmark-results.json`](../../../data/benchmark-results.json).
