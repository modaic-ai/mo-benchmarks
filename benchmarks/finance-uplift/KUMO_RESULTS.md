# Local Kumo Tabular on German credit

NVIDIA Kumo Tabular Large v1.0.1 was run locally on CPU using the public
`nvidia/Kumo-Tabular` weights and the `structured-data-models` library at commit
`837fc07b826742b1a1def716e60d6507ae7626e4`. No inference API was used.
The model received the original 20 customer fields as seven numeric and 13
categorical columns. The same fixed 200-row held-out cohort was used in both
runs, with 16 estimators per NVIDIA's large-model benchmark configuration.

| Context labels | Train rows | Accuracy | Balanced accuracy | Recall: bad risk |
| --- | ---: | ---: | ---: | ---: |
| Same selected rows used for Mo alignment | 200 (100 good, 100 bad) | 69.0% (138/200) | 65.8% | 55.9% (38/68) |
| Balanced published training rows | 412 (206 good, 206 bad) | 70.5% (141/200) | 71.6% | 75.0% (51/68) |
| Complete published training split | 700 (494 good, 206 bad) | 72.5% (145/200) | 64.5% | 39.7% (27/68) |

The test cohort has 132 good and 68 bad cases, so an all-good prediction would
score 66.0% accuracy and 0% bad-risk recall. Using the full, naturally
imbalanced training split raised Kumo's accuracy while reducing bad-risk
recall. The balanced 412-row set keeps every bad-risk training case and selects
206 good-risk cases without replacement using the cohort seed. It includes the
original 200 training examples. Its ordered source-index SHA-256 is
`0336c9254f50d02e59b5f476a4e0a897b310e462d6ac1ff1ace752b9dad57c7c`.
There is no exact train/test feature-record overlap.

For comparison on the same balanced 412 rows, TabPFN-2 scored 69.0% and
TabPFN-3.5 scored 72.0%. This is a single-run comparison on one small dataset,
not evidence of a general model ranking. The TabPFN-3.5 results are limited to
noncommercial research use under its model license.

To reproduce with local inference:

```bash
python -m pip install pandas pyarrow \
  'git+https://github.com/NVIDIA/structured-data-models.git@837fc07b826742b1a1def716e60d6507ae7626e4'
python benchmarks/finance-uplift/compare_kumo.py
python benchmarks/finance-uplift/compare_kumo.py --balanced-full-train
python benchmarks/finance-uplift/compare_kumo.py --full-train
```

The first run downloads the public Kumo model weights; subsequent predictions
run locally.
