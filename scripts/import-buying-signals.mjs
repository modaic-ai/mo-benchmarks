import { existsSync, mkdirSync, readFileSync, readdirSync, writeFileSync } from "node:fs";
import { basename, join, resolve } from "node:path";

const source = resolve(process.argv[2] ?? "../mo-examples/benchmarks/buying-signals/outputs");
const target = resolve("data/buying-signals.json");

function reportFiles(dir) {
  return readdirSync(dir, { withFileTypes: true }).flatMap((entry) => {
    const path = join(dir, entry.name);
    return entry.isDirectory() ? reportFiles(path) : entry.name.endsWith("-test-report.json") ? [path] : [];
  });
}

if (!existsSync(source)) throw new Error(`Report directory not found: ${source}`);
const paths = reportFiles(source);
if (paths.length !== 7) throw new Error(`Expected 7 complete reports; found ${paths.length}`);
const reports = paths.map((path) => JSON.parse(readFileSync(path, "utf8")));
const revisions = new Set(reports.map((report) => report.dataset_revision));
const cohorts = new Set(reports.map((report) => report.prediction_run.dataset_manifest_sha256));
if (revisions.size !== 1 || cohorts.size !== 1 || reports.some((report) => report.split !== "test" || report.pooled.n !== 1000)) {
  throw new Error("Reports must all be from the same complete test cohort");
}
const taskIds = ["business_goals", "decision_criteria", "decision_makers", "decision_making_process", "pain_points"];
const metrics = ["f1", "precision", "recall", "accuracy", "auroc", "ece"];
const summary = (value) => Object.fromEntries(metrics.map((metric) => [metric, value[metric]]));
const data = {
  benchmark: "Buying signal detection",
  source: "gong-io-research/call-playbook",
  revision: [...revisions][0],
  cohort_sha256: [...cohorts][0],
  split: "test",
  decisions_per_model: 1000,
  signals: taskIds.map((id) => ({ id, label: id.replaceAll("_", " ") })),
  models: reports.map((report) => ({
    id: report.prediction_run.name,
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
  })).sort((a, b) => b.macro.f1 - a.macro.f1),
  baseline_macro_f1: reports[0].baseline_macro_f1,
};
if (new Set(data.models.map((model) => model.id)).size !== 7) throw new Error("Duplicate model names");
mkdirSync(resolve("data"), { recursive: true });
writeFileSync(target, `${JSON.stringify(data, null, 2)}\n`);
console.log(`Wrote ${basename(target)} with ${data.models.length} aggregate model reports`);
