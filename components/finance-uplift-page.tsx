"use client";

import Image from "next/image";
import Link from "next/link";
import { Bar, BarChart, CartesianGrid, XAxis, YAxis } from "recharts";
import { ChartContainer, ChartTooltip, ChartTooltipContent, type ChartConfig } from "@/components/ui/chart";
import rawData from "@/data/finance-uplift.json";

type TaskResult = {
  slug: string;
  label: string;
  chartLabel?: string;
  dataset: string;
  evaluationSplit: string;
  n: number;
  training_labels: number;
  baseline_accuracy: number;
  aligned_accuracy: number | null;
  alignment_outcome?: "new_checkpoint" | "no_new_checkpoint";
  label_only_accuracy?: number;
  ground_reasoning_count?: number;
  uplift_pp: number | null;
  uplift_95pct_bootstrap_ci_pp: number[] | null;
  fixed_to_correct: number;
  regressed_to_wrong: number;
};

const data = rawData as { tasks: TaskResult[] };
const chartConfig = {
  baseline: { label: "Mo 1.3.1", color: "#9BAAB7" },
  labelOnly: { label: "Labels only", color: "#6899BC" },
  aligned: { label: "With reasoning", color: "#2D6598" },
} satisfies ChartConfig;

const percent = (value: number) => `${(value * 100).toFixed(1)}%`;
const points = (value: number) => `${value > 0 ? "+" : ""}${value.toFixed(1)} pp`;

export function FinanceUpliftPage() {
  const chartData = data.tasks.map((task) => ({
    name: task.chartLabel ?? task.label,
    baseline: task.baseline_accuracy,
    labelOnly: task.alignment_outcome === "no_new_checkpoint" ? null : (task.label_only_accuracy ?? task.aligned_accuracy),
    aligned: task.label_only_accuracy == null ? null : task.aligned_accuracy,
  }));
  const minimum = Math.floor(Math.min(...data.tasks.flatMap((task) => [task.baseline_accuracy, task.label_only_accuracy, task.aligned_accuracy].filter((value): value is number => value != null))) * 10) / 10;

  return (
    <main className="mx-auto max-w-[1120px] px-5 pb-14 pt-6 font-sans text-[#454545] sm:px-10 sm:pt-8">
      <header className="flex flex-wrap items-center justify-between gap-4 border-b border-[#e5e5e3] pb-5">
        <Link href="/" className="flex items-center gap-2.5 text-[15px] font-semibold tracking-[-0.02em] text-[#171717]">
          <Image src="/mo-logo.png" alt="Modaic" width={697} height={629} className="h-auto w-7 shrink-0 [image-rendering:pixelated]" priority />
          <span>Benchmarks</span>
        </Link>
        <nav aria-label="Benchmarks" className="flex items-center gap-5 text-[11px]">
          <Link href="/" className="text-[#777] hover:text-[#2a6496]">All benchmarks</Link>
          <span aria-current="page" className="font-medium text-[#2a6496]">Finance uplift</span>
          <a href="https://github.com/modaic-ai/mo-benchmarks" target="_blank" rel="noreferrer" className="text-[#2a6496] hover:underline">GitHub ↗</a>
        </nav>
      </header>

      <section className="border-b border-[#e5e5e3] py-8 sm:py-10">
        <p className="text-[10px] font-medium uppercase tracking-[0.12em] text-[#777]">Finance · alignment pilot</p>
        <h1 className="mt-2 text-[20px] font-semibold tracking-[-0.03em] text-[#171717]">What does alignment change?</h1>
        <p className="mt-3 max-w-[680px] text-[13px] leading-[1.65] text-[#696969]">
          We start with Mo 1.3.1, label up to 200 training decisions per task, and align a custom model. When alignment produces a new checkpoint, we test it on the same 200 held-out examples. For Banking77, we also add reviewed ground reasoning to the same training examples and measure a second alignment.
        </p>
      </section>

      <section className="pt-9 sm:pt-11">
        <h2 className="text-[19px] font-semibold tracking-[-0.03em] text-[#171717]">Held-out accuracy</h2>
        <p className="mt-1 text-[11px] text-[#888]">Mo 1.3.1 and aligned custom models · same 200 held-out rows per task</p>
        <div className="mt-6 rounded-lg border border-[#e8e8e6] bg-[#fcfcfb] px-3 pb-3 pt-6 sm:px-6">
          <div className="overflow-x-auto">
            <ChartContainer config={chartConfig} className="h-[350px] min-w-[900px] w-full aspect-auto">
              <BarChart accessibilityLayer data={chartData} margin={{ top: 20, right: 12, bottom: 5, left: -8 }}>
                <CartesianGrid vertical={false} stroke="#e7e9e9" />
                <XAxis dataKey="name" tickLine={false} axisLine={false} tick={{ fill: "#666", fontSize: 11 }} tickMargin={12} />
                <YAxis type="number" domain={[minimum, 1]} ticks={Array.from({ length: Math.round((1 - minimum) * 10) + 1 }, (_, i) => Number((minimum + i * 0.1).toFixed(1)))} tickFormatter={(value: number) => `${Math.round(value * 100)}%`} tickLine={false} axisLine={false} tick={{ fill: "#999", fontSize: 10 }} />
                <ChartTooltip cursor={{ fill: "#edf1f2" }} content={<ChartTooltipContent formatter={(value) => <span className="font-mono text-[#222]">{percent(Number(value))}</span>} />} />
                <Bar dataKey="baseline" fill="var(--color-baseline)" radius={[3, 3, 0, 0]} maxBarSize={62} />
                <Bar dataKey="labelOnly" fill="var(--color-labelOnly)" radius={[3, 3, 0, 0]} maxBarSize={62} />
                <Bar dataKey="aligned" fill="var(--color-aligned)" radius={[3, 3, 0, 0]} maxBarSize={62} />
              </BarChart>
            </ChartContainer>
          </div>
          <div className="mt-2 flex flex-wrap justify-center gap-6 text-[11px] text-[#666]">
            <span><i className="mr-2 inline-block size-2.5 rounded-[2px] bg-[#9BAAB7]" />Mo 1.3.1</span>
            <span><i className="mr-2 inline-block size-2.5 rounded-[2px] bg-[#6899BC]" />Labels only</span>
            <span><i className="mr-2 inline-block size-2.5 rounded-[2px] bg-[#2D6598]" />With reasoning (Banking77)</span>
          </div>
        </div>
      </section>

      <section className="mt-9 border-t border-[#e5e5e3] pt-4">
        <h2 className="text-[12px] font-medium text-[#333]">Full results</h2>
        <div className="mt-4 overflow-x-auto">
          <table className="w-full min-w-[760px] border-collapse text-left text-[11px] tabular-nums">
            <thead className="text-[#888]"><tr className="border-b border-[#dededc]">
              <th scope="col" className="py-2 pr-4 font-medium">Task</th>
              <th scope="col" className="px-2 py-2 text-right font-medium">Mo 1.3.1</th>
              <th scope="col" className="px-2 py-2 text-right font-medium">Labels only</th>
              <th scope="col" className="px-2 py-2 text-right font-medium">With reasoning</th>
              <th scope="col" className="px-2 py-2 text-right font-medium">Uplift</th>
              <th scope="col" className="px-2 py-2 text-right font-medium">95% interval</th>
              <th scope="col" className="pl-2 py-2 text-right font-medium">Labels</th>
            </tr></thead>
            <tbody>{data.tasks.map((task) => (
              <tr key={task.slug} className="border-b border-[#ededeb]">
                <th scope="row" className="py-3 pr-4 font-medium text-[#333]"><a href={`https://huggingface.co/datasets/${task.dataset}`} target="_blank" rel="noreferrer" className="hover:text-[#2a6496] hover:underline">{task.label} ↗</a></th>
                <td className="px-2 py-3 text-right text-[#666]">{percent(task.baseline_accuracy)}</td>
                <td className="px-2 py-3 text-right text-[#666]">{task.alignment_outcome === "no_new_checkpoint" ? "No checkpoint" : percent((task.label_only_accuracy ?? task.aligned_accuracy)!)}</td>
                <td className="px-2 py-3 text-right text-[#666]">{task.label_only_accuracy == null ? "—" : percent(task.aligned_accuracy!)}</td>
                <td className={`px-2 py-3 text-right font-semibold ${(task.uplift_pp ?? 0) > 0 ? "text-[#2D6598]" : "text-[#666]"}`}>{task.uplift_pp == null ? "—" : points(task.uplift_pp)}</td>
                <td className="px-2 py-3 text-right text-[#666]">{task.uplift_95pct_bootstrap_ci_pp?.map((x) => points(x)).join(" to ") ?? "—"}</td>
                <td className="pl-2 py-3 text-right text-[#666]">{task.training_labels}</td>
              </tr>
            ))}</tbody>
          </table>
        </div>
      </section>

      <section className="mt-5 border-t border-[#e5e5e3] pt-4">
        <details className="group">
          <summary className="flex cursor-pointer list-none items-center justify-between gap-4 text-[12px] font-medium text-[#333] marker:hidden">Methodology <span className="text-[17px] font-normal text-[#999] group-open:rotate-45">+</span></summary>
          <div className="mt-4 max-w-[780px] space-y-3 text-[11px] leading-[1.65] text-[#666]">
            <p>MultiFin and Twitter financial-news topics use published validation splits; the other completed tasks use test splits. Each has its own 200-row cohort. We excluded training text found anywhere in the full evaluation split. CFPB required additional near-copy filtering. For ESG, we used the original English FinNLP training release with the same 33 labels as the Flare test set and excluded one similar test article before scoring.</p>
            <p>Training calls used capture so Modaic created the examples. Their source labels were attached as the calls completed. For Banking77, a second alignment added curated reasoning to 167 of the same 200 examples. We left 33 labels without reasoning because their utterances did not support a defensible explanation. These rationales are derived from the taxonomy and training text, not supplied by the dataset.</p>
            <p>NumClaim labels began with weak supervision. The sentiment task uses only human or human-aggregated labels and reports accuracy by source in the results file. SENTiVENT is a derived binary task: a sentence is positive when it contains an expert-annotated economic event. It does not measure full event extraction.</p>
            <p>The held-out calls did not capture. We waited for each alignment and its automatic example batch to finish before scoring the corresponding checkpoint. If alignment produced no new checkpoint, the table marks that outcome without treating a rerun of the base model as uplift.</p>
            <p>Uplift is the aligned accuracy minus base accuracy on the same 200 rows. Intervals use paired bootstrap resampling; SENTiVENT resamples its 30 source articles because multiple sentences come from each article. These small public cohorts may overlap a foundation model&apos;s pretraining data; the results describe this pilot, not production performance.</p>
            <p><a href="https://github.com/modaic-ai/mo-benchmarks/tree/main/benchmarks/finance/finance_uplift" target="_blank" rel="noreferrer" className="text-[#2a6496] underline">Read the protocol and run it yourself ↗</a></p>
          </div>
        </details>
      </section>

      <footer className="mt-12 flex flex-wrap items-center justify-between gap-3 border-t-2 border-[#222] pt-4 text-[10px] text-[#888]">
        <p>Modaic Benchmarks · October 2026</p>
        <a href="https://github.com/modaic-ai/mo-benchmarks" target="_blank" rel="noreferrer" className="text-[#2a6496] hover:underline">Source &amp; methods ↗</a>
      </footer>
    </main>
  );
}
