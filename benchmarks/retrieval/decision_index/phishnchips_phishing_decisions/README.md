# PhishNChips phishing decisions

## Task

Decide whether a message is a phishing attempt.

## Task shape

The benchmark is rendered as complete state plus one typed question. Its
official headline metric is **accuracy**. Dataset rows are not
copied into this repository.

## Results

| Model | accuracy | Rows |
| --- | ---: | ---: |
| Mo 1.3.1 | 74.60% | — |
| Mo 1.3.2 | 73.90% | — |
| Jev 1.13 | 62.55% | — |
| Jev 1.14 | 84.15% | — |
| Luna Decisions | 0.00% | — |
| PPLX | 73.15% | — |
| GPT-6.1 | 83.20% | — |
| Mo Fast | 0.00% | — |
| Clef | 79.35% | — |

These are raw task scores. `Rows` is omitted because this result export records
coverage and scores, not per-task row counts. See the
[Decision Index result file](../../../decision_index/results.json).
