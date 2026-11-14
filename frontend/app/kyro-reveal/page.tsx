import type { Metadata } from "next";

export const metadata: Metadata = {
  title: "KyroAI — 3D Logo Reveal",
  description: "KyroAI interactive 3D logo reveal animation.",
};

export default function KyroRevealPage() {
  return (
    <main style={{ minHeight: "100dvh", width: "100%", background: "#050b0a" }}>
      <iframe
        title="KyroAI 3D Logo Reveal"
        src="/kyro-reveal.html"
        style={{ display: "block", width: "100%", height: "100dvh", border: 0 }}
      />
    </main>
  );
}
