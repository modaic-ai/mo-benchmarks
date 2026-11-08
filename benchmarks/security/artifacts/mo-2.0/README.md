# Mo 2.0 newer Security aggregate

This directory contains publication-safe aggregate metrics from the complete frozen newer Security panel. Row-level prompts and predictions are not published.

- Model requested and served: `mo-2.0`
- Production endpoint: `https://api.modaic.dev`
- Decisions: 3,808 across 10 benchmark views
- Failures, refusals, skips, truncations, and ties: 0
- Panel SHA-256: `2f82fdb99eae0fb0edb3cbbe5cf46ff2285b0e02ae0e1559d233b380a0f14b60`
- `metrics.json` SHA-256: `356146cdf84a1d86c2a18274a029b897edb77aeeafe992378b2cea687af6ffc1`
- Accuracy: 91.2553% micro; 89.4253% macro across benchmark views
- Calibration: correctness AUROC 0.852107; equal-width 15-bin ECE 0.019883; MCE 0.130763; multiclass Brier 0.136969; categorical NLL 0.231436

The metrics file includes exact per-view counts and the same accuracy and calibration measures.
