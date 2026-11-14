"use client";

import React from "react";
import Link from "next/link";
import { KyroLogo } from "./KyroLogo";

interface FooterProps {
  onPrivacyClick: () => void;
}

export function Footer({ onPrivacyClick }: FooterProps) {
  return (
    <footer className="border-t border-neutral-900 py-6 text-center text-xs text-neutral-500 flex flex-col sm:flex-row items-center justify-center gap-4">
      <span className="flex items-center gap-2">
        <KyroLogo size={18} />
        KyroAI • Next.js 16 + FastAPI + Supabase
      </span>
      <span className="hidden sm:inline">•</span>
      <a href="/kyro-reveal.html" target="_blank" rel="noopener noreferrer" className="text-emerald-400 hover:text-emerald-300 underline font-medium">
        3D Logo Reveal ↗
      </a>
      <span className="hidden sm:inline">•</span>
      <Link href="/storelab-3d" className="text-emerald-400 hover:text-emerald-300 underline font-medium">
        3D Studio
      </Link>
      <span className="hidden sm:inline">•</span>
      <Link href="/dashboard" className="text-neutral-400 hover:text-neutral-200 underline">
        Owner Portal
      </Link>
      <span className="hidden sm:inline">•</span>
      <button
        onClick={onPrivacyClick}
        type="button"
        className="text-neutral-400 hover:text-neutral-200 underline cursor-pointer"
      >
        Privacy Policy
      </button>
    </footer>
  );
}
