import { readFileSync, writeFileSync } from "node:fs";
import { fileURLToPath } from "node:url";
import path from "node:path";

const root = fileURLToPath(new URL("../", import.meta.url));
const data = JSON.parse(readFileSync(path.join(root, "data/buying-signals.json"), "utf8"));
const names = new Map([
  ["mo-2.0", "Mo 2.0"], ["mo-1.3.1", "Mo 1.3.1"], ["jev-1.13", "Jev 1.13"],
  ["jev-1.14", "Jev 1.14"], ["luna-decisions", "Luna Decisions"], ["pplx", "PPLX"],
  ["gpt-6.1", "GPT-6.1"], ["clef", "Clef"],
]);
const models = [...data.models].sort((a, b) => b.macro.accuracy - a.macro.accuracy);
if (models.length !== 8 || models.some((model) => !names.has(model.id))) throw new Error("Unexpected Buying Signals roster");
const fixed = (value, digits = 3) => Number(value).toFixed(digits);
const lines = [
  "# Gong Call Playbook buying-signal benchmark", "",
  "Test only: 200 examples per signal; 1,000 decisions per model. Primary display metric: macro accuracy at p ≥ 0.5.", "",
  "| Model | Model ID | Backend | Workers | Macro accuracy | Macro precision | Macro F1 | Min F1 | Macro recall | Macro AUROC | Macro ECE | p50 ms | p95 ms | p99 ms |",
  "|---|---|---|---:|---:|---:|---:|---:|---:|---:|---:|---:|---:|---:|",
];
for (const model of models) {
  lines.push(`| ${names.get(model.id)} | ${model.model_id} | ${model.backend} | ${model.workers} | ${fixed(model.macro.accuracy)} | ${fixed(model.macro.precision)} | ${fixed(model.macro.f1)} | ${fixed(model.min_task_f1)} | ${fixed(model.macro.recall)} | ${fixed(model.macro.auroc)} | ${fixed(model.macro.ece)} | ${fixed(model.latency_ms.p50, 0)} | ${fixed(model.latency_ms.p95, 0)} | ${fixed(model.latency_ms.p99, 0)} |`);
}
lines.push("", "## Per-signal F1", "", `| Model | ${data.signals.map((signal) => signal.id).join(" | ")} |`, `|---|${data.signals.map(() => "---:").join("|")}|`);
for (const model of models) lines.push(`| ${names.get(model.id)} | ${data.signals.map((signal) => fixed(model.by_signal[signal.id].f1)).join(" | ")} |`);
lines.push("", "Latency excludes retries and backoff. Worker count is in each report's provenance; runs with multiple workers measure latency under concurrent load. GPT chat JSON and native Noul probabilities have distinct backends.", "");
writeFileSync(path.join(root, "benchmarks/gtm/buying_signals/RESULTS.md"), lines.join("\n"));
console.log("Rendered Buying Signals results for eight supported models.");
