import type { Metadata } from "next";
import "./globals.css";

export const metadata: Metadata = {
  title: "KyroAI — Hardware & Desk Setup Prototypes",
  description: "Discover minimalist desk gear currently in prototyping. Join the waitlist for early access.",
};

export default function RootLayout({
  children,
}: {
  children: React.ReactNode;
}) {
  return (
    <html lang="en" className="dark h-full antialiased">
      <body className="min-h-full flex flex-col bg-neutral-950 text-neutral-100 selection:bg-emerald-500 selection:text-black">
        {children}
      </body>
    </html>
  );
}
