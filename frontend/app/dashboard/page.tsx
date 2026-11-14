"use client";

import React, { useState, useEffect } from "react";
import Link from "next/link";
import { KyroLogo } from "@/components/layout/KyroLogo";

interface OwnerStats {
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

const API_BASE_URL = process.env.NEXT_PUBLIC_API_URL || "http://localhost:8000";

export default function OwnerDashboard() {
  const [adminKey, setAdminKey] = useState<string>("");
  const [isAuthenticated, setIsAuthenticated] = useState<boolean>(false);
  const [stats, setStats] = useState<OwnerStats | null>(null);
  const [loading, setLoading] = useState<boolean>(false);
  const [error, setError] = useState<string | null>(null);

  // Unit Economics Calculator State (from Phase 8)
  const [sellingPrice, setSellingPrice] = useState<number>(799);
  const [productCost, setProductCost] = useState<number>(350);
  const [shippingCost, setShippingCost] = useState<number>(90);
  const [paymentFee, setPaymentFee] = useState<number>(25);
  const [cac, setCac] = useState<number>(135);

  const contributionMargin = sellingPrice - productCost - shippingCost - paymentFee - cac;

  // Retrieve saved admin key from localStorage
  useEffect(() => {
    const saved = localStorage.getItem("storelab_admin_key");
    if (saved) {
      setAdminKey(saved);
      fetchStats(saved);
    }
  }, []);

  const fetchStats = async (key: string) => {
    setLoading(true);
    setError(null);
    try {
      const res = await fetch(`${API_BASE_URL}/api/owner/stats`, {
        headers: {
          "X-Admin-Key": key.trim(),
        },
      });

      if (!res.ok) {
        if (res.status === 401) {
          throw new Error("Invalid Admin Key. Check your .env ADMIN_KEY or try 'storelab-admin-2026'.");
        }
        throw new Error("Failed to load owner stats from backend.");
      }

      const data = await res.json();
      setStats(data);
      setIsAuthenticated(true);
      localStorage.setItem("storelab_admin_key", key.trim());
    } catch (err: unknown) {
      const msg = err instanceof Error ? err.message : "Error authenticating.";
      setError(msg);
      setIsAuthenticated(false);
    } finally {
      setLoading(false);
    }
  };

  const handleLogin = (e: React.FormEvent) => {
    e.preventDefault();
    if (!adminKey) return;
    fetchStats(adminKey);
  };

  const handleLogout = () => {
    localStorage.removeItem("storelab_admin_key");
    setIsAuthenticated(false);
    setStats(null);
    setAdminKey("");
  };

  const handleDeleteEntry = async (email: string, productId?: string) => {
    if (!confirm(`Are you sure you want to remove ${email} from the waitlist?`)) return;

    try {
      const url = new URL(`${API_BASE_URL}/api/waitlist`);
      url.searchParams.set("email", email);
      if (productId) url.searchParams.set("product_id", productId);

      const res = await fetch(url.toString(), { method: "DELETE" });
      if (res.ok) {
        fetchStats(adminKey);
      }
    } catch {
      alert("Failed to delete entry.");
    }
  };

  const pageViews = (stats?.analytics_events?.page_view || 0) + (stats?.analytics_events?.page_view_3d || 0);
  const totalSignups = stats?.total_signups || 0;
  const conversionRate = pageViews > 0 ? ((totalSignups / pageViews) * 100).toFixed(1) : "0.0";

  return (
    <div className="min-h-screen bg-neutral-950 text-neutral-100 flex flex-col font-sans">
      {/* Dashboard Header */}
      <header className="border-b border-neutral-800 bg-neutral-900/60 backdrop-blur sticky top-0 z-30">
        <div className="max-w-6xl mx-auto px-6 py-4 flex items-center justify-between">
          <div className="flex items-center gap-3.5">
            <Link
              href="/"
              className="flex items-center gap-2.5 group"
            >
              <KyroLogo size={44} />
            </Link>
            <div>
              <h1 className="font-extrabold text-xl text-white">
                Kyro<span className="text-emerald-400">AI</span> Command Center
              </h1>
              <span className="text-[10px] text-neutral-400 font-medium">Store & Demand Validation Metrics</span>
            </div>
          </div>

          <div className="flex items-center gap-3">
            <Link
              href="/"
              className="text-xs font-medium text-neutral-400 hover:text-white transition-colors border border-neutral-800 px-3 py-1.5 rounded-lg"
            >
              View Storefront ↗
            </Link>
            {isAuthenticated && (
              <button
                onClick={handleLogout}
                className="text-xs font-medium text-rose-400 hover:text-rose-300 border border-rose-900/60 bg-rose-950/30 px-3 py-1.5 rounded-lg cursor-pointer"
              >
                Log Out
              </button>
            )}
          </div>
        </div>
      </header>

      {/* Main Content */}
      <main className="flex-1 max-w-6xl w-full mx-auto px-6 py-10 flex flex-col gap-8">
        {!isAuthenticated ? (
          <div className="max-w-md mx-auto w-full my-auto bg-neutral-900 border border-neutral-800 rounded-2xl p-8 space-y-6 shadow-2xl">
            <div className="space-y-2 text-center">
              <div className="w-12 h-12 rounded-2xl bg-neutral-800 border border-neutral-700 flex items-center justify-center mx-auto text-xl">
                🔒
              </div>
              <h2 className="text-xl font-bold text-white">Owner Authentication</h2>
              <p className="text-xs text-neutral-400">
                Enter your administrative key to view live customer demand and product metrics.
              </p>
            </div>

            {error && (
              <div className="p-3.5 rounded-xl bg-rose-950/60 border border-rose-800/80 text-rose-300 text-xs">
                {error}
              </div>
            )}

            <form onSubmit={handleLogin} className="space-y-4">
              <div>
                <label className="block text-xs font-medium text-neutral-300 mb-1.5">
                  Admin Passkey (default: storelab-admin-2026)
                </label>
                <input
                  type="password"
                  placeholder="Enter secret key"
                  value={adminKey}
                  onChange={(e) => setAdminKey(e.target.value)}
                  required
                  className="w-full bg-neutral-950 border border-neutral-700 rounded-xl px-4 py-2.5 text-sm text-white placeholder-neutral-500 focus:outline-none focus:border-emerald-500"
                />
              </div>

              <button
                type="submit"
                disabled={loading}
                className="w-full py-2.5 rounded-xl bg-emerald-500 hover:bg-emerald-400 text-black font-bold text-sm transition-all disabled:opacity-50 cursor-pointer shadow-md"
              >
                {loading ? "Verifying..." : "Unlock Dashboard"}
              </button>
            </form>
          </div>
        ) : (
          <div className="space-y-10">
            {/* Top Metric Cards */}
            <div className="grid grid-cols-1 sm:grid-cols-3 gap-6">
              <div className="bg-neutral-900 border border-neutral-800 rounded-2xl p-6 space-y-2">
                <span className="text-xs font-semibold uppercase tracking-wider text-neutral-400">
                  Total Waitlist Signups
                </span>
                <div className="text-4xl font-extrabold text-white">
                  {totalSignups}
                </div>
                <p className="text-xs text-emerald-400">Verified demand reservations</p>
              </div>

              <div className="bg-neutral-900 border border-neutral-800 rounded-2xl p-6 space-y-2">
                <span className="text-xs font-semibold uppercase tracking-wider text-neutral-400">
                  Total Page Views
                </span>
                <div className="text-4xl font-extrabold text-white">
                  {pageViews}
                </div>
                <p className="text-xs text-neutral-400">Standard & 3D Studio visits</p>
              </div>

              <div className="bg-neutral-900 border border-neutral-800 rounded-2xl p-6 space-y-2">
                <span className="text-xs font-semibold uppercase tracking-wider text-neutral-400">
                  Conversion Rate
                </span>
                <div className="text-4xl font-extrabold text-emerald-400">
                  {conversionRate}%
                </div>
                <p className="text-xs text-neutral-400">Signups / Total Page Views</p>
              </div>
            </div>

            {/* Product Interest Breakdown */}
            <div className="bg-neutral-900 border border-neutral-800 rounded-2xl p-6 space-y-6">
              <div className="flex items-center justify-between">
                <div>
                  <h3 className="font-bold text-lg text-white">Product Demand Breakdown</h3>
                  <p className="text-xs text-neutral-400">Signups per concept product</p>
                </div>
                <button
                  onClick={() => fetchStats(adminKey)}
                  className="text-xs border border-neutral-700 bg-neutral-800 hover:bg-neutral-700 px-3 py-1.5 rounded-lg text-neutral-200 cursor-pointer"
                >
                  ↻ Refresh
                </button>
              </div>

              <div className="space-y-4">
                {Object.entries(stats?.signups_by_product || {}).map(([productId, count]) => {
                  const percentage = totalSignups > 0 ? Math.round((count / totalSignups) * 100) : 0;
                  return (
                    <div key={productId} className="space-y-1.5">
                      <div className="flex items-center justify-between text-xs font-medium">
                        <span className="text-white capitalize">{productId.replace("-", " ")}</span>
                        <span className="text-neutral-400">
                          {count} signups ({percentage}%)
                        </span>
                      </div>
                      <div className="h-2.5 w-full bg-neutral-950 rounded-full overflow-hidden border border-neutral-800">
                        <div
                          className="h-full bg-emerald-500 rounded-full transition-all duration-500"
                          style={{ width: `${Math.max(percentage, count > 0 ? 5 : 0)}%` }}
                        />
                      </div>
                    </div>
                  );
                })}
              </div>
            </div>

            {/* Recent Signups Table with Customer Name */}
            <div className="bg-neutral-900 border border-neutral-800 rounded-2xl p-6 space-y-4">
              <div className="flex items-center justify-between">
                <div>
                  <h3 className="font-bold text-lg text-white">Recent Customer Registrations</h3>
                  <p className="text-xs text-neutral-400">Verified early-access supporters</p>
                </div>
                <span className="text-xs text-neutral-500">
                  {stats?.recent_signups?.length || 0} entries
                </span>
              </div>

              {(!stats?.recent_signups || stats.recent_signups.length === 0) ? (
                <div className="text-center py-10 border border-dashed border-neutral-800 rounded-xl text-neutral-500 text-xs">
                  No signups recorded yet. Test by reserving a product on the storefront!
                </div>
              ) : (
                <div className="overflow-x-auto">
                  <table className="w-full text-left text-xs">
                    <thead>
                      <tr className="border-b border-neutral-800 text-neutral-400">
                        <th className="py-2.5 px-3 font-semibold">Customer Name</th>
                        <th className="py-2.5 px-3 font-semibold">Email</th>
                        <th className="py-2.5 px-3 font-semibold">Product Reserved</th>
                        <th className="py-2.5 px-3 font-semibold text-right">Action</th>
                      </tr>
                    </thead>
                    <tbody className="divide-y divide-neutral-800/60">
                      {stats.recent_signups.map((entry, idx) => (
                        <tr key={idx} className="hover:bg-neutral-800/30 transition-colors">
                          <td className="py-2.5 px-3 font-medium text-white">{entry.name || "Early Supporter"}</td>
                          <td className="py-2.5 px-3 font-mono text-neutral-300">{entry.email}</td>
                          <td className="py-2.5 px-3 text-emerald-400 font-medium capitalize">{entry.product_id.replace("-", " ")}</td>
                          <td className="py-2.5 px-3 text-right">
                            <button
                              onClick={() => handleDeleteEntry(entry.email, entry.product_id)}
                              className="text-[11px] text-rose-400 hover:text-rose-300 underline cursor-pointer"
                              title="Delete user data (Privacy Compliance)"
                            >
                              Delete
                            </button>
                          </td>
                        </tr>
                      ))}
                    </tbody>
                  </table>
                </div>
              )}
            </div>

            {/* Unit Economics Calculator */}
            <div className="bg-neutral-900 border border-neutral-800 rounded-2xl p-6 space-y-6">
              <div>
                <h3 className="font-bold text-lg text-white">Unit Economics & Contribution Margin</h3>
                <p className="text-xs text-neutral-400">
                  Estimate net contribution per delivered unit before committing to inventory.
                </p>
              </div>

              <div className="grid grid-cols-1 sm:grid-cols-2 lg:grid-cols-5 gap-4">
                <div>
                  <label className="block text-[11px] font-medium text-neutral-400 mb-1">Selling Price (₹)</label>
                  <input
                    type="number"
                    value={sellingPrice}
                    onChange={(e) => setSellingPrice(Number(e.target.value))}
                    className="w-full bg-neutral-950 border border-neutral-800 rounded-lg px-3 py-2 text-sm text-white font-mono"
                  />
                </div>
                <div>
                  <label className="block text-[11px] font-medium text-neutral-400 mb-1">Product Cost (₹)</label>
                  <input
                    type="number"
                    value={productCost}
                    onChange={(e) => setProductCost(Number(e.target.value))}
                    className="w-full bg-neutral-950 border border-neutral-800 rounded-lg px-3 py-2 text-sm text-white font-mono"
                  />
                </div>
                <div>
                  <label className="block text-[11px] font-medium text-neutral-400 mb-1">Shipping & Pack (₹)</label>
                  <input
                    type="number"
                    value={shippingCost}
                    onChange={(e) => setShippingCost(Number(e.target.value))}
                    className="w-full bg-neutral-950 border border-neutral-800 rounded-lg px-3 py-2 text-sm text-white font-mono"
                  />
                </div>
                <div>
                  <label className="block text-[11px] font-medium text-neutral-400 mb-1">Payment Fees (₹)</label>
                  <input
                    type="number"
                    value={paymentFee}
                    onChange={(e) => setPaymentFee(Number(e.target.value))}
                    className="w-full bg-neutral-950 border border-neutral-800 rounded-lg px-3 py-2 text-sm text-white font-mono"
                  />
                </div>
                <div>
                  <label className="block text-[11px] font-medium text-neutral-400 mb-1">Estimated CAC (₹)</label>
                  <input
                    type="number"
                    value={cac}
                    onChange={(e) => setCac(Number(e.target.value))}
                    className="w-full bg-neutral-950 border border-neutral-800 rounded-lg px-3 py-2 text-sm text-white font-mono"
                  />
                </div>
              </div>

              <div className="p-4 rounded-xl bg-neutral-950 border border-neutral-800 flex flex-col sm:flex-row items-center justify-between gap-4">
                <div>
                  <span className="text-xs text-neutral-400">Contribution per Delivered Sale:</span>
                  <div className={`text-2xl font-bold font-mono ${contributionMargin >= 0 ? "text-emerald-400" : "text-rose-400"}`}>
                    ₹{contributionMargin.toLocaleString()}
                  </div>
                </div>
                <div className="text-[11px] text-neutral-500 max-w-sm">
                  {contributionMargin > 0
                    ? `✓ Healthy unit margin (${Math.round((contributionMargin / (sellingPrice || 1)) * 100)}%). Viable for testing paid acquisition once demand is proven.`
                    : "⚠ Negative margin! Increase selling price or renegotiate supplier/packaging costs."}
                </div>
              </div>
            </div>
          </div>
        )}
      </main>
    </div>
  );
}
