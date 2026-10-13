# Finance alignment uplift results

Each run used base `modaic/mo`, at most 200 captured and labeled training
examples, and a fixed 200-row held-out cohort. Seven alignments produced new
checkpoints. Their post-alignment scores were measured after the automatic
batch over captured examples finished with zero failures. FinCalc alignment
completed without a new checkpoint, so no post-alignment score is claimed.

| Task | Base Mo | Labels only | With ground reasoning | Final change | Paired 95% interval |
| --- | ---: | ---: | ---: | ---: | ---: |
| [Banking77 intents](https://huggingface.co/datasets/DeepPavlov/banking77) | 87.0% | 85.0% | 83.5% | −3.5 pp | −7.0 to −0.5 pp |
| [CFPB complaint routing](https://huggingface.co/datasets/Johnade/consumer_complaints_cfpb) | 45.0% | 45.5% | — | +0.5 pp | −6.0 to +7.0 pp |
| [ESG issue classification](https://huggingface.co/datasets/ChanceFocus/flare-mlesg) | 38.5% | 38.5% | — | 0.0 pp | −4.0 to +3.5 pp |
| [FinCalc entailment](https://huggingface.co/datasets/anespo28/fincalc-nli) | 92.0% | No checkpoint | — | — | — |
| [FOMC stance](https://huggingface.co/datasets/gtfintechlab/fomc_communication) | 53.0% | 67.0% | — | +14.0 pp | +7.0 to +21.5 pp |
| [German credit risk](https://huggingface.co/datasets/ChanceFocus/flare-german) | 52.5% | 57.0% | — | +4.5 pp | −4.5 to +13.5 pp |
| [Gold-price headlines](https://huggingface.co/datasets/ChanceFocus/flare-headlines) | 87.5% | 90.0% | — | +2.5 pp | −0.5 to +6.0 pp |
| [MultiFin topics](https://huggingface.co/datasets/awinml/MultiFin) | 68.0% | 78.0% | — | +10.0 pp | +4.5 to +15.5 pp |

The intervals are paired bootstrap intervals over each task's fixed 200 test
rows. FOMC corrected 43 previously wrong rows and regressed on 15; MultiFin
corrected 28 and regressed on 8. German credit corrected 46 and regressed on
37, yielding a useful +4.5-point gain with a wider interval. Gold corrected
8 and regressed on 3. ESG corrected and regressed on 7 each. CFPB corrected
23 and regressed on 22. These are task-specific results from one alignment
run per task, not a guarantee of uplift on every dataset.

## Cohort integrity

- Each training cohort came from data outside the published test split, except
  MultiFin, whose evaluation split is its published validation split. Exact
  train/evaluation input overlaps were removed before selecting training rows.
- ESG uses the [original FinNLP English training release](https://github.com/sagacemente/FinNLP_2023/blob/3009e332a34e639cdd78e2f98b5bd9cb6e99d0dc/FinESG-2023_Train_EN.json),
  whose 33 labels match the Flare test set. One test article with five-token
  Jaccard similarity of at least 0.6 to a selected training article was
  excluded before either checkpoint was scored. The training file is pinned
  by commit and SHA-256 checksum.
- The gold-headline release repeats each headline under nine distinct binary
  questions. Preparation selects only “Price or Not”; it removes exact
  cross-split overlaps and inputs with conflicting labels. The earlier
  direct-inference comparison mixed those nine questions, so its gold score
  is not directly comparable to this corrected cohort.
- The CFPB source repeats many narratives across published train and test
  CSVs. Preparation removed 11,780 training rows whose normalized text
  matched the full test split. It also deduplicated the test split and,
  before aligned scoring, excluded 136 near-copy test rows with five-token
  Jaccard similarity of at least 0.8 to selected training complaints. The
  final 200-row test cohort is balanced across 10 issues and has no near-copy
  pairs within it at that threshold.
- Banking77 reasoning was added to 167 of the same 200 captured annotations;
  33 labels lacked enough evidence in their utterance for a defensible
  explanation. These rationales were curated from the training text and
  intent taxonomy, not supplied by the source dataset. Its label-only
  checkpoint was 85.0%; the reasoning checkpoint was 83.5% on exactly the
  same held-out rows.

The source revisions, cohort selection, capture/annotation flow, and commands
to reproduce the runs are in the [protocol](README.md). Row-level source text
and model decisions are intentionally omitted from the repository.
