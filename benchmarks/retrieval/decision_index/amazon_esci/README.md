# Amazon ESCI

## Task

Classify product relevance to a shopping query.

## Task shape

The benchmark is rendered as complete state plus one typed question. Its
official headline metric is **macro-F1**. Dataset rows are not
copied into this repository.

## Results

| Model | macro-F1 | Rows |
| --- | ---: | ---: |
| Mo 1.3.1 | 59.44% | — |
| Mo 1.3.2 | 59.01% | — |
| Jev 1.13 | 55.21% | — |
| Jev 1.14 | 56.46% | — |
| Luna Decisions | 53.66% | — |
| PPLX | 60.40% | — |
| GPT-6.1 | 61.62% | — |
| Mo Fast | 56.05% | — |
| Clef | 57.37% | — |

These are raw task scores. `Rows` is omitted because this result export records
coverage and scores, not per-task row counts. See the
[Decision Index result file](../../../decision_index/results.json).
