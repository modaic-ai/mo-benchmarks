# NLI4CT

## Task

Classify inferences grounded in clinical-trial reports.

## Task shape

The benchmark is rendered as complete state plus one typed question. Its
official headline metric is **macro-F1**. Dataset rows are not
copied into this repository.

## Results

| Model | macro-F1 | Rows |
| --- | ---: | ---: |
| Mo 1.3.1 | 86.29% | — |
| Mo 1.3.2 | 86.00% | — |
| Jev 1.13 | 84.06% | — |
| Jev 1.14 | 85.02% | — |
| Luna Decisions | 78.42% | — |
| PPLX | 84.88% | — |
| GPT-6.1 | 88.02% | — |
| Mo Fast | 77.31% | — |
| Clef | 82.98% | — |

These are raw task scores. `Rows` is omitted because this result export records
coverage and scores, not per-task row counts. See the
[Decision Index result file](../../../decision_index/results.json).
