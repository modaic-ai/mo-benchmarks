# SATA-Bench

## Task

Complete sequential reasoning tasks with case-level exact scoring.

## Task shape

The benchmark is rendered as complete state plus one typed question. Its
official headline metric is **case exact accuracy**. Dataset rows are not
copied into this repository.

## Results

| Model | case exact accuracy | Rows |
| --- | ---: | ---: |
| Mo 1.3.1 | 22.61% | — |
| Mo 1.3.2 | 38.42% | — |
| Jev 1.13 | 26.42% | — |
| Jev 1.14 | 27.64% | — |
| Luna Decisions | 28.36% | — |
| PPLX | 28.18% | — |
| GPT-6.1 | 44.12% | — |
| Mo Fast | 32.79% | — |
| Clef | 33.45% | — |

These are raw task scores. `Rows` is omitted because this result export records
coverage and scores, not per-task row counts. See the
[Decision Index result file](../../../decision_index/results.json).
