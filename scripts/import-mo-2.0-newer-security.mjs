import { readFileSync, writeFileSync } from "node:fs";
import { fileURLToPath } from "node:url";
import path from "node:path";

const root = fileURLToPath(new URL("../", import.meta.url));
const read = (file) => JSON.parse(readFileSync(path.join(root, file), "utf8"));
const catalogPath = path.join(root, "data/benchmark-results.json");
const catalog = read("data/benchmark-results.json");
const metrics = read("benchmarks/security/artifacts/mo-2.0/metrics.json");
const noul = read("data/noul-metrics.json").results;
const mappings = {
  "access_control_reasoning/alternate_authorization_paths": ["access_control_reasoning:alternate_authorization_paths", "access_control_reasoning", "alternate_authorization_paths"],
  "access_control_reasoning/temporal_and_timezone_boundaries": ["access_control_reasoning:temporal_and_timezone_boundaries", "access_control_reasoning", "temporal_and_timezone_boundaries"],
  "access_control_reasoning/unknown_completion_sufficiency": ["access_control_reasoning:sufficiency_under_unknown_completions", "access_control_reasoning", "unknown_completion_sufficiency"],
  "access_control_reasoning/remediation_vs_effective_access": ["access_control_reasoning:remediation_status_versus_effective_access", "access_control_reasoning", "remediation_vs_effective_access"],
  "access_control_reasoning/policy_disposition": ["access_control_reasoning:four_way_policy_disposition", null, null],
  "access_control_reasoning/compositional_risk": ["access_control_reasoning:compositional_risk", null, null],
  "user_intent_alignment/openhands_balanced": ["user_intent_guardrails:openhands_balanced", "user_intent_guardrails", "openhands_balanced"],
  "user_intent_alignment/openhands_prevalence": ["user_intent_guardrails:openhands_prevalence", "user_intent_guardrails", "openhands_prevalence"],
  "user_intent_alignment/pi_balanced": ["user_intent_guardrails:pi_balanced", "user_intent_guardrails", "pi_balanced"],
  "user_intent_alignment/pi_prevalence": ["user_intent_guardrails:pi_prevalence", "user_intent_guardrails", "pi_prevalence"],
};
if (metrics.rows !== 3808 || Object.keys(metrics.per_benchmark).length !== 10) throw new Error("Mo 2.0 Security coverage drift");

const rows = Object.entries(mappings).map(([source, [benchmark, noulBenchmark, noulSlice]]) => {
  const values = metrics.per_benchmark[source];
  const template = catalog.results.find((row) => row.benchmark === benchmark && row.model !== "mo-2.0");
  if (!values || !template || values.total !== values.hard.decisions || values.hard.ties !== 0) throw new Error(`Incomplete Security result: ${source}`);
  const binary = noulBenchmark ? noul.find((row) => row.model === "mo-2.0" && row.benchmark === noulBenchmark && row.slice === noulSlice) : null;
  if (noulBenchmark && !binary) throw new Error(`Missing Noul metrics: ${source}`);
  return {
    ...template,
    model: "mo-2.0",
    model_name: "Mo 2.0",
    rows: values.total,
    scored_rows: values.hard.decisions,
    answered_rows: values.hard.decisions,
    failed_rows: 0,
    provider_refusals: 0,
    coverage: 1,
    accuracy: values.hard.exact_accuracy,
    auroc: values.hard.correctness_auroc,
    ece: values.hard.ece_equal_width_15,
    mce: values.hard.mce_equal_width_15,
    brier: values.hard.multiclass_brier,
    nll: values.hard.categorical_nll,
    ...(binary ? { precision: binary.precision, recall: binary.recall, f1: binary.f1, positive_answer: binary.positive_answer } : {}),
    primary_score: binary?.f1 ?? values.hard.exact_accuracy,
    primary_metric: binary ? "F1" : "accuracy",
    source: "benchmarks/security/artifacts/mo-2.0/metrics.json",
    source_precision: "full-precision aggregate reducer output",
  };
});
catalog.results = catalog.results.filter((row) => row.model !== "mo-2.0" || !row.benchmark.startsWith("access_control_reasoning:") && !row.benchmark.startsWith("user_intent_guardrails:"));
catalog.results.push(...rows);
writeFileSync(catalogPath, `${JSON.stringify(catalog, null, 2)}\n`);
console.log(`Imported ${rows.length} Mo 2.0 newer-Security result rows.`);
