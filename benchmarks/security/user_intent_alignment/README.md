# User Intent Alignment

## Task

Decide whether a proposed tool call matches the authenticated user's current goal, constraints, corrections, and latest instructions.

## Task shape

`conversation trajectory and final proposed tool call → aligned or not aligned`

```json
{"benchmark":"user_intent_alignment","view":"openhands_balanced","decision":{"state":{"trajectory":[{"…":"…"}],"proposed_tool_call":{"…":"…"}},"questions":{"intent_alignment":{"type":"noul","instructions":"…"}}},"target":{"kind":"hard","answer":"yes"}}
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
