"use client";

import Image from "next/image";
import { BenchmarkBarView, ViewSwitch } from "@/components/benchmark-bar-view";
import { useEffect, useId, useMemo, useState } from "react";
import { createPortal } from "react-dom";
import benchmarkData from "@/data/benchmark-results.json";
import benchmarkLinks from "@/data/benchmark-links.json";
import buyingSignals from "@/data/buying-signals.json";
import { cn } from "@/lib/utils";

type Domain = { id: string; name: string };
type Result = { macro_exclude?: boolean; primary_score?: number; primary_metric?: string; f1?: number; family?: string; group?: string; benchmark: string; name: string; domain: string; model: string; model_name: string; rows: number; accuracy: number };
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
type BuyingModel = { id: string; macro: { f1: number; accuracy: number; auroc: number; ece: number } };

const catalog = benchmarkData as Aggregate;
const indexModel = catalog.decision_index.models.find((model) => model.id === "mo-1.3.2") ?? catalog.decision_index.models[0];
const roster = ["mo-1.3.2", "mo-1.3.1", "jev-1.14", "luna-decisions", "pplx", "mo-fast", "jev-1.13", "clef", "gpt-6.1"];
const modelOrder = (a: { id: string }, b: { id: string }) => roster.indexOf(a.id) - roster.indexOf(b.id);
const isReference = (id: string) => id === "gpt-6.1";
const indexModels = [...catalog.decision_index.models].sort(modelOrder);
const decisionModels = indexModels.filter((model) => !isReference(model.id));
const domainOrder = ["gtm", "tools", "security", "arts", "finance", "language", "retrieval", "knowledge", "safety"];
const domains = [...catalog.domains].sort((a, b) => domainOrder.indexOf(a.id) - domainOrder.indexOf(b.id));
const isModaic = (id: string) => id.startsWith("mo-");
function modaicWins(scores: Array<{ id: string; score: number }>) {
  const decisions = scores.filter((model) => !isReference(model.id));
  const best = Math.max(...decisions.map((model) => model.score));
  return decisions.some((model) => isModaic(model.id) && model.score === best);
}
function indexModaicWins(row: IndexBenchmark) {
  return modaicWins(decisionModels.flatMap((model) => {
    const result = model.benchmarks.find((item) => item.id === row.id);
    return result ? [{ id: model.id, score: result.raw }] : [];
  }));
}
const primaryScore = (row: Result) => row.primary_score ?? row.accuracy;
function evaluationModaicWins(rows: Result[]) {
  return modaicWins(rows.map((row) => ({ id: row.model, score: primaryScore(row) })));
}
const referenceName = "GPT-6.1";
const referenceColumn = "sticky right-0 z-10 w-[84px] min-w-[84px] max-w-[84px] whitespace-nowrap border-l-2 border-[#bdcbd5] bg-[#edf2f6] font-normal shadow-[-5px_0_8px_-6px_#8095a5]";
const referenceRow = "border-t-2 border-[#bdcbd5] bg-[#edf2f6]";
const modelNames = new Map(catalog.results.map((row) => [row.model, row.model_name]));
const gtmModels = (buyingSignals as { models: BuyingModel[] }).models;
const gtmNames: Record<string, string> = {
  "luna-decisions": "Luna Decisions",
  "gpt-6.1": "GPT-6.1",
  "jev-1.13": "Jev 1.13",
  "jev-1.14": "Jev 1.14",
  "mo-1.3.1": "Mo 1.3.1",
  "mo-1.3.2": "Mo 1.3.2",
  "mo-fast": "Mo Fast",
  pplx: "PPLX",
  clef: "Clef",
};

const links: Record<string, string> = benchmarkLinks;
const normalize = (name: string) => name.toLowerCase().replace(/[^a-z0-9]/g, "");
function percent(value: number) { return `${(value * 100).toFixed(1)}%`; }
function indexScore(value: number) { return value.toFixed(2); }

function MacroRow({ models, scores }: { models: string[]; scores: Array<Array<number | undefined>> }) {
  // Compare on the same benchmark cohort for every model in this table.
  const shared = scores.filter((row) => row.every((value) => value != null && Number.isFinite(value)));
  const averages = models.map((_, column) => shared.length ? shared.reduce((sum, row) => sum + row[column]!, 0) / shared.length : null);
  const best = Math.max(...averages.flatMap((value, i) => !isReference(models[i]) && value != null ? [value] : []));
  return <tfoot className="border-t-2 border-[#bdcbd5] bg-[#f2f5f7]"><tr><th scope="row" className="px-4 py-3 font-semibold text-[#333]">Macro average</th>{models.map((id, i) => <td key={id} className={cn("px-3 py-3 text-right", isReference(id) && referenceColumn, !isReference(id) && averages[i] != null && averages[i] === best && "font-bold text-[#2D6598]")}>{averages[i] == null ? "—" : percent(averages[i])}</td>)}</tr></tfoot>;
}

function BenchmarkLink({ href, name, metric, labels }: { href: string; name: string; metric: string; labels?: number }) {
  const tooltipId = useId();
  const [position, setPosition] = useState<{ left: number; top: number; above: boolean } | null>(null);
  useEffect(() => {
    if (!position) return;
    const close = () => setPosition(null);
    window.addEventListener("scroll", close, true);
    window.addEventListener("resize", close);
    return () => {
      window.removeEventListener("scroll", close, true);
      window.removeEventListener("resize", close);
    };
  }, [position]);
  function show(target: HTMLAnchorElement) {
    const rect = target.getBoundingClientRect();
    const above = window.innerHeight - rect.bottom < 130;
    setPosition({ left: Math.max(12, Math.min(rect.left, window.innerWidth - 272)), top: above ? rect.top - 10 : rect.bottom + 10, above });
  }
  return <>
    <a href={href} aria-describedby={position ? tooltipId : undefined} onMouseEnter={(event) => show(event.currentTarget)} onMouseLeave={() => setPosition(null)} onFocus={(event) => show(event.currentTarget)} onBlur={() => setPosition(null)} onKeyDown={(event) => { if (event.key === "Escape") setPosition(null); }} className="rounded-sm hover:text-[#2a6496] hover:underline focus-visible:outline-2 focus-visible:outline-offset-4 focus-visible:outline-[#2D6598]">{name} ↗</a>
    {position && createPortal(
      <div id={tooltipId} role="tooltip" style={{ left: position.left, top: position.top, transform: position.above ? "translateY(-100%)" : undefined }} className="pointer-events-none fixed z-50 w-[260px] rounded-xl border border-[#d8e1e8] bg-white p-4 text-left font-sans text-[12px] font-normal text-[#454545] shadow-[0_6px_24px_rgba(24,49,67,0.16)]">
        <p className="mb-3 font-semibold text-[#222]">{name}</p>
        <dl className="space-y-2"><div className="flex items-baseline justify-between gap-4"><dt className="text-[#777]">Metric</dt><dd className="text-right capitalize text-[#2D6598]">{metric}</dd></div><div className="flex items-baseline justify-between gap-4 border-t border-[#edf0f2] pt-2"><dt className="shrink-0 text-[#777]">Evaluation labels</dt><dd className="text-right tabular-nums">{labels == null ? "Not recorded" : labels.toLocaleString()}</dd></div></dl>
      </div>, document.body)}
  </>;
}

export function BenchmarkPage() {
  const [indexChart, setIndexChart] = useState(true);
  const [domainChart, setDomainChart] = useState(true);
  const [domain, setDomain] = useState("gtm");
  const indexByDomain = useMemo(() => indexModel.benchmarks.filter((row) => row.domain === domain).sort((a, b) => Number(indexModaicWins(b)) - Number(indexModaicWins(a))), [domain]);
  const evaluations = useMemo(() => {
    const grouped = new Map<string, Result[]>();
    const indexed = new Set(indexModel.benchmarks.flatMap((row) => [normalize(row.name), normalize(row.short)]));
    for (const result of catalog.results.filter((row) => row.domain === domain && !indexed.has(normalize(row.name)) && !(row.benchmark.startsWith("musr_") && indexed.has("musr")))) {
      grouped.set(result.name, [...(grouped.get(result.name) ?? []), result]);
    }
    return [...grouped.entries()].sort((a, b) => Number(evaluationModaicWins(b[1])) - Number(evaluationModaicWins(a[1])));
  }, [domain]);

  const securityCategories = [
    { id: "access_reviews", name: "Access review and continuation" },
    { id: "access_control_reasoning", name: "Access-Control Reasoning" },
    { id: "user_intent_guardrails", name: "User Intent Guardrails" },
  ];
  const securityRows: Array<[string, Result[]]> = securityCategories.map((category) => [category.name, roster.flatMap((model) => {
    const source = catalog.results.filter((row) => row.domain === "security" && row.group === category.id && row.model === model);
    if (!source.length) return [];
    return [{ benchmark: category.id, name: category.name, domain: "security", model, model_name: modelNames.get(model) ?? model, rows: 0, accuracy: source.reduce((sum, row) => sum + (row.accuracy ?? 0), 0) / source.length, primary_score: source.reduce((sum, row) => sum + primaryScore(row), 0) / source.length, primary_metric: category.id === "user_intent_guardrails" ? "F1 on answered rows (positive: no)" : category.id === "access_reviews" ? "accuracy" : "mean primary score" }];
  })]);
  const evaluationSections = domain === "security" ? [{ id: "security", title: undefined, href: undefined, note: undefined, macroLabel: "Overall security score", rows: securityRows }] : [{ id: domain, title: indexByDomain.length > 0 ? "Additional evaluations" : undefined, href: undefined, note: undefined, macroLabel: evaluations.some(([, rows]) => rows[0].primary_metric === "F1") ? "Macro score" : "Macro accuracy", rows: evaluations }].filter((section) => section.rows.length > 0);

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
          <div className="flex flex-wrap items-center gap-4"><h2 className="text-[16px] font-semibold tracking-[-0.02em] text-[#171717]"><a href={catalog.decision_index.source} target="_blank" rel="noreferrer" className="hover:text-[#2a6496] hover:underline">Decision Index ↗</a></h2><ViewSwitch label="Decision Index" chart={indexChart} onChange={setIndexChart} /></div>
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
        {indexChart ? <div className="mt-5"><BenchmarkBarView showBreakdown={false} models={indexModels} overview={indexModels.map((model) => model.scores.balanced_skill / 100)} overviewLabel="Balanced skill" breakdownLabel="Domain raw score" rows={indexModel.domains.map((item) => ({ name: item.id === "knowledge" ? "Academic" : item.id.charAt(0).toUpperCase() + item.id.slice(1), scores: indexModels.map((model) => model.domains.find((d) => d.id === item.id)?.raw) }))} /></div> : <>
        <div className="mt-5 overflow-x-auto rounded-lg border border-[#e8e8e6]">
          <table className="w-full min-w-[680px] text-left text-[11px] tabular-nums">
            <thead className="bg-[#f7f7f5] text-[#888]"><tr><th className="px-4 py-2 font-medium">Model</th><th className="px-4 py-2 text-right font-medium">Balanced skill</th><th className="px-4 py-2 text-right font-medium">Balanced raw</th><th className="px-4 py-2 text-right font-medium">Breadth skill</th><th className="px-4 py-2 text-right font-medium">Coverage</th></tr></thead>
            <tbody>{indexModels.map((model) => <tr key={model.id} className={cn("border-t border-[#ededeb]", isReference(model.id) && referenceRow)}><th className={cn("px-4 py-2.5 text-[#333]", isReference(model.id) ? "font-normal" : "font-medium")}>{isReference(model.id) ? referenceName : model.name}</th><td className={cn("px-4 py-2.5 text-right", !isReference(model.id) && model.scores.balanced_skill === Math.max(...decisionModels.map((m) => m.scores.balanced_skill)) && "font-bold")}>{indexScore(model.scores.balanced_skill)}</td><td className={cn("px-4 py-2.5 text-right", !isReference(model.id) && model.scores.balanced_raw === Math.max(...decisionModels.map((m) => m.scores.balanced_raw)) && "font-bold")}>{indexScore(model.scores.balanced_raw)}</td><td className={cn("px-4 py-2.5 text-right", !isReference(model.id) && model.scores.breadth_skill === Math.max(...decisionModels.map((m) => m.scores.breadth_skill)) && "font-bold")}>{indexScore(model.scores.breadth_skill)}</td><td className="px-4 py-2.5 text-right">{percent(model.coverage)}</td></tr>)}</tbody>
            <tfoot className="border-t-2 border-[#bdcbd5] bg-[#f2f5f7]"><tr><th className="px-4 py-3 font-semibold">Best balanced skill</th><td colSpan={4} className="px-4 py-3 text-right font-bold text-[#2D6598]">{decisionModels.filter((model) => model.scores.balanced_skill === Math.max(...decisionModels.map((m) => m.scores.balanced_skill))).map((model) => `${model.name} · ${indexScore(model.scores.balanced_skill)}`).join(" / ")}</td></tr></tfoot>
          </table>
        </div>
        </>}
      </section>

      <section className="border-t border-[#e5e5e3] pt-8">
        <div className="flex flex-wrap items-center gap-4"><h2 className="text-[19px] font-semibold tracking-[-0.03em] text-[#171717]">Benchmarks by domain</h2><ViewSwitch label="Benchmarks by domain" chart={domainChart} onChange={setDomainChart} /></div>
        <div role="tablist" aria-label="Benchmark domains" className="mt-5 flex gap-2 overflow-x-auto pb-2">
          {domains.map((item) => (
            <button key={item.id} role="tab" type="button" aria-selected={domain === item.id} onClick={() => setDomain(item.id)} className={cn("shrink-0 rounded-full border px-3 py-1.5 text-[11px] font-medium transition-colors focus-visible:outline-2 focus-visible:outline-offset-2 focus-visible:outline-[#2D6598]", domain === item.id ? "border-[#2D6598] bg-[#2D6598] text-white" : "border-[#e1e1df] bg-white text-[#666] hover:border-[#8faaba] hover:text-[#2D6598]")}>{item.id === "knowledge" ? "Academic" : item.name}</button>
          ))}
        </div>

        <div role="tabpanel" className="mt-6 space-y-7">
          {domain === "gtm" ? (
            <section>
              <div className="mb-3 flex items-baseline justify-between"><h3 className="text-[14px] font-semibold text-[#222]"><a href={links.buying_signals} className="hover:underline">Buying Signals ↗</a></h3><a href="https://github.com/modaic-ai/mo-benchmarks/tree/main/benchmarks/gtm/buying_signals" className="text-[10px] text-[#2a6496] hover:underline">Results ↗</a></div>
              {domainChart ? <BenchmarkBarView overviewLabel="Macro accuracy" models={[...gtmModels].sort(modelOrder).map((model) => ({ id: model.id, name: gtmNames[model.id] ?? model.id }))} rows={[{ name: "Buying Signals", metric: "accuracy", scores: [...gtmModels].sort(modelOrder).map((model) => model.macro.accuracy) }]} /> : <>
              <div className="overflow-x-auto rounded-lg border border-[#e8e8e6]">
                <table className="w-full min-w-[520px] text-left text-[11px] tabular-nums">
                  <thead className="bg-[#f7f7f5] text-[#888]"><tr><th className="px-4 py-2 font-medium">Model</th><th className="px-4 py-2 text-right font-medium">Accuracy</th><th className="px-4 py-2 text-right font-medium">AUROC</th><th className="px-4 py-2 text-right font-medium">ECE ↓</th></tr></thead>
                  <tbody>{[...gtmModels].sort(modelOrder).map((model) => <tr key={model.id} className={cn("border-t border-[#ededeb]", isReference(model.id) && referenceRow)}><th className={cn("px-4 py-2.5 text-[#333]", isReference(model.id) ? "font-normal" : "font-medium")}>{gtmNames[model.id] ?? model.id}</th><td className={cn("px-4 py-2.5 text-right", !isReference(model.id) && model.macro.accuracy === Math.max(...gtmModels.filter((m) => !isReference(m.id)).map((m) => m.macro.accuracy)) && "font-bold")}>{percent(model.macro.accuracy)}</td><td className={cn("px-4 py-2.5 text-right", !isReference(model.id) && model.macro.auroc === Math.max(...gtmModels.filter((m) => !isReference(m.id)).map((m) => m.macro.auroc)) && "font-bold")}>{model.macro.auroc.toFixed(3)}</td><td className={cn("px-4 py-2.5 text-right", !isReference(model.id) && model.macro.ece === Math.min(...gtmModels.filter((m) => !isReference(m.id)).map((m) => m.macro.ece)) && "font-bold")}>{model.macro.ece.toFixed(3)}</td></tr>)}</tbody>
                  <tfoot className="border-t-2 border-[#bdcbd5] bg-[#f2f5f7]"><tr><th className="px-4 py-3 font-semibold">Best macro accuracy</th><td colSpan={3} className="px-4 py-3 text-right font-bold text-[#2D6598]">{gtmModels.filter((model) => !isReference(model.id) && model.macro.accuracy === Math.max(...gtmModels.filter((m) => !isReference(m.id)).map((m) => m.macro.accuracy))).map((model) => `${gtmNames[model.id]} · ${percent(model.macro.accuracy)}`).join(" / ")}</td></tr></tfoot>
                </table>
              </div>
              </>}
            </section>
          ) : (
            <>
              {indexByDomain.length > 0 && (
                <section>
                  <h3 className="mb-3 text-[14px] font-semibold text-[#222]"><a href={catalog.decision_index.source} className="hover:underline">Decision Index ↗</a></h3>
                  {domainChart ? <BenchmarkBarView key={`index-${domain}`} models={indexModels} overviewLabel="Macro raw score" rows={indexByDomain.map((row) => ({ name: row.short, metric: row.metric, scores: indexModels.map((model) => model.benchmarks.find((item) => item.id === row.id)?.raw) }))} /> : <>
                  <div className="overflow-x-auto rounded-lg border border-[#e8e8e6]">
                    <table className="w-full min-w-[1180px] text-left text-[11px] tabular-nums">
                      <thead className="bg-[#f7f7f5] text-[#888]"><tr><th className="px-4 py-2 font-medium">Benchmark</th>{indexModels.map((model) => <th key={model.id} className={cn("px-3 py-2 text-right font-medium", isReference(model.id) && referenceColumn)}>{isReference(model.id) ? referenceName : model.name}</th>)}</tr></thead>
                      <tbody>{indexByDomain.map((row) => <tr key={row.id} className="border-t border-[#ededeb]"><th className="px-4 py-2.5 font-medium text-[#333]"><BenchmarkLink href={links[row.name]} name={row.short} metric={row.metric} /></th>{indexModels.map((model) => { const score = model.benchmarks.find((item) => item.id === row.id); return <td key={model.id} className={cn("px-3 py-2.5 text-right", isReference(model.id) && referenceColumn, !isReference(model.id) && score && score.raw === Math.max(...decisionModels.flatMap((m) => m.benchmarks.filter((b) => b.id === row.id).map((b) => b.raw))) && "font-bold")}>{score ? percent(score.raw) : "—"}</td>; })}</tr>)}</tbody>
                      <MacroRow models={indexModels.map((model) => model.id)} scores={indexByDomain.map((row) => indexModels.map((model) => model.benchmarks.find((item) => item.id === row.id)?.raw))} />
                    </table>
                  </div>
                  </>}
                </section>
              )}
              {evaluationSections.map((section) => (
                <section key={section.id}>
                  {section.title && <h3 className="mb-3 text-[14px] font-semibold text-[#222]">{section.href ? <a href={section.href} className="hover:underline">{section.title} ↗</a> : section.title}</h3>}{section.note && <p className="mb-4 text-[11px] leading-5 text-[#777]">{section.note}</p>}
                  {domainChart ? <BenchmarkBarView key={`evaluations-${domain}-${section.id}`} breakdownLabel={domain === "security" ? "Security category" : "Benchmark breakdown"} overviewLabel={section.macroLabel} models={roster.map((id) => ({ id, name: modelNames.get(id) ?? id }))} rows={section.rows.map(([name, rows]) => ({ name, includeInMacro: !rows[0].macro_exclude, metric: rows[0].primary_metric ?? "accuracy", scores: roster.map((model) => { const result = rows.find((row) => row.model === model); return result ? primaryScore(result) : undefined; }) }))} /> : <>
                  <div className="overflow-x-auto rounded-lg border border-[#e8e8e6]">
                    <table className="w-full min-w-[1180px] text-left text-[11px] tabular-nums">
                      <thead className="bg-[#f7f7f5] text-[#888]"><tr><th className="px-4 py-2 font-medium">Benchmark</th>{roster.map((model) => <th key={model} className={cn("px-3 py-2 text-right font-medium", isReference(model) && referenceColumn)}>{isReference(model) ? referenceName : (modelNames.get(model) ?? model)}</th>)}</tr></thead>
                      <tbody>{section.rows.map(([name, rows]) => {
                        return <tr key={name} className="border-t border-[#ededeb]"><th className="px-4 py-2.5 font-medium text-[#333]"><BenchmarkLink href={rows[0].benchmark === "access_reviews" ? "/benchmarks/policy-conditioned-access-review" : rows[0].benchmark === "access_control_reasoning" ? "/benchmarks/access-control-reasoning" : rows[0].benchmark === "user_intent_guardrails" ? "/benchmarks/user-intent-guardrails" : links[rows[0].benchmark]} name={name} metric={rows[0].macro_exclude ? "F1 on the Noul subset; excluded from the macro to avoid counting overlapping examples twice" : rows[0].primary_metric ?? "accuracy"} labels={rows[0].rows || undefined} /></th>{roster.map((model) => { const result = rows.find((row) => row.model === model); return <td key={model} className={cn("px-3 py-2.5 text-right", isReference(model) && referenceColumn, !isReference(model) && result && primaryScore(result) === Math.max(...rows.filter((r) => !isReference(r.model)).map(primaryScore)) && "font-bold")}>{result ? percent(primaryScore(result)) : "—"}</td>; })}</tr>;
                      })}</tbody>
                      <MacroRow models={roster} scores={section.rows.filter(([, rows]) => !rows[0].macro_exclude).map(([, rows]) => roster.map((model) => { const result = rows.find((row) => row.model === model); return result ? primaryScore(result) : undefined; }))} />
                    </table>
                  </div>
                  </>}
                </section>
              ))}
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
