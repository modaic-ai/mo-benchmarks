# Mo 2.0 production-API benchmark artifacts

[`metrics.json`](metrics.json) is the unchanged, publication-safe aggregate from
the completed Mo 2.0 hosted panel. All requests went through the production
`modaic.dev` API.

- 37,712/37,712 decisions scored with no refusals, skips, truncations, or ties.
- 29 benchmark views: 13 public-transfer, 12 Finance, and four legacy Security
  splits.
- Hard exact accuracy: 75.3357%; macro benchmark accuracy: 71.9199%.
- Correctness AUROC: 0.759591; equal-width 15-bin ECE/MCE:
  0.099959/0.142732; multiclass Brier: 0.369153; categorical NLL: 0.735675.
- SHA-256: `7831ab981882b1842b540c7292e4e1908df75c053f3d2f615ee7a7550456178a`.

The row-level prediction file is intentionally excluded under the repository's
publication policy. This aggregate retains the per-view counts and metrics used
by the website importer without publishing benchmark inputs or predictions.
