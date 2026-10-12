# Gong Call Playbook buying-signal benchmark

Test only: 200 examples per signal; 1,000 decisions per model. Primary display metric: macro accuracy at p ≥ 0.5.

| Model | Model ID | Backend | Workers | Macro accuracy | Macro precision | Macro F1 | Min F1 | Macro recall | Macro AUROC | Macro ECE | p50 ms | p95 ms | p99 ms |
|---|---|---|---:|---:|---:|---:|---:|---:|---:|---:|---:|---:|---:|---:|---:|---:|
| mo | modaic/mo | modaic | 1 | 0.821 | 0.830 | 0.721 | 0.376 | 0.708 | 0.918 | 0.113 | 117 | 195 | 284 |
| luna-decisions | openai/gpt-6-luna-decisions | openrouter_decisions | 1 | 0.815 | 0.761 | 0.757 | 0.586 | 0.815 | 0.884 | 0.129 | 245 | 353 | 1266 |
| perplexity-decider | perplexity/pplx-decider-v1.1-27b | openrouter_decisions | 1 | 0.814 | 0.853 | 0.703 | 0.341 | 0.664 | 0.917 | 0.115 | 376 | 509 | 567 |
| openai-latest | openai/gpt-6.1-sol | openrouter_chat | 8 | 0.787 | 0.703 | 0.743 | 0.636 | 0.875 | 0.920 | 0.183 | 3140 | 5484 | 6791 |
| mo-fast | modaic/mo-fast | modaic | 1 | 0.774 | 0.717 | 0.718 | 0.598 | 0.824 | 0.904 | 0.160 | 120 | 186 | 283 |
| jev-latest | ~typesafe/jev-latest | openrouter_decisions | 1 | 0.773 | 0.706 | 0.728 | 0.647 | 0.840 | 0.899 | 0.153 | 210 | 311 | 379 |
| clef | cloudflare/clef | openrouter_decisions | 1 | 0.769 | 0.775 | 0.625 | 0.313 | 0.590 | 0.882 | 0.160 | 394 | 1475 | 2625 |

## Per-signal F1

| Model | business_goals | decision_criteria | decision_makers | decision_making_process | pain_points |
|---|---:|---:|---:|---:|---:|
| mo | 0.809 | 0.780 | 0.810 | 0.376 | 0.828 |
| luna-decisions | 0.829 | 0.765 | 0.778 | 0.586 | 0.826 |
| perplexity-decider | 0.809 | 0.728 | 0.816 | 0.341 | 0.820 |
| openai-latest | 0.838 | 0.785 | 0.636 | 0.673 | 0.785 |
| mo-fast | 0.806 | 0.773 | 0.598 | 0.634 | 0.780 |
| jev-latest | 0.804 | 0.754 | 0.673 | 0.647 | 0.763 |
| clef | 0.782 | 0.550 | 0.675 | 0.313 | 0.804 |

Latency excludes retries and backoff. Worker count is in each report's provenance; runs with multiple workers measure latency under concurrent load. GPT chat JSON and native Noul probabilities have distinct backends.
