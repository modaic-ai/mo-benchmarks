# Compositional Access Continuation

## Task

Decide whether an exact access grant or group membership should be retained or revoked at review time.

## Task shape

`identity, target, direct and indirect grants, memberships, events, conflicts, policy coverage, and review policy → retain or revoke`

```json
{"benchmark":"compositional_access_continuation","split":"test","decision":{"state":{"…":"…"},"questions":{"…":{"type":"choice","criteria":{"…":"…"}}}},"target":{"kind":"hard","answer":"…"}}
```

The benchmark has held-out test and validation splits. It tests interacting access rules, indirect grants, incident state, role changes, regrant authority, and separation-of-duties constraints.

Three representative Security rows are visible in [`../examples.jsonl`](../examples.jsonl). The complete dataset is private: [`modaic/security-decision-benchmarks`](https://huggingface.co/datasets/modaic/security-decision-benchmarks/tree/33e882d646f5a98f21eb53ec8c02299f6df21333).

## Results

| Model | Test · 382 | Validation · 964 |
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

Scores are exact-answer accuracy on hard-target rows.
