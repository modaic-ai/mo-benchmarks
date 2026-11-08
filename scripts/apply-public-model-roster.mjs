import { readFileSync, writeFileSync } from "node:fs";
import { fileURLToPath } from "node:url";
import path from "node:path";

const root = fileURLToPath(new URL("../", import.meta.url));
const retired = new Set(["mo-1.3.2", "mo-fast"]);
const read = (file) => JSON.parse(readFileSync(path.join(root, file), "utf8"));
const write = (file, value) => writeFileSync(path.join(root, file), `${JSON.stringify(value, null, 2)}\n`);
const keep = (row) => !retired.has(row.id ?? row.model);

const catalog = read("data/benchmark-results.json");
catalog.models = catalog.models.filter(keep);
catalog.results = catalog.results.filter(keep);
catalog.decision_index.models = catalog.decision_index.models.filter(keep);
catalog.noul_results = catalog.noul_results.filter(keep);
write("data/benchmark-results.json", catalog);

const index = read("benchmarks/decision_index/results.json");
index.models = index.models.filter(keep);
write("benchmarks/decision_index/results.json", index);

const noul = read("data/noul-metrics.json");
noul.results = noul.results.filter(keep);
write("data/noul-metrics.json", noul);

const buying = read("data/buying-signals.json");
buying.models = buying.models.filter(keep);
write("data/buying-signals.json", buying);

for (const [name, rows] of Object.entries({
  catalog_models: catalog.models,
  catalog_results: catalog.results,
  decision_index_models: index.models,
  noul_results: noul.results,
  buying_signal_models: buying.models,
})) {
  if (rows.some((row) => retired.has(row.id ?? row.model))) throw new Error(`${name}: retired model remains`);
}
console.log("Removed Mo 1.3.2 and Mo Fast from all public aggregate rosters.");
