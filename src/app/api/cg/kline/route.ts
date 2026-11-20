import { NextRequest, NextResponse } from "next/server";
import { cgGet } from "@/lib/cg/client";
import { parseInterval, clampLimit, instrumentKeyOK } from "@/lib/cg/params";
import { fetchBinCandles } from "@/lib/cg/fallbacks";
import { archivedCandles } from "@/lib/cg/store";
import type { KlineRow, OiKlineRow } from "@/lib/cg/types";

export const dynamic = "force-dynamic";

export async function GET(req: NextRequest) {
  const sp = req.nextUrl.searchParams;
  const type = sp.get("type") === "oi" ? "oi_kline" : "kline";
  const interval = parseInterval(sp.get("interval"));
  if (!interval) {
    return NextResponse.json({ ok: false, error: "invalid interval" }, { status: 400 });
  }
  const limit = clampLimit(sp.get("limit"), 300, 2880);
  const symbol = sp.get("symbol") ?? "Binance_BTCUSDT";
  if (!instrumentKeyOK(symbol)) {
    return NextResponse.json({ ok: false, error: `invalid symbol ${symbol}` }, { status: 400 });
  }
  try {
    let rows: KlineRow[] | OiKlineRow[] | null = null;

    const pair = /^Binance_([A-Z0-9]+)USDT$/.exec(symbol);
    if (type === "kline" && pair && limit <= 1500) {
      const bin = await fetchBinCandles(pair[1], interval, limit).catch(() => []);
      if (bin.length) {
        rows = bin.slice(-limit).map((b) => [Math.floor(b.t / 1000), b.o, b.h, b.l, b.c, b.v] as unknown as KlineRow);
      }
    }

    if (!rows || !rows.length) {
      const payload = await cgGet(
        `/api/v2/kline?symbol=${encodeURIComponent(`${symbol}#${type}`)}&interval=${interval}&minLimit=false&limit=${limit}`,
        15_000
      );
      rows = (Array.isArray(payload) ? payload : (payload as { data?: unknown } | null)?.data) as typeof rows;
    }

    if (!Array.isArray(rows)) {
      throw new Error("Invalid Coinglass candle response");
    }
    if (!rows.length && type === "kline" && interval === "m15") throw new Error("No candle history returned");
    return NextResponse.json({ ok: true, symbol, interval, type, rows });
  } catch (e) {
    if (type === "kline" && interval === "m15") {
      const cached = archivedCandles(symbol, limit);
      if (cached.length) {
        const rows: KlineRow[] = cached.map((b) => [Math.floor(b.t / 1000), b.o, b.h, b.l, b.c, b.v]);
        return NextResponse.json({ ok: true, symbol, interval, type, rows, source: "candle archive", stale: true, dataAt: cached.at(-1)?.t });
      }
    }
    return NextResponse.json({ ok: false, error: e instanceof Error ? e.message : "fetch failed" }, { status: 502 });
  }
}
