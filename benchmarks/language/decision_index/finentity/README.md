# FinEntity

## Task

Identify entities in financial text.

## Task shape

The benchmark is rendered as complete state plus one typed question. Its
official headline metric is **macro-F1**. Dataset rows are not
copied into this repository.

## Results

| Model | macro-F1 | Rows |
| --- | ---: | ---: |
| Mo 1.3.1 | 95.30% | — |
| Mo 1.3.2 | 95.70% | — |
| Jev 1.13 | 86.98% | — |
| Jev 1.14 | 87.72% | — |
| Luna Decisions | 82.95% | — |
| PPLX | 95.42% | — |
| GPT-6.1 | 91.40% | — |
| Mo Fast | 85.00% | — |
| Clef | 96.09% | — |

These are raw task scores. `Rows` is omitted because this result export records
coverage and scores, not per-task row counts. See the
[Decision Index result file](../../../decision_index/results.json).
