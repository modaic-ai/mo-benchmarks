# ROD101 Essay Scoring

## Task

Assign a holistic essay-quality score from 1 to 10.

## Task shape

`state.essay → ordered score decision`. Each JSONL row contains one complete `state`, exactly one typed
question, and a controller-side target.

```json
{"decision": {"state": {"…": "…"}, "questions": {"decision": {"type": "score", "criteria": ["1", "…", "10"]}}}, "target": {"kind": "hard", "answer": "…"}}
```

Data: [`rod101_essay_scoring.jsonl.gz`](../../../data/rod101_essay_scoring.jsonl.gz) (81 rows).

## Results

| Model | Accuracy | Rows |
| --- | ---: | ---: |
| Mo 1.3.1 | 16.05% | 81 |
| Mo 1.3.2 | 16.05% | 81 |
| Jev 1.13 | 24.69% | 81 |
| Jev 1.14 | 28.40% | 81 |
| Luna Decisions | 24.69% | 81 |
| PPLX | 17.28% | 81 |
| GPT-6.1 | 29.63% | 81 |
| Mo Fast | 16.05% | 81 |
| Clef | 29.63% | 81 |

Headline values are exact-answer accuracy. Additional calibration metrics are
in [`data/benchmark-results.json`](../../../data/benchmark-results.json).
