# Finance alignment uplift pilot

This pilot measures the change in held-out accuracy when a saved Modaic model
using `modaic/mo` is aligned on labeled examples. The tasks cover financial
news topics, numerical claims, financial sentiment, sentence-level economic
events, ESG issues, German credit risk, FOMC stance, MultiFin topics,
gold-price headlines, FinCalc entailment, Banking77 intents, and CFPB complaint routing.
Each task gets its own saved model.

## Data boundary

`prepare.py` pins the source repositories to exact revisions and selects
fixed 200-row evaluation cohorts using seed `20261002`. MultiFin and Twitter
Financial News Topic use their published validation splits; the other tasks
use published `test` splits. ESG uses the [original FinNLP English training release](https://github.com/sagacemente/FinNLP_2023/blob/3009e332a34e639cdd78e2f98b5bd9cb6e99d0dc/FinESG-2023_Train_EN.json)
with 33 labels that exactly match the [Flare ESG test set](https://huggingface.co/datasets/ChanceFocus/flare-mlesg).
It selects at most 200 rows from each source's separate `train` split for
alignment. It removes training rows whose normalized text appears anywhere
in the full evaluation split, then removes duplicate training inputs. CFPB's
published CSVs repeat many complaint narratives across and within splits, so
its test cohort is deduplicated before sampling. The prepared
cohorts and row-level decisions are ignored by Git.

For the new tasks, preparation removes any same-text rows with contradictory
labels and deduplicates evaluation inputs. The ESG evaluation also excludes any
test article with five-token Jaccard similarity of at least 0.6 to a selected
training article; one such article was found. All cohort selection happens
before baseline or aligned scoring.

For [Twitter Financial News Topic](https://huggingface.co/datasets/zeroshot/twitter-financial-news-topic),
preparation decodes HTML entities and removes tracking URLs. It drops
contradictory same-text labels and removes training posts matching any post in
the full validation split before sampling. The two 200-row cohorts contain
10 posts per topic across all 20 labels. Its source commit and both CSV
checksums are pinned in `tasks.py`; near copies of selected training posts
are excluded from evaluation at five-token Jaccard similarity of at least 0.8.

The additional pilots use the published test splits of
[NumClaim](https://huggingface.co/datasets/gtfintechlab/Numclaim),
[ModernFinBERT Training Data v2](https://huggingface.co/datasets/neoyipeng/modernfinbert-training-v2),
and [SENTiVENT](https://huggingface.co/datasets/GillesJacobs/sentivent).
NumClaim asks whether a sentence makes a forward-looking numerical claim; its
source labels were initially produced by weak supervision and partly checked
by people. The sentiment pilot excludes rows marked `llm_consensus` and reports
each source separately, because its remaining sources use different financial
text and label conventions. SENTiVENT uses the sentence-level config and asks
whether an expert annotated at least one economic event in the sentence. This
is a derived binary task, not the source dataset's full extraction task.
Preparation pins every file by revision and SHA-256 checksum, removes exact
train/test overlaps and conflicts, and excludes near-copy test sentences.

We inspected [Financial Statement Fraud Detection](https://huggingface.co/datasets/WaguyMZ/Financial_statements_fraud_dataset)
but did not run it: the ready-to-use CSV contains AAER identifiers, enforcement
descriptions, and fraud-specific fields that disclose the target. After removing
them, it retains mainly counts of extracted features rather than the filing
contents needed for a meaningful decision. Its roughly 5% fraud prevalence
also makes accuracy on a small sampled cohort a poor operational measure.

The saved model receives the same question schema and state as the original
finance benchmark. Baseline and final evaluation calls use `capture=False`.
Only the distinct training rows use `capture=True`. The response supplies the
new example ID; the runner immediately annotates that captured example with
the source label, while other training decisions continue. Modaic assigns the
annotated examples to its own train/test split. The public benchmark cohort
is never sent as an alignment example or annotation.

## Run

Install [uv](https://docs.astral.sh/uv/) and provide `MODAIC_API_KEY` in your
environment. Optionally set `MODAIC_WORKSPACE` (default: `modaic_labs`). From
this directory:

```bash
uv sync --locked
for task in twitter-financial-news-topic numclaim modernfinbert-sentiment sentivent-event esg german-credit fomc multifin gold-headlines fincalc-nli banking77-routing; do
  uv run --locked python prepare.py --task "$task"
  uv run --locked python run.py --task "$task" --phase baseline
  uv run --locked python run.py --task "$task" --phase train
  uv run --locked python run.py --task "$task" --phase align --max-metric-calls 200
  uv run --locked python run.py --task "$task" --phase final
done

uv run --locked python prepare.py --task cfpb-routing
uv run --locked python run.py --task cfpb-routing --phase baseline
uv run --locked python run.py --task cfpb-routing --phase train
uv run --locked python cfpb_clean.py --phase prepare
uv run --locked python cfpb_clean.py --phase baseline
uv run --locked python run.py --task cfpb-routing --phase align --max-metric-calls 200
uv run --locked python cfpb_clean.py --phase final
```

The phases resume completed rows and use stable idempotency keys. Each task
makes 200 held-out baseline decisions, 200 captured and labeled training
decisions, an alignment job capped at 200 metric calls, and 200 held-out final
decisions if alignment produces a new checkpoint. An improving alignment
also triggers Modaic's batch run over the captured examples. The `align`
phase waits for that batch to complete before `final` can score uplift.

CFPB receives a second, preselected test cohort through `cfpb_clean.py`. The
published source has 19,679 test records but only 17,200 distinct narratives;
11,780 of its 78,071 training rows exactly match text somewhere in the full
test split. Preparation excludes those training rows. The clean cohort also
removes test rows whose five-token Jaccard similarity to any selected training
row is at least 0.8, then selects 20 distinct rows per issue while excluding
near copies within the selected test cohort. The initial `run.py` CFPB
baseline creates the saved model and is exploratory. `cfpb_clean.py` baseline
and final are the public comparison; both use the same selected 200 rows.

### Banking77 reasoning follow-up

The first Banking77 alignment uses only the source labels. To measure whether
ground reasoning helps, run a second alignment on the **same 200 captured
examples** after the first final evaluation:

```bash
uv run --locked python reasoning.py --phase preview > outputs/banking77-routing.reasoning-preview.jsonl
uv run --locked python reasoning.py --phase annotate
uv run --locked python reasoning.py --phase align --max-metric-calls 200
uv run --locked python reasoning.py --phase final
```

`reasoning.py` contains intent-specific routing rules and includes the exact
customer wording in each rationale. These rationales are curated from the
training utterances and the Banking77 label taxonomy; the dataset does not
provide human-written rationales. Rows whose label is ambiguous or conflicts
with the utterance are listed in `AMBIGUOUS_ROWS` and receive no fabricated
reasoning. This run adds reasoning to 167 of the same 200 annotations and does
not add any labels or captured examples. Its report preserves the label-only
accuracy as an intermediate checkpoint, so base Mo, label-only alignment, and
reasoning alignment can all be compared on the identical held-out 200 rows.

Base Mo reached 87.5% on gold-price headlines and 92.0% on FinCalc-NLI. Their
alignment runs followed the lower-accuracy tasks. The headline release
contains nine yes/no questions for every text; `prepare.py` selects only
its “Price or Not” question before scoring gold-price detection.

The headline is `aligned accuracy - baseline accuracy` in percentage points,
computed on identical held-out rows. The report also records the counts of
individual rows corrected and regressed. These public datasets may have been
seen during foundation-model training, and the 200-row cohorts give limited
precision; the result measures this specific alignment run, not all finance
tasks or production performance.
