# Argument Quality Ranking

## Task

Classify whether an argument is high or low quality for its topic.

## Task shape

`state.topic + state.argument → binary choice`. Each JSONL row contains one complete `state`, exactly one typed
question, and a controller-side target.

```json
{"decision": {"state": {"…": "…"}, "questions": {"decision": {"type": "choice", "criteria": {"…": "…"}}}}, "target": {"kind": "hard", "answer": "…"}}
```

Data: [`argument_quality_ranking.jsonl.gz`](../../../data/argument_quality_ranking.jsonl.gz) (2,469 rows).

## Results

| Model | Accuracy | Rows |
| --- | ---: | ---: |
| Mo 1.3.1 | 28.88% | 2,469 |
| Mo 1.3.2 | 47.83% | 2,469 |
| Jev 1.13 | 18.27% | 2,469 |
| Jev 1.14 | 19.97% | 2,469 |
| Luna Decisions | 29.65% | 2,469 |
| PPLX | 31.23% | 2,469 |
| GPT-6.1 | 52.57% | 2,469 |
| Mo Fast | 38.27% | 2,469 |
| Clef | 26.81% | 2,469 |

Headline values are exact-answer accuracy. Additional calibration metrics are
in [`data/benchmark-results.json`](../../../data/benchmark-results.json).
