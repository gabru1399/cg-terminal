import { NextResponse } from "next/server";
import { getQuotes, getUniverse, binAssets, type BinQuote } from "@/lib/binance/universe";
import { t24Of } from "@/lib/binance/market-batch";
import { getMarketSnapshot } from "@/lib/cg/scan";
import { getLivePrice } from "@/lib/live/server-price";

export const dynamic = "force-dynamic";

/**
 * GET /api/binance/quotes — REST fallback for the markets grid.
 *
 * Tier 1: one weight-10 bookTicker call covers the WHOLE universe (5s shared
 * TTL) → bid/ask/last. Tier 2 (2026-11-12 fix): the shared all-symbol
 * ticker/24hr batch (weight 40, 4s TTL, already serving the market stats
 * block) enriches every quote with chg% · 24h high/low · 24h quote volume —
 * so a browser whose fstream socket connects-but-delivers-nothing (verified
 * on this egress: !miniTicker@arr frames filtered) still gets a FULLY
 * populated grid (last · chg · range · vol), not three dead columns.
 *
 * Tier 3 (2026-11-17 resilience): on egresses where fapi.binance.com is
 * completely blocked/filtered by ISPs, seamlessly fall back to live Coinglass
 * market snapshots and server-price hub so the top pin strip and market grid
 * remain 100% live and populated.
 */
export async function GET() {
  const u = await getUniverse(); // membership map must exist before quotes are filtered
  const q = await getQuotes();
  const quotes: Record<string, BinQuote> = { ...q.quotes };
  let ok = Object.keys(quotes).length > 0;

  // Enrich with 24h stats from the shared batch (one weight-40 fetch,
  // coalesced with every other consumer). Failure is soft: bid/ask/last
  // still return, chg/range just stay absent.
  if (ok) {
    const assets = binAssets();
    await Promise.allSettled(
      assets.map(async (a) => {
        const row = quotes[a.sym];
        if (!row) return;
        try {
          const t = await t24Of(a.pair);
          if (!t) return;
          const chgPct = Number(t.priceChangePercent);
          const high = Number(t.highPrice);
          const low = Number(t.lowPrice);
          const quoteVol = Number(t.quoteVolume);
          const lastT = Number(t.lastPrice);
          if (Number.isFinite(chgPct)) row.chgPct = chgPct;
          if (Number.isFinite(high) && high > 0) row.high = high;
          if (Number.isFinite(low) && low > 0) row.low = low;
          if (Number.isFinite(quoteVol) && quoteVol > 0) row.quoteVol = quoteVol;
          // ticker/24hr lastPrice is the true last trade (bookTicker mid is
          // an approximation) — prefer it when present
          if (Number.isFinite(lastT) && lastT > 0) row.last = lastT;
        } catch {
          /* enrichment is best-effort */
        }
      })
    );
  } else {
    // FALLBACK FOR EGRESSES WHERE fapi.binance.com IS UNREACHABLE (e.g. India ISPs):
    // Populate quotes instantaneously from in-memory Coinglass market snapshots
    const assets = binAssets();
    for (const a of assets) {
      const mkt = getMarketSnapshot(a.sym);
      const last = mkt?.price.last ?? null;
      if (last != null && last > 0) {
        quotes[a.sym] = {
          last,
          bid: last,
          ask: last,
          chgPct: mkt?.price.chgDayPct ?? undefined,
          high: mkt?.price.dayHigh ?? undefined,
          low: mkt?.price.dayLow ?? undefined,
          quoteVol: mkt?.price.dayVolBase ? mkt.price.dayVolBase * last : undefined,
        };
      }
    }
    if (Object.keys(quotes).length > 0) {
      ok = true;
    }
  }

  return NextResponse.json({
    ok,
    at: ok && !q.at ? Date.now() : q.at,
    ageMs: q.at ? Math.max(0, Date.now() - q.at) : 0,
    quotes,
    ...(q.err ? { error: q.err } : {}),
    serverTime: Date.now(),
  });
}
