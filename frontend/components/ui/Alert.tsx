"use client";

import React from "react";
import { FeedbackState } from "@/lib/types";

interface AlertProps {
  feedback: FeedbackState | null;
  onDismiss: () => void;
}

export function Alert({ feedback, onDismiss }: AlertProps) {
  if (!feedback) return null;

  const isSuccess = feedback.type === "success";
  const isError = feedback.type === "error";

  return (
    <div
      role="alert"
      className={`max-w-2xl mx-auto w-full p-4 rounded-xl border text-sm flex items-center justify-between transition-all ${
        isSuccess
          ? "bg-emerald-950/70 border-emerald-600/80 text-emerald-200"
          : isError
          ? "bg-rose-950/70 border-rose-600/80 text-rose-200"
          : "bg-blue-950/70 border-blue-600/80 text-blue-200"
      }`}
    >
      <div className="flex items-center gap-3">
        {isSuccess ? (
          <svg className="w-5 h-5 text-emerald-400 shrink-0" fill="none" viewBox="0 0 24 24" stroke="currentColor">
            <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M5 13l4 4L19 7" />
          </svg>
        ) : isError ? (
          <svg className="w-5 h-5 text-rose-400 shrink-0" fill="none" viewBox="0 0 24 24" stroke="currentColor">
            <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M12 8v4m0 4h.01M21 12a9 9 0 11-18 0 9 9 0 0118 0z" />
          </svg>
        ) : (
          <svg className="w-5 h-5 text-blue-400 shrink-0" fill="none" viewBox="0 0 24 24" stroke="currentColor">
            <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M13 16h-1v-4h-1m1-4h.01M21 12a9 9 0 11-18 0 9 9 0 0118 0z" />
          </svg>
        )}
        <span>{feedback.text}</span>
      </div>
      <button
        onClick={onDismiss}
        type="button"
        className="text-xs opacity-75 hover:opacity-100 ml-4 font-semibold underline cursor-pointer"
      >
        Dismiss
      </button>
    </div>
  );
}
