# BRIGHT

## Task

Rank documents for reasoning-intensive retrieval queries.

## Task shape

The benchmark is rendered as complete state plus one typed question. Its
official headline metric is **nDCG@10**. Dataset rows are not
copied into this repository.

## Results

| Model | nDCG@10 | Rows |
| --- | ---: | ---: |
| Mo 1.3.1 | 49.98% | — |
| Mo 1.3.2 | 49.27% | — |
| Jev 1.13 | 47.52% | — |
| Jev 1.14 | 47.59% | — |
| Luna Decisions | 41.63% | — |
| PPLX | 50.85% | — |
| GPT-6.1 | 52.36% | — |
| Mo Fast | 0.00% | — |
| Clef | 47.46% | — |

These are raw task scores. `Rows` is omitted because this result export records
coverage and scores, not per-task row counts. See the
[Decision Index result file](../../../decision_index/results.json).
