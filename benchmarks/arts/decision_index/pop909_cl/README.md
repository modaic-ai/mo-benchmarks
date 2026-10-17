# POP909-CL

## Task

Classify a musical chord by pitch class.

## Task shape

The benchmark is rendered as complete state plus one typed question. Its
official headline metric is **accuracy**. Dataset rows are not
copied into this repository.

## Results

| Model | accuracy | Rows |
| --- | ---: | ---: |
| Mo 1.3.1 | 56.10% | — |
| Mo 1.3.2 | 62.08% | — |
| Jev 1.13 | 16.58% | — |
| Jev 1.14 | 15.86% | — |
| Luna Decisions | 20.62% | — |
| PPLX | 55.88% | — |
| GPT-6.1 | 81.47% | — |
| Mo Fast | 40.33% | — |
| Clef | 15.47% | — |

These are raw task scores. `Rows` is omitted because this result export records
coverage and scores, not per-task row counts. See the
[Decision Index result file](../../../decision_index/results.json).
