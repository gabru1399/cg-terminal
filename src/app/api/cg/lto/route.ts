import { NextRequest, NextResponse } from "next/server";
import { cgGet, FAPI } from "@/lib/cg/client";
import { anyTerminalSym, knownSym } from "@/lib/cg/sym-gate";
import { hlCoinOf, resolveCgSym } from "@/lib/binance/aliases";
import { fetchHlCtxAndBook, fetchHlRecentTrades } from "@/lib/cg/fallbacks";
import { BoundedMap } from "@/lib/cg/bounded";
import { rowsOf } from "@/lib/cg/store";
import type { LtoArchiveRow, LtoGroup, LtoSupport } from "@/lib/cg/types";

export const dynamic = "force-dynamic";

const cache = new BoundedMap<{ at: number; body: Awaited<ReturnType<typeof loadOrders>> }>(32);
const pending = new Map<string, ReturnType<typeof loadOrders>>();

function lastBtcSnapshot(minVolUsd: number) {
  const rows = rowsOf("lto:open", (row: LtoArchiveRow) => `${row.at}|${row.i}|${row.id}`) as LtoArchiveRow[];
  const at = rows.reduce((latest, row) => Math.max(latest, row.at || 0), 0);
  if (!at || Date.now() - at > 60 * 60_000) return null;
  return { at, minVolUsd: 1_000_000, rows: rows.filter((row) => row.at === at && row.usd >= Math.max(1_000_000, minVolUsd)) };
}

export async function GET(req: NextRequest) {
  const sp = req.nextUrl.searchParams;
  const requestedMin = Number(sp.get("minVolUsd") ?? 100_000);
  const minVolUsd = Number.isFinite(requestedMin) ? Math.max(0, requestedMin) : 100_000;
  const symbol = (sp.get("symbol") ?? "BTC").trim().toUpperCase();
  if (!(await anyTerminalSym(symbol))) {
    return NextResponse.json({ ok: false, error: `unknown asset ${symbol}` }, { status: 400 });
  }

  const cacheKey = `${symbol}|${minVolUsd}`;
  const hit = cache.get(cacheKey);
  if (hit && Date.now() - hit.at < (hit.body.status === "live" ? 20_000 : 10_000)) {
    return NextResponse.json(hit.body);
  }
  try {
    let refresh = pending.get(cacheKey);
    if (!refresh) {
      refresh = loadOrders(symbol, minVolUsd, hit?.body).then((body) => {
        cache.set(cacheKey, { at: Date.now(), body });
        return body;
      }).finally(() => pending.delete(cacheKey));
      pending.set(cacheKey, refresh);
    }
    return NextResponse.json(await refresh);
  } catch (e) {
    return NextResponse.json(
      { ok: false, error: e instanceof Error ? e.message : "fetch failed" },
      { status: 502 }
    );
  }
}

interface ExchangeCoverage {
  market: string;
  instruments: number;
  openOrders: number;
  hasData: boolean;
  status: "live" | "stale" | "unavailable";
  dataAt: number | null;
}

interface OrdersSnapshot {
  support: LtoSupport;
  perExchange: Record<string, ExchangeCoverage>;
  groups: LtoGroup[];
}

async function loadOrders(symbol: string, minVolUsd: number, previous?: OrdersSnapshot) {
  const cgSym = resolveCgSym(symbol);
  const hasPerp = await knownSym(symbol);
  let support: LtoSupport | null = null;
  let supportAvailable = false;
  const groups: LtoGroup[] = [];
  const seen = new Set<string>();
  const perExchange: Record<string, ExchangeCoverage> = {};

  if (hasPerp) {
    try {
      support = (await cgGet(
        `/api/largeTakerOrder/support/v3?symbol=${encodeURIComponent(cgSym)}`,
        10 * 60_000,
        FAPI
      )) as LtoSupport | null;
      supportAvailable = Array.isArray(support?.futures) || Array.isArray(support?.spot);
    } catch {
      // A failed support lookup can still use the last known exchange list.
    }
    if (!supportAvailable) support = previous?.support ?? null;

    if (support) {
      const sections = [
        ...(support?.futures ?? []).map((s) => ({ ...s, market: "futures" as const })),
        ...(support?.spot ?? []).map((s) => ({ ...s, market: "spot" as const })),
      ];

      const byExchange = new Map<string, { market: string; instruments: number }>();
      for (const s of sections) {
        const prev = byExchange.get(s.exchange);
        byExchange.set(s.exchange, {
          market: prev ? "all" : s.market,
          instruments: (prev?.instruments ?? 0) + (s.instruments?.length ?? 0),
        });
      }
      const exchanges = [...byExchange.entries()];

      const settled = await Promise.allSettled(
        exchanges.map(([ex]) =>
          cgGet(
            `/api/largeTakerOrder/v3?exchange=${encodeURIComponent(ex)}&symbol=${encodeURIComponent(
              cgSym
            )}&market=all&limit=3000${minVolUsd > 0 ? `&minVolUsd=${minVolUsd}` : ""}`,
            0,
            FAPI
          )
        )
      );

      settled.forEach((r, i) => {
        const [ex, meta] = exchanges[i];
        const data = r.status === "fulfilled" ? r.value : null;
        const wrapped = (data as { data?: unknown } | null)?.data;
        const fresh = Array.isArray(data) ? data : Array.isArray(wrapped) ? wrapped : null;
        const last = previous?.perExchange[ex]?.dataAt;
        const stale = !fresh && last != null && Date.now() - last < 10 * 60_000;
        const entry = (perExchange[ex] = {
          market: meta.market,
          instruments: meta.instruments,
          openOrders: 0,
          hasData: fresh !== null || stale,
          status: fresh ? "live" : stale ? "stale" : "unavailable",
          dataAt: fresh ? Date.now() : stale ? last : null,
        });
        const exchangeGroups = fresh ?? (stale ? previous?.groups.filter((g) => g.instrument.exName === ex) : null) ?? [];
        for (const g of exchangeGroups as LtoGroup[]) {
          const inst = g?.instrument;
          if (!inst?.instrumentId || !Array.isArray(g.list)) continue;
          const key = `${inst.exName}|${inst.instrumentId}|${inst.type}`;
          if (seen.has(key)) continue;
          const list = g.list.filter(
            (it) => it && Number.isFinite(it.price) && it.price > 0 && (it.state == null || it.state === 1)
              && Number.isFinite(it.currentUsd) && it.currentUsd > 0 && it.currentUsd >= minVolUsd
          );
          if (!list.length) continue;
          seen.add(key);
          entry.openOrders += list.length;
          groups.push({ instrument: inst, list });
        }
      });
    }
  }

  // Hyperliquid xyz live L2 resting levels + recent trades when HL maps this symbol
  let hlFallback: {
    coin: string;
    bids: { price: number; usd: number; sz: number }[];
    asks: { price: number; usd: number; sz: number }[];
    recentTrades: { time: number; px: number; sz: number; usd: number; side: "buy" | "sell" }[];
  } | null = null;
  const available = Object.values(perExchange);
  const live = available.filter((venue) => venue.status === "live").length;
  const retained = available.filter((venue) => venue.status === "stale").length;
  const archive = symbol === "BTC" && live + retained === 0 && (!supportAvailable || available.length > 0)
    ? lastBtcSnapshot(minVolUsd) : null;
  const hlCoin = !live && !retained && !archive ? hlCoinOf(symbol) : null;
  if (hlCoin) {
    const [ctxBook, trades] = await Promise.all([
      fetchHlCtxAndBook(symbol).catch(() => null),
      fetchHlRecentTrades(hlCoin).catch(() => []),
    ]);
    if (ctxBook?.book || trades.length) {
      hlFallback = {
        coin: hlCoin,
        bids: (ctxBook?.book?.bids ?? [])
          .map((b) => ({ price: b.px, sz: b.sz, usd: Math.round(b.px * b.sz) }))
          .filter((b) => b.usd >= Math.min(minVolUsd, 10_000))
          .slice(0, 15),
        asks: (ctxBook?.book?.asks ?? [])
          .map((a) => ({ price: a.px, sz: a.sz, usd: Math.round(a.px * a.sz) }))
          .filter((a) => a.usd >= Math.min(minVolUsd, 10_000))
          .slice(0, 15),
        recentTrades: trades.slice(0, 40),
      };
    }
  }

  const status = live
    ? live === available.length && supportAvailable ? "live" : "partial"
    : retained || archive ? "stale"
    : !hasPerp || (supportAvailable && !available.length) ? "unsupported" : "unavailable";
  return {
    ok: true,
    supported: status !== "unsupported" || !!hlFallback,
    symbol,
    minVolUsd,
    support: { spot: support?.spot ?? [], futures: support?.futures ?? [] },
    perExchange,
    groups,
    status,
    archive,
    hlFallback,
    updatedAt: archive?.at ?? Math.max(0, ...available.map((venue) => venue.dataAt ?? 0)),
  };
}
