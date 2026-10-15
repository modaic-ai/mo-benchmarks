# Benchmark data

This directory contains complete decision rows for 13 public benchmarks:

- ARC Challenge
- Argument Quality Ranking
- CodeJudgeBench
- GPQA Diamond
- HaluEval Summarization
- JudgeBench
- MMLU-Pro
- MT-Bench Human Judgments
- MuSR Murder Mysteries
- MuSR Object Placements
- MuSR Team Allocation
- OR-Bench Toxic
- ROD101 Essay Scoring

`benchmark-datasets.json` records row counts and SHA-256 digests. Each gzip
JSONL row contains one complete state, exactly one typed question, and its
controller-side target.

Aggregate model results are in `benchmark-results.json`.
