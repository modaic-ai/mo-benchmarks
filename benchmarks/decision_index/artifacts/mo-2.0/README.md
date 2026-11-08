# Mo 2.0 scoring artifacts

These are the unchanged, publication-safe outputs from the pinned official
Decision Index public-suite reducer for Mo 2.0. The evaluation completed all
140,178 cases and 312,320 independently dispatched fields through the
production `modaic.dev` API.

| File | SHA-256 | Purpose |
| --- | --- | --- |
| [`scores.json`](scores.json) | `4984e215d96e1f605edb135dfbafc1d948e4940902b12a8262ead85c17657a40` | Complete official reducer output |
| [`index.json`](index.json) | `c576517dbccf356445e61ad4f58e12a6ecc1cbca056c77ba39a9511387dfdafe` | Headline, domain, and per-benchmark index values |
| [`benchmark-summary.json`](benchmark-summary.json) | `89ee46c2a3b29a6618708886e6561f5e4554103f4f99adf716b0bdf14e062bc3` | Per-benchmark counts, metrics, and aggregate latency |
| [`exact-metrics.json`](exact-metrics.json) | `aa9cbc5682be5946b8f8261584d4800e3599574488aab6e9d96a8511b1d9712a` | Scalar exact accuracy and terminal-outcome counts |
| [`scoring-receipt.json`](scoring-receipt.json) | `86978b6cf1a597e97e17f0ec04ae4f03a6e0d2930902a8ff36c107d3d5312a32` | Suite verification, scorer commit, and result-wire identity |

The official result wire contained 140,178 rows and had SHA-256
`3d4e820726dcdd3ffecd5ab4fd1e968add9798fe00b597b493392c6325e1895e`.
It and the 312,320 raw API predictions are not published here: they are
row-level outputs, and this repository's publication policy keeps row-level
outputs and benchmark inputs out of Git. The receipt and aggregate artifacts
are sufficient to verify the published score without exposing those records.

The reducer used Decision Index kit commit
`62d2f51de34a2de64906345b6bc3e98e27ff55c7`. Decision Index 0.4.1 reuses this
official 0.3 public suite; the separate Full administration is private.
