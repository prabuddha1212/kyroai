"use client";

import React from "react";
import { Product } from "@/lib/types";
import { Badge } from "@/components/ui/Badge";

interface ProductCardProps {
  product: Product;
  isSelected: boolean;
  onSelect: (product: Product) => void;
}

export function ProductCard({ product, isSelected, onSelect }: ProductCardProps) {
  return (
    <div
      className={`relative rounded-2xl border transition-all flex flex-col justify-between overflow-hidden group ${
        isSelected
          ? "bg-neutral-900/95 border-emerald-500 shadow-xl shadow-emerald-500/10 ring-1 ring-emerald-500"
          : "bg-neutral-900/40 border-neutral-800/90 hover:border-neutral-700 hover:bg-neutral-900/70"
      }`}
    >
      <div className="relative h-48 w-full bg-neutral-950 overflow-hidden">
        {product.image_url ? (
          <img
            src={product.image_url}
            alt={product.name}
            loading="lazy"
            className="w-full h-full object-cover object-center transition-transform duration-500 group-hover:scale-105"
          />
        ) : (
          <div className="w-full h-full flex items-center justify-center bg-neutral-800 text-neutral-500 text-xs">
            Concept Render
          </div>
        )}
        <div className="absolute inset-0 bg-gradient-to-t from-neutral-900/90 via-transparent to-black/30" />

        <div className="absolute top-3 left-3 flex items-center gap-1.5">
          {product.badge && <Badge variant="primary">{product.badge}</Badge>}
          {product.category && <Badge variant="secondary">{product.category}</Badge>}
        </div>

        <div className="absolute bottom-3 right-3 text-right">
          <div className="text-xl font-extrabold text-white">
            ₹{product.price.toLocaleString()}
          </div>
          {product.original_price && (
            <div className="text-xs line-through text-neutral-400">
              ₹{product.original_price.toLocaleString()}
            </div>
          )}
        </div>
      </div>

      <div className="p-5 flex-1 flex flex-col justify-between space-y-4">
        <div>
          <h3 className="text-lg font-bold text-neutral-100 group-hover:text-white transition-colors">
            {product.name}
          </h3>
          {product.tagline && (
            <p className="text-xs text-emerald-400 font-medium mt-0.5 mb-2">
              {product.tagline}
            </p>
          )}
          <p className="text-xs text-neutral-400 leading-relaxed line-clamp-3">
            {product.description}
          </p>

          {product.features && product.features.length > 0 && (
            <ul className="mt-3 space-y-1.5 border-t border-neutral-800/60 pt-3">
              {product.features.map((feat, idx) => (
                <li key={idx} className="flex items-center text-[11px] text-neutral-400 gap-1.5">
                  <span className="text-emerald-400 text-xs">✓</span>
                  <span>{feat}</span>
                </li>
              ))}
            </ul>
          )}
        </div>

        <div className="pt-2">
          <button
            type="button"
            aria-pressed={isSelected}
            onClick={() => onSelect(product)}
            className={`w-full py-2.5 px-4 rounded-xl text-xs font-semibold tracking-wide transition-all cursor-pointer flex items-center justify-center gap-1.5 ${
              isSelected
                ? "bg-emerald-500 text-black shadow-md shadow-emerald-500/20 hover:bg-emerald-400 font-bold"
                : "bg-neutral-800 hover:bg-neutral-700 text-neutral-200 hover:text-white border border-neutral-700/60"
            }`}
          >
            {isSelected ? "Selected ✓" : "Reserve Early Access"}
          </button>
        </div>
      </div>
    </div>
  );
}
