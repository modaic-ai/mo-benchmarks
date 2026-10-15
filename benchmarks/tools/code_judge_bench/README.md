# CodeJudgeBench

## Task

Choose the better of two code implementations for a programming problem.

## Task shape

`state.problem + code_A + code_B → pairwise choice`. Each JSONL row contains one complete `state`, exactly one typed
question, and a controller-side target.

```json
{"decision": {"state": {"…": "…"}, "questions": {"decision": {"type": "choice", "criteria": {"…": "…"}}}}, "target": {"kind": "hard", "answer": "…"}}
```

Data: [`code_judge_bench.jsonl.gz`](../../../data/code_judge_bench.jsonl.gz) (344 rows).

## Results

| Model | Accuracy | Rows |
| --- | ---: | ---: |
| Mo 1.3.1 | 73.55% | 344 |
| Mo 1.3.2 | 74.42% | 344 |
| Jev 1.13 | 63.37% | 344 |
| Jev 1.14 | 63.37% | 344 |
| Luna Decisions | 62.79% | 344 |
| PPLX | 72.67% | 344 |
| GPT-6.1 | 94.19% | 344 |
| Mo Fast | 66.57% | 344 |
| Clef | 64.24% | 344 |

Headline values are exact-answer accuracy. Additional calibration metrics are
in [`data/benchmark-results.json`](../../../data/benchmark-results.json).
