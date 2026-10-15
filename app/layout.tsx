import type { Metadata } from "next";
import "./fonts.css";
import "./globals.css";

export const metadata: Metadata = {
  title: "Modaic Benchmarks",
  description: "Decision-model evaluations across knowledge, language, retrieval, tools, arts, finance, security, and GTM.",
  openGraph: {
    title: "Modaic Benchmarks",
    description: "Decision-model evaluations and benchmark-by-benchmark results.",
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
