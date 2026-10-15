# MuSR Object Placements

## Task

Track object locations through a long sequence of events.

## Task shape

`state.question → choice question over locations`. Each JSONL row contains one complete `state`, exactly one typed
question, and a controller-side target.

```json
{"decision": {"state": {"…": "…"}, "questions": {"decision": {"type": "choice", "criteria": {"…": "…"}}}}, "target": {"kind": "hard", "answer": "…"}}
```

Data: [`musr_object_placements.jsonl.gz`](../../../data/musr_object_placements.jsonl.gz) (256 rows).

## Results

| Model | Accuracy | Rows |
| --- | ---: | ---: |
| Mo 1.3.1 | 67.58% | 256 |
| Mo 1.3.2 | 56.64% | 256 |
| Jev 1.13 | 49.22% | 256 |
| Jev 1.14 | 62.11% | 256 |
| Luna Decisions | 50.78% | 256 |
| PPLX | 62.89% | 256 |
| GPT-6.1 | 84.38% | 256 |
| Mo Fast | 58.59% | 256 |
| Clef | 67.58% | 256 |

Headline values are exact-answer accuracy. Additional calibration metrics are
in [`data/benchmark-results.json`](../../../data/benchmark-results.json).
