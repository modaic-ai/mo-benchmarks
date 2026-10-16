"use client";

import { useId, useState } from "react";
import { cn } from "@/lib/utils";

type Model = { id: string; name: string };
export type ChartRow = { name: string; metric?: string; includeInMacro?: boolean; scores: Array<number | undefined> };
const modelColors: Record<string, string> = {
  "mo-1.3.2": "#cc5d66",
  "mo-1.3.1": "#cc5d66",
  "mo-fast": "#cc5d66",
  "jev-1.14": "#e04db5",
  "jev-1.13": "#e04db5",
  "pplx": "#176e7f",
  "clef": "#f28119",
  "luna-decisions": "#000000",
  "gpt-6.1": "#b5c1cb",
};
const reference = (id: string) => id === "gpt-6.1";

export function ViewSwitch({ chart, onChange, label }: { chart: boolean; onChange: (chart: boolean) => void; label: string }) {
  return <div role="group" aria-label={`${label} view`} className="inline-flex shrink-0 rounded-lg border border-[#dededb] bg-[#f5f5f3] p-0.5 text-[11px]">
    {[true, false].map((value) => <button key={String(value)} type="button" aria-pressed={chart === value} onClick={() => onChange(value)} className={cn("rounded-md px-3 py-1.5 transition-colors focus-visible:outline-2 focus-visible:outline-[#2D6598]", chart === value ? "bg-white font-medium text-[#222] shadow-sm" : "text-[#777] hover:text-[#222]")}>{value ? "Chart" : "Table"}</button>)}
  </div>;
}

function Bars({ models, scores, label, metric = "accuracy" }: { models: Model[]; scores: Array<number | undefined>; label: string; metric?: string }) {
  const metricLabel = /f1/i.test(metric) ? "F1" : /ndcg/i.test(metric) ? "nDCG@10" : /accuracy/i.test(metric) ? "Acc" : /skill/i.test(metric) ? "Skill" : "Score";
  const available = scores.filter((score): score is number => score != null && Number.isFinite(score));
  const minimum = available.length > 0 && Math.min(...available) > 0.4 ? 0.4 : 0;
  const best = Math.max(...scores.flatMap((score, i) => !reference(models[i].id) && score != null ? [score] : []));
  return <div role="img" aria-label={`${label}. Metric: ${metric}. Axis starts at ${minimum * 100}%.`} className="space-y-2.5">
    <div className="grid grid-cols-[100px_minmax(0,1fr)_48px] gap-3 text-[10px] font-medium text-[#777]"><span /><span /><span title={metric} aria-label={metric} className="text-right">{metricLabel}</span></div>
    {models.map((model, i) => ({ model, score: scores[i] })).sort((a, b) => Number(reference(a.model.id)) - Number(reference(b.model.id)) || (b.score ?? -Infinity) - (a.score ?? -Infinity)).map(({ model, score }) => {
      const winner = !reference(model.id) && score != null && score === best;
      return <div key={model.id} className={cn("grid grid-cols-[100px_minmax(0,1fr)_48px] items-center gap-3 text-[11px]", reference(model.id) && "mt-4 border-t border-[#cbd5dc] bg-[#edf2f6] py-2") }>
        <span className={cn("truncate", winner && "font-bold text-[#2D6598]")}>{model.name}</span>
        <div className="h-4 overflow-hidden rounded-sm bg-[#edf0f1]"><div className="h-full rounded-sm transition-[width] duration-300 motion-reduce:transition-none" style={{ width: `${Math.max(0, Math.min(100, ((score ?? 0) - minimum) / (1 - minimum) * 100))}%`, background: modelColors[model.id] ?? "#b6c4cf" }} /></div>
        <span className={cn("text-right tabular-nums", winner && "font-bold text-[#2D6598]")}>{score == null ? "—" : `${(score * 100).toFixed(1)}%`}</span>
      </div>;
    })}
    <div className="ml-[112px] mr-[60px] flex justify-between border-t border-[#ddd] pt-1 text-[9px] text-[#999]"><span>{minimum * 100}%</span><span>{(minimum + (1 - minimum) / 2) * 100}%</span><span>100%</span></div>
  </div>;
}

export function BenchmarkBarView({ models, rows, overview, overviewLabel = "Macro accuracy", breakdownLabel = "Benchmark breakdown", showBreakdown = true }: { models: Model[]; rows: ChartRow[]; overview?: Array<number | undefined>; overviewLabel?: string; breakdownLabel?: string; showBreakdown?: boolean }) {
  const [selected, setSelected] = useState(0);
  const selectId = useId();
  const shared = rows.filter((row) => row.includeInMacro !== false && row.scores.every((score) => score != null && Number.isFinite(score)));
  const macro = overview ?? models.map((_, i) => shared.length ? shared.reduce((sum, row) => sum + row.scores[i]!, 0) / shared.length : undefined);
  const best = Math.max(...macro.flatMap((score, i) => !reference(models[i].id) && score != null ? [score] : []));
  const leaders = models.filter((model, i) => !reference(model.id) && macro[i] === best).map((model) => model.name);
  const row = rows[selected] ?? rows[0];
  return <div className={cn("grid gap-5", showBreakdown && rows.length > 1 && "lg:grid-cols-2")}>
    <section className="rounded-xl border border-[#dce4ea] bg-[#fafcfd] p-5">
      <div className="mb-5"><h3 className="text-[13px] font-semibold text-[#222]">{overviewLabel}</h3><p className="mt-1 text-[11px] text-[#2D6598]">{leaders.length ? `${leaders.join(" / ")} leads decision models` : "No shared results available"}</p></div>
      <Bars models={models} scores={macro} label={overviewLabel} metric={overviewLabel.toLowerCase().includes("skill") ? "balanced skill" : overviewLabel.toLowerCase().includes("f1") ? "F1" : /raw|score/i.test(overviewLabel) ? "mean primary metric score" : "accuracy"} />
    </section>
    {showBreakdown && row && rows.length > 1 && <section className="rounded-xl border border-[#e5e5e3] p-5">
      <div className="mb-5"><label htmlFor={selectId} className="block text-[13px] font-semibold text-[#222]">{breakdownLabel}</label><select id={selectId} value={Math.min(selected, rows.length - 1)} onChange={(event) => setSelected(Number(event.target.value))} className="mt-2 w-full rounded-md border border-[#dededb] bg-white px-2 py-1 text-[11px] text-[#555] focus:outline-[#2D6598]">{rows.map((item, i) => <option key={item.name} value={i}>{item.name}</option>)}</select></div>
      <Bars models={models} scores={row.scores} label={row.name} metric={row.metric ?? "accuracy"} />
    </section>}
  </div>;
}
