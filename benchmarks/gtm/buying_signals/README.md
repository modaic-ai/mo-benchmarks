# Buying-signal detection

This benchmark asks for `p(signal present)` in a speaker-tagged sales-call excerpt. It uses five **separate binary tasks** from [Gong Call Playbook](https://huggingface.co/datasets/gong-io-research/call-playbook): business goals, decision criteria, decision makers, decision-making process, and pain points. Each task contributes 200 rows from its `test.csv`, for 1,000 decisions per model. A label for one task is never reused for another task.

The dataset revision is pinned to `d83dd6557965c261c2de9fbf0fa04589aad528fd`; the published cohort SHA-256 is `ba8100e7949a151b5913ceec8b63797fdd80fe2d7971a0aec0da4439ccf0f19d`. `prepare.py` writes label-free model inputs, separate labels, and a hashed manifest. `run_models.py` reads inputs only. `reproduce.sh` checks the manifest against the published cohort before making model calls.

## Access and setup

Gong publishes this data under its [Confidential Dataset License](https://huggingface.co/datasets/gong-io-research/call-playbook/blob/main/LICENSE). Obtain written consent covering your use and transmissions to Modaic and OpenRouter before downloading or running the evaluation. The script requires `--external-data-authorized` as an explicit confirmation. Keep `data/` and `outputs/` private; both are ignored by Git and are never needed to build the public site.

Use Python 3.13+, [uv](https://docs.astral.sh/uv/), and Node.js. The `uv.lock` file pins the Python environment. Set `MODAIC_API_KEY` and `OPENROUTER_API_KEY` as environment variables or in the repository root `.env` (ignored by Git). Then, from this directory:

```bash
./reproduce.sh --external-data-authorized
```

This runs `mo-fast` and `mo` on Modaic, then Jev, Luna, Perplexity, and Clef on OpenRouter's decisions endpoint, and finally GPT-6.1 Sol on OpenRouter's strict-JSON chat endpoint with `reasoning.effort: "medium"`. It generates complete reports and refreshes the site's aggregate file. Calls run sequentially by model. GPT-6.1 Sol uses eight workers; all other models use one. This is the concurrency used for the published latency results.

For a small pilot or to inspect the cohort before the full run:

```bash
uv sync --locked
uv run --locked python prepare.py
uv run --locked python run_models.py --plan
uv run --locked python run_models.py --models mo-fast --limit 5 --external-data-authorized
uv run --locked python -m unittest test_benchmark.py
```

`--limit` adds that many new predictions per selected model, spread round-robin across tasks. Repeating a run resumes its existing output. Model IDs are specified in `run_models.py` and may be changed with `--override NAME=MODEL_ID`; use a fresh output directory when changing a model ID or worker count. Hosted model behavior and availability can change, so new runs need not reproduce the published numbers exactly.

## Scoring and artifacts

The website's headline is **macro accuracy**: the unweighted mean of five per-task accuracy scores. The fixed positive threshold is `p_signal >= 0.5`, with no test-set tuning. Reports also include macro F1, precision, recall, AUROC, and ten-bin expected calibration error (ECE; lower is better), plus per-task and pooled scores. `report.py` scores only a complete, matching test cohort. Latency p50/p95/p99 measures each successful HTTP attempt and excludes retries and backoff; the eight-worker GPT latency was measured under concurrent load.

`outputs/` contains private row-level probabilities and run provenance. The reports and predictions do not contain excerpts. `scripts/import-buying-signals.mjs` validates complete reports, merges them into the nine-model aggregate, and writes `data/buying-signals.json` at the repository root. Only that aggregate JSON and [RESULTS.md](RESULTS.md) are committed. To score existing predictions or regenerate just the aggregates:

```bash
uv run --locked python report.py --predictions outputs/mo-test.jsonl --output outputs/mo-test-report.json
uv run --locked python compare.py --output-dir outputs --output outputs/leaderboard.md
cd ../../..
node scripts/import-buying-signals.mjs
```
