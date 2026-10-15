# ModernFinBERT Sentiment

## Task

Classify sentiment in financial text.

## Task shape

`financial text → sentiment choice`. Each evaluation item is rendered as complete state plus exactly one
typed question; the target remains outside the model-visible decision.

```json
{"decision": {"state": {"…": "…"}, "questions": {"decision": {"type": "choice", "criteria": {"…": "…"}}}}, "target": {"kind": "hard", "answer": "…"}}
```

## Results

| Model | Accuracy | Rows |
| --- | ---: | ---: |
| Mo 1.3.1 | 70.00% | 200 |
| Mo 1.3.2 | 70.50% | 200 |
| Jev 1.13 | 73.00% | 200 |
| Jev 1.14 | 73.50% | 200 |
| Luna Decisions | 68.50% | 200 |
| PPLX | 69.50% | 200 |
| GPT-6.1 | 72.50% | 200 |
| Mo Fast | 70.00% | 200 |
| Clef | 68.50% | 200 |

Headline values are exact-answer accuracy. Additional calibration metrics are
in [`data/benchmark-results.json`](../../../data/benchmark-results.json).
