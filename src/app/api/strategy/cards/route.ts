import { NextRequest, NextResponse } from "next/server";
import { fetchBinCandles } from "@/lib/cg/fallbacks";
import { runPlaybook, type PlaybookCandle, type PlaybookCard, ENGINE_EVIDENCE, EA5_SYMS } from "@/lib/strategy/playbook";

export const dynamic = "force-dynamic";

/**
 * GET /api/strategy/cards?sym=BTC (optional; default scans the crypto-major desk set)
 *
 * Runs the VALIDATED playbook engines (EA-2 sweep-acceptance, EA-5 cascade-exhaustion
 * ETH/SOL, EA-6 SMC BOS+FVG) on real Binance 15m klines (taker-buy split included)
 * and returns live candidate cards. Rules are the parity-verified 1:1 port of the
 * backtests (R546/R548) — scripts/parity_replay.py replayed 120 real signal windows
 * through this exact engine with 100% entry/stop/target agreement.
 *
 * 4500 bars (≈47 days) are fetched so the h4 EMA89 bias converges like the backtest's
 * full-history warmup (0.2% residual seed influence — verified in the parity replay);
 * only the last ~8 bars can emit cards. Data flows through the shared fapi circuit
 * breaker; on 429/418 the route serves a stale-marked empty set rather than hammering.
 */
const DEFAULT_SYMS = ["BTC", "ETH", "SOL"];

/**
 * History-page cache: pages 2-3 of the kline window are CLOSED bars — immutable
 * data — so they are fetched once per symbol per 15 minutes and reused. Steady
 * state costs one 1500-bar call per scan instead of three (fapi weight 2, not 6).
 */
const histCache = new Map<string, { rows: { t: number; o: number; h: number; l: number; c: number; v: number; tbb: number }[]; ts: number }>();
const HIST_TTL = 15 * 60_000;

export async function GET(req: NextRequest) {
  const symParam = req.nextUrl.searchParams.get("sym")?.trim().toUpperCase() ?? "";
  const syms = symParam
    ? symParam.split(",").map((s) => s.trim()).filter(Boolean)
    : DEFAULT_SYMS;
  const out: { sym: string; ok: boolean; error?: string; cards: PlaybookCard[]; ctx: unknown }[] = [];
  const now = Date.now();

  await Promise.all(
    syms.map(async (s) => {
      try {
        // Page 1: trailing 1500 bars (fresh every scan). Pages 2-3: closed history,
        // cached per symbol for 15 min (immutable data — see histCache docs).
        const fresh = await fetchBinCandles(s, "m15", 1500).catch(() => [] as never);
        if (!fresh.length) {
          out.push({ sym: s, ok: false, error: "no kline data (upstream unavailable or stale)", cards: [], ctx: null });
          return;
        }
        const cacheKey = s.toUpperCase();
        let cached = histCache.get(cacheKey);
        if (!cached || Date.now() - cached.ts > HIST_TTL || !cached.rows.length) {
          const oldest: number[] = [];
          let hist: Awaited<ReturnType<typeof fetchBinCandles>> = [];
          for (let page = 0; page < 2; page++) {
            const batch = await fetchBinCandles(s, "m15", 1500, undefined, undefined, oldest[page - 1]).catch(() => [] as never);
            if (!batch.length) break;
            hist = hist.concat(batch);
            oldest.push(batch[0].t);
            if (batch.length < 1500) break;
          }
          cached = {
            rows: hist.map((x) => ({ t: x.t, o: x.o, h: x.h, l: x.l, c: x.c, v: x.v, tbb: x.tbb ?? 0 })),
            ts: Date.now(),
          };
          histCache.set(cacheKey, cached);
        }
        // combine: cached history + fresh tail, de-dup on open time, chronological
        const seen = new Set<number>();
        const candles = [...cached.rows, ...fresh]
          .filter((x) => (seen.has(x.t) ? false : (seen.add(x.t), true)))
          .sort((a, b) => a.t - b.t);
        if (!candles.length) {
          out.push({ sym: s, ok: false, error: "no kline data (upstream unavailable or stale)", cards: [], ctx: null });
          return;
        }
        const cs: PlaybookCandle[] = candles
          // drop the forming bar: signals evaluate CLOSED bars only
          .filter((c) => c.t + 15 * 60_000 <= now)
          .map((c) => ({ t: c.t, o: c.o, h: c.h, l: c.l, c: c.c, v: c.v, tbb: c.tbb ?? 0 }));
        const { cards, ctx } = runPlaybook(cs, `${s.toUpperCase()}USDT`);
        out.push({
          sym: s,
          ok: true,
          cards: cards.map((c) =>
            EA5_SYMS.has(s) ? c : { ...c, note: c.engine === "EA5" ? `${c.note} (engine not live on ${s})` : c.note }
          ),
          ctx,
        });
      } catch (e) {
        out.push({ sym: s, ok: false, error: e instanceof Error ? e.message : "playbook failed", cards: [], ctx: null });
      }
    })
  );

  return NextResponse.json({
    ok: out.some((o) => o.ok),
    ts: now,
    engines: ENGINE_EVIDENCE,
    suspended: ["EA1", "EA3", "EA4", "EA7", "EA8"],
    weights: { EA2: 0.3, EA5: 0.467, EA6: 0.233 },
    assets: out,
  });
}
