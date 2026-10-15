# ARC Challenge

## Task

Answer a grade-school science multiple-choice question.

## Task shape

`state.question → choice question with answer options`. Each JSONL row contains one complete `state`, exactly one typed
question, and a controller-side target.

```json
{"decision": {"state": {"…": "…"}, "questions": {"decision": {"type": "choice", "criteria": {"…": "…"}}}}, "target": {"kind": "hard", "answer": "…"}}
```

Data: [`arc_challenge.jsonl.gz`](../../../data/arc_challenge.jsonl.gz) (1,172 rows).

## Results

| Model | Accuracy | Rows |
| --- | ---: | ---: |
| Mo 1.3.1 | 97.01% | 1,172 |
| Mo 1.3.2 | 97.35% | 1,172 |
| Jev 1.13 | 97.70% | 1,172 |
| Jev 1.14 | 97.53% | 1,172 |
| Luna Decisions | 96.25% | 1,172 |
| PPLX | 96.84% | 1,172 |
| GPT-6.1 | 98.29% | 1,172 |
| Mo Fast | 96.59% | 1,172 |
| Clef | 97.87% | 1,172 |

Headline values are exact-answer accuracy. Additional calibration metrics are
in [`data/benchmark-results.json`](../../../data/benchmark-results.json).
