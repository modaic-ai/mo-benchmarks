# CFPB Complaint Routing

## Task

Route a consumer-finance complaint to the correct product category.

## Task shape

`complaint narrative → product choice`. Each evaluation item is rendered as complete state plus exactly one
typed question; the target remains outside the model-visible decision.

```json
{"decision": {"state": {"…": "…"}, "questions": {"decision": {"type": "choice", "criteria": {"…": "…"}}}}, "target": {"kind": "hard", "answer": "…"}}
```

## Results

| Model | Accuracy | Rows |
| --- | ---: | ---: |
| Mo 1.3.1 | 46.00% | 200 |
| Mo 1.3.2 | 47.00% | 200 |
| Jev 1.13 | 44.00% | 200 |
| Jev 1.14 | 46.00% | 200 |
| Luna Decisions | 45.50% | 200 |
| PPLX | 44.50% | 200 |
| GPT-6.1 | 49.00% | 200 |
| Mo Fast | 44.00% | 200 |
| Clef | 46.50% | 200 |

Headline values are exact-answer accuracy. Additional calibration metrics are
in [`data/benchmark-results.json`](../../../data/benchmark-results.json).
