"use client";

import Image from "next/image";
import { useMemo, useState } from "react";
import { ArrowDownRight, ArrowUpRight, MoveUpRight } from "lucide-react";
import { Bar, BarChart, CartesianGrid, Cell, XAxis, YAxis } from "recharts";
import { ChartContainer, ChartTooltip, ChartTooltipContent, type ChartConfig } from "@/components/ui/chart";
import rawData from "@/data/buying-signals.json";
import { cn } from "@/lib/utils";

type Metric = "f1" | "precision" | "recall" | "accuracy" | "auroc" | "ece";
type Metrics = Record<Metric, number>;
type Model = {
  id: string;
  model_id: string;
  backend: string;
  workers: number;
  macro: Metrics;
  min_task_f1: number;
  by_signal: Record<string, Metrics & { n: number; positive: number }>;
  latency_ms: { p50: number; p95: number; p99: number };
};
type BenchmarkData = {
  benchmark: string;
  source: string;
  revision: string;
  split: string;
  decisions_per_model: number;
  signals: { id: string; label: string }[];
  models: Model[];
  baseline_macro_f1: { always_present: number; always_absent: number };
};

const data = rawData as BenchmarkData;
const metricLabels: Record<Metric, string> = {
  f1: "F1", precision: "Precision", recall: "Recall", accuracy: "Accuracy", auroc: "AUROC", ece: "ECE",
};
const metrics: Metric[] = ["f1", "recall", "precision", "accuracy", "auroc", "ece"];
const chartConfig = { score: { label: "Score", color: "var(--chart-1)" } } satisfies ChartConfig;
const signalNames: Record<string, string> = {
  business_goals: "Business goals",
  decision_criteria: "Decision criteria",
  decision_makers: "Decision makers",
  decision_making_process: "Decision process",
  pain_points: "Pain points",
};
const displayNames: Record<string, string> = {
  "luna-decisions": "Luna decisions",
  "openai-latest": "GPT-6.1 Sol",
  "jev-latest": "Jev latest",
  mo: "modaic/mo",
  "mo-fast": "modaic/mo-fast",
  "perplexity-decider": "Perplexity decider",
  clef: "Clef",
};

function formatScore(value: number) { return value.toFixed(3); }
function formatMs(value: number) { return Math.round(value).toLocaleString(); }
function isModaic(model: Model) { return model.backend === "modaic"; }

function SectionHeading({ number, title, note, id }: { number: string; title: string; note?: string; id: string }) {
  return (
    <div id={id} className="scroll-mt-8 flex flex-wrap items-baseline justify-between gap-x-6 gap-y-2 border-t-2 border-black pt-4">
      <div className="flex items-baseline gap-3">
        <span className="font-mono text-[10px] text-[#8a8a8a]">{number}</span>
        <h2 className="font-sans text-[17px] font-semibold tracking-[-0.025em] text-[#171717]">{title}</h2>
      </div>
      {note && <p className="font-sans text-[11px] text-[#777]">{note}</p>}
    </div>
  );
}

export function BenchmarkPage() {
  const [metric, setMetric] = useState<Metric>("f1");
  const [selectedModel, setSelectedModel] = useState("luna-decisions");
  const activeModel = data.models.find((model) => model.id === selectedModel) ?? data.models[0];
  const ranked = useMemo(() => [...data.models].sort((a, b) => metric === "ece" ? a.macro[metric] - b.macro[metric] : b.macro[metric] - a.macro[metric]), [metric]);
  const rankingChart = ranked.map((model) => ({ name: displayNames[model.id] ?? model.id, score: model.macro[metric], id: model.id }));
  const signalChart = data.signals.map((signal) => ({ name: signalNames[signal.id] ?? signal.label, score: activeModel.by_signal[signal.id].f1 }));
  const fastest = [...data.models].sort((a, b) => a.latency_ms.p50 - b.latency_ms.p50)[0];
  const bestCalibrated = [...data.models].sort((a, b) => a.macro.ece - b.macro.ece)[0];

  return (
    <main className="mx-auto max-w-[1440px] px-7 pb-16 pt-8 text-[12px] leading-[1.45] text-[#444] sm:px-11 sm:pt-10">
      <header className="flex flex-wrap items-center justify-between gap-x-10 gap-y-4 border-b border-[#ddd] pb-5">
        <div className="flex items-center gap-2.5">
          <span className="relative flex size-6 items-center justify-center overflow-hidden">
            <Image src="/mo-logo-transparent.png" alt="" width={24} height={24} className="scale-[1.8] object-contain" priority />
          </span>
          <a href="#top" className="font-sans text-[16px] font-semibold text-[#171717] hover:underline">Modaic Benchmarks</a>
          <span className="hidden font-sans text-[11px] text-[#999] sm:inline">/ Evidence for decisions</span>
        </div>
        <nav aria-label="Page sections" className="flex items-center gap-5 font-sans text-[11px]">
          <a href="#results" className="text-[#2a6496] underline-offset-3 hover:underline">Results</a>
          <a href="#signals" className="text-[#2a6496] underline-offset-3 hover:underline">Signals</a>
          <a href="#method" className="text-[#2a6496] underline-offset-3 hover:underline">Method</a>
          <a href="https://github.com/modaic-ai/mo-benchmarks" target="_blank" rel="noreferrer" className="inline-flex items-center gap-1 text-[#2a6496] underline-offset-3 hover:underline">
            GitHub <MoveUpRight aria-hidden="true" className="size-3" />
          </a>
        </nav>
      </header>

      <section id="top" className="grid gap-8 pb-8 pt-10 lg:grid-cols-[minmax(0,1fr)_330px] lg:gap-16 lg:pt-14">
        <div>
          <p className="mb-3 font-mono text-[10px] font-medium uppercase tracking-[0.14em] text-[#888]">Benchmark 01 <span className="mx-2 text-[#ccc]">/</span> Sales intelligence</p>
          <h1 className="max-w-[790px] font-sans text-[clamp(2.15rem,4.3vw,4.25rem)] font-semibold leading-[1.04] tracking-[-0.055em] text-[#171717]">Can models spot the buying signals?</h1>
          <p className="mt-5 max-w-[650px] font-sans text-[13px] leading-[1.65] text-[#666]">
            Seven models evaluated on five buying-signal tasks from Gong Call Playbook. Each decision asks whether a specific signal appears in a sales-call excerpt.
          </p>
          <div className="mt-7 flex flex-wrap items-center gap-x-5 gap-y-2 font-sans text-[11px]">
            <a href="#results" className="inline-flex items-center gap-1.5 border-b border-[#2a6496] pb-0.5 text-[#2a6496] hover:text-[#174463]">Explore results <MoveUpRight aria-hidden="true" className="size-3" /></a>
            <a href="#method" className="text-[#777] underline decoration-[#ccc] underline-offset-3 hover:text-[#333]">How we measured it</a>
          </div>
        </div>
        <aside className="border-l-2 border-black pl-5 font-sans lg:mt-3" aria-label="Key result">
          <p className="font-mono text-[10px] uppercase tracking-[0.12em] text-[#888]">Highest macro F1</p>
          <div className="mt-3 flex items-end gap-3">
            <span className="font-sans text-[64px] font-semibold leading-none tracking-[-0.07em] text-[#171717]">{formatScore(data.models[0].macro.f1)}</span>
            <ArrowUpRight aria-hidden="true" className="mb-2 size-4 text-[#597c60]" />
          </div>
          <p className="mt-2 text-[13px] font-medium text-[#222]">{displayNames[data.models[0].id]}</p>
          <p className="mt-2 max-w-[280px] text-[11px] leading-[1.5] text-[#777]">Mean F1 across five signals at a fixed 0.5 probability threshold.</p>
        </aside>
      </section>

      <div className="mb-13 grid grid-cols-2 border-y border-[#ddd] md:grid-cols-4" aria-label="Benchmark scope">
        {[
          ["MODELS", "07", "Decision systems compared"],
          ["SIGNALS", "05", "Binary detection tasks"],
          ["TEST DECISIONS", "1,000", "Per model, 200 per signal"],
          ["BASELINE F1", formatScore(data.baseline_macro_f1.always_present), "Always-present classifier"],
        ].map(([label, value, note], index) => (
          <div key={label} className={cn("min-w-0 py-4 pr-3 md:py-5", index % 2 !== 0 && "pl-4", index > 1 && "border-t border-[#ddd] md:border-t-0", index !== 0 && "md:border-l md:pl-5")}>
            <p className="font-mono text-[9px] font-medium tracking-[0.1em] text-[#999]">{label}</p>
            <p className="mt-1.5 font-sans text-[24px] font-semibold leading-none tracking-[-0.045em] text-[#222]">{value}</p>
            <p className="mt-1.5 font-sans text-[10px] text-[#888]">{note}</p>
          </div>
        ))}
      </div>

      <section className="mb-13">
        <SectionHeading id="results" number="01" title="Model results" note="Higher is better, except ECE and latency" />
        <div className="mt-5 flex flex-wrap items-center gap-1.5" role="group" aria-label="Choose metric">
          {metrics.map((item) => (
            <button key={item} type="button" aria-pressed={metric === item} onClick={() => setMetric(item)} className={cn("border px-2.5 py-1.5 font-sans text-[11px] transition-colors focus-visible:outline-2 focus-visible:outline-offset-2 focus-visible:outline-[#2a6496]", metric === item ? "border-[#222] bg-[#222] text-white" : "border-[#ddd] text-[#666] hover:border-[#888] hover:text-[#222]")}>{metricLabels[item]}</button>
          ))}
          <span className="ml-auto hidden font-sans text-[10px] text-[#888] sm:block">Macro average · test split</span>
        </div>

        <div className="mt-5 grid gap-8 lg:grid-cols-[minmax(0,1fr)_270px] lg:gap-12">
          <div className="min-w-0">
            <div className="mb-2 flex items-baseline justify-between gap-4">
              <h3 className="font-sans text-[13px] font-semibold text-[#222]">Macro {metricLabels[metric]}</h3>
              <span className="font-mono text-[10px] text-[#999]">{metric === "ece" ? "LOWER IS BETTER" : "HIGHER IS BETTER"}</span>
            </div>
            <ChartContainer config={chartConfig} className="h-[300px] w-full min-w-0 aspect-auto sm:h-[340px]">
              <BarChart accessibilityLayer data={rankingChart} layout="vertical" margin={{ top: 2, right: 34, bottom: 5, left: 0 }}>
                <CartesianGrid horizontal={false} stroke="#eeeeee" />
                <XAxis type="number" domain={[0, metric === "ece" ? 0.25 : 1]} tickFormatter={(value: number) => `${Math.round(value * 100)}%`} tickLine={false} axisLine={false} tick={{ fill: "#999", fontSize: 10 }} />
                <YAxis dataKey="name" type="category" width={118} tickLine={false} axisLine={false} tick={{ fill: "#555", fontSize: 10 }} />
                <ChartTooltip cursor={{ fill: "#f4f4f4" }} content={<ChartTooltipContent hideLabel formatter={(value) => <span className="font-mono font-medium text-[#222]">{Number(value).toFixed(3)}</span>} />} />
                <Bar dataKey="score" radius={[0, 2, 2, 0]} barSize={18}>
                  {rankingChart.map((item, index) => <Cell key={item.id} fill={isModaic(ranked[index]) ? "#346b87" : index === 0 ? "#171717" : "#9d9d9d"} />)}
                </Bar>
              </BarChart>
            </ChartContainer>
          </div>
          <div className="grid grid-cols-2 gap-4 border-t border-[#ddd] pt-4 font-sans lg:block lg:border-l lg:border-t-0 lg:pl-5 lg:pt-0">
            <div className="lg:pb-6">
              <p className="font-mono text-[9px] uppercase tracking-[0.09em] text-[#999]">Fastest p50</p>
              <p className="mt-2 text-[22px] font-semibold leading-none tracking-[-0.035em] text-[#222]">{formatMs(fastest.latency_ms.p50)} <span className="text-[11px] font-normal text-[#888]">ms</span></p>
              <p className="mt-1.5 text-[11px] text-[#777]">{displayNames[fastest.id]}</p>
            </div>
            <div className="lg:border-t lg:border-[#ddd] lg:py-6">
              <p className="font-mono text-[9px] uppercase tracking-[0.09em] text-[#999]">Lowest ECE</p>
              <p className="mt-2 text-[22px] font-semibold leading-none tracking-[-0.035em] text-[#222]">{formatScore(bestCalibrated.macro.ece)}</p>
              <p className="mt-1.5 text-[11px] text-[#777]">{displayNames[bestCalibrated.id]}</p>
            </div>
            <div className="col-span-2 border-t border-[#ddd] pt-4 lg:pt-6">
              <p className="font-mono text-[9px] uppercase tracking-[0.09em] text-[#999]">Read this chart</p>
              <p className="mt-2 max-w-[270px] text-[11px] leading-[1.55] text-[#777]">F1 balances false positives and missed signals. Recall measures how many real signals were found. ECE measures how closely probabilities match observed frequencies.</p>
            </div>
          </div>
        </div>

        <div className="mt-7 overflow-x-auto border-t border-[#ddd]">
          <table className="w-full min-w-[900px] border-collapse text-left font-sans text-[11px] tabular-nums">
            <caption className="sr-only">Model leaderboard across macro metrics and median latency</caption>
            <thead><tr className="text-[10px] text-[#888]">
              <th scope="col" className="py-3 pr-4 font-medium">Model</th>
              {(["f1", "precision", "recall", "accuracy", "auroc", "ece"] as Metric[]).map((item) => (
                <th key={item} scope="col" className="px-2 py-3 text-right font-medium"><button type="button" onClick={() => setMetric(item)} className={cn("inline-flex items-center gap-1 hover:text-[#222]", metric === item && "text-[#222]")} aria-label={`Sort by macro ${metricLabels[item]}`}>{metricLabels[item]}{metric === item && (item === "ece" ? <ArrowDownRight aria-hidden="true" className="size-3" /> : <ArrowUpRight aria-hidden="true" className="size-3" />)}</button></th>
              ))}
              <th scope="col" className="py-3 pl-2 text-right font-medium">p50 ms</th>
            </tr></thead>
            <tbody>{ranked.map((model, index) => (
              <tr key={model.id} className="border-t border-[#e6e6e6] hover:bg-[#fafafa]">
                <th scope="row" className="py-3 pr-4 font-medium text-[#222]"><span className="mr-3 font-mono text-[10px] text-[#aaa]">{String(index + 1).padStart(2, "0")}</span>{displayNames[model.id]}<span className="ml-2 font-mono text-[9px] font-normal text-[#aaa]">{model.workers > 1 ? `${model.workers} workers` : ""}</span></th>
                {(["f1", "precision", "recall", "accuracy", "auroc", "ece"] as Metric[]).map((item) => <td key={item} className={cn("px-2 py-3 text-right", item === metric ? "font-semibold text-[#171717]" : "text-[#666]")}>{formatScore(model.macro[item])}</td>)}
                <td className="py-3 pl-2 text-right text-[#666]">{formatMs(model.latency_ms.p50)}</td>
              </tr>
            ))}</tbody>
          </table>
        </div>
        <p className="mt-2 font-sans text-[10px] text-[#888]">GPT-6.1 Sol used strict JSON chat and eight workers. Other models used Noul decisions and one worker; latency is measured under different load.</p>
      </section>

      <section className="mb-13">
        <SectionHeading id="signals" number="02" title="Signal breakdown" note="F1 by buying-signal category" />
        <div className="mt-5 flex flex-wrap items-center gap-2">
          <label htmlFor="model-select" className="font-sans text-[11px] text-[#888]">Model</label>
          <select id="model-select" value={selectedModel} onChange={(event) => setSelectedModel(event.target.value)} className="min-w-[190px] border border-[#ccc] bg-white px-2.5 py-1.5 font-sans text-[11px] text-[#222] outline-none focus:border-[#555]">
            {data.models.map((model) => <option key={model.id} value={model.id}>{displayNames[model.id]}</option>)}
          </select>
          <span className="font-sans text-[10px] text-[#999]">200 test examples per signal</span>
        </div>
        <div className="mt-5 grid gap-7 lg:grid-cols-[minmax(0,1fr)_290px] lg:gap-12">
          <ChartContainer config={chartConfig} className="h-[260px] w-full min-w-0 aspect-auto sm:h-[300px]">
            <BarChart accessibilityLayer data={signalChart} layout="vertical" margin={{ top: 0, right: 30, bottom: 8, left: 0 }}>
              <CartesianGrid horizontal={false} stroke="#eee" />
              <XAxis type="number" domain={[0, 1]} tickFormatter={(value: number) => `${Math.round(value * 100)}%`} tickLine={false} axisLine={false} tick={{ fill: "#999", fontSize: 10 }} />
              <YAxis dataKey="name" type="category" width={118} tickLine={false} axisLine={false} tick={{ fill: "#555", fontSize: 10 }} />
              <ChartTooltip cursor={{ fill: "#f4f4f4" }} content={<ChartTooltipContent hideLabel formatter={(value) => <span className="font-mono font-medium text-[#222]">F1 {Number(value).toFixed(3)}</span>} />} />
              <Bar dataKey="score" fill={isModaic(activeModel) ? "#346b87" : "#454545"} radius={[0, 2, 2, 0]} barSize={20} />
            </BarChart>
          </ChartContainer>
          <div className="border-t border-[#ddd] pt-4 lg:border-l lg:border-t-0 lg:pl-5 lg:pt-1">
            <p className="font-mono text-[9px] uppercase tracking-[0.09em] text-[#999]">Selected model</p>
            <p className="mt-2 font-sans text-[16px] font-semibold text-[#222]">{displayNames[activeModel.id]}</p>
            <p className="mt-1 break-all font-mono text-[10px] text-[#999]">{activeModel.model_id}</p>
            <div className="mt-5 border-t border-[#ddd] pt-4">
              <p className="font-mono text-[9px] uppercase tracking-[0.09em] text-[#999]">Lowest signal F1</p>
              <p className="mt-2 font-sans text-[22px] font-semibold leading-none text-[#222]">{formatScore(activeModel.min_task_f1)}</p>
              <p className="mt-1.5 font-sans text-[11px] text-[#777]">{signalNames[data.signals.reduce((lowest, current) => activeModel.by_signal[current.id].f1 < activeModel.by_signal[lowest.id].f1 ? current : lowest).id]}</p>
            </div>
            <p className="mt-5 font-sans text-[10px] leading-[1.5] text-[#888]">The five labels come from separate binary tasks. A row labeled for one signal is not assumed to be labeled for the others.</p>
          </div>
        </div>
      </section>

      <section className="mb-12">
        <SectionHeading id="method" number="03" title="Methodology" note="Frozen test set · zero-shot prompting" />
        <div className="mt-5 grid gap-6 font-sans text-[11px] leading-[1.65] text-[#666] md:grid-cols-3 md:gap-10">
          <div><p className="mb-2 font-mono text-[9px] font-medium uppercase tracking-[0.09em] text-[#999]">Dataset</p><p>Five binary tasks from <a className="text-[#2a6496] underline decoration-[#c5d5e4] underline-offset-2 hover:decoration-[#2a6496]" href="https://huggingface.co/datasets/gong-io-research/call-playbook" target="_blank" rel="noreferrer">Gong Call Playbook</a>. Each task contributes 200 test rows. No training rows, call excerpts, or individual predictions are published here. Dataset revision <code className="break-all font-mono text-[10px] text-[#888]">{data.revision.slice(0, 12)}</code>.</p></div>
          <div><p className="mb-2 font-mono text-[9px] font-medium uppercase tracking-[0.09em] text-[#999]">Scoring</p><p>Models return p(signal present). A fixed threshold of 0.5 determines the positive class. Every headline classification metric is the unweighted mean of the five task scores. ECE uses ten probability bins. No threshold was tuned on test data.</p></div>
          <div><p className="mb-2 font-mono text-[9px] font-medium uppercase tracking-[0.09em] text-[#999]">Timing &amp; scope</p><p>Latency percentiles include only each successful HTTP attempt, excluding retries and backoff. GPT used eight concurrent workers; all others used one. This measures excerpt-level signal detection, not whether every signal in a full call was found.</p></div>
        </div>
      </section>

      <footer className="flex flex-wrap items-start justify-between gap-x-8 gap-y-4 border-t-2 border-black pt-5 font-sans text-[10px] leading-[1.55] text-[#888]">
        <p>Modaic Benchmarks <span className="mx-1 text-[#ccc]">/</span> Buying signal detection <span className="mx-1 text-[#ccc]">/</span> October 2026</p>
        <div className="flex flex-wrap gap-x-5 gap-y-2">
          <a href="https://huggingface.co/datasets/gong-io-research/call-playbook" target="_blank" rel="noreferrer" className="text-[#2a6496] hover:underline">Dataset source ↗</a>
          <a href="https://github.com/modaic-ai/mo-benchmarks" target="_blank" rel="noreferrer" className="text-[#2a6496] hover:underline">Source &amp; methods ↗</a>
          <a href="https://x.com/modaicdev" target="_blank" rel="noreferrer" className="text-[#2a6496] hover:underline">@modaicdev ↗</a>
        </div>
      </footer>
    </main>
  );
}
