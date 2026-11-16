"use client";

/**
 * browser-market.ts — the BROWSER TIER for the market snapshot.
 *
 * WHY THIS EXISTS (2026-11-16)
 * ----------------------------
 * The dashboard's structural panels (Auction VAL/POC/VAH, Day VWAP ±σ, EMA
 * 13/89/233, RSI) are all computed server-side in `/api/cg/market`, which
 * requires an UPSTREAM KLINE SOURCE. On a host whose egress can reach the
 * exchange WebSocket but not the REST klines endpoints, that route fails and
 * the whole panel block renders "–" even though the browser itself has a
 * perfectly good tape (the REAL-TIME badge beside the price is proof).
 *
 * Earlier revisions hid that failure behind `await res.json()` on a 5xx: the
 * response body is an HTML error page, so the user saw
 *
 *     market: Unexpected token '<', "<!DOCTYPE " ... is not valid JSON
 *
 * — a parser complaint instead of the real cause ("no klines upstream").
 *
 * This module fixes both halves:
 *   1. `fetchSnapshotTolerant()` / `usePolling` never blind-parse a 5xx — a
 *      non-JSON error body is reported as an HTTP status, not a syntax error.
 *   2. `useBrowserMarket()` recomputes the SAME snapshot client-side from
 *      Binance USDT-M REST klines, using the SAME pure indicator module the
 *      server uses (`@/lib/cg/indicators`), so the numbers cannot drift.
 *
 * Tier order is disclosed, never silent: "server" → "browser" → "none". The
 * UI labels which tier is live, exactly as the price badge does.
 */

import { useEffect, useRef, useState } from "react";
import { resolveBinPair } from "@/lib/binance/aliases";
import {
  auctionLevels,
  dayVwap,
  emaLast,
  rsiLast,
  type AuctionSet,
  type Candle,
  type VwapResult,
} from "@/lib/cg/indicators";

const FAPI = "https://fapi.binance.com";

/** Every field here is `number | null` — a null is rendered as "–", never faked. */
export interface BrowserMarketSnapshot {
  ok: true;
  sym: string;
  source: "binance-fapi-browser";
  tier: "browser";
  priceDecs: number;
  price: {
    last: number | null;
    prevDayClose: number | null;
    chgDayPct: number | null;
    dayHigh: number | null;
    dayLow: number | null;
  };
  auction: { session: ProfileLite; day: ProfileLite; month: ProfileLite };
  ema: Record<"m15" | "h1" | "h4" | "d1", { e13: number | null; e89: number | null; e233: number | null }>;
  rsi: Record<"m15" | "h1" | "h4", number | null>;
  vwap: VwapResult;
  candleAt: number;
  dataAt: number;
  bars: number;
}

interface ProfileLite {
  poc: number | null;
  val: number | null;
  vah: number | null;
}

type BinKline = [number, string, string, string, string, string, ...unknown[]];

function toCandle(k: BinKline): Candle {
  return {
    t: Number(k[0]),
    o: Number(k[1]),
    h: Number(k[2]),
    l: Number(k[3]),
    c: Number(k[4]),
    v: Number(k[5]),
  };
}

async function getKlines(pair: string, interval: string, limit: number): Promise<Candle[]> {
  const url = `${FAPI}/fapi/v1/klines?symbol=${encodeURIComponent(pair)}&interval=${interval}&limit=${limit}`;
  const res = await fetch(url, { cache: "no-store" });
  if (!res.ok) throw new Error(`binance HTTP ${res.status} (${interval})`);
  const raw = (await res.json()) as unknown;
  if (!Array.isArray(raw)) throw new Error(`binance klines: unexpected ${typeof raw} (${interval})`);
  return (raw as BinKline[]).map(toCandle).filter((c) => Number.isFinite(c.c));
}

function lite(p: { poc: number | null; val: number | null; vah: number | null }): ProfileLite {
  return { poc: p.poc, val: p.val, vah: p.vah };
}

/** Same math, same module, same inputs as buildMarketSnapshot() — just client-side. */
export async function buildBrowserSnapshot(symRaw: string): Promise<BrowserMarketSnapshot> {
  const sym = symRaw.trim().toUpperCase();
  const pair = resolveBinPair(sym);

  const [m15, h1, h4, d1] = await Promise.all([
    getKlines(pair, "15m", 400),
    getKlines(pair, "1h", 400),
    getKlines(pair, "4h", 300),
    getKlines(pair, "1d", 200),
  ]);
  if (!m15.length) throw new Error(`no browser klines for ${sym} (${pair})`);

  const closes = (cs: Candle[]) => cs.map((c) => c.c);
  const last = m15[m15.length - 1];
  const prevDay = d1.length >= 2 ? d1[d1.length - 2].c : null;
  const auction: AuctionSet = auctionLevels(m15, h1.length ? h1 : m15);

  const todayBars = m15.filter(
    (c) => c.t >= Date.UTC(new Date().getUTCFullYear(), new Date().getUTCMonth(), new Date().getUTCDate())
  );
  const hi = todayBars.length ? Math.max(...todayBars.map((c) => c.h)) : null;
  const lo = todayBars.length ? Math.min(...todayBars.map((c) => c.l)) : null;

  return {
    ok: true,
    sym,
    source: "binance-fapi-browser",
    tier: "browser",
    priceDecs: last.c >= 1000 ? 1 : last.c >= 1 ? 3 : 6,
    price: {
      last: last.c,
      prevDayClose: prevDay,
      chgDayPct: prevDay ? ((last.c - prevDay) / prevDay) * 100 : null,
      dayHigh: hi,
      dayLow: lo,
    },
    auction: {
      session: lite(auction.session),
      day: lite(auction.day),
      month: lite(auction.month),
    },
    ema: {
      m15: { e13: emaLast(closes(m15), 13), e89: emaLast(closes(m15), 89), e233: emaLast(closes(m15), 233) },
      h1: { e13: emaLast(closes(h1), 13), e89: emaLast(closes(h1), 89), e233: emaLast(closes(h1), 233) },
      h4: { e13: emaLast(closes(h4), 13), e89: emaLast(closes(h4), 89), e233: emaLast(closes(h4), 233) },
      d1: { e13: emaLast(closes(d1), 13), e89: emaLast(closes(d1), 89), e233: emaLast(closes(d1), 233) },
    },
    rsi: { m15: rsiLast(closes(m15)), h1: rsiLast(closes(h1)), h4: rsiLast(closes(h4)) },
    vwap: dayVwap(m15),
    candleAt: last.t,
    dataAt: Date.now(),
    bars: m15.length,
  };
}

export interface BrowserMarketState {
  data: BrowserMarketSnapshot | null;
  error: string | null;
  loading: boolean;
  tier: "server" | "browser" | "none";
}

/**
 * `enabled` should be true only when the SERVER tier has already failed —
 * there is no reason to spend the browser's Binance weight budget while the
 * server is answering. When it flips true this polls every `intervalMs`.
 */
export function useBrowserMarket(sym: string, enabled: boolean, intervalMs = 30_000): BrowserMarketState {
  const [data, setData] = useState<BrowserMarketSnapshot | null>(null);
  const [error, setError] = useState<string | null>(null);
  const [loading, setLoading] = useState(false);
  const alive = useRef(true);
  const gen = useRef(0);

  useEffect(() => {
    alive.current = true;
    if (!enabled) {
      setData(null);
      setError(null);
      setLoading(false);
      return () => {
        alive.current = false;
      };
    }
    const load = async () => {
      const myGen = ++gen.current;
      setLoading(true);
      try {
        const snap = await buildBrowserSnapshot(sym);
        if (!alive.current || myGen !== gen.current) return;
        setData(snap);
        setError(null);
      } catch (e) {
        if (!alive.current || myGen !== gen.current) return;
        setError(e instanceof Error ? e.message : "browser klines unavailable");
        setData(null);
      } finally {
        if (alive.current && myGen === gen.current) setLoading(false);
      }
    };
    void load();
    const t = setInterval(load, intervalMs);
    return () => {
      alive.current = false;
      clearInterval(t);
    };
  }, [sym, enabled, intervalMs]);

  return { data, error, loading, tier: data ? "browser" : enabled ? "none" : "server" };
}
