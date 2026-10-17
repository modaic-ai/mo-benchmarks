# ChessBench

## Task

Choose the correct chess decision from a board state.

## Task shape

The benchmark is rendered as complete state plus one typed question. Its
official headline metric is **accuracy**. Dataset rows are not
copied into this repository.

## Results

| Model | accuracy | Rows |
| --- | ---: | ---: |
| Mo 1.3.1 | 18.10% | — |
| Mo 1.3.2 | 17.58% | — |
| Jev 1.13 | 17.22% | — |
| Jev 1.14 | 16.88% | — |
| Luna Decisions | 16.56% | — |
| PPLX | 17.68% | — |
| GPT-6.1 | 41.70% | — |
| Mo Fast | 16.88% | — |
| Clef | 24.50% | — |

These are raw task scores. `Rows` is omitted because this result export records
coverage and scores, not per-task row counts. See the
[Decision Index result file](../../../decision_index/results.json).
