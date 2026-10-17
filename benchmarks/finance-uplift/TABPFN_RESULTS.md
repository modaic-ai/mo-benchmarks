# TabPFN on German credit

TabPFN-2 and TabPFN-3.5 were evaluated on the same fixed 200-row held-out German credit cohort
used in the finance uplift comparison. The 20 customer fields were passed as
tabular features: seven numeric fields and 13 categorical fields encoded using
training rows only. The published `ChanceFocus/flare-german` source revision and
cohort checksum are pinned in `data/german-credit.json`. Train and test feature
records have no exact overlap.

| Model | Training data | Train rows | Accuracy | Balanced accuracy | Recall: bad risk |
| --- | --- | ---: | ---: | ---: | ---: |
| TabPFN-2 | Same selected rows used for Mo alignment | 200 (100 good, 100 bad) | 65.0% (130/200) | 64.9% | 64.7% (44/68) |
| TabPFN-3.5 | Same selected rows used for Mo alignment | 200 (100 good, 100 bad) | 70.0% (140/200) | 67.6% | 60.3% (41/68) |
| TabPFN-2 | Balanced published training rows | 412 (206 good, 206 bad) | 69.0% (138/200) | 69.4% | 70.6% (48/68) |
| TabPFN-3.5 | Balanced published training rows | 412 (206 good, 206 bad) | 72.0% (144/200) | 71.7% | 70.6% (48/68) |
| TabPFN-2 | Complete published training split | 700 (494 good, 206 bad) | 72.0% (144/200) | 62.7% | 33.8% (23/68) |
| TabPFN-3.5 | Complete published training split | 700 (494 good, 206 bad) | 71.0% (142/200) | 62.3% | 35.3% (24/68) |

The held-out cohort has 132 good and 68 bad cases. Predicting `good` for every
case would score 66.0% accuracy, but 0% recall on bad risks. The full-training
run for both versions misses more bad risks than the 200-row run. These are
single local CPU runs using `tabpfn==9.2.0`, not estimates for every credit
dataset. The 3.5 weights required the user's own acceptance of Prior Labs'
[noncommercial license](https://huggingface.co/Prior-Labs/tabpfn_3_5/blob/main/LICENSE).
The 3.5 results here are for research use, not the Mo marketing chart.

The 412-row set keeps all 206 published bad-risk training rows and selects 206
good-risk rows without replacement. It includes the original 200 selected
examples; the additional good rows are selected using the cohort seed. The
ordered source-index SHA-256 is
`0336c9254f50d02e59b5f476a4e0a897b310e462d6ac1ff1ace752b9dad57c7c`.

To reproduce:

```bash
python -m pip install 'tabpfn==9.2.0' 'pyarrow==26.0.0'
python benchmarks/finance-uplift/compare_tabpfn.py
python benchmarks/finance-uplift/compare_tabpfn.py --balanced-full-train
python benchmarks/finance-uplift/compare_tabpfn.py --full-train
python benchmarks/finance-uplift/compare_tabpfn.py --model-version v3.5
python benchmarks/finance-uplift/compare_tabpfn.py --model-version v3.5 --balanced-full-train
python benchmarks/finance-uplift/compare_tabpfn.py --model-version v3.5 --full-train
```

The 3.5 commands use Prior Labs' official login and license flow on first run.
