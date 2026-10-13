# Finance alignment uplift results

All three completed runs used base `modaic/mo`, at most 200 captured and
labeled training examples, and the same 200 held-out rows before and after
alignment. Scores below are accuracy on those held-out rows. Each reported
aligned checkpoint was scored after its automatic batch over captured
examples completed with zero failures.

| Task | Base Mo | Labels only | With ground reasoning | Final change | Paired 95% interval |
| --- | ---: | ---: | ---: | ---: | ---: |
| [CFPB complaint routing](https://huggingface.co/datasets/Johnade/consumer_complaints_cfpb) | 45.0% | 45.5% | — | +0.5 pp | −6.0 to +7.0 pp |
| [MultiFin topics](https://huggingface.co/datasets/awinml/MultiFin) | 68.0% | 78.0% | — | +10.0 pp | +4.5 to +15.5 pp |
| [Banking77 intents](https://huggingface.co/datasets/DeepPavlov/banking77) | 87.0% | 85.0% | 83.5% | −3.5 pp | −7.0 to −0.5 pp |

The intervals are paired bootstrap intervals over each task's fixed test rows,
not an estimate across tasks or model families. MultiFin corrected 28
previously wrong rows and regressed on 8. CFPB corrected 23 and regressed on
22. The Banking77 reasoning checkpoint corrected 2 and regressed on 9 relative
to base Mo. The evidence here supports a MultiFin uplift, but not a general
claim that 200-label alignment improves every financial task.

Banking77 reasoning was added to 167 of the same 200 captured annotations;
33 labels lacked enough evidence in their utterance for a defensible
explanation. These rationales were curated from the training text and intent
taxonomy, not supplied by the source dataset. Its label-only checkpoint was
85.0%, and the second checkpoint was 83.5% on exactly the same test rows.

The CFPB source repeats many narratives across published train and test CSVs.
Preparation removed 11,780 training rows whose normalized text matched the
full test split. It also deduplicated the test split and, before aligned
scoring, excluded 136 near-copy test rows with five-token Jaccard similarity
of at least 0.8 to any selected training complaint. The final 200-row test
cohort is balanced across its 10 issues and has no near-copy pairs within it
at that threshold. Base Mo scored 48.5% on an earlier exact-deduplicated
exploratory sample; the public 45.0% baseline and 45.5% final score both use
the stricter cohort.

We also screened [FinCalc-NLI](https://huggingface.co/datasets/anespo28/fincalc-nli)
on a separate 200-row test cohort. Base Mo scored 92.0%; a partial training
capture run was stopped before alignment to prioritize tasks with lower
starting accuracy. No aligned FinCalc score is reported.
The source revisions, cohort selection, capture/annotation flow, and commands
to reproduce the completed runs are in the [protocol](README.md). Row-level
source text and model decisions are intentionally omitted from the repository.
