# Banking77 Intent Routing

## Task

Route a banking support request to the correct intent.

## Task shape

`customer utterance → intent choice`. Each evaluation item is rendered as complete state plus exactly one
typed question; the target remains outside the model-visible decision.

```json
{"decision": {"state": {"…": "…"}, "questions": {"decision": {"type": "choice", "criteria": {"…": "…"}}}}, "target": {"kind": "hard", "answer": "…"}}
```

## Results

| Model | Accuracy | Rows |
| --- | ---: | ---: |
| Mo 1.3.1 | 87.00% | 200 |
| Mo 1.3.2 | 93.00% | 200 |
| Jev 1.13 | 82.50% | 200 |
| Jev 1.14 | 82.50% | 200 |
| Luna Decisions | 82.00% | 200 |
| PPLX | 86.50% | 200 |
| GPT-6.1 | 90.00% | 200 |
| Mo Fast | 83.50% | 200 |
| Clef | 96.50% | 200 |

Headline values are exact-answer accuracy. Additional calibration metrics are
in [`data/benchmark-results.json`](../../../data/benchmark-results.json).
