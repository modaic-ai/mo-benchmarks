# MuSR Team Allocation

## Task

Choose the team assignment that satisfies a set of constraints.

## Task shape

`state.question → choice question over allocations`. Each JSONL row contains one complete `state`, exactly one typed
question, and a controller-side target.

```json
{"decision": {"state": {"…": "…"}, "questions": {"decision": {"type": "choice", "criteria": {"…": "…"}}}}, "target": {"kind": "hard", "answer": "…"}}
```

Data: [`musr_team_allocation.jsonl.gz`](../../../data/musr_team_allocation.jsonl.gz) (250 rows).

## Results

| Model | Accuracy | Rows |
| --- | ---: | ---: |
| Mo 1.3.1 | 74.00% | 250 |
| Mo 1.3.2 | 75.60% | 250 |
| Jev 1.13 | 72.80% | 250 |
| Jev 1.14 | 79.60% | 250 |
| Luna Decisions | 67.20% | 250 |
| PPLX | 75.60% | 250 |
| GPT-6.1 | 86.80% | 250 |
| Mo Fast | 72.00% | 250 |
| Clef | 94.00% | 250 |

Headline values are exact-answer accuracy. Additional calibration metrics are
in [`data/benchmark-results.json`](../../../data/benchmark-results.json).
