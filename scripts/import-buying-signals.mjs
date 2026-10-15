import { existsSync, mkdirSync, readFileSync, readdirSync, writeFileSync } from "node:fs";
import { basename, join, resolve } from "node:path";

const source = resolve(process.argv[2] ?? "benchmarks/gtm/buying_signals/outputs");
const target = resolve("data/buying-signals.json");
const expectedIds = ["mo-1.3.1", "mo-1.3.2", "jev-1.13", "jev-1.14", "luna-decisions", "pplx", "gpt-6.1", "mo-fast", "clef"];
const aliases = new Map([
  ["mo", "mo-1.3.1"],
  ["jev-latest", "jev-1.13"],
  ["openai-latest", "gpt-6.1"],
  ["perplexity-decider", "pplx"],
]);

function reportFiles(dir) {
  return readdirSync(dir, { withFileTypes: true }).flatMap((entry) => {
    const path = join(dir, entry.name);
    return entry.isDirectory() ? reportFiles(path) : entry.name.endsWith("-test-report.json") ? [path] : [];
  });
}

if (!existsSync(source)) throw new Error(`Report directory not found: ${source}`);
const paths = reportFiles(source);
if (paths.length < 1) throw new Error("Expected at least one complete report");
const reports = paths.map((path) => JSON.parse(readFileSync(path, "utf8")));
const revisions = new Set(reports.map((report) => report.dataset_revision));
const cohorts = new Set(reports.map((report) => report.prediction_run.dataset_manifest_sha256));
if (revisions.size !== 1 || cohorts.size !== 1 || reports.some((report) => report.split !== "test" || report.pooled.n !== 1000)) {
  throw new Error("Reports must all be from the same complete test cohort");
}
const taskIds = ["business_goals", "decision_criteria", "decision_makers", "decision_making_process", "pain_points"];
const metrics = ["f1", "precision", "recall", "accuracy", "auroc", "ece"];
const summary = (value) => Object.fromEntries(metrics.map((metric) => [metric, value[metric]]));
const existing = existsSync(target) ? JSON.parse(readFileSync(target, "utf8")) : null;
if (existing && (existing.revision !== [...revisions][0] || existing.cohort_sha256 !== [...cohorts][0] || existing.decisions_per_model !== 1000)) {
  throw new Error("Existing aggregate belongs to a different cohort");
}
const imported = reports.map((report) => ({
  id: aliases.get(report.prediction_run.name) ?? report.prediction_run.name,
  model_id: report.prediction_run.model,
  backend: report.prediction_run.backend,
  workers: report.latency.workers,
  macro: summary(report.macro),
  min_task_f1: report.min_task_f1,
  by_signal: Object.fromEntries(taskIds.map((id) => [id, { ...summary(report.by_task[id]), n: report.by_task[id].n, positive: report.by_task[id].positive }])),
  latency_ms: {
    p50: report.latency.p50_ms,
    p95: report.latency.p95_ms,
    p99: report.latency.p99_ms,
  },
}));
const merged = new Map((existing?.models ?? []).map((model) => [aliases.get(model.id) ?? model.id, { ...model, id: aliases.get(model.id) ?? model.id }]));
for (const model of imported) merged.set(model.id, model);
if (new Set(imported.map((model) => model.id)).size !== imported.length) throw new Error("Duplicate imported model names");
if (expectedIds.some((id) => !merged.has(id)) || merged.size !== expectedIds.length) {
  throw new Error(`Expected exactly these nine models: ${expectedIds.join(", ")}`);
}
const data = {
  benchmark: "Buying signal detection",
  source: "gong-io-research/call-playbook",
  revision: [...revisions][0],
  cohort_sha256: [...cohorts][0],
  split: "test",
  decisions_per_model: 1000,
  signals: taskIds.map((id) => ({ id, label: id.replaceAll("_", " ") })),
  models: [...merged.values()].sort((a, b) => b.macro.f1 - a.macro.f1),
  baseline_macro_f1: reports[0].baseline_macro_f1 ?? existing?.baseline_macro_f1,
};
mkdirSync(resolve("data"), { recursive: true });
writeFileSync(target, `${JSON.stringify(data, null, 2)}\n`);
console.log(`Wrote ${basename(target)} with ${data.models.length} aggregate model reports`);
