# Finance alignment uplift pilot

This pilot measures the change in held-out accuracy when a saved Modaic model
using `modaic/mo` is aligned on labeled examples. The featured tasks are
MultiFin topic routing, Banking77 intent routing, and CFPB complaint routing.
Each task gets its own saved model.

## Data boundary

`prepare.py` pins the source repositories to exact revisions and selects
fixed 200-row evaluation cohorts using seed `20261002`. MultiFin uses
`only_english_highlevel/validation`; Banking77 and CFPB use official `test` splits.
It selects at most 200 rows from each source's separate `train` split for
alignment. It removes training rows whose normalized text appears anywhere
in the full evaluation split, then removes duplicate training inputs. CFPB's
published CSVs repeat many complaint narratives across and within splits, so
its test cohort is deduplicated before sampling. The prepared
cohorts and row-level decisions are ignored by Git.

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
for task in multifin banking77-routing; do
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

FinCalc-NLI is available as an optional task, but was not aligned after base
Mo reached 92% on its fixed test cohort. The featured runs prioritize lower
starting accuracy.

The headline is `aligned accuracy - baseline accuracy` in percentage points,
computed on identical held-out rows. The report also records the counts of
individual rows corrected and regressed. These public datasets may have been
seen during foundation-model training, and the 200-row cohorts give limited
precision; the result measures this specific alignment run, not all finance
tasks or production performance.
