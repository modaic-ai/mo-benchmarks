# JevBench

JevBench evaluates Choice, Noul, and Score decisions across easy, standard,
and hard tiers. Results use all 231 rows from the pinned public revision
[`c6004e008ffba24aec091261ca1a5c02f7324702`](https://github.com/MindWareAI/jev-bench/tree/c6004e008ffba24aec091261ca1a5c02f7324702).

## Task shape

Each row contains a complete state and one typed question: a categorical
Choice, a binary Noul decision, or an ordered Score rubric. For example:

```json
{"state":{"scenario":"…"},"questions":{"decision":{"type":"choice","criteria":{"A":"…","B":"…"}}}}
```

See [RESULTS.md](RESULTS.md) for the nine-model result matrix, including
precision, recall, and F1 on the 74-row Noul subset.

No example was truncated or skipped. ECE and MCE use 15 equal-width bins.
