# German Credit

## Task

Classify the credit-risk outcome from an applicant record.

## Task shape

`applicant attributes → credit-risk choice`. Each evaluation item is rendered as complete state plus exactly one
typed question; the target remains outside the model-visible decision.

```json
{"decision": {"state": {"…": "…"}, "questions": {"decision": {"type": "choice", "criteria": {"…": "…"}}}}, "target": {"kind": "hard", "answer": "…"}}
```

## Results

| Model | Accuracy | Rows |
| --- | ---: | ---: |
| Mo 1.3.1 | 52.50% | 200 |
| Mo 1.3.2 | 53.50% | 200 |
| Jev 1.13 | 43.50% | 200 |
| Jev 1.14 | 44.00% | 200 |
| Luna Decisions | 38.50% | 200 |
| PPLX | 52.00% | 200 |
| GPT-6.1 | 75.00% | 200 |
| Mo Fast | 34.00% | 200 |
| Clef | 35.50% | 200 |

Headline values are exact-answer accuracy. Additional calibration metrics are
in [`data/benchmark-results.json`](../../../data/benchmark-results.json).
