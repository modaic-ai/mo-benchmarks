# CLINC150+OOS

## Task

Route an utterance to an intent or out-of-scope class.

## Task shape

The benchmark is rendered as complete state plus one typed question. Its
official headline metric is **macro-F1**. Dataset rows are not
copied into this repository.

## Results

| Model | macro-F1 | Rows |
| --- | ---: | ---: |
| Mo 1.3.1 | 91.76% | — |
| Mo 1.3.2 | 96.93% | — |
| Jev 1.13 | 89.27% | — |
| Jev 1.14 | 90.12% | — |
| Luna Decisions | 88.86% | — |
| PPLX | 91.52% | — |
| GPT-6.1 | 96.28% | — |
| Mo Fast | 88.99% | — |
| Clef | 97.41% | — |

These are raw task scores. `Rows` is omitted because this result export records
coverage and scores, not per-task row counts. See the
[Decision Index result file](../../../decision_index/results.json).
