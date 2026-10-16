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

<!-- NOUL_METRICS_START -->
## Noul metrics

Positive answer: `yes` (hallucinated).

| Model | Precision | Recall | F1 | Answered |
| --- | ---: | ---: | ---: | ---: |
| Mo 1.3.1 | 85.10% | 43.09% | 57.21% | 10,000/10,000 |
| Mo 1.3.2 | 94.02% | 30.78% | 46.38% | 10,000/10,000 |
| Jev 1.13 | 82.77% | 56.49% | 67.15% | 10,000/10,000 |
| Jev 1.14 | 80.10% | 62.44% | 70.17% | 10,000/10,000 |
| Luna Decisions | 95.13% | 59.66% | 73.33% | 10,000/10,000 |
| PPLX | 93.91% | 30.78% | 46.36% | 10,000/10,000 |
| GPT-6.1 | 74.41% | 77.27% | 75.81% | 10,000/10,000 |
| Mo Fast | 79.14% | 48.92% | 60.47% | 10,000/10,000 |
| Clef | 91.81% | 42.53% | 58.14% | 10,000/10,000 |

Precision, recall, and F1 are computed on answered Noul rows. Unanswered requests are not mapped to either answer and remain incorrect in full-denominator accuracy. Structured values are in [`data/noul-metrics.json`](../../../data/noul-metrics.json).
<!-- NOUL_METRICS_END -->
