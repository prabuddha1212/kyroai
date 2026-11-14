import React from "react";

interface BadgeProps {
  children: React.ReactNode;
  variant?: "primary" | "secondary";
  className?: string;
}

export function Badge({ children, variant = "primary", className = "" }: BadgeProps) {
  if (variant === "primary") {
    return (
      <span className={`text-[10px] font-bold uppercase tracking-wider px-2 py-0.5 rounded-md bg-emerald-500 text-black shadow-sm ${className}`}>
        {children}
      </span>
    );
  }

  return (
    <span className={`text-[10px] uppercase tracking-wider px-2 py-0.5 rounded-md bg-neutral-950/80 text-neutral-300 border border-neutral-700/60 backdrop-blur-sm ${className}`}>
      {children}
    </span>
  );
}
