import type { Metadata } from "next";

export const metadata: Metadata = {
  title: "StoreLab 3D — Interactive Product Studio",
  description: "Rotate and inspect upcoming desk setup gear in real-time 3D.",
};

/**
 * StoreLab 3D prototype wrapper.
 * Route: /storelab-3d
 * The 3D scene is loaded from public/storelab-3d.html.
 */
export default function StoreLab3DPage() {
  return (
    <main style={{ minHeight: "100dvh", width: "100%", background: "#07090a" }}>
      <iframe
        title="StoreLab 3D interactive product showcase"
        src="/storelab-3d.html"
        style={{ display: "block", width: "100%", height: "100dvh", border: 0 }}
      />
    </main>
  );
}

