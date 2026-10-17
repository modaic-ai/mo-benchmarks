# JudgeBench

## Task

Choose the better of two candidate responses to a question.

## Task shape

`state.question + response_A + response_B → pairwise choice`. Each JSONL row contains one complete `state`, exactly one typed
question, and a controller-side target.

```json
{"decision": {"state": {"…": "…"}, "questions": {"decision": {"type": "choice", "criteria": {"…": "…"}}}}, "target": {"kind": "hard", "answer": "…"}}
```

Data: [`judge_bench.jsonl.gz`](../../../data/judge_bench.jsonl.gz) (280 rows).

## Results

| Model | Accuracy | Rows |
| --- | ---: | ---: |
| Mo 1.3.1 | 80.36% | 280 |
| Mo 1.3.2 | 80.71% | 280 |
| Jev 1.13 | 77.86% | 280 |
| Jev 1.14 | 77.50% | 280 |
| Luna Decisions | 67.14% | 280 |
| PPLX | 80.71% | 280 |
| GPT-6.1 | 94.29% | 280 |
| Mo Fast | 80.00% | 280 |
| Clef | 76.07% | 280 |

Headline values are exact-answer accuracy. Additional calibration metrics are
in [`data/benchmark-results.json`](../../../data/benchmark-results.json).
