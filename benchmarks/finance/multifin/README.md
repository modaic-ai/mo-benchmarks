# MultiFin

## Task

Classify a financial text across the benchmark's topic labels.

## Task shape

`financial text → topic choice`. Each evaluation item is rendered as complete state plus exactly one
typed question; the target remains outside the model-visible decision.

```json
{"decision": {"state": {"…": "…"}, "questions": {"decision": {"type": "choice", "criteria": {"…": "…"}}}}, "target": {"kind": "hard", "answer": "…"}}
```

## Results

| Model | Accuracy | Rows |
| --- | ---: | ---: |
| Mo 1.3.1 | 65.00% | 200 |
| Mo 1.3.2 | 68.50% | 200 |
| Jev 1.13 | 71.00% | 200 |
| Jev 1.14 | 74.00% | 200 |
| Luna Decisions | 68.00% | 200 |
| PPLX | 67.50% | 200 |
| GPT-6.1 | 77.50% | 200 |
| Mo Fast | 72.00% | 200 |
| Clef | 70.00% | 200 |

Headline values are exact-answer accuracy. Additional calibration metrics are
in [`data/benchmark-results.json`](../../../data/benchmark-results.json).
