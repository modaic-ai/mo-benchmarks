# HoVer

## Task

Verify a claim using multi-hop evidence.

## Task shape

The benchmark is rendered as complete state plus one typed question. Its
official headline metric is **accuracy**. Dataset rows are not
copied into this repository.

## Results

| Model | accuracy | Rows |
| --- | ---: | ---: |
| Mo 1.3.1 | 82.23% | — |
| Mo 1.3.2 | 83.55% | — |
| Jev 1.13 | 72.85% | — |
| Jev 1.14 | 76.78% | — |
| Luna Decisions | 71.03% | — |
| PPLX | 74.12% | — |
| GPT-6.1 | 83.00% | — |
| Mo Fast | 81.93% | — |
| Clef | 65.58% | — |

These are raw task scores. `Rows` is omitted because this result export records
coverage and scores, not per-task row counts. See the
[Decision Index result file](../../../decision_index/results.json).
