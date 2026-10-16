import { readFileSync, writeFileSync } from "node:fs";
import { fileURLToPath } from "node:url";
import path from "node:path";
const root = fileURLToPath(new URL("../", import.meta.url));
const read = (file) => readFileSync(path.join(root, file), "utf8");
const names = { "Mo 1.3.1": "mo-1.3.1", "Mo 1.3.2": "mo-1.3.2", "Jev 1.13": "jev-1.13", "Jev 1.14": "jev-1.14", "Luna Decisions": "luna-decisions", PPLX: "pplx", "GPT-6.1": "gpt-6.1", "Mo Fast": "mo-fast", Clef: "clef" };
function tables(slug) {
  return read(`benchmarks/security/${slug}/README.md`).split(/\n\s*\n/).filter((block) => block.trim().startsWith("|")).map((block) => block.trim().split("\n").map((line) => line.split("|").slice(1, -1).map((cell) => cell.trim())));
}
const catalog = JSON.parse(read("data/benchmark-results.json"));
const original = catalog.results;
const security = [];
for (const [old, slug, label] of [["access_recommendation_test", "policy_conditioned_access_review", "Policy-Conditioned Access Review"], ["access_continuation_test", "compositional_access_continuation", "Compositional Access Continuation"]]) {
  const table = tables(slug)[0];
  for (const cells of table.slice(2)) {
    const model = names[cells[0]];
    const prior = original.find((row) => [old, slug].includes(row.benchmark) && row.model === model);
    if (!prior || Math.abs(prior.accuracy * 100 - parseFloat(cells[1])) > 0.0051) throw new Error(`Test result mismatch: ${slug}/${model}`);
    security.push({ ...prior, benchmark: slug, name: label, family: slug, group: "access_reviews", split: "test" });
  }
}
function addViews(slug, table, counts) {
  const headers = table[0];
  for (const cells of table.slice(2)) {
    const view = cells[0];
    const rows = counts[view];
    if (!rows) throw new Error(`Missing view denominator: ${view}`);
    for (let i = 1; i < headers.length; i++) {
      const model = names[headers[i]];
      const accuracy = parseFloat(cells[i]) / 100;
      if (!model || !Number.isFinite(accuracy) || accuracy < 0 || accuracy > 1) throw new Error(`Invalid result: ${view}/${headers[i]}`);
      const failures = model === "jev-1.13" ? ({ "Pi balanced": 6, "Pi prevalence": 104 }[view] ?? 0) : 0;
      security.push({ benchmark: `${slug}:${view.toLowerCase().replaceAll(/[^a-z0-9]+/g, "_")}`, name: view, family: slug, group: slug, domain: "security", model, model_name: headers[i], rows, scored_rows: rows, answered_rows: rows - failures, failed_rows: failures, accuracy, source: `benchmarks/security/${slug}/README.md`, source_precision: "published accuracy rounded to 2 decimal percentage points" });
    }
  }
}
addViews("access_control_reasoning", tables("access_control_reasoning")[1], Object.fromEntries(tables("access_control_reasoning")[1].slice(2).map((row) => [row[0], 20])));
// This source table has models as rows. Transpose it to the common view format.
const intent = tables("user_intent_guardrails")[0];
const transposed = [["View", ...intent.slice(2).map((row) => row[0])], []];
for (let i = 1; i < intent[0].length; i++) transposed.push([intent[0][i], ...intent.slice(2).map((row) => row[i])]);
addViews("user_intent_guardrails", transposed, { "OpenHands balanced": 532, "OpenHands prevalence": 882, "Pi balanced": 366, "Pi prevalence": 1908 });
const noul = JSON.parse(read("data/noul-metrics.json")).results;
const accessSlices = {
  "Alternate authorization paths": "alternate_authorization_paths",
  "Temporal and timezone boundaries": "temporal_and_timezone_boundaries",
  "Sufficiency under unknown completions": "unknown_completion_sufficiency",
  "Remediation status versus effective access": "remediation_vs_effective_access",
};
for (const row of security) {
  const slice = row.family === "access_control_reasoning" ? accessSlices[row.name] : row.family === "user_intent_guardrails" ? row.name.toLowerCase().replaceAll(" ", "_") : undefined;
  if (slice) {
    const metric = noul.find((item) => item.benchmark === row.family && item.slice === slice && item.model === row.model);
    if (!metric) throw new Error(`Missing Noul metrics: ${row.family}/${slice}/${row.model}`);
    Object.assign(row, { precision: metric.precision, recall: metric.recall, f1: metric.f1, positive_answer: metric.positive_answer, answered_rows: metric.answered_rows, coverage: metric.coverage, primary_score: metric.f1, primary_metric: "F1" });
  } else Object.assign(row, { primary_score: row.accuracy, primary_metric: "accuracy" });
}
if (security.length !== 108 || read("benchmarks/security/examples.jsonl").trim().split("\n").length !== 3) throw new Error("Unexpected Security result or public example count");
const other = original.filter((row) => row.domain !== "security" && row.benchmark !== "jev_bench_noul").map((row) => {
  const metric = noul.find((item) => item.benchmark === row.benchmark && item.slice === "overall" && item.model === row.model);
  return { ...row, ...(metric ? { precision: metric.precision, recall: metric.recall, f1: metric.f1, positive_answer: metric.positive_answer, primary_score: metric.f1, primary_metric: "F1" } : { primary_score: row.accuracy, primary_metric: "accuracy" }) };
});
const jevNoul = noul.filter((row) => row.benchmark === "jev_bench").map((row) => ({ ...row, benchmark: "jev_bench_noul", name: "JevBench Noul subset", macro_exclude: true, primary_score: row.f1, primary_metric: "F1" }));
catalog.results = [...other, ...security, ...jevNoul];
catalog.noul_results = noul;
writeFileSync(path.join(root, "data/benchmark-results.json"), JSON.stringify(catalog, null, 2) + "\n");
const links = JSON.parse(read("data/benchmark-links.json"));
links.jev_bench_noul = "https://github.com/MindWareAI/jev-bench";
for (const key of Object.keys(links)) if (key.startsWith("access_continuation") || key.startsWith("access_recommendation") || key.startsWith("user_intent_alignment")) delete links[key];
for (const row of security) links[row.benchmark] = `/benchmarks/${row.family.replaceAll("_", "-")}`;
writeFileSync(path.join(root, "data/benchmark-links.json"), JSON.stringify(links, null, 2) + "\n");
console.log(`Imported ${security.length} Security result cells from checked-in protocols; retained 3 public examples.`);
