import { NextRequest, NextResponse } from "next/server";
import { fetchBinCandles } from "@/lib/cg/fallbacks";
import { runPlaybook, type PlaybookCandle, type PlaybookCard, ENGINE_EVIDENCE, EA5_SYMS } from "@/lib/strategy/playbook";

export const dynamic = "force-dynamic";

/**
 * GET /api/strategy/cards?sym=BTC (optional; default scans the crypto-major desk set)
 *
 * Runs the VALIDATED playbook engines (EA-2 sweep-acceptance, EA-5 cascade-exhaustion
 * ETH/SOL, EA-6 SMC BOS+FVG) on real Binance 15m klines (taker-buy split included)
 * over the last ~1000 bars and returns live candidate cards. Rules are the 1:1 port
 * of the backtest (R546/R547) — the same logic that earned the validated numbers.
 * Data flows through the shared fapi circuit breaker; on 429/418 the route serves
 * a stale-marked empty set rather than hammering.
 */
const DEFAULT_SYMS = ["BTC", "ETH", "SOL"];

export async function GET(req: NextRequest) {
  const symParam = req.nextUrl.searchParams.get("sym")?.trim().toUpperCase() ?? "";
  const syms = symParam ? [symParam] : DEFAULT_SYMS;
  const out: { sym: string; ok: boolean; error?: string; cards: PlaybookCard[]; ctx: unknown }[] = [];
  const now = Date.now();

  await Promise.all(
    syms.map(async (s) => {
      try {
        const candles = await fetchBinCandles(s, "m15", 1000);
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
