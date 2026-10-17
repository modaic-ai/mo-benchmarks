# Finance held-out external-model comparison

Jev and GPT-6.1 Sol were scored on the same fixed 200-row held-out cohort for
each of the seven tasks in the standalone finance chart. The score is exact
choice accuracy. No evaluation label or alignment example was sent in a model
request. [The runner and cohort protocol](README.md#jev-and-gpt-61-sol-comparison)
and [the aggregate JSON](../../../data/finance-external-comparison.json) contain
the request settings, cohort fingerprints, and per-task counts.

| Held-out task | Jev | GPT-6.1 Sol (medium reasoning) |
| --- | ---: | ---: |
| Financial sentiment | 72.5% | 75.0% |
| FOMC stance | 62.5% | 55.5% |
| German credit | 41.0% | 79.5% |
| Gold headlines | 84.5% | 87.5% |
| MultiFin | 74.0% | 79.0% |
| SENTiVENT event | 74.0% | 73.0% |
| Twitter topics | 71.0% | 76.0% |
| **Mean across tasks** | **68.5%** | **75.1%** |

The configured model IDs were `~typesafe/jev-latest` and
`openai/gpt-6.1-sol`. OpenRouter reported serving
`typesafe/jev-1.13-20260917` and `openai/gpt-6.1-sol`, respectively. GPT used
`reasoning.effort: "medium"`. Both runs used eight concurrent workers and
completed 1,400 decisions. Jev used the native Decisions `choice` endpoint;
GPT used Chat Completions with a strict JSON-schema choice. Both received the
same task instructions, label criteria, and row state. The prepared test rows
were never used for alignment.

MultiFin and Twitter topics use their published validation splits; the other
five tasks use published test splits. These are small, task-specific cohorts,
and public source data could have appeared in foundation-model training.
