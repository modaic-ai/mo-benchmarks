# iSarcasmEval

## Task

Detect sarcasm in English text.

## Task shape

The benchmark is rendered as complete state plus one typed question. Its
official headline metric is **Sarcasm F1 · track A, English**. Dataset rows are not
copied into this repository.

## Results

| Model | Sarcasm F1 · track A, English | Rows |
| --- | ---: | ---: |
| Mo 1.3.1 | 64.19% | — |
| Mo 1.3.2 | 66.80% | — |
| Jev 1.13 | 50.51% | — |
| Jev 1.14 | 53.67% | — |
| Luna Decisions | 37.26% | — |
| PPLX | 71.04% | — |
| GPT-6.1 | 61.69% | — |
| Mo Fast | 53.35% | — |
| Clef | 46.39% | — |

These are raw task scores. `Rows` is omitted because this result export records
coverage and scores, not per-task row counts. See the
[Decision Index result file](../../../decision_index/results.json).
