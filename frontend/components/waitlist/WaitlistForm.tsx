"use client";

import React, { useState } from "react";
import { Product, FeedbackState } from "@/lib/types";
import { joinWaitlist } from "@/lib/api";
import { useAnalytics } from "@/hooks/useAnalytics";

interface WaitlistFormProps {
  selectedProduct: Product;
  products: Product[];
  selectedProductId: string;
  onSelectProductId: (id: string) => void;
  onFeedback: (feedback: FeedbackState | null) => void;
  onPrivacyClick: () => void;
}

export function WaitlistForm({
  selectedProduct,
  products,
  selectedProductId,
  onSelectProductId,
  onFeedback,
  onPrivacyClick,
}: WaitlistFormProps) {
  const [name, setName] = useState<string>("");
  const [email, setEmail] = useState<string>("");
  const [consent, setConsent] = useState<boolean>(true);
  const [honeypot, setHoneypot] = useState<string>("");
  const [submitting, setSubmitting] = useState<boolean>(false);

  const { trackEvent } = useAnalytics();

  const handleSubmit = async (e: React.FormEvent) => {
    e.preventDefault();

    if (!name || name.trim().length < 2) {
      onFeedback({ type: "error", text: "Please enter your full name (minimum 2 characters)." });
      return;
    }
    if (!email || !email.includes("@")) {
      onFeedback({ type: "error", text: "Please enter a valid email address." });
      return;
    }
    if (!selectedProductId) {
      onFeedback({ type: "error", text: "Please select a product to reserve." });
      return;
    }
    if (!consent) {
      onFeedback({ type: "error", text: "Please agree to the privacy policy to continue." });
      return;
    }

    setSubmitting(true);
    onFeedback(null);

    try {
      const data = await joinWaitlist({
        product_id: selectedProductId,
        name: name.trim(),
        email: email.trim().toLowerCase(),
        consent_given: consent,
        honeypot: honeypot || undefined,
      });

      onFeedback({
        type: data.is_duplicate ? "info" : "success",
        text: data.message || "Spot reserved! A confirmation email has been dispatched.",
      });

      trackEvent("waitlist_joined", selectedProductId, {
        customer_name: name.trim(),
        email_domain: email.split("@")[1],
      });

      setEmail("");
      setName("");
    } catch (err: unknown) {
      const message = err instanceof Error ? err.message : "An unexpected network error occurred.";
      onFeedback({ type: "error", text: message });
    } finally {
      setSubmitting(false);
    }
  };

  return (
    <section
      aria-labelledby="waitlist-heading"
      className="max-w-2xl mx-auto w-full bg-neutral-900 border border-emerald-500/50 rounded-2xl p-6 sm:p-8 shadow-2xl backdrop-blur-md"
    >
      <div className="flex flex-col sm:flex-row sm:items-center justify-between gap-4 pb-4 border-b border-neutral-800">
        <div>
          <span className="text-[11px] text-emerald-400 font-bold uppercase tracking-wider">
            Early-Access Reservation
          </span>
          <h2 id="waitlist-heading" className="text-2xl font-bold text-white mt-0.5">
            Reserve: {selectedProduct.name}
          </h2>
          <p className="text-xs text-neutral-400 mt-1">
            Target Price: <strong className="text-white">₹{selectedProduct.price.toLocaleString()}</strong> • Zero upfront charge.
          </p>
        </div>

        <div className="text-xs text-neutral-400">
          <span className="text-neutral-500">Selected Product:</span>{" "}
          <select
            value={selectedProductId}
            onChange={(e) => onSelectProductId(e.target.value)}
            className="bg-neutral-950 border border-neutral-700 text-white rounded-lg px-2.5 py-1 text-xs ml-1 focus:outline-none focus:border-emerald-500"
          >
            {products.map((p) => (
              <option key={p.id} value={p.id}>
                {p.name} (₹{p.price})
              </option>
            ))}
          </select>
        </div>
      </div>

      <form onSubmit={handleSubmit} className="mt-6 space-y-4">
        <input
          type="text"
          name="website"
          value={honeypot}
          onChange={(e) => setHoneypot(e.target.value)}
          tabIndex={-1}
          autoComplete="off"
          style={{ display: "none" }}
          aria-hidden="true"
        />

        <div className="grid grid-cols-1 sm:grid-cols-2 gap-3">
          <div>
            <label className="block text-xs font-medium text-neutral-300 mb-1.5">
              Your Full Name
            </label>
            <input
              type="text"
              placeholder="e.g. Alex Morgan"
              value={name}
              onChange={(e) => setName(e.target.value)}
              required
              className="w-full bg-neutral-950 border border-neutral-700/80 rounded-xl px-4 py-3 text-sm text-white placeholder-neutral-500 focus:outline-none focus:border-emerald-500 transition-colors"
            />
          </div>

          <div>
            <label className="block text-xs font-medium text-neutral-300 mb-1.5">
              Email Address
            </label>
            <input
              type="email"
              placeholder="e.g. alex@gmail.com"
              value={email}
              onChange={(e) => setEmail(e.target.value)}
              required
              className="w-full bg-neutral-950 border border-neutral-700/80 rounded-xl px-4 py-3 text-sm text-white placeholder-neutral-500 focus:outline-none focus:border-emerald-500 transition-colors"
            />
          </div>
        </div>

        <button
          type="submit"
          disabled={submitting}
          className="w-full bg-emerald-500 hover:bg-emerald-400 text-black font-bold py-3.5 rounded-xl text-sm transition-all disabled:opacity-50 cursor-pointer shadow-lg shadow-emerald-500/20"
        >
          {submitting ? "Reserving Spot & Sending Confirmation..." : `Confirm Reservation for ${selectedProduct.name}`}
        </button>

        <div className="flex items-start gap-2.5 pt-1">
          <input
            type="checkbox"
            id="consent"
            checked={consent}
            onChange={(e) => setConsent(e.target.checked)}
            className="mt-0.5 h-4 w-4 rounded border-neutral-700 bg-neutral-950 text-emerald-500 focus:ring-emerald-500 cursor-pointer"
          />
          <label htmlFor="consent" className="text-xs text-neutral-400 cursor-pointer">
            I consent to receive early access notification emails for this concept product. Zero spam, and unsubscribe anytime.{" "}
            <button
              type="button"
              onClick={onPrivacyClick}
              className="text-emerald-400 underline hover:text-emerald-300 ml-1 font-medium cursor-pointer"
            >
              Privacy Notice
            </button>
          </label>
        </div>
      </form>
    </section>
  );
}
