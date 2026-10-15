# CRUXEval

## Task

Predict or reason about Python program execution.

## Task shape

The benchmark is rendered as complete state plus one typed question. Its
official headline metric is **accuracy**. Dataset rows are not
copied into this repository.

## Results

| Model | accuracy | Rows |
| --- | ---: | ---: |
| Mo 1.3.1 | 86.49% | — |
| Mo 1.3.2 | 88.07% | — |
| Jev 1.13 | 72.98% | — |
| Jev 1.14 | 75.96% | — |
| Luna Decisions | 65.44% | — |
| PPLX | 85.61% | — |
| GPT-6.1 | 100.00% | — |
| Mo Fast | 64.74% | — |
| Clef | 86.49% | — |

These are raw task scores. `Rows` is omitted because this result export records
coverage and scores, not per-task row counts. See the
[Decision Index result file](../../../decision_index/results.json).
