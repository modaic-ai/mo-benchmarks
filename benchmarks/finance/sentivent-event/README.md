# SentiVent Event

## Task

Classify the event expressed in a financial passage.

## Task shape

`financial passage → event choice`. Each evaluation item is rendered as complete state plus exactly one
typed question; the target remains outside the model-visible decision.

```json
{"decision": {"state": {"…": "…"}, "questions": {"decision": {"type": "choice", "criteria": {"…": "…"}}}}, "target": {"kind": "hard", "answer": "…"}}
```

## Results

| Model | Accuracy | Rows |
| --- | ---: | ---: |
| Mo 1.3.1 | 71.50% | 200 |
| Mo 1.3.2 | 69.00% | 200 |
| Jev 1.13 | 73.00% | 200 |
| Jev 1.14 | 73.50% | 200 |
| Luna Decisions | 76.50% | 200 |
| PPLX | 71.50% | 200 |
| GPT-6.1 | 72.50% | 200 |
| Mo Fast | 67.50% | 200 |
| Clef | 69.00% | 200 |

Headline values are exact-answer accuracy. Additional calibration metrics are
in [`data/benchmark-results.json`](../../../data/benchmark-results.json).
