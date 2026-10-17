# VAST

## Task

Classify stance toward a target.

## Task shape

The benchmark is rendered as complete state plus one typed question. Its
official headline metric is **macro-F1**. Dataset rows are not
copied into this repository.

## Results

| Model | macro-F1 | Rows |
| --- | ---: | ---: |
| Mo 1.3.1 | 77.48% | — |
| Mo 1.3.2 | 74.77% | — |
| Jev 1.13 | 64.63% | — |
| Jev 1.14 | 73.23% | — |
| Luna Decisions | 57.37% | — |
| PPLX | 76.72% | — |
| GPT-6.1 | 79.74% | — |
| Mo Fast | 78.01% | — |
| Clef | 59.34% | — |

These are raw task scores. `Rows` is omitted because this result export records
coverage and scores, not per-task row counts. See the
[Decision Index result file](../../../decision_index/results.json).
