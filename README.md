# Modaic Benchmarks

A collection of reproducible evaluations for decision models, with aggregate results at [bench.modaic.dev](https://bench.modaic.dev/). Each benchmark has its own dataset version, protocol, runner, scoring code, and results.

## Benchmarks

| Benchmark | Question | Result | Reproduce |
| --- | --- | --- | --- |
| Buying-signal detection | Can a model identify a specified buying signal in a sales-call excerpt? | [Live comparison](https://bench.modaic.dev) · [results](benchmarks/buying-signals/RESULTS.md) | [Protocol and runner](benchmarks/buying-signals/README.md) |
| Finance alignment uplift | How much does alignment change Mo's held-out accuracy on financial classification tasks? | [Live comparison](https://bench.modaic.dev/finance-uplift) · [results](benchmarks/finance-uplift/RESULTS.md) | [Protocol and runner](benchmarks/finance-uplift/README.md) |

## Reproduce the buying-signal benchmark

The complete runner is in this repository. It downloads the **test split only** at a pinned [Gong Call Playbook](https://huggingface.co/datasets/gong-io-research/call-playbook) revision, checks the prepared cohort against the published one, runs the seven configured models, scores their predictions, and regenerates `data/buying-signals.json`.

Install [uv](https://docs.astral.sh/uv/) and Node.js, set `MODAIC_API_KEY` and `OPENROUTER_API_KEY` in your environment or a root `.env`, then run:

```bash
cd benchmarks/buying-signals
./reproduce.sh --external-data-authorized
```

This makes 7,000 model decisions and may incur API charges. The runner resumes partial outputs, so rerunning the command continues incomplete models. GPT-6.1 Sol uses eight workers; the other models use one. Predictions, labels, and call excerpts stay under ignored `benchmarks/buying-signals/data/` and `outputs/`. See the [benchmark protocol](benchmarks/buying-signals/README.md) for a dry run, a small pilot, model IDs, metrics, and limitations.

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

For the finance uplift benchmark, complete the phases in its [protocol](benchmarks/finance-uplift/README.md), then regenerate the public aggregate file with:

```bash
node scripts/import-finance-uplift.mjs
```

## Adding a benchmark

Place its protocol, pinned dependencies, runner, and tests under `benchmarks/<slug>/`. Keep private inputs and row-level outputs in that benchmark's ignored `data/` and `outputs/` directories. Commit a separate aggregate artifact in the top-level `data/` directory, then add its page and a row to the index above.
