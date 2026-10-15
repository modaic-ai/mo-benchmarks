# ANLI

## Task

Classify adversarial natural-language inference examples.

## Task shape

The benchmark is rendered as complete state plus one typed question. Its
official headline metric is **macro-F1**. Dataset rows are not
copied into this repository.

## Results

| Model | macro-F1 | Rows |
| --- | ---: | ---: |
| Mo 1.3.1 | 74.85% | — |
| Mo 1.3.2 | 76.00% | — |
| Jev 1.13 | 74.79% | — |
| Jev 1.14 | 74.42% | — |
| Luna Decisions | 67.42% | — |
| PPLX | 74.28% | — |
| GPT-6.1 | 81.00% | — |
| Mo Fast | 77.48% | — |
| Clef | 69.97% | — |

These are raw task scores. `Rows` is omitted because this result export records
coverage and scores, not per-task row counts. See the
[Decision Index result file](../../../decision_index/results.json).
