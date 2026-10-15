import type { Metadata } from "next";
import { FinanceUpliftPage } from "@/components/finance-uplift-page";

export const metadata: Metadata = {
  title: "Finance alignment uplift · Modaic Benchmarks",
  description: "Held-out accuracy before and after task-specific alignment across 12 finance benchmarks.",
};

export default function FinanceUpliftRoute() {
  return <FinanceUpliftPage />;
}
