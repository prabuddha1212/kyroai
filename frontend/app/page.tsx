"use client";

import React, { useState, useEffect } from "react";
import Link from "next/link";
import { Header } from "@/components/layout/Header";
import { Footer } from "@/components/layout/Footer";
import { ProductGrid } from "@/components/products/ProductGrid";
import { WaitlistForm } from "@/components/waitlist/WaitlistForm";
import { PrivacyModal } from "@/components/waitlist/PrivacyModal";
import { Alert } from "@/components/ui/Alert";
import { useProducts } from "@/hooks/useProducts";
import { useAnalytics } from "@/hooks/useAnalytics";
import { Product, FeedbackState } from "../lib/types";
import { FALLBACK_PRODUCTS } from "../lib/constants";

export default function Home() {
  const { products, loading } = useProducts();
  const { trackEvent } = useAnalytics();

  const [selectedProductId, setSelectedProductId] = useState<string>("desk-mat");
  const [feedback, setFeedback] = useState<FeedbackState | null>(null);
  const [showPrivacyModal, setShowPrivacyModal] = useState<boolean>(false);

  useEffect(() => {
    trackEvent("page_view");
  }, [trackEvent]);

  const handleSelectProduct = (product: Product) => {
    setSelectedProductId(product.id);
    trackEvent("product_click", product.id);
    setFeedback(null);
  };

  const selectedProduct =
    products.find((p) => p.id === selectedProductId) ||
    products[0] ||
    FALLBACK_PRODUCTS[0];

  return (
    <div className="min-h-screen bg-neutral-950 text-neutral-100 flex flex-col font-sans selection:bg-emerald-500 selection:text-black">
      {/* Navigation Header */}
      <Header />

      {/* Main Content */}
      <main className="flex-1 max-w-7xl w-full mx-auto px-4 sm:px-6 py-10 sm:py-14 flex flex-col gap-10">
        {/* Hero Section */}
        <div className="text-center max-w-3xl mx-auto space-y-4">
          <div className="inline-flex items-center gap-2 px-3 py-1 rounded-full bg-neutral-900 border border-neutral-800 text-xs text-neutral-300">
            <span className="w-2 h-2 rounded-full bg-emerald-500 animate-pulse" />
            <span>Demand Validation Experiment • Phase 6</span>
          </div>

          <h1 className="text-4xl sm:text-5xl lg:text-6xl font-extrabold tracking-tight bg-gradient-to-b from-white via-neutral-100 to-neutral-400 bg-clip-text text-transparent">
            Upcoming Gear & Accessories
          </h1>

          <p className="text-neutral-400 text-base sm:text-lg leading-relaxed max-w-2xl mx-auto">
            Explore concept desk equipment currently in prototyping. Reserve early-bird access with zero upfront payment. We only manufacture what the community wants.
          </p>

          <div className="flex items-center justify-center gap-2 pt-1">
            <Link
              href="/storelab-3d"
              className="inline-flex items-center gap-2 px-4 py-2 rounded-xl bg-neutral-900 hover:bg-neutral-800 border border-emerald-500/40 text-xs font-semibold text-emerald-400 hover:text-emerald-300 transition-all shadow-md shadow-emerald-500/5 group"
            >
              <span>Explore products in interactive 3D studio</span>
              <span className="transition-transform group-hover:translate-x-0.5">✨ →</span>
            </Link>
          </div>
        </div>

        {/* Global Feedback Alert */}
        <Alert feedback={feedback} onDismiss={() => setFeedback(null)} />

        {/* Product Cards Grid */}
        <ProductGrid
          products={products}
          loading={loading}
          selectedProductId={selectedProductId}
          onSelectProduct={handleSelectProduct}
        />

        {/* Unified Customer Signup Form */}
        {selectedProduct && (
          <WaitlistForm
            selectedProduct={selectedProduct}
            products={products.length > 0 ? products : FALLBACK_PRODUCTS}
            selectedProductId={selectedProductId}
            onSelectProductId={setSelectedProductId}
            onFeedback={setFeedback}
            onPrivacyClick={() => setShowPrivacyModal(true)}
          />
        )}
      </main>

      {/* Privacy Notice Modal */}
      <PrivacyModal
        isOpen={showPrivacyModal}
        onClose={() => setShowPrivacyModal(false)}
      />

      {/* Footer */}
      <Footer onPrivacyClick={() => setShowPrivacyModal(true)} />
    </div>
  );
}
