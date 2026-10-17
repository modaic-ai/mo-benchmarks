# BANKING77

## Task

Route a banking request to its intent.

## Task shape

The benchmark is rendered as complete state plus one typed question. Its
official headline metric is **macro-F1**. Dataset rows are not
copied into this repository.

## Results

| Model | macro-F1 | Rows |
| --- | ---: | ---: |
| Mo 1.3.1 | 80.81% | — |
| Mo 1.3.2 | 92.05% | — |
| Jev 1.13 | 79.74% | — |
| Jev 1.14 | 79.96% | — |
| Luna Decisions | 76.61% | — |
| PPLX | 80.57% | — |
| GPT-6.1 | 86.04% | — |
| Mo Fast | 83.24% | — |
| Clef | 94.08% | — |

These are raw task scores. `Rows` is omitted because this result export records
coverage and scores, not per-task row counts. See the
[Decision Index result file](../../../decision_index/results.json).
