# GPQA Diamond

## Task

Answer a graduate-level science multiple-choice question.

## Task shape

`state.question_with_inline_options → choice question`. Each JSONL row contains one complete `state`, exactly one typed
question, and a controller-side target.

```json
{"decision": {"state": {"…": "…"}, "questions": {"decision": {"type": "choice", "criteria": {"…": "…"}}}}, "target": {"kind": "hard", "answer": "…"}}
```

Data: [`gpqa_diamond.jsonl.gz`](../../../data/gpqa_diamond.jsonl.gz) (198 rows).

## Results

| Model | Accuracy | Rows |
| --- | ---: | ---: |
| Mo 1.3.1 | 55.56% | 198 |
| Mo 1.3.2 | 58.08% | 198 |
| Jev 1.13 | 68.18% | 198 |
| Jev 1.14 | 68.69% | 198 |
| Luna Decisions | 47.98% | 198 |
| PPLX | 55.56% | 198 |
| GPT-6.1 | 94.44% | 198 |
| Mo Fast | 47.47% | 198 |
| Clef | 45.96% | 198 |

Headline values are exact-answer accuracy. Additional calibration metrics are
in [`data/benchmark-results.json`](../../../data/benchmark-results.json).
