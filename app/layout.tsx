import type { Metadata } from "next";
import "./fonts.css";
import "./globals.css";

export const metadata: Metadata = {
  title: "Modaic Benchmarks — Buying signal detection",
  description: "A test-only comparison of seven decision models on Gong Call Playbook buying signals.",
  openGraph: {
    title: "Modaic Benchmarks — Buying signal detection",
    description: "Five buying signals. Seven models. 1,000 test decisions per model.",
    type: "website",
  },
};

export default function RootLayout({ children }: Readonly<{ children: React.ReactNode }>) {
  return (
    <html lang="en">
      <body>{children}</body>
    </html>
  );
}
