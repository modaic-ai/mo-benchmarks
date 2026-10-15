# HaluEval Summarization

## Task

Decide whether a summary is supported by its source document.

## Task shape

`state.document + state.summary → binary Noul decision`. Each JSONL row contains one complete `state`, exactly one typed
question, and a controller-side target.

```json
{"decision": {"state": {"…": "…"}, "questions": {"decision": {"type": "noul"}}}, "target": {"kind": "hard", "answer": "…"}}
```

Data: [`halueval_summarization.jsonl.gz`](../../../data/halueval_summarization.jsonl.gz) (10,000 rows).

## Results

| Model | Accuracy | Rows |
| --- | ---: | ---: |
| Mo 1.3.1 | 67.71% | 10,000 |
| Mo 1.3.2 | 64.34% | 10,000 |
| Jev 1.13 | 72.31% | 10,000 |
| Jev 1.14 | 73.41% | 10,000 |
| Luna Decisions | 78.26% | 10,000 |
| PPLX | 64.32% | 10,000 |
| GPT-6.1 | 75.30% | 10,000 |
| Mo Fast | 67.95% | 10,000 |
| Clef | 69.31% | 10,000 |

Headline values are exact-answer accuracy. Additional calibration metrics are
in [`data/benchmark-results.json`](../../../data/benchmark-results.json).
