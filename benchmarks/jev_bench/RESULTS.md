# JevBench results

| Model | Overall | Easy | Standard | Hard | AUROC | ECE | Brier | NLL |
| --- | ---: | ---: | ---: | ---: | ---: | ---: | ---: | ---: |
| Mo 1.3.1 | 90.04% | 100.00% | 100.00% | 79.28% | 0.9471 | 0.0369 | 0.1280 | 0.2382 |
| Mo 1.3.2 | 89.18% | 100.00% | 100.00% | 77.48% | 0.9551 | 0.0296 | 0.1332 | 0.2258 |
| Jev 1.13 | 86.58% | 100.00% | 98.61% | 72.97% | 0.9290 | 0.0388 | 0.1778 | 0.3063 |
| Jev 1.14 | 90.04% | 100.00% | 98.61% | 80.18% | 0.9404 | 0.0567 | 0.1379 | 0.2519 |
| Luna Decisions | 90.48% | 100.00% | 97.22% | 81.98% | 0.8303 | 0.0625 | 0.1503 | 9.1939 |
| PPLX | 88.74% | 100.00% | 100.00% | 76.58% | 0.9402 | 0.0555 | 0.1554 | 0.3047 |
| GPT-6.1 | 99.57% | 100.00% | 100.00% | 99.10% | 0.7891 | 0.0181 | 0.0171 | 0.0482 |
| Mo Fast | 89.18% | 100.00% | 97.22% | 79.28% | 0.8720 | 0.0467 | 0.1723 | 0.3122 |
| Clef | 88.31% | 100.00% | 98.61% | 76.58% | 0.9060 | 0.0308 | 0.1645 | 0.3084 |

Accuracy is exact-answer accuracy. AUROC scores whether the model's argmax is
correct using maximum conditional option probability. ECE uses 15 equal-width
bins. Brier and NLL are multiclass decision metrics.
