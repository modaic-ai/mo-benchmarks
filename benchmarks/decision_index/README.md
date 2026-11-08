# Decision Index

This folder publishes model scores and the complete per-benchmark breakdown.
It does not copy the benchmark data.

Source: [Decision Index](https://huggingface.co/spaces/multimodalart/jev-decision-index)

The machine-readable breakdown is in [`results.json`](results.json).
The unchanged Mo 2.0 reducer outputs and checksums are in
[`artifacts/mo-2.0/`](artifacts/mo-2.0/README.md).

Mo 2.0 was scored on all 140,178 public-suite cases. Decision Index 0.4.1
reuses this official 0.3 public suite; its separate Full administration is not
publicly self-serve.

Each of the 37 task READMEs is filed under its domain folder in `benchmarks/`.
Those pages describe the task, task shape, official metric, and model
result matrix.
