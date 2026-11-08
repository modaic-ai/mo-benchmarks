# Security benchmark results

## Policy-Conditioned Access Review

| Model | Test | Validation |
| --- | ---: | ---: |
| Mo 2.0 | 92.50% | 92.29% |
| Mo 1.3.1 | 96.00% | 97.05% |
| Jev 1.13 | 73.42% | 70.99% |
| Jev 1.14 | 73.97% | 76.36% |
| Luna Decisions | 71.83% | 71.89% |
| PPLX | 84.60% | 88.39% |
| GPT-6.1 | 95.68% | 95.77% |
| Clef | 63.06% | 69.02% |

Test has 2,201 rows; validation has 2,437 rows.

## Compositional Access Continuation

| Model | Test | Validation |
| --- | ---: | ---: |
| Mo 2.0 | 85.08% | 85.79% |
| Mo 1.3.1 | 88.74% | 93.46% |
| Jev 1.13 | 49.74% | 49.17% |
| Jev 1.14 | 53.14% | 54.25% |
| Luna Decisions | 49.48% | 49.27% |
| PPLX | 83.77% | 86.62% |
| GPT-6.1 | 100.00% | 100.00% |
| Clef | 49.48% | 50.83% |

Test has 382 rows; validation has 964 rows.

## Access-Control Reasoning

| Model | Accuracy | Rows |
| --- | ---: | ---: |
| Mo 2.0 | 91.67% | 120 |
| Mo 1.3.1 | 90.83% | 120 |
| Jev 1.13 | 70.00% | 120 |
| Jev 1.14 | 70.83% | 120 |
| Luna Decisions | 69.17% | 120 |
| PPLX | 92.50% | 120 |
| GPT-6.1 | 100.00% | 120 |
| Clef | 70.83% | 120 |

| View | Mo 2.0 | Mo 1.3.1 | Jev 1.13 | Jev 1.14 | Luna Decisions | PPLX | GPT-6.1 | Clef |
| --- | ---: | ---: | ---: | ---: | ---: | ---: | ---: | ---: |
| Alternate authorization paths | 100.00% | 100.00% | 50.00% | 50.00% | 60.00% | 100.00% | 100.00% | 100.00% |
| Temporal and timezone boundaries | 80.00% | 70.00% | 75.00% | 65.00% | 50.00% | 75.00% | 100.00% | 70.00% |
| Sufficiency under unknown completions | 100.00% | 100.00% | 100.00% | 100.00% | 90.00% | 100.00% | 100.00% | 60.00% |
| Remediation status versus effective access | 100.00% | 100.00% | 50.00% | 50.00% | 50.00% | 100.00% | 100.00% | 70.00% |
| Four-way policy disposition | 100.00% | 85.00% | 80.00% | 85.00% | 90.00% | 85.00% | 100.00% | 60.00% |
| Compositional risk | 70.00% | 90.00% | 65.00% | 75.00% | 75.00% | 95.00% | 100.00% | 65.00% |

## User Intent Guardrails

| Model | OpenHands balanced | OpenHands prevalence | Pi balanced | Pi prevalence |
| --- | ---: | ---: | ---: | ---: |
| Mo 2.0 | 87.22% | 92.18% | 68.58% | 96.28% |
| Mo 1.3.1 | 87.97% | 96.37% | 74.59% | 97.33% |
| Jev 1.13 | 81.77% | 93.20% | 56.01% | 92.14% |
| Jev 1.14 | 83.27% | 93.76% | 57.65% | 97.27% |
| Luna Decisions | 81.58% | 85.94% | 61.75% | 93.71% |
| PPLX | 84.59% | 96.60% | 65.57% | 98.58% |
| GPT-6.1 | 96.99% | 99.32% | 95.08% | 99.53% |
| Clef | 82.52% | 90.82% | 58.47% | 93.92% |

The four views contain 532, 882, 366, and 1,908 rows respectively. Scores are exact-answer accuracy on hard-target rows. Jev 1.13 returned 360/366 and 1,804/1,908 answers on the two Pi views; unanswered requests are counted incorrect in the displayed accuracy. ECE and MCE use 15 equal-width bins and, for those two partial-response cells, are computed on answered rows only.

<!-- NOUL_METRICS_START -->
## Noul precision, recall, and F1

### Access-Control Reasoning

Positive answer: `yes`. Cells are `precision / recall / F1`.

| Model | Alternate paths | Time boundaries | Unknown sufficiency | Remediation vs access |
| --- | ---: | ---: | ---: | ---: |
| Mo 2.0 | 100.00% / 100.00% / 100.00% | 75.00% / 90.00% / 81.82% | 100.00% / 100.00% / 100.00% | 100.00% / 100.00% / 100.00% |
| Mo 1.3.1 | 100.00% / 100.00% / 100.00% | 75.00% / 60.00% / 66.67% | 100.00% / 100.00% / 100.00% | 100.00% / 100.00% / 100.00% |
| Jev 1.13 | 0.00% / 0.00% / 0.00% | 100.00% / 50.00% / 66.67% | 100.00% / 100.00% / 100.00% | 0.00% / 0.00% / 0.00% |
| Jev 1.14 | 0.00% / 0.00% / 0.00% | 71.43% / 50.00% / 58.82% | 100.00% / 100.00% / 100.00% | 0.00% / 0.00% / 0.00% |
| Luna Decisions | 100.00% / 20.00% / 33.33% | 0.00% / 0.00% / 0.00% | 90.00% / 90.00% / 90.00% | 0.00% / 0.00% / 0.00% |
| PPLX | 100.00% / 100.00% / 100.00% | 100.00% / 50.00% / 66.67% | 100.00% / 100.00% / 100.00% | 100.00% / 100.00% / 100.00% |
| GPT-6.1 | 100.00% / 100.00% / 100.00% | 100.00% / 100.00% / 100.00% | 100.00% / 100.00% / 100.00% | 100.00% / 100.00% / 100.00% |
| Clef | 100.00% / 100.00% / 100.00% | 100.00% / 40.00% / 57.14% | 100.00% / 20.00% / 33.33% | 100.00% / 40.00% / 57.14% |

### User Intent Guardrails

Positive answer: `no` (not aligned). Cells are `precision / recall / F1`.

| Model | OpenHands balanced | OpenHands prevalence | Pi balanced | Pi prevalence |
| --- | ---: | ---: | ---: | ---: |
| Mo 2.0 | 95.41% / 78.20% / 85.95% | 44.68% / 71.19% / 54.90% | 94.74% / 39.34% / 55.60% | 8.96% / 37.50% / 14.46% |
| Mo 1.3.1 | 95.09% / 80.08% / 86.94% | 72.88% / 72.88% / 72.88% | 91.67% / 54.10% / 68.04% | 12.77% / 37.50% / 19.05% |
| Jev 1.13 | 91.22% / 70.30% / 79.41% | 49.37% / 66.10% / 56.52% | 72.13% / 24.18% / 36.21% | 5.88% / 12.50% / 8.00% |
| Jev 1.14 | 90.78% / 74.06% / 81.57% | 52.56% / 69.49% / 59.85% | 70.00% / 26.78% / 38.74% | 7.14% / 18.75% / 10.34% |
| Luna Decisions | 80.22% / 83.83% / 81.99% | 29.03% / 76.27% / 42.06% | 74.16% / 36.07% / 48.53% | 3.57% / 25.00% / 6.25% |
| PPLX | 97.92% / 70.68% / 82.10% | 83.72% / 61.02% / 70.59% | 96.72% / 32.24% / 48.36% | 23.81% / 31.25% / 27.03% |
| GPT-6.1 | 97.35% / 96.62% / 96.98% | 94.92% / 94.92% / 94.92% | 95.58% / 94.54% / 95.05% | 66.67% / 87.50% / 75.68% |
| Clef | 87.12% / 76.32% / 81.36% | 39.62% / 71.19% / 50.91% | 71.83% / 27.87% / 40.16% | 3.70% / 25.00% / 6.45% |

Precision, recall, and F1 are computed on answered Noul rows. Unanswered requests are not mapped to either answer and remain incorrect in full-denominator accuracy. Structured values are in [`data/noul-metrics.json`](../../data/noul-metrics.json).
<!-- NOUL_METRICS_END -->
