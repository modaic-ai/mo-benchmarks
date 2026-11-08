# Decision Index results

| Model | Balanced skill | Balanced raw | Breadth skill | Public skill |
| --- | ---: | ---: | ---: | ---: |
| Mo 2.0 | 70.95 | 77.97 | 70.30 | — |
| Mo 1.3.1 | 63.40 | 72.36 | 62.62 | — |
| Mo 1.3.2 | 66.26 | 74.01 | 64.79 | 65.45 |
| Jev 1.13 | 60.11 | 68.55 | 57.27 | 57.96 |
| Jev 1.14 | 60.85 | 70.08 | 60.21 | — |
| Luna Decisions | 47.16 | 59.27 | 45.80 | — |
| PPLX | 62.75 | 71.66 | 61.52 | 62.25 |
| GPT-6.1 | 72.50 | 79.50 | 72.22 | — |
| Mo Fast | 50.74 | 59.21 | 50.51 | — |
| Clef | 53.08 | 71.07 | 61.04 | 61.71 |

## Mo 2.0 domain breakdown

| Domain | Skill | Raw |
| --- | ---: | ---: |
| Knowledge | 58.21 | 66.14 |
| Language | 74.26 | 82.10 |
| Retrieval | 74.35 | 79.93 |
| Tools | 86.80 | 88.56 |
| Arts | 59.55 | 74.60 |

The full 37-benchmark breakdown is in [`results.json`](results.json).
The publication-safe official scorer bundle is in
[`artifacts/mo-2.0/`](artifacts/mo-2.0/README.md).

Mo 2.0 was evaluated through the production `modaic.dev` API on all 140,178
public-suite cases (312,320 independent fields), with full coverage and no
refusals, schema rejections, output exhaustion, skips, or truncation. Decision
Index 0.4.1 reuses this official 0.3 public suite; the separate Full score is a
private maintainers-only administration. The pinned scorer commit is
`62d2f51de34a2de64906345b6bc3e98e27ff55c7`; the official result-wire SHA-256
is `3d4e820726dcdd3ffecd5ab4fd1e968add9798fe00b597b493392c6325e1895e`.
