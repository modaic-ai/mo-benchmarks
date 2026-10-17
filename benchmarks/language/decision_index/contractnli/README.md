# ContractNLI

## Task

Classify hypotheses against contract text.

## Task shape

The benchmark is rendered as complete state plus one typed question. Its
official headline metric is **macro-F1**. Dataset rows are not
copied into this repository.

## Results

| Model | macro-F1 | Rows |
| --- | ---: | ---: |
| Mo 1.3.1 | 77.68% | — |
| Mo 1.3.2 | 78.51% | — |
| Jev 1.13 | 71.69% | — |
| Jev 1.14 | 70.85% | — |
| Luna Decisions | 76.98% | — |
| PPLX | 78.38% | — |
| GPT-6.1 | 75.24% | — |
| Mo Fast | 77.34% | — |
| Clef | 81.35% | — |

These are raw task scores. `Rows` is omitted because this result export records
coverage and scores, not per-task row counts. See the
[Decision Index result file](../../../decision_index/results.json).
