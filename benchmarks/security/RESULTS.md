# Security benchmark results

## Policy-Conditioned Access Review

| Model | Test | Validation |
| --- | ---: | ---: |
| Mo 1.3.1 | 96.00% | 97.05% |
| Mo 1.3.2 | 86.73% | 87.53% |
| Jev 1.13 | 73.42% | 70.99% |
| Jev 1.14 | 73.97% | 76.36% |
| Luna Decisions | 71.83% | 71.89% |
| PPLX | 84.60% | 88.39% |
| GPT-6.1 | 95.68% | 95.77% |
| Mo Fast | 83.60% | 89.08% |
| Clef | 63.06% | 69.02% |

Test has 2,201 rows; validation has 2,437 rows.

## Compositional Access Continuation

| Model | Test | Validation |
| --- | ---: | ---: |
| Mo 1.3.1 | 88.74% | 93.46% |
| Mo 1.3.2 | 84.03% | 86.72% |
| Jev 1.13 | 49.74% | 49.17% |
| Jev 1.14 | 53.14% | 54.25% |
| Luna Decisions | 49.48% | 49.27% |
| PPLX | 83.77% | 86.62% |
| GPT-6.1 | 100.00% | 100.00% |
| Mo Fast | 65.45% | 68.36% |
| Clef | 49.48% | 50.83% |

Test has 382 rows; validation has 964 rows.

## Access-Control Reasoning

| Model | Accuracy | Rows |
| --- | ---: | ---: |
| Mo 1.3.1 | 90.83% | 120 |
| Mo 1.3.2 | 94.17% | 120 |
| Jev 1.13 | 70.00% | 120 |
| Jev 1.14 | 70.83% | 120 |
| Luna Decisions | 69.17% | 120 |
| PPLX | 92.50% | 120 |
| GPT-6.1 | 100.00% | 120 |
| Mo Fast | 70.00% | 120 |
| Clef | 70.83% | 120 |

| View | Mo 1.3.1 | Mo 1.3.2 | Jev 1.13 | Jev 1.14 | Luna Decisions | PPLX | GPT-6.1 | Mo Fast | Clef |
| --- | ---: | ---: | ---: | ---: | ---: | ---: | ---: | ---: | ---: |
| Alternate authorization paths | 100.00% | 100.00% | 50.00% | 50.00% | 60.00% | 100.00% | 100.00% | 80.00% | 100.00% |
| Temporal and timezone boundaries | 70.00% | 75.00% | 75.00% | 65.00% | 50.00% | 75.00% | 100.00% | 75.00% | 70.00% |
| Sufficiency under unknown completions | 100.00% | 100.00% | 100.00% | 100.00% | 90.00% | 100.00% | 100.00% | 50.00% | 60.00% |
| Remediation status versus effective access | 100.00% | 100.00% | 50.00% | 50.00% | 50.00% | 100.00% | 100.00% | 100.00% | 70.00% |
| Four-way policy disposition | 85.00% | 90.00% | 80.00% | 85.00% | 90.00% | 85.00% | 100.00% | 80.00% | 60.00% |
| Compositional risk | 90.00% | 100.00% | 65.00% | 75.00% | 75.00% | 95.00% | 100.00% | 35.00% | 65.00% |

## User Intent Guardrails

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

The four views contain 532, 882, 366, and 1,908 rows respectively. Scores are exact-answer accuracy on hard-target rows. Jev 1.13 returned 360/366 and 1,804/1,908 answers on the two Pi views; unanswered requests are counted incorrect in the displayed accuracy. ECE and MCE use 15 equal-width bins and, for those two partial-response cells, are computed on answered rows only.

<!-- NOUL_METRICS_START -->
## Noul precision, recall, and F1

### Access-Control Reasoning

Positive answer: `yes`. Cells are `precision / recall / F1`.

| Model | Alternate paths | Time boundaries | Unknown sufficiency | Remediation vs access |
| --- | ---: | ---: | ---: | ---: |
| Mo 1.3.1 | 100.00% / 100.00% / 100.00% | 75.00% / 60.00% / 66.67% | 100.00% / 100.00% / 100.00% | 100.00% / 100.00% / 100.00% |
| Mo 1.3.2 | 100.00% / 100.00% / 100.00% | 100.00% / 50.00% / 66.67% | 100.00% / 100.00% / 100.00% | 100.00% / 100.00% / 100.00% |
| Jev 1.13 | 0.00% / 0.00% / 0.00% | 100.00% / 50.00% / 66.67% | 100.00% / 100.00% / 100.00% | 0.00% / 0.00% / 0.00% |
| Jev 1.14 | 0.00% / 0.00% / 0.00% | 71.43% / 50.00% / 58.82% | 100.00% / 100.00% / 100.00% | 0.00% / 0.00% / 0.00% |
| Luna Decisions | 100.00% / 20.00% / 33.33% | 0.00% / 0.00% / 0.00% | 90.00% / 90.00% / 90.00% | 0.00% / 0.00% / 0.00% |
| PPLX | 100.00% / 100.00% / 100.00% | 100.00% / 50.00% / 66.67% | 100.00% / 100.00% / 100.00% | 100.00% / 100.00% / 100.00% |
| GPT-6.1 | 100.00% / 100.00% / 100.00% | 100.00% / 100.00% / 100.00% | 100.00% / 100.00% / 100.00% | 100.00% / 100.00% / 100.00% |
| Mo Fast | 100.00% / 60.00% / 75.00% | 100.00% / 50.00% / 66.67% | 0.00% / 0.00% / 0.00% | 100.00% / 100.00% / 100.00% |
| Clef | 100.00% / 100.00% / 100.00% | 100.00% / 40.00% / 57.14% | 100.00% / 20.00% / 33.33% | 100.00% / 40.00% / 57.14% |

### User Intent Guardrails

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

Precision, recall, and F1 are computed on answered Noul rows. Unanswered requests are not mapped to either answer and remain incorrect in full-denominator accuracy. Structured values are in [`data/noul-metrics.json`](../../data/noul-metrics.json).
<!-- NOUL_METRICS_END -->
