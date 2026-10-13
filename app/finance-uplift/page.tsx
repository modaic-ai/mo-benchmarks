import type { Metadata } from "next";
import { FinanceUpliftPage } from "@/components/finance-uplift-page";

export const metadata: Metadata = {
  title: "Modaic Benchmarks — Finance alignment uplift",
  description: "Measure how Modaic alignment changes Mo's accuracy on held-out finance classification tasks.",
};

export default function FinancePage() {
  return <FinanceUpliftPage />;
}
