# MT-Bench Human Judgments

## Task

Predict which of two assistant responses human judges prefer.

## Task shape

`state.question + response_A + response_B → pairwise choice`. Each JSONL row contains one complete `state`, exactly one typed
question, and a controller-side target.

```json
{"decision": {"state": {"…": "…"}, "questions": {"decision": {"type": "choice", "criteria": {"…": "…"}}}}, "target": {"kind": "hard", "answer": "…"}}
```

Data: [`mt_bench_human_judgments.jsonl.gz`](../../../data/mt_bench_human_judgments.jsonl.gz) (1,000 rows).

## Results

| Model | Accuracy | Rows |
| --- | ---: | ---: |
| Mo 1.3.1 | 75.70% | 1,000 |
| Mo 1.3.2 | 76.40% | 1,000 |
| Jev 1.13 | 77.10% | 1,000 |
| Jev 1.14 | 76.40% | 1,000 |
| Luna Decisions | 68.80% | 1,000 |
| PPLX | 75.50% | 1,000 |
| GPT-6.1 | 71.90% | 1,000 |
| Mo Fast | 75.80% | 1,000 |
| Clef | 76.90% | 1,000 |

Headline values are exact-answer accuracy. Additional calibration metrics are
in [`data/benchmark-results.json`](../../../data/benchmark-results.json).
