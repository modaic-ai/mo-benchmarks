"use client";

import Image from "next/image";
import Link from "next/link";
import { useMemo, useState } from "react";
import benchmarkData from "@/data/benchmark-results.json";
import buyingSignals from "@/data/buying-signals.json";
import { cn } from "@/lib/utils";

type Domain = { id: string; name: string };
type Result = { benchmark: string; name: string; domain: string; model: string; model_name: string; rows: number; accuracy: number };
type IndexBenchmark = { id: number; name: string; short: string; domain: string; metric: string; raw: number; skill: number };
type IndexDomain = { id: string; raw: number; skill: number };
type Aggregate = {
  domains: Domain[];
  results: Result[];
  decision_index: {
    source: string;
    models: Array<{
      id: string;
      name: string;
      coverage: number;
      scores: { balanced_raw: number; balanced_skill: number; breadth_skill: number; public_skill: number };
      domains: IndexDomain[];
      benchmarks: IndexBenchmark[];
    }>;
  };
};
type BuyingModel = { id: string; macro: { accuracy: number; auroc: number; ece: number } };

const catalog = benchmarkData as Aggregate;
const indexModel = catalog.decision_index.models.find((model) => model.id === "mo-1.3.2") ?? catalog.decision_index.models[0];
const roster = ["mo-1.3.1", "mo-1.3.2", "jev-1.13", "jev-1.14", "luna-decisions", "pplx", "gpt-6.1", "mo-fast", "clef"];
const modelNames = new Map(catalog.results.map((row) => [row.model, row.model_name]));
const gtmModels = (buyingSignals as { models: BuyingModel[] }).models;
const gtmNames: Record<string, string> = {
  "luna-decisions": "Luna decisions",
  "gpt-6.1": "GPT-6.1",
  "jev-1.13": "Jev 1.13",
  "jev-1.14": "Jev 1.14",
  "mo-1.3.1": "Mo 1.3.1",
  "mo-1.3.2": "Mo 1.3.2",
  "mo-fast": "Mo Fast",
  pplx: "PPLX",
  clef: "Clef",
};

function percent(value: number) { return `${(value * 100).toFixed(1)}%`; }
function indexScore(value: number) { return value.toFixed(2); }

export function BenchmarkPage() {
  const [domain, setDomain] = useState("knowledge");
  const indexByDomain = useMemo(() => indexModel.benchmarks.filter((row) => row.domain === domain), [domain]);
  const evaluations = useMemo(() => {
    const grouped = new Map<string, Result[]>();
    for (const result of catalog.results.filter((row) => row.domain === domain)) {
      grouped.set(result.name, [...(grouped.get(result.name) ?? []), result]);
    }
    return [...grouped.entries()];
  }, [domain]);

  return (
    <main className="mx-auto max-w-[1160px] px-5 pb-14 pt-6 font-sans text-[#454545] sm:px-10 sm:pt-8">
      <header className="flex items-center justify-between gap-5 border-b border-[#e5e5e3] pb-5">
        <a href="#top" className="flex items-center gap-2.5 text-[15px] font-semibold tracking-[-0.02em] text-[#171717]">
          <Image src="/mo-logo.png" alt="Modaic" width={697} height={629} className="h-auto w-7 shrink-0 [image-rendering:pixelated]" priority />
          <span>Benchmarks</span>
        </a>
        <a href="https://github.com/modaic-ai/mo-benchmarks" target="_blank" rel="noreferrer" className="text-[11px] text-[#2a6496] hover:underline">GitHub ↗</a>
      </header>

      <section id="top" className="grid gap-7 border-b border-[#e5e5e3] py-9 md:grid-cols-[minmax(0,1fr)_230px] md:items-end">
        <div>
          <p className="text-[10px] font-medium uppercase tracking-[0.14em] text-[#2D6598]">Decision Index</p>
          <h1 className="mt-2 text-[25px] font-semibold tracking-[-0.04em] text-[#171717]">Broad decision skill, benchmark by benchmark.</h1>
          <p className="mt-3 max-w-[650px] text-[13px] leading-[1.65] text-[#696969]">Compare decision models across the Decision Index, JevBench, public transfer benchmarks, Finance, Security, and GTM.</p>
        </div>
        <div className="border-l-[3px] border-[#2D6598] pl-4">
          <p className="text-[10px] font-medium uppercase tracking-[0.12em] text-[#777]">Mo 1.3.2 balanced skill</p>
          <p className="mt-1 text-[32px] font-semibold tracking-[-0.04em] text-[#171717]">{indexScore(indexModel.scores.balanced_skill)}</p>
          <p className="mt-1 text-[10px] text-[#888]">Balanced raw {indexScore(indexModel.scores.balanced_raw)}</p>
        </div>
      </section>

      <section className="py-8">
        <div className="flex items-baseline justify-between gap-4">
          <h2 className="text-[16px] font-semibold tracking-[-0.02em] text-[#171717]">Decision Index breakdown</h2>
          <a href={catalog.decision_index.source} target="_blank" rel="noreferrer" className="text-[10px] text-[#2a6496] hover:underline">Source ↗</a>
        </div>
        <div className="mt-4 grid grid-cols-2 gap-px overflow-hidden rounded-lg border border-[#e5e5e3] bg-[#e5e5e3] sm:grid-cols-5">
          {indexModel.domains.map((item) => (
            <div key={item.id} className="bg-[#fcfcfb] px-4 py-4">
              <p className="text-[10px] capitalize text-[#777]">{item.id}</p>
              <p className="mt-1 text-[20px] font-semibold text-[#222]">{percent(item.skill)}</p>
              <p className="mt-1 text-[9px] text-[#999]">raw {percent(item.raw)}</p>
            </div>
          ))}
        </div>
        <div className="mt-5 overflow-x-auto rounded-lg border border-[#e8e8e6]">
          <table className="w-full min-w-[680px] text-left text-[11px] tabular-nums">
            <thead className="bg-[#f7f7f5] text-[#888]"><tr><th className="px-4 py-2 font-medium">Model</th><th className="px-4 py-2 text-right font-medium">Balanced skill</th><th className="px-4 py-2 text-right font-medium">Balanced raw</th><th className="px-4 py-2 text-right font-medium">Breadth skill</th><th className="px-4 py-2 text-right font-medium">Coverage</th></tr></thead>
            <tbody>{catalog.decision_index.models.map((model) => <tr key={model.id} className="border-t border-[#ededeb]"><th className="px-4 py-2.5 font-medium text-[#333]">{model.name}</th><td className="px-4 py-2.5 text-right font-medium text-[#2D6598]">{indexScore(model.scores.balanced_skill)}</td><td className="px-4 py-2.5 text-right">{indexScore(model.scores.balanced_raw)}</td><td className="px-4 py-2.5 text-right">{indexScore(model.scores.breadth_skill)}</td><td className="px-4 py-2.5 text-right">{percent(model.coverage)}</td></tr>)}</tbody>
          </table>
        </div>
      </section>

      <section className="border-t border-[#e5e5e3] pt-8">
        <h2 className="text-[19px] font-semibold tracking-[-0.03em] text-[#171717]">Benchmarks by domain</h2>
        <div role="tablist" aria-label="Benchmark domains" className="mt-5 flex gap-2 overflow-x-auto pb-2">
          {catalog.domains.map((item) => (
            <button key={item.id} role="tab" type="button" aria-selected={domain === item.id} onClick={() => setDomain(item.id)} className={cn("shrink-0 rounded-full border px-3 py-1.5 text-[11px] font-medium transition-colors focus-visible:outline-2 focus-visible:outline-offset-2 focus-visible:outline-[#2D6598]", domain === item.id ? "border-[#2D6598] bg-[#2D6598] text-white" : "border-[#e1e1df] bg-white text-[#666] hover:border-[#8faaba] hover:text-[#2D6598]")}>{item.name}</button>
          ))}
        </div>

        <div role="tabpanel" className="mt-6 space-y-7">
          {domain === "gtm" ? (
            <section>
              <div className="mb-3 flex items-baseline justify-between"><h3 className="text-[14px] font-semibold text-[#222]">Buying Signals</h3><a href="https://github.com/modaic-ai/mo-benchmarks/tree/main/benchmarks/gtm/buying_signals" className="text-[10px] text-[#2a6496] hover:underline">Results ↗</a></div>
              <div className="overflow-x-auto rounded-lg border border-[#e8e8e6]">
                <table className="w-full min-w-[520px] text-left text-[11px] tabular-nums">
                  <thead className="bg-[#f7f7f5] text-[#888]"><tr><th className="px-4 py-2 font-medium">Model</th><th className="px-4 py-2 text-right font-medium">Accuracy</th><th className="px-4 py-2 text-right font-medium">AUROC</th><th className="px-4 py-2 text-right font-medium">ECE ↓</th></tr></thead>
                  <tbody>{[...gtmModels].sort((a, b) => b.macro.accuracy - a.macro.accuracy).map((model) => <tr key={model.id} className="border-t border-[#ededeb]"><th className="px-4 py-2.5 font-medium text-[#333]">{gtmNames[model.id] ?? model.id}</th><td className="px-4 py-2.5 text-right">{percent(model.macro.accuracy)}</td><td className="px-4 py-2.5 text-right">{model.macro.auroc.toFixed(3)}</td><td className="px-4 py-2.5 text-right">{model.macro.ece.toFixed(3)}</td></tr>)}</tbody>
                </table>
              </div>
            </section>
          ) : (
            <>
              {domain === "finance" && (
                <section className="rounded-lg border border-[#e8e8e6] bg-[#fcfcfb] px-5 py-4">
                  <div className="flex flex-wrap items-center justify-between gap-3">
                    <div>
                      <h3 className="text-[14px] font-semibold text-[#222]">Finance alignment uplift</h3>
                      <p className="mt-1 text-[11px] text-[#777]">Held-out results before and after task-specific alignment across 12 finance benchmarks.</p>
                    </div>
                    <Link href="/finance-uplift" className="text-[11px] font-medium text-[#2a6496] hover:underline">View uplift results →</Link>
                  </div>
                </section>
              )}
              {indexByDomain.length > 0 && (
                <section>
                  <h3 className="mb-3 text-[14px] font-semibold text-[#222]">Decision Index</h3>
                  <div className="overflow-x-auto rounded-lg border border-[#e8e8e6]">
                    <table className="w-full min-w-[1180px] text-left text-[11px] tabular-nums">
                      <thead className="bg-[#f7f7f5] text-[#888]"><tr><th className="px-4 py-2 font-medium">Benchmark</th><th className="px-4 py-2 font-medium">Metric</th>{catalog.decision_index.models.map((model) => <th key={model.id} className="px-3 py-2 text-right font-medium">{model.name}</th>)}</tr></thead>
                      <tbody>{indexByDomain.map((row) => <tr key={row.id} className="border-t border-[#ededeb]"><th className="px-4 py-2.5 font-medium text-[#333]">{row.short}</th><td className="px-4 py-2.5 text-[#777]">{row.metric}</td>{catalog.decision_index.models.map((model) => { const score = model.benchmarks.find((item) => item.id === row.id); return <td key={model.id} className="px-3 py-2.5 text-right">{score ? percent(score.raw) : "—"}</td>; })}</tr>)}</tbody>
                    </table>
                  </div>
                </section>
              )}
              {evaluations.length > 0 && (
                <section>
                  <h3 className="mb-3 text-[14px] font-semibold text-[#222]">Additional evaluations</h3>
                  <div className="overflow-x-auto rounded-lg border border-[#e8e8e6]">
                    <table className="w-full min-w-[1180px] text-left text-[11px] tabular-nums">
                      <thead className="bg-[#f7f7f5] text-[#888]"><tr><th className="px-4 py-2 font-medium">Benchmark</th><th className="px-4 py-2 text-right font-medium">Rows</th>{roster.map((model) => <th key={model} className="px-3 py-2 text-right font-medium">{modelNames.get(model) ?? model}</th>)}</tr></thead>
                      <tbody>{evaluations.map(([name, rows]) => {
                        return <tr key={name} className="border-t border-[#ededeb]"><th className="px-4 py-2.5 font-medium text-[#333]">{name}</th><td className="px-4 py-2.5 text-right text-[#777]">{(rows[0]?.rows ?? 0).toLocaleString()}</td>{roster.map((model) => { const result = rows.find((row) => row.model === model); return <td key={model} className="px-3 py-2.5 text-right">{result ? percent(result.accuracy) : "—"}</td>; })}</tr>;
                      })}</tbody>
                    </table>
                  </div>
                </section>
              )}
              {indexByDomain.length === 0 && evaluations.length === 0 && <p className="rounded-lg border border-[#e8e8e6] bg-[#fcfcfb] p-5 text-[12px] text-[#777]">No published results in this domain yet.</p>}
            </>
          )}
        </div>
      </section>

      <footer className="mt-12 flex flex-wrap items-center justify-between gap-3 border-t-2 border-[#222] pt-4 text-[10px] text-[#888]">
        <p>Modaic Benchmarks · October 2026</p>
        <a href="https://github.com/modaic-ai/mo-benchmarks" target="_blank" rel="noreferrer" className="text-[#2a6496] hover:underline">Source &amp; methods ↗</a>
      </footer>
    </main>
  );
}
