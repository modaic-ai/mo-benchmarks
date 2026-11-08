import { readFileSync, writeFileSync } from "node:fs";
import { fileURLToPath } from "node:url";
import path from "node:path";

const root = fileURLToPath(new URL("../", import.meta.url));
const indexPath = process.argv[2];
if (!indexPath) throw new Error("Usage: node scripts/import-decision-index.mjs /path/to/index.json");

const readJson = (file) => JSON.parse(readFileSync(file, "utf8"));
const writeJson = (file, value) => writeFileSync(file, `${JSON.stringify(value, null, 2)}\n`);
const canonicalPath = path.join(root, "benchmarks/decision_index/results.json");
const catalogPath = path.join(root, "data/benchmark-results.json");
const canonicalText = readFileSync(canonicalPath, "utf8");
const canonical = JSON.parse(canonicalText);
const catalog = readJson(catalogPath);
const scored = readJson(path.resolve(indexPath));

if (scored.edition !== "0.3" || scored.panel_id !== "decision-index-0.3") {
  throw new Error(`Unexpected Decision Index suite: ${scored.edition}/${scored.panel_id}`);
}
if (scored.index !== 70.95 || scored.raw_index !== 77.97 || scored.scores?.breadth_skill !== 70.3) {
  throw new Error("Mo 2.0 headline scores differ from the verified scoring receipt");
}
if (canonical.models.some((model) => model.id === "mo-2.0")) {
  throw new Error("Refusing to overwrite an existing Mo 2.0 result");
}

const template = canonical.models.find((model) => model.id === "mo-1.3.2");
if (!template) throw new Error("Missing benchmark metadata template");
const indexedIds = scored.areas.flatMap((area) => area.benchmarks);
if (indexedIds.length !== 37 || new Set(indexedIds).size !== 37) {
  throw new Error(`Expected 37 unique indexed benchmarks, received ${indexedIds.length}`);
}

const benchmarkMetadata = new Map(template.benchmarks.map((benchmark) => [benchmark.id, benchmark]));
const benchmarks = indexedIds.map((id) => {
  const metadata = benchmarkMetadata.get(id);
  const result = scored.benchmarks[String(id)];
  if (!metadata || !result || result.in_index !== true || result.coverage !== 1) {
    throw new Error(`Incomplete indexed benchmark ${id}`);
  }
  return {
    id,
    name: metadata.name,
    short: metadata.short,
    domain: metadata.domain,
    metric: metadata.metric,
    raw: result.raw,
    skill: result.skill,
    coverage: result.coverage,
  };
});

const model = {
  id: "mo-2.0",
  name: "Mo 2.0",
  scores: scored.scores,
  coverage: 1,
  domains: scored.areas.map((area) => ({
    id: area.id,
    raw: area.raw,
    skill: area.skill,
    coverage: area.coverage,
  })),
  benchmarks,
};

const modelJson = JSON.stringify(model, null, 2).split("\n").map((line) => `    ${line}`).join("\n");
const modelsMarker = '  "models": [\n';
if (!canonicalText.includes(modelsMarker)) throw new Error("Canonical model-list marker not found");
const updatedCanonicalText = canonicalText
  .replace(/  "generated_utc": "[^"]+",\n/, '  "generated_utc": "2026-11-08T07:05:57Z",\n')
  .replace(modelsMarker, `${modelsMarker}${modelJson},\n`);
const updatedCanonical = JSON.parse(updatedCanonicalText);
catalog.decision_index = updatedCanonical;
writeFileSync(canonicalPath, updatedCanonicalText);
writeJson(catalogPath, catalog);
console.log(`Imported ${benchmarks.length} Mo 2.0 Decision Index benchmark scores.`);
