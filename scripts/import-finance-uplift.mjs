import { readFileSync, writeFileSync } from "node:fs";
import { resolve } from "node:path";

const root = resolve(import.meta.dirname, "..");
const tasks = [
  {
    slug: "esg",
    label: "ESG issue classification",
    chartLabel: "ESG issues",
    dataset: "ChanceFocus/flare-mlesg",
    evaluationSplit: "test",
  },
  {
    slug: "german-credit",
    label: "German credit risk",
    chartLabel: "German credit",
    dataset: "ChanceFocus/flare-german",
    evaluationSplit: "test",
  },
  {
    slug: "fomc",
    label: "FOMC stance",
    chartLabel: "FOMC stance",
    dataset: "gtfintechlab/fomc_communication",
    evaluationSplit: "test",
  },
  {
    slug: "gold-headlines",
    label: "Gold-price headlines",
    chartLabel: "Gold headlines",
    dataset: "ChanceFocus/flare-headlines",
    evaluationSplit: "test",
  },
  {
    slug: "fincalc-nli",
    label: "FinCalc entailment",
    chartLabel: "FinCalc",
    dataset: "anespo28/fincalc-nli",
    evaluationSplit: "test",
  },
  {
    slug: "multifin",
    label: "MultiFin topics",
    chartLabel: "MultiFin",
    dataset: "awinml/MultiFin",
    evaluationSplit: "validation",
  },
  {
    slug: "banking77-routing",
    label: "Banking77 intents",
    chartLabel: "Banking77",
    dataset: "DeepPavlov/banking77",
    evaluationSplit: "test",
  },
  {
    slug: "cfpb-routing",
    label: "CFPB complaints",
    chartLabel: "CFPB",
    dataset: "Johnade/consumer_complaints_cfpb",
    evaluationSplit: "test",
  },
];

const imported = tasks.map((task) => {
  const reportName = task.slug === "banking77-routing" ? `${task.slug}.reasoning.report.json` : `${task.slug}.report.json`;
  const path = resolve(root, "benchmarks/finance-uplift/outputs", reportName);
  const report = JSON.parse(readFileSync(path, "utf8"));
  if (report.task !== task.slug || report.base_model !== "modaic/mo") {
    throw new Error(`${task.slug}: unexpected task or base model`);
  }
  if (report.n !== 200 || report.training_labels > 200 || report.training_labels < 1) {
    throw new Error(`${task.slug}: invalid evaluation or label count`);
  }
  if (report.batch_status !== "completed" && report.batch_status !== "not_applicable") {
    throw new Error(`${task.slug}: alignment batch has not completed`);
  }
  if (report.alignment_outcome === "no_new_checkpoint") {
    if (report.aligned_accuracy !== null || report.uplift_pp !== null ||
        report.uplift_95pct_bootstrap_ci_pp !== null || report.batch_status !== "not_applicable") {
      throw new Error(`${task.slug}: no-checkpoint alignment must not claim uplift`);
    }
  } else if (Math.abs(report.uplift_pp - (report.aligned_accuracy - report.baseline_accuracy) * 100) > 1e-9) {
    throw new Error(`${task.slug}: uplift does not match accuracies`);
  }
  if (task.slug === "banking77-routing" &&
      (report.ground_reasoning_count !== 167 || typeof report.label_only_accuracy !== "number")) {
    throw new Error("Banking77: reasoning comparison is incomplete");
  }
  if (task.slug === "cfpb-routing" &&
      (report.near_duplicate_test_rows_excluded !== 136 ||
       !report.source_train_cohort_sha256 || !report.test_similarity_exclusion)) {
    throw new Error("CFPB: clean held-out test comparison is required");
  }
  if (task.slug === "esg" &&
      (report.near_duplicate_test_rows_excluded !== 1 || !report.test_similarity_exclusion ||
       !report.source_train_revision)) {
    throw new Error("ESG: disjoint FinNLP training and clean held-out test comparison is required");
  }
  const metrics = { ...report };
  delete metrics.task;
  return { ...task, ...metrics };
}).sort((a, b) => a.baseline_accuracy - b.baseline_accuracy);

const output = {
  benchmark: "Finance alignment uplift",
  base_model: "modaic/mo",
  method: "One saved model per task; up to 200 captured training rows; fixed held-out evaluation. Banking77 also compares a second alignment after adding audited ground reasoning to the same examples.",
  tasks: imported,
};
writeFileSync(resolve(root, "data/finance-uplift.json"), JSON.stringify(output, null, 2) + "\n");
console.log(`Imported ${imported.length} completed finance uplift reports.`);
