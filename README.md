# Modaic Benchmarks

Decision-model evaluations and aggregate results at [bench.modaic.dev](https://bench.modaic.dev/).

## Benchmarks

| Benchmark | Question | Result | Reproduce |
| --- | --- | --- | --- |
| Decision Index | How broad is model skill across knowledge, language, retrieval, tools, and arts? | [results](benchmarks/decision_index/RESULTS.md) | [Protocol](benchmarks/decision_index/README.md) |
| JevBench | How accurately does a model handle Choice, Noul, and Score decisions across three difficulty tiers? | [results](benchmarks/jev_bench/RESULTS.md) | [Protocol](benchmarks/jev_bench/README.md) |
| Security | Can a model make access recommendation and continuation decisions? | [results](benchmarks/security/RESULTS.md) | [Protocol](benchmarks/security/README.md) |
| Open benchmark suite | How well does a model transfer across 13 named public benchmarks? | [live comparison](https://bench.modaic.dev) | [Datasets](data/README.md) |
| Finance | How do nine models compare across 12 finance tasks? | [live comparison](https://bench.modaic.dev) | [Tasks and results](benchmarks/finance/README.md) |
| Finance alignment uplift | What changes after task-specific alignment on up to 200 labeled examples? | [live results](https://bench.modaic.dev/finance-uplift) · [results](benchmarks/finance/finance_uplift/RESULTS.md) | [Protocol and runner](benchmarks/finance/finance_uplift/README.md) |
| Buying-signal detection | Can a model identify a specified buying signal in a sales-call excerpt? | [Live comparison](https://bench.modaic.dev) · [results](benchmarks/gtm/buying_signals/RESULTS.md) | [Protocol and runner](benchmarks/gtm/buying_signals/README.md) |

## Reproduce the buying-signal benchmark

The complete runner is in this repository. It downloads the **test split only** at a pinned [Gong Call Playbook](https://huggingface.co/datasets/gong-io-research/call-playbook) revision, checks the prepared cohort against the published one, runs the seven configured models, scores their predictions, and regenerates `data/buying-signals.json`.

Install [uv](https://docs.astral.sh/uv/) and Node.js, set `MODAIC_API_KEY` and `OPENROUTER_API_KEY` in your environment or a root `.env`, then run:

```bash
cd benchmarks/gtm/buying_signals
./reproduce.sh --external-data-authorized
```

This makes 7,000 model decisions and may incur API charges. The runner resumes partial outputs, so rerunning the command continues incomplete models. GPT-6.1 Sol uses medium reasoning and eight workers; the other models use one worker. Predictions, labels, and call excerpts stay under ignored `benchmarks/gtm/buying_signals/data/` and `outputs/`. See the [benchmark protocol](benchmarks/gtm/buying_signals/README.md) for a dry run, a small pilot, model IDs, metrics, and limitations.

## Run the website

```bash
npm ci
npm run dev
```

The site reads the committed aggregate file in `data/`. To regenerate it from seven complete local reports without rerunning models:

```bash
node scripts/import-buying-signals.mjs
```

The importer rejects incomplete or mismatched test cohorts and publishes only aggregate metrics.

For the finance uplift benchmark, complete the phases in its [protocol](benchmarks/finance/finance_uplift/README.md), then regenerate the public aggregate file with:

```bash
node scripts/import-finance-uplift.mjs
```

## Adding a benchmark

Place its protocol, pinned dependencies, runner, and tests under `benchmarks/<slug>/`. Keep private inputs and row-level outputs in that benchmark's ignored `data/` and `outputs/` directories. Commit a separate aggregate artifact in the top-level `data/` directory, then add its page and a row to the index above.
