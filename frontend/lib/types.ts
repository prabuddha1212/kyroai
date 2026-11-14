export interface Product {
  id: string;
  name: string;
  tagline?: string;
  price: number;
  original_price?: number;
  category?: string;
  badge?: string;
  image_url?: string;
  description: string;
  features?: string[];
  is_active?: boolean;
}

export interface WaitlistPayload {
  product_id: string;
  name: string;
  email: string;
  consent_given: boolean;
  honeypot?: string;
}

export interface WaitlistResponse {
  success: boolean;
  message: string;
  is_duplicate?: boolean;
  data?: unknown;
}

export interface FeedbackState {
  type: "success" | "error" | "info";
  text: string;
}

export interface OwnerStats {
  total_signups: number;
  signups_by_product: Record<string, number>;
  analytics_events: Record<string, number>;
  recent_signups: Array<{
    id?: number;
    name?: string;
    product_id: string;
    email: string;
    created_at?: string;
  }>;
}
