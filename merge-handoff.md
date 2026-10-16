# Benchmark rename merge handoff

## Scope of this branch

This branch changes benchmark folders, documentation, private-dataset references, and result artifacts only. The website was intentionally left untouched because its implementation has diverged on the merge branch.

Base commit before this rename work: `79dcfe0` on `codex/benchmark-catalog-expansion`.

Local evaluation panel: 3,808 rows, SHA-256 `2f82fdb99eae0fb0edb3cbbe5cf46ff2285b0e02ae0e1559d233b380a0f14b60`. It contains 120 Access-Control Reasoning rows and 3,688 User Intent Guardrails rows.

## Security folder mapping

| Previous folder | New benchmark family | Split handling |
| --- | --- | --- |
| `security/access_recommendation_test` | `security/policy_conditioned_access_review` | `test` |
| `security/access_recommendation_validation` | `security/policy_conditioned_access_review` | `validation` |
| `security/access_continuation_test` | `security/compositional_access_continuation` | `test` |
| `security/access_continuation_validation` | `security/compositional_access_continuation` | `validation` |
| — | `security/access_control_reasoning` | six mechanism views |
| — | `security/user_intent_guardrails` | four source/distribution views |

The first two are benchmark families with test and validation splits, not four separate benchmark tasks.

## Website work intentionally deferred

Do not resolve this branch by restoring the old Security slugs. After merging into the current website branch:

1. Update Security navigation, routes, imports, labels, and table keys to the four family names above.
2. Map the old recommendation test/validation cells to the two splits of `policy_conditioned_access_review`.
3. Map the old continuation test/validation cells to the two splits of `compositional_access_continuation`.
4. Add the six-view Access-Control Reasoning breakdown and four-view User Intent Guardrails breakdown from the merged result artifact.
5. Regenerate any derived website aggregate from source results; do not hand-copy stale cells.
6. Preserve exactly three public Security examples total.

Files under `app/`, `components/`, and `data/benchmark-results.json` were deliberately not changed in this rename pass.

## Result status

- Policy-Conditioned Access Review: all nine models complete on test and validation.
- Compositional Access Continuation: all nine models complete on test and validation.
- Access-Control Reasoning: all nine models are complete, including all six view scores.
- User Intent Guardrails: all result cells are populated. Jev 1.13 returned 360/366 and 1,804/1,908 answers on the two Pi views; its unanswered requests are counted incorrect against the full denominators. Jev 1.14 completed every row.

The evaluation used the frozen panel without truncation or skipped rows. Eight models completed all 3,808 rows. Jev 1.13 produced 3,698 answers and 110 explicit failures across the 3,808 attempted rows; failures are scored incorrect for exact-answer accuracy, while its calibration metrics cover answered rows only.

## Data boundary

Complete Security datasets remain in the private Hugging Face dataset [`modaic/security-decision-benchmarks`](https://huggingface.co/datasets/modaic/security-decision-benchmarks/tree/33e882d646f5a98f21eb53ec8c02299f6df21333). GitHub must contain only the three representative rows already stored at `benchmarks/security/examples.jsonl`. Do not add full rows, private exports, source traces, or dataset-construction notes to the public repository.

The expanded four-family private staging tree validates locally at 10,264 rows. The private Hub repository was replaced and independently reloaded at immutable revision `33e882d646f5a98f21eb53ec8c02299f6df21333`; the obsolete archive file is absent.

User Intent Guardrails balanced and prevalence views overlap within each source. Keep them as separate evaluation views and do not pool them. Access-Control Reasoning is a calibration/development benchmark, not an independent final test set.

## Merge checks

- Confirm the four Security folders above are the only leaf Security benchmark folders.
- Confirm all nine model names appear in each result table.
- Confirm `benchmarks/security/examples.jsonl` has exactly three rows.
- Search changed public files for internal model aliases, source-system names, credentials, local paths, and private row content.
- Run the catalog validator and the website branch's own typecheck, lint, and production build after resolving drift.
