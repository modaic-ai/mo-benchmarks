# Modaic Benchmarks

A public results site for decision-model benchmarks, built with Next.js and the shadcn chart component. The first benchmark measures buying-signal detection on the five binary tasks in [Gong Call Playbook](https://huggingface.co/datasets/gong-io-research/call-playbook).

## Buying-signal benchmark

- **Cohort:** 200 test examples for each of five signals; 1,000 decisions per model.
- **Models:** seven fixed model IDs, including Modaic, Jev, Luna, Perplexity, Clef, and GPT.
- **Headline:** macro F1 at a fixed `p(signal) >= 0.5` threshold.
- **Other metrics:** macro precision, recall, accuracy, AUROC, 10-bin ECE, per-signal scores, and p50/p95/p99 request latency.
- **Dataset revision:** `d83dd6557965c261c2de9fbf0fa04589aad528fd`.

The site contains **aggregate metrics only**. It does not include licensed call excerpts, labels, or row-level predictions. The source dataset is governed by [Gong's license](https://huggingface.co/datasets/gong-io-research/call-playbook/blob/main/LICENSE); obtain the necessary permission before reproducing the evaluation.

GPT used a strict JSON chat response and eight concurrent workers. The other models used Noul decisions and one worker. Latency measures the successful HTTP attempt and excludes retries and backoff. The test set was not used for threshold tuning.

## Development

```bash
npm ci
npm run dev
```

The site reads the committed aggregate file at [`data/buying-signals.json`](data/buying-signals.json). If you have access to the complete private report files from the evaluation, update it with:

```bash
node scripts/import-buying-signals.mjs /path/to/buying-signals/outputs
npm run build
```

The import script rejects incomplete or mismatched test cohorts and emits only aggregate fields. `app/globals.css` is copied byte-for-byte from `mo-hit-list`, and the charts use the shadcn chart component with Recharts.
