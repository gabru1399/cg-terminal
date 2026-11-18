"use client";

import { useEffect, useMemo, useState } from "react";
import { usePolling } from "./use-cg-data";
import type { PlaybookCard, PlaybookContext } from "@/lib/strategy/playbook";
import type { DeskLiveSnapshot } from "@/lib/desk/live";

/**
 * PlaybookDesk — the Punch-Trade panel.
 *
 * Shows live candidate cards from the VALIDATED engines (EA-2 sweep-acceptance,
 * EA-5 cascade-exhaustion ETH/SOL, EA-6 SMC BOS+FVG — R546/R547 backtests on real
 * Binance 15m data), each with its structural stop and 40/40/20 target ladder.
 * PUNCH queues the card into desk/state.json (status "suggested") + desk/inbox/WAKE.md
 * so atg-exec executes it on Delta Exchange India — the desk's own wake protocol.
 * Punched orders and their lifecycle status show below from /api/desk/live.
 */

interface CardsPayload {
  ok: boolean;
  ts: number;
  engines: Record<string, string>;
  suspended: string[];
  weights: Record<string, number>;
  assets: { sym: string; ok: boolean; error?: string; cards: PlaybookCard[]; ctx: PlaybookContext | null }[];
}

const ENGINE_STYLE: Record<string, string> = {
  EA2: "bg-sky-500/15 text-sky-300 ring-sky-500/40",
  EA5: "bg-violet-500/15 text-violet-300 ring-violet-500/40",
  EA6: "bg-amber-500/15 text-amber-300 ring-amber-500/40",
};
const STATUS_STYLE: Record<string, string> = {
  confirmed: "bg-emerald-500/15 text-emerald-300",
  armed: "bg-neutral-500/15 text-neutral-300",
  "pending-fill": "bg-cyan-500/15 text-cyan-300",
};

function fmt(v: number | null | undefined): string {
  if (v == null || !Number.isFinite(v)) return "–";
  const abs = Math.abs(v);
  const decs = abs >= 1000 ? 1 : abs >= 10 ? 2 : abs >= 0.1 ? 4 : 6;
  return v.toLocaleString("en-US", { minimumFractionDigits: decs, maximumFractionDigits: decs });
}

export function PlaybookDesk({ sym }: { sym: string }) {
  const cards = usePolling<CardsPayload>(`/api/strategy/cards?sym=${encodeURIComponent(sym)}`, 30_000);
  const desk = usePolling<DeskLiveSnapshot>("/api/desk/live", 30_000);
  const [equity, setEquity] = useState("10000");
  const [riskPct, setRiskPct] = useState("0.25");
  const [punching, setPunching] = useState<string | null>(null);
  const [punched, setPunched] = useState<Record<string, string>>({});
  const [dest, setDest] = useState<"mt5" | "desk">("mt5");
  const [mt5Symbols, setMt5Symbols] = useState<Record<string, { symbol: string; basisPct: number | null; fresh: boolean }>>({});
  const [now, setNow] = useState(Date.now());
  useEffect(() => {
    const t = setInterval(() => setNow(Date.now()), 15_000);
    return () => clearInterval(t);
  }, []);

  // MT5 symbol resolution — light GET on the punch route (reads desk/mt5.json server-side)
  useEffect(() => {
    let alive = true;
    fetch("/api/desk/mt5-punch")
      .then((r) => r.json())
      .then((d: { ok: boolean; symbols?: Record<string, { symbol: string; basisPct: number | null; fresh: boolean }> }) => {
        if (alive && d.ok && d.symbols) setMt5Symbols(d.symbols);
      })
      .catch(() => {});
    const t = setInterval(() => {
      fetch("/api/desk/mt5-punch")
        .then((r) => r.json())
        .then((d: { ok: boolean; symbols?: Record<string, { symbol: string; basisPct: number | null; fresh: boolean }> }) => {
          if (alive && d.ok && d.symbols) setMt5Symbols(d.symbols);
        })
        .catch(() => {});
    }, 60_000);
    return () => {
      alive = false;
      clearInterval(t);
    };
  }, []);

  const asset = cards.data?.assets?.[0];
  const ctx = asset?.ctx ?? null;
  const liveCards = useMemo(
    () => (asset?.cards ?? []).filter((c) => c.validUntilTs >= now && (c.targets[0] > 0 || c.status === "armed")),
    [asset, now]
  );
  const punchedOrders = useMemo(
    () => (desk.data?.orders ?? []).filter((o) => (o as { mode?: string }).mode === "terminal-punch" || (o as { mode?: string }).mode === "terminal-mt5-punch").slice(0, 8),
    [desk]
  );

  async function punch(card: PlaybookCard) {
    setPunching(card.id);
    try {
      const endpoint = dest === "mt5" ? "/api/desk/mt5-punch" : "/api/desk/punch";
      const res = await fetch(endpoint, {
        method: "POST",
        headers: { "Content-Type": "application/json" },
        body: JSON.stringify({ card, equity: Number(equity) || undefined, riskPct: Number(riskPct) || undefined }),
      });
      const j = (await res.json()) as { ok: boolean; orderId?: string; error?: string; ticket?: number; lots?: number; riskUsd?: number; mt5Symbol?: string };
      setPunched((p) => ({
        ...p,
        [card.id]: j.ok
          ? dest === "mt5"
            ? `MT5 ticket ${j.ticket} · ${j.mt5Symbol} ${j.lots} lots · $${j.riskUsd}`
            : `queued ${j.orderId}`
          : `failed: ${j.error}`,
      }));
    } catch (e) {
      setPunched((p) => ({ ...p, [card.id]: `failed: ${e instanceof Error ? e.message : "network"}` }));
    } finally {
      setPunching(null);
    }
  }

  return (
    <div className="flex flex-col gap-3">
      <div className="flex flex-wrap items-center justify-between gap-2 rounded-lg border border-amber-800/40 bg-[#11151a] p-4">
        <div>
          <div className="text-sm font-semibold text-neutral-100">{sym} · Validated Playbook & Punch Trade</div>
          <div className="mt-1 text-xs text-neutral-400">
            EA-2 sweep-acceptance · EA-5 cascade-exhaustion (ETH/SOL) · EA-6 SMC BOS+FVG — 1:1 parity ports of the R546/R548 backtests (120/120 replay-exact). PUNCH fires the order: MT5 DIRECT (this PC's MetaTrader) or DESK QUEUE (atg-exec, Delta India).
          </div>
        </div>
        <span className="rounded bg-amber-500/15 px-2 py-0.5 text-[10px] font-semibold text-amber-300">PF 1.50 · maxDD 26.2R · weights EA5 .467 / EA2 .30 / EA6 .233</span>
      </div>

      {/* punch destination */}
      <div className="flex flex-wrap items-center gap-2 rounded-lg border border-neutral-800/80 bg-[#0d1117] px-3 py-2 text-xs">
        <span className="text-neutral-500 uppercase tracking-wider text-[10px] font-semibold">punch destination</span>
        {([["mt5", "MT5 DIRECT ▸ this PC's MetaTrader"], ["desk", "DESK QUEUE ▸ atg-exec (Delta India)"]] as const).map(([v, label]) => (
          <button
            key={v}
            onClick={() => setDest(v)}
            className={`rounded-md px-3 py-1 font-semibold transition-colors ${dest === v ? (v === "mt5" ? "bg-amber-600 text-white" : "bg-sky-600 text-white") : "bg-neutral-800 text-neutral-400 hover:bg-neutral-700"}`}
          >
            {label}
          </button>
        ))}
        {dest === "mt5" && (
          <span className="text-neutral-500">
            {mt5Symbols[sym]
              ? `→ ${mt5Symbols[sym].symbol}${mt5Symbols[sym].basisPct != null ? ` · basis ${mt5Symbols[sym].basisPct}%${mt5Symbols[sym].fresh ? "" : " (stale)"}` : ""} · $6 prop risk cap · comment cg_terminal`
              : "· no MT5 symbol mapped for this asset (desk/mt5.json) — punch will be rejected"}
          </span>
        )}
      </div>

      {/* session context strip */}
      <div className="grid grid-cols-2 gap-2 sm:grid-cols-4 lg:grid-cols-8">
        {[
          ["VWAP", fmt(ctx?.vwap)],
          ["±1σ", ctx?.vwap != null && ctx?.sigma != null ? fmt(ctx.vwap - ctx.sigma) : "–"],
          ["POC", fmt(ctx?.rPOC)],
          ["VAH", fmt(ctx?.rVAH)],
          ["VAL", fmt(ctx?.rVAL)],
          ["PDH", fmt(ctx?.pdh)],
          ["PDL", fmt(ctx?.pdl)],
          ["h4 bias", ctx?.biasUp == null ? "–" : ctx.biasUp ? "UP" : "DOWN"],
        ].map(([k, v]) => (
          <div key={k} className="rounded-md border border-neutral-800/80 bg-[#0d1117] px-2.5 py-1.5">
            <div className="text-[9px] uppercase tracking-wider text-neutral-500">{k}</div>
            <div className="font-mono text-xs font-bold tabular-nums text-neutral-100">{v}</div>
          </div>
        ))}
      </div>

      {/* sizing inputs */}
      <div className="flex flex-wrap items-center gap-3 rounded-lg border border-neutral-800/80 bg-[#0d1117] px-3 py-2 text-xs text-neutral-400">
        <label className="flex items-center gap-1.5">
          equity $
          <input value={equity} onChange={(e) => setEquity(e.target.value)} inputMode="decimal"
            className="w-24 rounded border border-neutral-700 bg-neutral-900 px-2 py-1 font-mono text-xs text-neutral-100 outline-none focus:border-amber-500/60" />
        </label>
        <label className="flex items-center gap-1.5">
          risk/trade %
          <input value={riskPct} onChange={(e) => setRiskPct(e.target.value)} inputMode="decimal"
            className="w-16 rounded border border-neutral-700 bg-neutral-900 px-2 py-1 font-mono text-xs text-neutral-100 outline-none focus:border-amber-500/60" />
        </label>
        <span className="text-neutral-500">qty hint = equity × risk% × engine weight ÷ stop distance · live-start 0.25% until 50 fills confirm</span>
      </div>

      {/* cards */}
      {!cards.data && <div className="rounded-lg border border-neutral-800 bg-[#0d1117] p-6 text-sm text-neutral-500">loading playbook…</div>}
      {cards.data && !asset?.ok && (
        <div className="rounded-lg border border-neutral-800 bg-[#0d1117] p-6 text-sm text-neutral-400">
          playbook data unavailable: {asset?.error ?? "upstream klines unreachable (fapi circuit breaker may be open — try again shortly)"}
        </div>
      )}
      {cards.data && asset?.ok && liveCards.length === 0 && (
        <div className="rounded-lg border border-neutral-800 bg-[#0d1117] p-6 text-sm text-neutral-400">
          No live {sym} cards. The engines are quiet — no sweep, cascade or BOS+FVG window is active on the last 15m closes. Cards appear only when the exact validated trigger conditions print; nothing is invented.
        </div>
      )}
      {liveCards.map((c) => {
        const ageMin = Math.max(0, Math.round((now - c.signalTs) / 60_000));
        const state = punched[c.id];
        return (
          <div key={c.id} className="rounded-lg border border-neutral-800/90 bg-[#0d1117] p-3.5">
            <div className="flex flex-wrap items-center gap-2">
              <span className={`rounded px-1.5 py-0.5 font-mono text-[10px] font-bold ring-1 ${ENGINE_STYLE[c.engine]}`}>{c.engine}</span>
              <span className={`rounded px-1.5 py-0.5 font-mono text-[10px] font-bold ${c.side === "long" ? "bg-emerald-500/15 text-emerald-300" : "bg-red-500/15 text-red-300"}`}>
                {c.side.toUpperCase()}
              </span>
              <span className={`rounded px-1.5 py-0.5 font-mono text-[10px] font-semibold ${STATUS_STYLE[c.status] ?? "bg-neutral-500/15 text-neutral-300"}`}>{c.status}</span>
              <span className="font-mono text-[10px] text-neutral-500">{c.kind} · {ageMin}m ago · weight {c.weight}</span>
              <span className="ml-auto font-mono text-[10px] text-neutral-500">R {c.rPlanned}</span>
            </div>
            <div className="mt-2 grid grid-cols-2 gap-2 sm:grid-cols-3 lg:grid-cols-6">
              {[
                ["entry", c.entry],
                ["stop", c.stop],
                ["T1", c.targets[0] || null],
                ["T2", c.targets[1] || null],
                ["T3", c.targets[2] || null],
              ].map(([k, v]) => (
                <div key={k as string} className="rounded-md border border-neutral-800/80 bg-[#11151a] px-2.5 py-1.5">
                  <div className="text-[9px] uppercase tracking-wider text-neutral-500">{k as string}</div>
                  <div className="font-mono text-xs font-bold tabular-nums text-neutral-100">{fmt(v as number)}</div>
                </div>
              ))}
              <div className="rounded-md border border-neutral-800/80 bg-[#11151a] px-2.5 py-1.5">
                <div className="text-[9px] uppercase tracking-wider text-neutral-500">qty hint</div>
                <div className="font-mono text-xs font-bold tabular-nums text-neutral-100">
                  {Number(equity) > 0 && Math.abs(c.entry - c.stop) > 0 && c.targets[0] > 0
                    ? fmt((Number(equity) * Number(riskPct) * c.weight) / 100 / Math.abs(c.entry - c.stop))
                    : "–"}
                </div>
              </div>
            </div>
            <div className="mt-2 flex flex-wrap items-center justify-between gap-2">
              <div className="text-[11px] text-neutral-400">{c.note}</div>
              {c.targets[0] > 0 ? (
                <button
                  onClick={() => punch(c)}
                  disabled={punching === c.id || Boolean(state)}
                  className={`rounded-md px-4 py-1.5 text-xs font-bold transition-all ${
                    state || punching === c.id
                      ? "bg-neutral-700 text-neutral-400"
                      : dest === "mt5"
                      ? "bg-amber-600 text-white hover:bg-amber-500 shadow-[0_0_16px_-6px_rgba(245,158,11,0.7)]"
                      : c.side === "long"
                      ? "bg-emerald-600 text-white hover:bg-emerald-500 shadow-[0_0_16px_-6px_rgba(16,185,129,0.7)]"
                      : "bg-red-600 text-white hover:bg-red-500 shadow-[0_0_16px_-6px_rgba(239,68,68,0.7)]"
                  }`}
                >
                  {punching === c.id ? (dest === "mt5" ? "sending to MT5…" : "queuing…") : state ? state : dest === "mt5" ? `PUNCH ${c.side.toUpperCase()} ▸ MT5` : `PUNCH ${c.side.toUpperCase()} ▸ atg-exec`}
                </button>
              ) : (
                <span className="rounded bg-neutral-800 px-3 py-1.5 text-[10px] text-neutral-500">armed — punch enabled once the confirmation close prints</span>
              )}
            </div>
          </div>
        );
      })}

      {/* punched orders lifecycle */}
      {punchedOrders.length > 0 && (
        <div className="rounded-lg border border-neutral-800/90 bg-[#0d1117] p-3.5">
          <div className="mb-2 text-xs font-semibold uppercase tracking-wider text-neutral-400">Punched orders → atg-exec lifecycle</div>
          <div className="overflow-x-auto">
            <table className="w-full text-left font-mono text-[11px]">
              <thead>
                <tr className="text-neutral-500">
                  {["id", "sym", "side", "status", "entry", "stop", "ticket"].map((h) => (
                    <th key={h} className="px-2 py-1 font-normal">{h}</th>
                  ))}
                </tr>
              </thead>
              <tbody className="text-neutral-200">
                {punchedOrders.map((o) => (
                  <tr key={o.id} className="border-t border-neutral-800/60">
                    <td className="px-2 py-1 text-neutral-500">{o.id}</td>
                    <td className="px-2 py-1">{o.sym}</td>
                    <td className={`px-2 py-1 ${o.side === "long" ? "text-emerald-300" : "text-red-300"}`}>{o.side}</td>
                    <td className="px-2 py-1">{o.status}</td>
                    <td className="px-2 py-1">{fmt(o.entry)}</td>
                    <td className="px-2 py-1">{fmt(o.stop)}</td>
                    <td className="px-2 py-1">{o.ticket ?? "–"}</td>
                  </tr>
                ))}
              </tbody>
            </table>
          </div>
        </div>
      )}

      <div className="text-[10px] leading-relaxed text-neutral-500">
        Engines: {Object.entries(cards.data?.engines ?? {}).map(([k, v]) => `${k} ${v}`).join(" · ")} — portfolio PF 1.50, +128.1R weighted, maxDD 26.2R, engine correlations ≤ 0.12 (201-day real-data validation, net of fees/slippage, stop-first worst-case fills; EA-6 re-validated no-lookahead R548).
        Suspended and never emitted: {(cards.data?.suspended ?? ["EA1", "EA3", "EA4", "EA7", "EA8"]).join(", ")}. Cards expire when their entry window closes; the tape decides, the panel only reports it. MT5 DIRECT punches carry the T1 rung as the broker TP; the 40/40/20 ladder and auto-BE are then managed by the desk's cg_terminal loop (scripts/mt5_cg_trader.py --auto-be).
      </div>
    </div>
  );
}
