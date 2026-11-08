import { createHash } from "node:crypto";
import { readFileSync, writeFileSync } from "node:fs";
import { fileURLToPath } from "node:url";
import path from "node:path";

const root = fileURLToPath(new URL("../", import.meta.url));
const artifactPath = path.join(root, "benchmarks/mo-2.0-production-api/metrics.json");
const aggregatePath = path.join(root, "data/benchmark-results.json");
const expectedSha256 = "7831ab981882b1842b540c7292e4e1908df75c053f3d2f615ee7a7550456178a";
const artifactBytes = readFileSync(artifactPath);
const actualSha256 = createHash("sha256").update(artifactBytes).digest("hex");
if (actualSha256 !== expectedSha256) throw new Error(`Mo 2.0 metrics checksum mismatch: ${actualSha256}`);

const metrics = JSON.parse(artifactBytes.toString("utf8"));
const catalog = JSON.parse(readFileSync(aggregatePath, "utf8"));
const views = Object.entries(metrics.per_benchmark);
if (metrics.rows !== 37712 || metrics.scored_rows !== 37712 || metrics.provider_refusals !== 0 || views.length !== 29) {
  throw new Error("Mo 2.0 hosted-panel coverage drift");
}

const display = new Map(catalog.results.map((row) => [row.benchmark, row]));
const security = {
  okta_policy_test: "policy_conditioned_access_review",
  okta_composed_test: "compositional_access_continuation",
};
const rows = [];
for (const [sourceBenchmark, values] of views) {
  if (sourceBenchmark === "okta_policy_validation" || sourceBenchmark === "okta_composed_validation") continue;
  const benchmark = security[sourceBenchmark] ?? sourceBenchmark.split("/").at(-1);
  const template = display.get(benchmark);
  if (!template) throw new Error(`No public catalog row for ${sourceBenchmark}`);
  const hard = values.hard;
  if (hard.requested_decisions !== hard.decisions || hard.provider_refusals !== 0 || hard.coverage !== 1) {
    throw new Error(`Incomplete Mo 2.0 result for ${sourceBenchmark}`);
  }
  rows.push({
    ...template,
    model: "mo-2.0",
    model_name: "Mo 2.0",
    rows: hard.requested_decisions,
    scored_rows: hard.decisions,
    provider_refusals: 0,
    coverage: 1,
    accuracy: hard.exact_accuracy_all_requests,
    auroc: hard.correctness_auroc,
    ece: hard.ece_equal_width_15,
    mce: hard.mce_equal_width_15,
    brier: hard.multiclass_brier,
    nll: hard.categorical_nll,
    primary_score: hard.exact_accuracy_all_requests,
    primary_metric: "accuracy",
  });
}
if (rows.length !== 27) throw new Error(`Expected 27 website rows, received ${rows.length}`);

catalog.results = catalog.results.filter((row) => row.model !== "mo-2.0").concat(rows);
const ood = views.filter(([name]) => name.startsWith("ood/")).map(([, values]) => values.hard);
const finance = views.filter(([name]) => name.startsWith("finance/")).map(([, values]) => values.hard);
catalog.models = catalog.models.filter((model) => model.id !== "mo-2.0");
catalog.models.unshift({
  id: "mo-2.0",
  name: "Mo 2.0",
  open_benchmarks: {
    micro_accuracy: ood.reduce((sum, row) => sum + row.exact_accuracy_all_requests * row.requested_decisions, 0) / ood.reduce((sum, row) => sum + row.requested_decisions, 0),
    macro_accuracy: ood.reduce((sum, row) => sum + row.exact_accuracy_all_requests, 0) / ood.length,
    rows: ood.reduce((sum, row) => sum + row.requested_decisions, 0),
  },
  finance: {
    macro_accuracy: finance.reduce((sum, row) => sum + row.exact_accuracy_all_requests, 0) / finance.length,
    rows: finance.reduce((sum, row) => sum + row.requested_decisions, 0),
  },
});
writeFileSync(aggregatePath, JSON.stringify(catalog, null, 2) + "\n");
console.log(`Imported ${rows.length} Mo 2.0 website rows from ${views.length} completed benchmark views.`);
