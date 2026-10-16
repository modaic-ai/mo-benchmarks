# Auxiliary metrics audit

This audit covers every benchmark family currently documented in this repository. Accuracy remains the common headline metric. Precision, recall, and F1 are required only for Noul decisions, whose answer space is consistently `yes`/`no` across rows.

## Metric contract

All decision benchmarks should retain row count, answered coverage, exact-answer accuracy, correctness AUROC, 15-bin equal-width ECE/MCE, multiclass Brier, categorical NLL, and tie count where probability outputs are available.

Additional metrics depend on task shape:

| Task shape | Required auxiliary metrics |
| --- | --- |
| Noul (`yes`/`no`) | Precision, recall, and F1 for the named positive answer. |
| Choice | Accuracy and calibration. Do not add class metrics merely because a particular dataset has two choices. |
| Score | Accuracy and calibration unless the benchmark's official contract specifies an ordinal metric. |
| Retrieval/ranking | Preserve the official ranking metric, such as nDCG@10. |

Provider failures or unanswered requests remain incorrect in full-denominator accuracy. Classification metrics must additionally report answered coverage; they must not silently map an unanswered request to a semantic class.

## Open benchmarks

| Benchmark | Shape | Current gap | Required addition |
| --- | --- | --- | --- |
| ARC Challenge | Choice | None | Accuracy/calibration is sufficient |
| Argument Quality Ranking | Choice | None | Accuracy/calibration is sufficient |
| CodeJudgeBench | Choice | None | Accuracy/calibration is sufficient |
| GPQA Diamond | Choice | None | Accuracy/calibration is sufficient |
| HaluEval Summarization | Noul | None | Precision, recall, and F1 are reported with `yes` as the positive answer |
| JudgeBench | Choice | None | Accuracy/calibration is sufficient |
| MMLU-Pro | Choice | None | Accuracy/calibration is sufficient |
| MT-Bench Human Judgments | Choice | None | Accuracy/calibration is sufficient |
| MuSR Murder Mysteries | Choice | None | Accuracy/calibration is sufficient |
| MuSR Object Placements | Choice | None | Accuracy/calibration is sufficient |
| MuSR Team Allocation | Choice | None | Accuracy/calibration is sufficient |
| OR-Bench Toxic | Ten-class choice | None | Accuracy/calibration is sufficient |
| ROD101 Essay Scoring | Score | None | Accuracy/calibration is sufficient |

OR-Bench Toxic is not binary in the published cohort. Every row has ten answer options, so accuracy remains its task score.

## Finance benchmarks

All 12 Finance benchmarks use the Choice primitive. Accuracy and calibration are sufficient; none require a precision/recall/F1 backfill under the Noul-only rule.

| Benchmark | Options | Required addition |
| --- | ---: | --- |
| Banking77 Intent Routing | 77 | None |
| CFPB Complaint Routing | 10 | None |
| ESG Classification | 33 | None |
| FinCalc NLI | 3 | None |
| FOMC Stance | 3 | None |
| German Credit | 2 | None |
| Gold Headlines | 2 | None |
| ModernFinBERT Sentiment | 3 | None |
| MultiFin | 6 | None |
| NumClaim | 2 | None |
| SentiVent Event | 2 | None |
| Twitter Financial News Topic | 20 | None |

The separate Finance Uplift pilot does not require a class-metric backfill under this rule.

## Security benchmarks

| Benchmark | Shape | Current gap | Required addition |
| --- | --- | --- | --- |
| Policy-Conditioned Access Review | Choice, test and validation | None | Accuracy/calibration is sufficient |
| Compositional Access Continuation | Choice, test and validation | None | Accuracy/calibration is sufficient |
| Access-Control Reasoning | Four Noul views, one Choice view, one Score view | None | Precision, recall, and F1 are reported for each Noul view |
| User Intent Guardrails | Noul across four reporting views | None | Precision, recall, and F1 are reported per view with `no` as the positive answer |

For Jev 1.13 on User Intent Guardrails, full-denominator accuracy includes unanswered requests as incorrect. Precision/recall/F1 must expose answered coverage and treat unanswered requests as abstentions rather than inventing a class prediction.

## Other benchmark families

| Family | Audit result |
| --- | --- |
| Buying Signals | Noul and complete: precision/recall/F1 are already present for all nine models. |
| JevBench | Mixed primitive: 74 Noul, 139 Choice, and 18 Score rows. Precision/recall/F1 are reported for the Noul subset; accuracy by difficulty and calibration remain the full-benchmark metrics. |
| Decision Index | Uses each task's official metric: 11 F1-based tasks, two nDCG@10 tasks, three case-exact tasks, and 21 accuracy tasks. Preserve those official headlines. Add the common calibration suite only where matched probability artifacts are available for all nine models. |
| Finance Uplift | Choice-based; no class-metric backfill required. |

The frozen Decision Index corpus uses the Choice primitive throughout, including tasks with two choices. It does not require a Noul precision/recall/F1 backfill.

## Noul count

Five benchmark families contain Noul decisions:

1. HaluEval Summarization: one Noul benchmark.
2. Access-Control Reasoning: four Noul views inside a mixed six-view family.
3. User Intent Guardrails: four Noul reporting views.
4. JevBench: 74 Noul rows inside a mixed 231-row benchmark.
5. Buying Signals: Noul, with the requested metrics already complete.

The backfill is complete for all ten previously missing slices: one HaluEval benchmark, four Access-Control Reasoning views, four User Intent Guardrails views, and one JevBench Noul subset. Across nine models, that is 90 result cells.

## Backfill status

- All ten missing Noul result slices were backfilled from retained nine-model predictions without rerunning inference.
- Buying Signals needs no backfill for precision, recall, or F1.
- Choice and Score benchmarks keep accuracy and their existing calibration or official metrics.
- Public aggregate files contain metrics only and do not expose private Security rows or prompts.

Structured results are in [`data/noul-metrics.json`](../data/noul-metrics.json) and are also embedded under `noul_results` in [`data/benchmark-results.json`](../data/benchmark-results.json).

No Noul precision/recall/F1 backfill remains outstanding.
