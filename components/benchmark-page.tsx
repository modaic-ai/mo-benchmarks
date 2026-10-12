"use client";

import Image from "next/image";
import { useState } from "react";
import { Bar, BarChart, CartesianGrid, Cell, LabelList, XAxis, YAxis } from "recharts";
import { ChartContainer, ChartTooltip, ChartTooltipContent, type ChartConfig } from "@/components/ui/chart";
import rawData from "@/data/buying-signals.json";
import { cn } from "@/lib/utils";

type Metric = "accuracy" | "precision" | "f1" | "recall" | "auroc" | "ece";
type Metrics = Record<Metric, number>;
type Model = {
  id: string;
  model_id: string;
  workers: number;
  macro: Metrics;
  latency_ms: { p50: number; p95: number; p99: number };
};
type BenchmarkData = {
  revision: string;
  models: Model[];
};

const data = rawData as BenchmarkData;
const metrics: Metric[] = ["accuracy", "precision", "f1", "recall", "auroc", "ece"];
const metricLabels: Record<Metric, string> = {
  accuracy: "Accuracy", precision: "Precision", f1: "F1", recall: "Recall", auroc: "AUROC", ece: "ECE",
};
const displayNames: Record<string, string> = {
  "luna-decisions": "Luna decisions",
  "openai-latest": "GPT-6.1 Sol",
  "jev-latest": "Jev latest",
  mo: "Mo",
  "mo-fast": "Mo Fast",
  "perplexity-decider": "Perplexity decider",
  clef: "Clef",
};
const chartNames: Record<string, string> = {
  "luna-decisions": "Luna",
  "openai-latest": "GPT-6.1",
  "jev-latest": "Jev",
  mo: "Mo",
  "mo-fast": "Mo Fast",
  "perplexity-decider": "Perplexity",
  clef: "Clef",
};
const chartColors: Record<string, string> = {
  mo: "#2D6598",
  "mo-fast": "#66A1B5",
  "luna-decisions": "#648D79",
  "openai-latest": "#8177AA",
  "jev-latest": "#B38396",
  "perplexity-decider": "#BD9163",
  clef: "#89929B",
};
const chartConfig = { score: { label: "Score", color: "#2D6598" } } satisfies ChartConfig;

function percent(value: number) { return `${(value * 100).toFixed(1)}%`; }
function score(value: number) { return value.toFixed(3); }

export function BenchmarkPage() {
  const [metric, setMetric] = useState<Metric>("accuracy");
  const accuracyWinner = [...data.models].sort((a, b) => b.macro.accuracy - a.macro.accuracy)[0];
  const ranked = [...data.models].sort((a, b) => metric === "ece" ? a.macro.ece - b.macro.ece : b.macro[metric] - a.macro[metric]);
  const chartData = ranked.map((model) => ({ id: model.id, name: chartNames[model.id], score: model.macro[metric] }));
  const chartMin = Math.floor(Math.min(...chartData.map((item) => item.score)) * 20) / 20;
  const chartMax = Math.ceil(Math.max(...chartData.map((item) => item.score)) * 20) / 20;
  const chartTicks = Array.from({ length: Math.round((chartMax - chartMin) * 20) + 1 }, (_, index) => Number((chartMin + index * 0.05).toFixed(2)));

  return (
    <main className="mx-auto max-w-[1120px] px-5 pb-14 pt-6 font-sans text-[#454545] sm:px-10 sm:pt-8">
      <header className="flex items-center justify-between gap-5 border-b border-[#e5e5e3] pb-5">
        <a
          href="#top"
          className="flex items-center gap-2.5 text-[15px] font-semibold tracking-[-0.02em] text-[#171717]"
        >
          <Image
            src="/mo-logo.png"
            alt="Modaic"
            width={697}
            height={629}
            className="h-auto w-7 shrink-0 [image-rendering:pixelated]"
            priority
          />
          <span>Benchmarks</span>
        </a>
        <a
          href="https://github.com/modaic-ai/mo-benchmarks"
          target="_blank"
          rel="noreferrer"
          className="text-[11px] text-[#2a6496] hover:underline"
        >
          GitHub ↗
        </a>
      </header>

      <section
        id="top"
        className="grid gap-6 border-b border-[#e5e5e3] py-8 sm:py-10 md:grid-cols-[minmax(0,1fr)_190px] md:items-end md:gap-8"
      >
        <div>
          <h1 className="text-[19px] font-semibold tracking-[-0.03em] text-[#171717]">
            Who catches the signals?
          </h1>
          <p className="mt-3 max-w-[600px] text-[13px] leading-[1.65] text-[#696969]">
            Each model estimates the probability that a specified buying signal
            is present in a speaker-tagged sales-call excerpt. We score those
            probabilities and decisions at a fixed 0.5 threshold against Gong’s
            held-out labels across five tasks—1,000 decisions per model.
          </p>
        </div>
        <div className="border-l-[3px] border-[#2D6598] pl-4">
          <p className="text-[10px] font-medium uppercase tracking-[0.12em] text-[#777]">
            Best accuracy
          </p>
          <p className="text-[19px] font-semibold tracking-[-0.03em] text-[#171717]">
            {percent(accuracyWinner.macro.accuracy)}
          </p>
          <p className="mt-2 text-[12px] font-medium text-[#2D6598]">
            {displayNames[accuracyWinner.id]}
          </p>
        </div>
      </section>

      <section id="results" className="pt-9 sm:pt-11">
        <div className="flex flex-wrap items-end justify-between gap-3">
          <div>
            <h2 className="text-[19px] font-semibold tracking-[-0.03em] text-[#171717]">
              Model comparison
            </h2>
            <p className="mt-1 text-[11px] text-[#888]">
              Macro average across five tasks · 0.5 decision threshold
            </p>
          </div>
        </div>

        <div
          className="mt-6 flex flex-wrap gap-2"
          role="group"
          aria-label="Choose metric"
        >
          {metrics.map((item) => (
            <button
              key={item}
              type="button"
              aria-pressed={metric === item}
              onClick={() => setMetric(item)}
              className={cn(
                "rounded-full border px-3 py-1.5 text-[11px] font-medium transition-colors focus-visible:outline-2 focus-visible:outline-offset-2 focus-visible:outline-[#2D6598]",
                metric === item
                  ? "border-[#2D6598] bg-[#2D6598] text-white"
                  : "border-[#e1e1df] bg-white text-[#666] hover:border-[#8faaba] hover:text-[#2D6598]",
              )}
              aria-label={
                item === "ece" ? "ECE, lower is better" : metricLabels[item]
              }
            >
              {metricLabels[item]}
              {item === "ece" ? " ↓" : ""}
            </button>
          ))}
        </div>

        <div className="mt-5 overflow-x-auto rounded-lg border border-[#e8e8e6] bg-[#fcfcfb] px-3 pb-3 pt-6 sm:px-6">
          <div className="min-w-[590px]">
            <p className="px-2 text-[12px] font-medium text-[#333]">
              {metricLabels[metric]} by model
              {metric === "ece" && (
                <span className="ml-2 text-[#8a5b43]">↓ Lower is better</span>
              )}
            </p>
            <ChartContainer
              config={chartConfig}
              className="mt-3 h-[350px] w-full aspect-auto"
            >
              <BarChart
                accessibilityLayer
                data={chartData}
                margin={{ top: 24, right: 16, bottom: 5, left: -10 }}
              >
                <CartesianGrid vertical={false} stroke="#e7e9e9" />
                <XAxis
                  dataKey="name"
                  tickLine={false}
                  axisLine={false}
                  interval={0}
                  tick={{ fill: "#666", fontSize: 11 }}
                  tickMargin={12}
                />
                <YAxis
                  type="number"
                  domain={[chartMin, chartMax]}
                  ticks={chartTicks}
                  allowDataOverflow
                  tickFormatter={(value: number) =>
                    `${Math.round(value * 100)}%`
                  }
                  tickLine={false}
                  axisLine={false}
                  tick={{ fill: "#999", fontSize: 10 }}
                />
                <ChartTooltip
                  cursor={{ fill: "#edf1f2" }}
                  content={
                    <ChartTooltipContent
                      hideLabel
                      formatter={(value) => (
                        <span className="font-mono font-medium text-[#222]">
                          {percent(Number(value))}
                        </span>
                      )}
                    />
                  }
                />
                <Bar dataKey="score" radius={[3, 3, 0, 0]} maxBarSize={62}>
                  {chartData.map((item) => (
                    <Cell key={item.id} fill={chartColors[item.id]} />
                  ))}
                  <LabelList
                    dataKey="score"
                    position="top"
                    formatter={(value) => percent(Number(value))}
                    className="fill-[#555] text-[10px] font-medium"
                  />
                </Bar>
              </BarChart>
            </ChartContainer>
          </div>
        </div>
        <p className="mt-3 text-[10px] leading-[1.5] text-[#888]">
          Each bar is the unweighted average of five test-set{" "}
          {metricLabels[metric].toLowerCase()} scores. The y-axis is truncated
          to make close scores easier to compare.
        </p>
      </section>

      <section className="mt-9 border-t border-[#e5e5e3] pt-4">
        <details open className="group">
          <summary className="flex cursor-pointer list-none items-center justify-between gap-4 text-[12px] font-medium text-[#333] marker:hidden">
            Full results{" "}
            <span className="text-[17px] font-normal text-[#999] group-open:rotate-45">
              +
            </span>
          </summary>
          <div className="mt-4 overflow-x-auto">
            <table className="w-full min-w-[740px] border-collapse text-left text-[11px] tabular-nums">
              <caption className="sr-only">
                All model metrics and median latency, sorted by the selected
                chart metric
              </caption>
              <thead className="text-[#888]">
                <tr className="border-b border-[#dededc]">
                  <th scope="col" className="py-2 pr-4 font-medium">
                    Model
                  </th>
                  {metrics.map((item) => (
                    <th
                      key={item}
                      scope="col"
                      className={cn(
                        "px-2 py-2 text-right font-medium",
                        item === metric && "text-[#2D6598]",
                      )}
                    >
                      {metricLabels[item]}
                      {item === "ece" ? " ↓" : ""}
                    </th>
                  ))}
                  <th scope="col" className="py-2 pl-2 text-right font-medium">
                    p50 ms
                  </th>
                </tr>
              </thead>
              <tbody>
                {ranked.map((model) => (
                  <tr key={model.id} className="border-b border-[#ededeb]">
                    <th
                      scope="row"
                      className="py-2.5 pr-4 font-medium text-[#333]"
                    >
                      {displayNames[model.id]}
                    </th>
                    {metrics.map((item) => (
                      <td
                        key={item}
                        className={cn(
                          "px-2 py-2.5 text-right",
                          item === metric
                            ? "font-semibold text-[#2D6598]"
                            : "text-[#666]",
                        )}
                      >
                        {score(model.macro[item])}
                      </td>
                    ))}
                    <td className="py-2.5 pl-2 text-right text-[#666]">
                      {Math.round(model.latency_ms.p50).toLocaleString()}
                    </td>
                  </tr>
                ))}
              </tbody>
            </table>
          </div>
          <p className="mt-3 text-[10px] leading-[1.5] text-[#888]">
            GPT-6.1 Sol ran with eight workers; other models ran with one.
            Latency reflects different concurrency loads and excludes retries.
          </p>
        </details>
      </section>

      <section id="method" className="mt-5 border-t border-[#e5e5e3] pt-4">
        <details className="group">
          <summary className="flex cursor-pointer list-none items-center justify-between gap-4 text-[12px] font-medium text-[#333] marker:hidden">
            Methodology{" "}
            <span className="text-[17px] font-normal text-[#999] group-open:rotate-45">
              +
            </span>
          </summary>
          <div className="mt-4 max-w-[780px] space-y-3 text-[11px] leading-[1.65] text-[#666]">
            <p>
              Five binary tasks from{" "}
              <a
                href="https://huggingface.co/datasets/gong-io-research/call-playbook"
                target="_blank"
                rel="noreferrer"
                className="text-[#2a6496] underline"
              >
                Gong Call Playbook
              </a>{" "}
              contribute 200 test rows each. No training rows, call excerpts, or
              individual predictions are published here. Dataset revision{" "}
              <code className="font-mono">{data.revision.slice(0, 12)}</code>.
            </p>
            <p>
              Models return p(signal present). A fixed 0.5 threshold determines
              the positive class. Reported classification metrics are unweighted
              means of five task scores. ECE uses ten probability bins; lower
              ECE is better. No threshold was tuned on test data.
            </p>
            <p>
              Latency percentiles include each successful HTTP attempt only,
              excluding retries and backoff. This measures signal detection in
              excerpts, not full-call coverage.
            </p>
          </div>
        </details>
      </section>

      <footer className="mt-12 flex flex-wrap items-center justify-between gap-3 border-t-2 border-[#222] pt-4 text-[10px] text-[#888]">
        <p>Modaic Benchmarks · October 2026</p>
        <a
          href="https://github.com/modaic-ai/mo-benchmarks"
          target="_blank"
          rel="noreferrer"
          className="text-[#2a6496] hover:underline"
        >
          Source &amp; methods ↗
        </a>
      </footer>
    </main>
  );
}
