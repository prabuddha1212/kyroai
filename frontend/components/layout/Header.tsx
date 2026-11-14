"use client";

import React from "react";
import Link from "next/link";
import { KyroLogo } from "./KyroLogo";
import { API_BASE_URL } from "@/lib/constants";

export function Header() {
  return (
    <header className="border-b border-neutral-800/80 bg-neutral-950/80 backdrop-blur sticky top-0 z-30">
      <div className="max-w-7xl mx-auto px-4 sm:px-6 py-4 flex items-center justify-between">
        <Link href="/" className="flex items-center gap-3.5 group">
          <KyroLogo size={52} />
          <div>
            <span className="font-extrabold text-2xl tracking-tight text-white group-hover:text-emerald-400 transition-colors">
              Kyro<span className="text-emerald-400">AI</span>
            </span>
            <span className="ml-2 text-[10px] px-2 py-0.5 rounded-full bg-emerald-950/80 text-emerald-400 border border-emerald-800/80 font-medium tracking-wide uppercase align-middle">
              MVP Prototype
            </span>
          </div>
        </Link>

        <div className="flex items-center gap-2.5">
          <Link
            href="/storelab-3d"
            className="text-xs font-semibold text-emerald-400 hover:text-emerald-300 bg-emerald-950/80 hover:bg-emerald-900/60 border border-emerald-700/60 hover:border-emerald-500 px-3 py-1.5 rounded-lg flex items-center gap-1.5 transition-all shadow-sm shadow-emerald-500/10"
          >
            <span>View in 3D ✨</span>
          </Link>

          <Link
            href="/dashboard"
            className="text-xs font-medium text-neutral-400 hover:text-white transition-colors border border-neutral-800 hover:border-neutral-700 px-3 py-1.5 rounded-lg flex items-center gap-1.5"
          >
            <svg className="w-3.5 h-3.5 text-neutral-400" fill="none" viewBox="0 0 24 24" stroke="currentColor">
              <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M9 19v-6a2 2 0 00-2-2H5a2 2 0 00-2 2v6a2 2 0 002 2h2a2 2 0 002-2zm0 0V9a2 2 0 012-2h2a2 2 0 012 2v10m-6 0a2 2 0 002 2h2a2 2 0 002-2m0 0V5a2 2 0 012-2h2a2 2 0 012 2v14a2 2 0 01-2 2h-2a2 2 0 01-2-2z" />
            </svg>
            <span>Owner Dashboard</span>
          </Link>

          <a
            href={`${API_BASE_URL}/docs`}
            target="_blank"
            rel="noopener noreferrer"
            className="hidden sm:inline-flex text-xs font-medium text-neutral-400 hover:text-white transition-colors border border-neutral-800 hover:border-neutral-700 px-3 py-1.5 rounded-lg"
          >
            API Docs ↗
          </a>
        </div>
      </div>
    </header>
  );
}
