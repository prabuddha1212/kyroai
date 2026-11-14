"use client";

import React from "react";
import { Product } from "@/lib/types";
import { ProductCard } from "./ProductCard";
import { ProductCardSkeleton } from "./ProductCardSkeleton";

interface ProductGridProps {
  products: Product[];
  loading: boolean;
  selectedProductId: string;
  onSelectProduct: (product: Product) => void;
}

export function ProductGrid({
  products,
  loading,
  selectedProductId,
  onSelectProduct,
}: ProductGridProps) {
  if (loading) {
    return (
      <div className="grid grid-cols-1 sm:grid-cols-2 lg:grid-cols-4 gap-6">
        {[1, 2, 3, 4].map((n) => (
          <ProductCardSkeleton key={n} />
        ))}
      </div>
    );
  }

  return (
    <div className="grid grid-cols-1 sm:grid-cols-2 lg:grid-cols-4 gap-6">
      {products.map((product) => (
        <ProductCard
          key={product.id}
          product={product}
          isSelected={selectedProductId === product.id}
          onSelect={onSelectProduct}
        />
      ))}
    </div>
  );
}
