import React from "react";

export function ProductCardSkeleton() {
  return (
    <div className="rounded-2xl border border-neutral-800 bg-neutral-900/40 p-5 space-y-4 animate-pulse">
      <div className="h-44 bg-neutral-800 rounded-xl w-full" />
      <div className="h-4 bg-neutral-800 rounded w-1/3" />
      <div className="h-6 bg-neutral-800 rounded w-3/4" />
      <div className="h-12 bg-neutral-800/60 rounded" />
      <div className="h-10 bg-neutral-800 rounded-xl w-full pt-4" />
    </div>
  );
}
