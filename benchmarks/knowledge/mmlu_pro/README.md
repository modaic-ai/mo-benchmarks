# MMLU-Pro

## Task

Answer a challenging multi-domain knowledge and reasoning question.

## Task shape

`state.question → choice question with up to ten options`. Each JSONL row contains one complete `state`, exactly one typed
question, and a controller-side target.

```json
{"decision": {"state": {"…": "…"}, "questions": {"decision": {"type": "choice", "criteria": {"…": "…"}}}}, "target": {"kind": "hard", "answer": "…"}}
```

Data: [`mmlu_pro.jsonl.gz`](../../../data/mmlu_pro.jsonl.gz) (12,032 rows).

## Results

| Model | Accuracy | Rows |
| --- | ---: | ---: |
| Mo 1.3.1 | 71.35% | 12,032 |
| Mo 1.3.2 | 72.90% | 12,032 |
| Jev 1.13 | 82.81% | 12,032 |
| Jev 1.14 | 82.40% | 12,032 |
| Luna Decisions | 57.02% | 12,032 |
| PPLX | 70.69% | 12,032 |
| GPT-6.1 | 89.31% | 12,032 |
| Mo Fast | 67.21% | 12,032 |
| Clef | 65.78% | 12,032 |

Headline values are exact-answer accuracy. Additional calibration metrics are
in [`data/benchmark-results.json`](../../../data/benchmark-results.json).
