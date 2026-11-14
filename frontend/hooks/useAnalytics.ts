"use client";

import { useCallback } from "react";
import { trackEvent as apiTrackEvent } from "../lib/api";

export function useAnalytics() {
  const track = useCallback(
    (eventName: string, productId?: string, meta?: Record<string, unknown>) => {
      return apiTrackEvent(eventName, productId, meta);
    },
    []
  );

  return { trackEvent: track };
}
