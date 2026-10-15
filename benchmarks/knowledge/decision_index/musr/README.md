# MuSR

## Task

Solve long-context multi-step reasoning problems.

## Task shape

The benchmark is rendered as complete state plus one typed question. Its
official headline metric is **accuracy**. Dataset rows are not
copied into this repository.

## Results

| Model | accuracy | Rows |
| --- | ---: | ---: |
| Mo 1.3.1 | 72.34% | — |
| Mo 1.3.2 | 69.28% | — |
| Jev 1.13 | 66.09% | — |
| Jev 1.14 | 72.07% | — |
| Luna Decisions | 56.65% | — |
| PPLX | 70.74% | — |
| GPT-6.1 | 85.64% | — |
| Mo Fast | 68.88% | — |
| Clef | 83.78% | — |

These are raw task scores. `Rows` is omitted because this result export records
coverage and scores, not per-task row counts. See the
[Decision Index result file](../../../decision_index/results.json).
