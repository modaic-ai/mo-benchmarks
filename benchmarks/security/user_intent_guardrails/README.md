# User Intent Guardrails

## Task

Decide whether a proposed tool call matches the authenticated user's current goal, constraints, corrections, and latest instructions.

## Task shape

`conversation trajectory and final proposed tool call → aligned or not aligned`

```json
{"benchmark":"user_intent_guardrails","view":"openhands_balanced","decision":{"state":{"trajectory":[{"…":"…"}],"proposed_tool_call":{"…":"…"}},"questions":{"intent_alignment":{"type":"noul","instructions":"…"}}},"target":{"kind":"hard","answer":"yes"}}
```

Results are reported on four views:

- OpenHands balanced: 532 rows
- OpenHands prevalence: 882 rows
- Pi balanced: 366 rows
- Pi prevalence: 1,908 rows

Balanced and prevalence views from the same source overlap. They are separate reporting views and must not be pooled as independent examples.

Three representative Security rows are visible in [`../examples.jsonl`](../examples.jsonl). The complete dataset is private: [`modaic/security-decision-benchmarks`](https://huggingface.co/datasets/modaic/security-decision-benchmarks/tree/33e882d646f5a98f21eb53ec8c02299f6df21333).

## Results

| Model | OpenHands balanced | OpenHands prevalence | Pi balanced | Pi prevalence |
| --- | ---: | ---: | ---: | ---: |
| Mo 1.3.1 | 87.97% | 96.37% | 74.59% | 97.33% |
| Mo 1.3.2 | 83.83% | 96.15% | 65.03% | 98.17% |
| Jev 1.13 | 81.77% | 93.20% | 56.01% | 92.14% |
| Jev 1.14 | 83.27% | 93.76% | 57.65% | 97.27% |
| Luna Decisions | 81.58% | 85.94% | 61.75% | 93.71% |
| PPLX | 84.59% | 96.60% | 65.57% | 98.58% |
| GPT-6.1 | 96.99% | 99.32% | 95.08% | 99.53% |
| Mo Fast | 81.39% | 87.64% | 59.29% | 90.83% |
| Clef | 82.52% | 90.82% | 58.47% | 93.92% |

Scores are exact-answer accuracy on hard-target rows. Jev 1.13 returned 360/366 and 1,804/1,908 answers on the two Pi views; unanswered requests are counted incorrect in the displayed accuracy. Correctness AUROC, 15-bin ECE/MCE, multiclass Brier, and categorical NLL for those two cells apply to answered rows only.

<!-- NOUL_METRICS_START -->
## Noul metrics

Positive answer: `no` (not aligned). Cells are `precision / recall / F1`.

| Model | OpenHands balanced | OpenHands prevalence | Pi balanced | Pi prevalence |
| --- | ---: | ---: | ---: | ---: |
| Mo 1.3.1 | 95.09% / 80.08% / 86.94% | 72.88% / 72.88% / 72.88% | 91.67% / 54.10% / 68.04% | 12.77% / 37.50% / 19.05% |
| Mo 1.3.2 | 96.39% / 70.30% / 81.30% | 77.78% / 59.32% / 67.31% | 98.25% / 30.60% / 46.67% | 17.24% / 31.25% / 22.22% |
| Jev 1.13 | 91.22% / 70.30% / 79.41% | 49.37% / 66.10% / 56.52% | 72.13% / 24.18% / 36.21% | 5.88% / 12.50% / 8.00% |
| Jev 1.14 | 90.78% / 74.06% / 81.57% | 52.56% / 69.49% / 59.85% | 70.00% / 26.78% / 38.74% | 7.14% / 18.75% / 10.34% |
| Luna Decisions | 80.22% / 83.83% / 81.99% | 29.03% / 76.27% / 42.06% | 74.16% / 36.07% / 48.53% | 3.57% / 25.00% / 6.25% |
| PPLX | 97.92% / 70.68% / 82.10% | 83.72% / 61.02% / 70.59% | 96.72% / 32.24% / 48.36% | 23.81% / 31.25% / 27.03% |
| GPT-6.1 | 97.35% / 96.62% / 96.98% | 94.92% / 94.92% / 94.92% | 95.58% / 94.54% / 95.05% | 66.67% / 87.50% / 75.68% |
| Mo Fast | 88.48% / 72.18% / 79.50% | 29.84% / 62.71% / 40.44% | 69.32% / 33.33% / 45.02% | 4.05% / 43.75% / 7.41% |
| Clef | 87.12% / 76.32% / 81.36% | 39.62% / 71.19% / 50.91% | 71.83% / 27.87% / 40.16% | 3.70% / 25.00% / 6.45% |

Precision, recall, and F1 are computed on answered Noul rows. Unanswered requests are not mapped to either answer and remain incorrect in full-denominator accuracy. Structured values are in [`data/noul-metrics.json`](../../../data/noul-metrics.json).
<!-- NOUL_METRICS_END -->
