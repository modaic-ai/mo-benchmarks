# Access-Control Reasoning

## Task

Resolve difficult access-control decisions that require exact reasoning across authorization paths, time, incomplete evidence, remediation state, policy disposition, and interacting risks.

## Task shape

`access state, proposed change or review action, policy facts, and one typed question → the policy-consistent answer`

```json
{"benchmark":"access_control_reasoning","view":"alternate_authorization_paths","decision":{"state":{"…":"…"},"questions":{"…":{"type":"noul","instructions":"…"}}},"target":{"kind":"hard","answer":"yes"}}
```

The 120-row calibration set has six equally sized views:

- Alternate authorization paths
- Temporal and timezone boundaries
- Sufficiency under unknown completions
- Remediation status versus effective access
- Four-way policy disposition
- Compositional risk

This is a calibration and development benchmark, not an independent final test set.

Three representative Security rows are visible in [`../examples.jsonl`](../examples.jsonl). The complete dataset is private: [`modaic/security-decision-benchmarks`](https://huggingface.co/datasets/modaic/security-decision-benchmarks/tree/33e882d646f5a98f21eb53ec8c02299f6df21333).

## Results

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

### View breakdown

| View | Mo 1.3.1 | Mo 1.3.2 | Jev 1.13 | Jev 1.14 | Luna Decisions | PPLX | GPT-6.1 | Mo Fast | Clef |
| --- | ---: | ---: | ---: | ---: | ---: | ---: | ---: | ---: | ---: |
| Alternate authorization paths | 100.00% | 100.00% | 50.00% | 50.00% | 60.00% | 100.00% | 100.00% | 80.00% | 100.00% |
| Temporal and timezone boundaries | 70.00% | 75.00% | 75.00% | 65.00% | 50.00% | 75.00% | 100.00% | 75.00% | 70.00% |
| Sufficiency under unknown completions | 100.00% | 100.00% | 100.00% | 100.00% | 90.00% | 100.00% | 100.00% | 50.00% | 60.00% |
| Remediation status versus effective access | 100.00% | 100.00% | 50.00% | 50.00% | 50.00% | 100.00% | 100.00% | 100.00% | 70.00% |
| Four-way policy disposition | 85.00% | 90.00% | 80.00% | 85.00% | 90.00% | 85.00% | 100.00% | 80.00% | 60.00% |
| Compositional risk | 90.00% | 100.00% | 65.00% | 75.00% | 75.00% | 95.00% | 100.00% | 35.00% | 65.00% |

Scores are exact-answer accuracy on hard-target rows.
