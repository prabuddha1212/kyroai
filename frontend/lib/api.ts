import { API_BASE_URL, FALLBACK_PRODUCTS } from "./constants";
import { Product, WaitlistPayload, WaitlistResponse, OwnerStats } from "./types";

export async function getProducts(): Promise<Product[]> {
  try {
    const res = await fetch(`${API_BASE_URL}/api/products`);
    if (res.ok) {
      const data = await res.json();
      if (Array.isArray(data) && data.length > 0) {
        return data;
      }
    }
  } catch (err) {
    console.warn("Failed to fetch products from backend, falling back to static catalogue:", err);
  }
  return FALLBACK_PRODUCTS;
}

export async function joinWaitlist(payload: WaitlistPayload): Promise<WaitlistResponse> {
  const res = await fetch(`${API_BASE_URL}/api/waitlist`, {
    method: "POST",
    headers: { "Content-Type": "application/json" },
    body: JSON.stringify(payload),
  });

  const data = await res.json();
  if (!res.ok) {
    throw new Error(data.detail || "Unable to complete reservation right now.");
  }
  return data;
}

export async function trackEvent(
  eventName: string,
  productId?: string,
  meta?: Record<string, unknown>
): Promise<void> {
  try {
    await fetch(`${API_BASE_URL}/api/analytics/event`, {
      method: "POST",
      headers: { "Content-Type": "application/json" },
      body: JSON.stringify({ event_name: eventName, product_id: productId, meta }),
    });
  } catch {
    // Analytics fail silently
  }
}

export async function getOwnerStats(adminKey: string): Promise<OwnerStats> {
  const res = await fetch(`${API_BASE_URL}/api/owner/stats`, {
    headers: {
      "X-Admin-Key": adminKey.trim(),
    },
  });

  if (!res.ok) {
    if (res.status === 401) {
      throw new Error("Invalid Admin Key. Check your .env ADMIN_KEY.");
    }
    throw new Error("Failed to load owner stats from backend.");
  }

  return res.json();
}
