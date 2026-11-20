"use client";

import { fmtNum, fmtPct } from "@/lib/cg/format";
import DerivativesPanel from "./derivatives-panel";
import { usePolling } from "./use-cg-data";

const PERIODS = ["15m", "1h", "4h"] as const;
const OI_PERIODS = ["1h", "4h", "24h"] as const;

interface QuantResponse {
  sym: string;
  supported: boolean;
  reason?: string;
  stale?: boolean;
  source?: string;
  lsRatios?: Record<(typeof PERIODS)[number], {
    global: { ratio: number } | null;
    topAccounts: { ratio: number } | null;
    topPositions: { ratio: number } | null;
    taker: { buySellRatio: number } | null;
  }>;
  oiQuadrant?: Record<(typeof OI_PERIODS)[number], {
    quadrant: string;
    oiDeltaPct: number;
    priceDeltaPct: number;
  } | null>;
  funding?: { annualizedAprPct: number | null; fundingSpreadBps: number | null };
  basis?: { basisPct: number | null; coinbasePremiumBps: number | null };
}

function value(n: number | null | undefined, suffix = "") {
  return n == null || !Number.isFinite(n) ? "—" : `${fmtNum(n, 2)}${suffix}`;
}

export default function QuantTool({ sym, tradfi }: { sym: string; tradfi: boolean }) {
  const q = usePolling<QuantResponse>(`/api/cg/quant?sym=${encodeURIComponent(sym)}`, 30_000);
  const data = q.data?.sym === sym ? q.data : null;
  const hasMetrics = data && (Object.values(data.lsRatios ?? {}).some((period) => Object.values(period).some(Boolean))
    || OI_PERIODS.some((period) => data.oiQuadrant?.[period])
    || data.funding?.annualizedAprPct != null || data.funding?.fundingSpreadBps != null
    || data.basis?.basisPct != null || data.basis?.coinbasePremiumBps != null);
  return (
    <div className="space-y-3">
      <section className="rounded-lg border border-neutral-800 bg-neutral-900/60 p-3 text-xs text-neutral-300">
        <div className="flex flex-wrap items-center justify-between gap-2">
          <h2 className="text-sm font-semibold text-neutral-100">{sym} · Perpetual positioning</h2>
          <button className="rounded border border-neutral-700 px-2 py-1" onClick={q.refresh}>Refresh</button>
        </div>
        {(q.error || data?.stale || !hasMetrics) && (
          <p role="status" className="mt-2 text-neutral-400">
            {q.error ?? (q.loading ? "Loading positioning data…" : data?.stale ? "Latest snapshot may be stale." : data?.reason ?? "Positioning data is temporarily unavailable.")}
          </p>
        )}
        {hasMetrics && (
          <>
            <div className="my-3 grid grid-cols-2 gap-2 md:grid-cols-4">
              <div>Funding APR <strong className="block font-mono">{value(data.funding?.annualizedAprPct, "%")}</strong></div>
              <div>Funding spread <strong className="block font-mono">{value(data.funding?.fundingSpreadBps, " bps")}</strong></div>
              <div>Spot–perp basis <strong className="block font-mono">{value(data.basis?.basisPct, "%")}</strong></div>
              <div>Coinbase premium <strong className="block font-mono">{value(data.basis?.coinbasePremiumBps, " bps")}</strong></div>
            </div>
            <div className="grid gap-4 lg:grid-cols-2">
              <div className="overflow-x-auto">
                <table className="w-full text-left">
                  <thead className="text-neutral-400"><tr><th>Window</th><th>Long/short</th><th>Top accounts</th><th>Top positions</th><th>Taker buy/sell</th></tr></thead>
                  <tbody>
                    {PERIODS.map((period) => {
                      const row = data.lsRatios?.[period];
                      return <tr key={period} className="border-t border-neutral-800"><th className="py-1">{period}</th><td>{value(row?.global?.ratio)}</td><td>{value(row?.topAccounts?.ratio)}</td><td>{value(row?.topPositions?.ratio)}</td><td>{value(row?.taker?.buySellRatio)}</td></tr>;
                    })}
                  </tbody>
                </table>
              </div>
              <table className="w-full text-left">
                <thead className="text-neutral-400"><tr><th>Window</th><th>Open interest</th><th>Price</th><th>Quadrant</th></tr></thead>
                <tbody>
                  {OI_PERIODS.map((period) => {
                    const row = data.oiQuadrant?.[period];
                    return <tr key={period} className="border-t border-neutral-800"><th className="py-1">{period}</th><td>{row ? fmtPct(row.oiDeltaPct) : "—"}</td><td>{row ? fmtPct(row.priceDeltaPct) : "—"}</td><td>{row?.quadrant.replaceAll("_", " ").toLowerCase() ?? "—"}</td></tr>;
                  })}
                </tbody>
              </table>
            </div>
            {data.source && <p className="mt-3 break-words text-neutral-500">{data.source}</p>}
          </>
        )}
      </section>
      {tradfi && <DerivativesPanel sym={sym} cashPrice={null} />}
    </div>
  );
}
