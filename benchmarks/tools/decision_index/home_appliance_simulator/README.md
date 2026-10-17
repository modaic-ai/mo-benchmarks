# Home appliance simulator

## Task

Choose actions in a simulated home-appliance environment.

## Task shape

The benchmark is rendered as complete state plus one typed question. Its
official headline metric is **case exact accuracy**. Dataset rows are not
copied into this repository.

## Results

| Model | case exact accuracy | Rows |
| --- | ---: | ---: |
| Mo 1.3.1 | 82.95% | — |
| Mo 1.3.2 | 80.68% | — |
| Jev 1.13 | 52.27% | — |
| Jev 1.14 | 46.59% | — |
| Luna Decisions | 43.18% | — |
| PPLX | 80.68% | — |
| GPT-6.1 | 82.95% | — |
| Mo Fast | 46.59% | — |
| Clef | 80.68% | — |

These are raw task scores. `Rows` is omitted because this result export records
coverage and scores, not per-task row counts. See the
[Decision Index result file](../../../decision_index/results.json).
