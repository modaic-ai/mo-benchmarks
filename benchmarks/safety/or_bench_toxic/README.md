# OR-Bench Toxic

## Task

Assign the applicable safety-risk category to a prompt.

## Task shape

`state.prompt → choice over safety categories`. Each JSONL row contains one complete `state`, exactly one typed
question, and a controller-side target.

```json
{"decision": {"state": {"…": "…"}, "questions": {"decision": {"type": "choice", "criteria": {"…": "…"}}}}, "target": {"kind": "hard", "answer": "…"}}
```

Data: [`or_bench_toxic.jsonl.gz`](../../../data/or_bench_toxic.jsonl.gz) (524 rows).

## Results

| Model | Accuracy | Rows |
| --- | ---: | ---: |
| Mo 1.3.1 | 74.62% | 524 |
| Mo 1.3.2 | 74.24% | 524 |
| Jev 1.13 | 70.99% | 524 |
| Jev 1.14 | 69.47% | 524 |
| Luna Decisions | 68.89% | 524 |
| PPLX | 75.00% | 524 |
| GPT-6.1 | 75.57% | 524 |
| Mo Fast | 72.14% | 524 |
| Clef | 70.80% | 524 |

Headline values are exact-answer accuracy. Additional calibration metrics are
in [`data/benchmark-results.json`](../../../data/benchmark-results.json).
