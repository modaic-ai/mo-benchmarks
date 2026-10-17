# ACOS

## Task

Identify aspect, category, opinion, and sentiment information.

## Task shape

The benchmark is rendered as complete state plus one typed question. Its
official headline metric is **per-review F1**. Dataset rows are not
copied into this repository.

## Results

| Model | per-review F1 | Rows |
| --- | ---: | ---: |
| Mo 1.3.1 | 29.29% | — |
| Mo 1.3.2 | 30.05% | — |
| Jev 1.13 | 29.52% | — |
| Jev 1.14 | 32.89% | — |
| Luna Decisions | 14.43% | — |
| PPLX | 28.24% | — |
| GPT-6.1 | 49.52% | — |
| Mo Fast | 33.29% | — |
| Clef | 33.17% | — |

These are raw task scores. `Rows` is omitted because this result export records
coverage and scores, not per-task row counts. See the
[Decision Index result file](../../../decision_index/results.json).
