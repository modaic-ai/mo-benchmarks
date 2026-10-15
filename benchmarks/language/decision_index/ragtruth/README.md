# RAGTruth

## Task

Detect hallucinated content in generated answers.

## Task shape

The benchmark is rendered as complete state plus one typed question. Its
official headline metric is **F1 on hallucinated class**. Dataset rows are not
copied into this repository.

## Results

| Model | F1 on hallucinated class | Rows |
| --- | ---: | ---: |
| Mo 1.3.1 | 82.20% | — |
| Mo 1.3.2 | 82.12% | — |
| Jev 1.13 | 76.53% | — |
| Jev 1.14 | 75.19% | — |
| Luna Decisions | 73.74% | — |
| PPLX | 83.14% | — |
| GPT-6.1 | 72.03% | — |
| Mo Fast | 0.00% | — |
| Clef | 79.54% | — |

These are raw task scores. `Rows` is omitted because this result export records
coverage and scores, not per-task row counts. See the
[Decision Index result file](../../../decision_index/results.json).
