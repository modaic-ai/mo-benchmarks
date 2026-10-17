# FinCalc NLI

## Task

Decide whether a numerical financial claim follows from the supplied evidence.

## Task shape

`financial evidence + claim → entailment choice`. Each evaluation item is rendered as complete state plus exactly one
typed question; the target remains outside the model-visible decision.

```json
{"decision": {"state": {"…": "…"}, "questions": {"decision": {"type": "choice", "criteria": {"…": "…"}}}}, "target": {"kind": "hard", "answer": "…"}}
```

## Results

| Model | Accuracy | Rows |
| --- | ---: | ---: |
| Mo 1.3.1 | 89.00% | 200 |
| Mo 1.3.2 | 93.50% | 200 |
| Jev 1.13 | 69.00% | 200 |
| Jev 1.14 | 71.50% | 200 |
| Luna Decisions | 68.50% | 200 |
| PPLX | 89.00% | 200 |
| GPT-6.1 | 98.50% | 200 |
| Mo Fast | 65.00% | 200 |
| Clef | 68.50% | 200 |

Headline values are exact-answer accuracy. Additional calibration metrics are
in [`data/benchmark-results.json`](../../../data/benchmark-results.json).
