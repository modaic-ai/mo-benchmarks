# MuSR Murder Mysteries

## Task

Identify the culprit from a long-form murder mystery.

## Task shape

`state.question → choice question over suspects`. Each JSONL row contains one complete `state`, exactly one typed
question, and a controller-side target.

```json
{"decision": {"state": {"…": "…"}, "questions": {"decision": {"type": "choice", "criteria": {"…": "…"}}}}, "target": {"kind": "hard", "answer": "…"}}
```

Data: [`musr_murder_mysteries.jsonl.gz`](../../../data/musr_murder_mysteries.jsonl.gz) (250 rows).

## Results

| Model | Accuracy | Rows |
| --- | ---: | ---: |
| Mo 1.3.1 | 75.60% | 250 |
| Mo 1.3.2 | 74.80% | 250 |
| Jev 1.13 | 72.80% | 250 |
| Jev 1.14 | 74.00% | 250 |
| Luna Decisions | 59.60% | 250 |
| PPLX | 74.00% | 250 |
| GPT-6.1 | 86.40% | 250 |
| Mo Fast | 68.80% | 250 |
| Clef | 84.40% | 250 |

Headline values are exact-answer accuracy. Additional calibration metrics are
in [`data/benchmark-results.json`](../../../data/benchmark-results.json).
