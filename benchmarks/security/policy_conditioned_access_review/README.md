# Policy-Conditioned Access Review

## Task

Decide whether existing access should be approved or revoked under the supplied organizational review policy.

## Task shape

`review item, assignment, governance history, profile changes, usage evidence, separation-of-duties status, and review policy → approve or revoke`

```json
{"benchmark":"policy_conditioned_access_review","split":"test","decision":{"state":{"…":"…"},"questions":{"…":{"type":"choice","criteria":{"…":"…"}}}},"target":{"kind":"hard","answer":"…"}}
```

The benchmark has held-out test and validation splits. It tests whether the decision follows the supplied policy while combining identity, entitlement, activity, and governance evidence.

Three representative Security rows are visible in [`../examples.jsonl`](../examples.jsonl). The complete dataset is private: [`modaic/security-decision-benchmarks`](https://huggingface.co/datasets/modaic/security-decision-benchmarks/tree/33e882d646f5a98f21eb53ec8c02299f6df21333).

## Results

| Model | Test · 2,201 | Validation · 2,437 |
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

Scores are exact-answer accuracy on hard-target rows.
