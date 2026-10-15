# ToolRet

## Task

Rank tools for a user request.

## Task shape

The benchmark is rendered as complete state plus one typed question. Its
official headline metric is **nDCG@10**. Dataset rows are not
copied into this repository.

## Results

| Model | nDCG@10 | Rows |
| --- | ---: | ---: |
| Mo 1.3.1 | 67.89% | — |
| Mo 1.3.2 | 69.09% | — |
| Jev 1.13 | 65.28% | — |
| Jev 1.14 | 64.79% | — |
| Luna Decisions | 58.90% | — |
| PPLX | 67.58% | — |
| GPT-6.1 | 67.24% | — |
| Mo Fast | 0.00% | — |
| Clef | 69.06% | — |

These are raw task scores. `Rows` is omitted because this result export records
coverage and scores, not per-task row counts. See the
[Decision Index result file](../../../decision_index/results.json).
