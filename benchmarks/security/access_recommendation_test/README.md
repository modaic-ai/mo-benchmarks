# Modaic Access Recommendation

## Task

Recommend whether to keep or remove existing access from a review snapshot. This folder represents the held-out **test** split.

## Task shape

`review item, assignment, governance history, profile changes, usage evidence, and separation-of-duties status → approve or revoke`.

```json
{"benchmark": "access_recommendation", "split": "test", "decision": {"state": {"…": "…"}, "questions": {"…": {"type": "choice", "criteria": {"…": "…"}}}}, "target": {"kind": "hard", "answer": "…"}}
```

Three representative rows for the Security suite are visible in
[`../examples.jsonl`](../examples.jsonl). The complete dataset is private:
[`modaic/security-decision-benchmarks`](https://huggingface.co/datasets/modaic/security-decision-benchmarks/tree/f1617a20780cef96be15eb6e345e003e976cf292).

## Results

| Model | Accuracy | Rows |
| --- | ---: | ---: |
| Mo 1.3.1 | 96.00% | 2,201 |
| Mo 1.3.2 | 86.73% | 2,201 |
| Jev 1.13 | 73.42% | 2,201 |
| Jev 1.14 | 73.97% | 2,201 |
| Luna Decisions | 71.83% | 2,201 |
| PPLX | 84.60% | 2,201 |
| GPT-6.1 | 95.68% | 2,201 |
| Mo Fast | 83.60% | 2,201 |
| Clef | 63.06% | 2,201 |

Headline values are exact-answer accuracy on hard-target rows. ECE and MCE use
15 equal-width bins; complete calibration metrics are in
[`data/benchmark-results.json`](../../../data/benchmark-results.json).
