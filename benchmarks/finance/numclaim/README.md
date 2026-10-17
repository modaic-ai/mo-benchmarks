# NumClaim

## Task

Decide whether a numerical claim is supported by financial evidence.

## Task shape

`financial evidence + numerical claim → support choice`. Each evaluation item is rendered as complete state plus exactly one
typed question; the target remains outside the model-visible decision.

```json
{"decision": {"state": {"…": "…"}, "questions": {"decision": {"type": "choice", "criteria": {"…": "…"}}}}, "target": {"kind": "hard", "answer": "…"}}
```

## Results

| Model | Accuracy | Rows |
| --- | ---: | ---: |
| Mo 1.3.1 | 94.50% | 200 |
| Mo 1.3.2 | 94.50% | 200 |
| Jev 1.13 | 93.50% | 200 |
| Jev 1.14 | 92.50% | 200 |
| Luna Decisions | 93.00% | 200 |
| PPLX | 94.00% | 200 |
| GPT-6.1 | 93.50% | 200 |
| Mo Fast | 92.00% | 200 |
| Clef | 92.50% | 200 |

Headline values are exact-answer accuracy. Additional calibration metrics are
in [`data/benchmark-results.json`](../../../data/benchmark-results.json).
