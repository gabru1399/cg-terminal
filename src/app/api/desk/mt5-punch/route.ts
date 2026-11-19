import { NextRequest, NextResponse } from "next/server";
import { existsSync, readFileSync, appendFileSync, writeFileSync, mkdirSync } from "node:fs";
import { spawn } from "node:child_process";
import path from "node:path";
import type { PlaybookCard } from "@/lib/strategy/playbook";

export const dynamic = "force-dynamic";

/**
 * POST /api/desk/mt5-punch — PUNCH the card STRAIGHT into local MT5.
 *
 * Runs on the user's PC next to the MetaTrader terminal (same machine as
 * `npm start`). Pipeline:
 *   1. resolve the broker symbol: card.sym (e.g. SOLUSDT) → base (SOL) →
 *      config.symbol_map (SOLUSD) → broker-suffixed name (SOLUSD.p) using the
 *      symbol keys live in desk/mt5.json (fallback: desk/mt5_symbols_universe.json)
 *   2. translate the card levels from perp (Binance) prices to MT5 CFD prices
 *      with the live basis recorded in desk/mt5.json (mt5 = perp × (1+basis/100));
 *      if mt5.json is stale/missing, levels go through untranslated and the
 *      response says so
 *   3. spawn `python scripts/mt5_punch.py` (python_cmd from desk/daemon.json)
 *      which enforces the prop-account guards ($6 risk cap, cg_terminal comment,
 *      magic 42001, drawdown floors) and calls mt5.order_send
 *   4. mirror the ticket into desk/state.json (status "placed-mt5") + a WAKE.md
 *      EXEC log line so the desk files stay the single source of truth
 *
 * The T1 bracket is what the MT5 order carries as TP (the 40/40/20 scale-out
 * is then managed by the desk's auto-BE/ratchet loop in mt5_cg_trader.py).
 */
interface Mt5PunchBody {
  card: PlaybookCard;
  riskUsd?: number; // optional: only ever LOWERS the $6 prop cap
}

const ROOT = (() => {
  // standalone production runs with cwd .next/standalone, where scripts/ is not
  // copied — walk up from the cwd until BOTH desk/state.json and scripts/mt5_punch.py
  // exist (the real repo root), falling back to cwd for dev mode.
  const cwd = process.cwd();
  const candidates = [cwd, path.resolve(cwd, ".."), path.resolve(cwd, "..", "..")];
  for (const dir of candidates) {
    if (existsSync(path.join(dir, "scripts", "mt5_punch.py")) && existsSync(path.join(dir, "desk", "state.json"))) return dir;
  }
  for (const dir of candidates) {
    if (existsSync(path.join(dir, "desk", "state.json"))) return dir;
  }
  return cwd;
})();

function readJson(p: string): any | null {
  try {
    return JSON.parse(readFileSync(p, "utf8"));
  } catch {
    return null;
  }
}

/** base asset (SOLUSDT -> SOL, 1000PEPEUSDT -> 1000PEPE) */
function baseAsset(sym: string): string {
  return sym.replace(/USDT$/i, "").replace(/USDT-M$/i, "").toUpperCase();
}

/** Find the broker symbol for a base: prefer live mt5.json keys, fall back to the universe dump. */
function resolveMt5Symbol(base: string, state: any, mt5: any): { symbol: string; source: string } | null {
  const mapped = state?.config?.symbol_map?.[base];
  const candidates = mapped ? [mapped] : [`${base}USD`, base];
  const live: string[] = mt5?.spreads ? Object.keys(mt5.spreads) : [];
  if (live.length) {
    for (const c of candidates) {
      const exact = live.find((s) => s.toUpperCase() === c.toUpperCase());
      if (exact) return { symbol: exact, source: "mt5.json" };
    }
    for (const c of candidates) {
      const suffixed = live.find((s) => s.toUpperCase().startsWith(`${c.toUpperCase()}.`) || s.toUpperCase().startsWith(`${c.toUpperCase()}PI`));
      if (suffixed) return { symbol: suffixed, source: "mt5.json+suffix" };
    }
    return null;
  }
  // fallback: static universe file
  const uni = readJson(path.join(ROOT, "desk", "mt5_symbols_universe.json"));
  if (uni) {
    const all: string[] = [];
    for (const lst of Object.values<any[]>(uni)) {
      for (const s of lst ?? []) all.push(String(s?.name ?? ""));
    }
    for (const c of candidates) {
      const exact = all.find((s) => s.toUpperCase() === c.toUpperCase());
      if (exact) return { symbol: exact, source: "universe" };
    }
    for (const c of candidates) {
      const suffixed = all.find((s) => s.toUpperCase().startsWith(`${c.toUpperCase()}.`));
      if (suffixed) return { symbol: suffixed, source: "universe+suffix" };
    }
  }
  return null;
}

function sh(cmd: string, args: string[], input: string, timeoutMs: number): Promise<{ code: number; out: string; err: string }> {
  return new Promise((resolve) => {
    const p = spawn(cmd, args, { cwd: ROOT, windowsHide: true });
    let out = "";
    let err = "";
    const timer = setTimeout(() => p.kill("SIGKILL"), timeoutMs);
    p.stdout.on("data", (d) => (out += d));
    p.stderr.on("data", (d) => (err += d));
    p.on("error", (e) => {
      clearTimeout(timer);
      resolve({ code: -1, out, err: String(e) });
    });
    p.on("close", (code) => {
      clearTimeout(timer);
      resolve({ code: code ?? -1, out, err });
    });
    p.stdin.write(input);
    p.stdin.end();
  });
}

export async function GET() {
  // light resolver for the panel: which MT5 symbol (and basis) a punch would use
  const now = Date.now();
  const state = readJson(path.join(ROOT, "desk", "state.json")) ?? {};
  const mt5 = readJson(path.join(ROOT, "desk", "mt5.json"));
  const fresh = mt5?.ts && now - mt5.ts < 10 * 60_000;
  const out: Record<string, { symbol: string; basisPct: number | null; fresh: boolean }> = {};
  const bases = new Set<string>();
  for (const b of Object.keys(state?.config?.symbol_map ?? {})) bases.add(String(b));
  if (mt5?.spreads) {
    for (const [sym, s] of Object.entries<any>(mt5.spreads)) {
      if (s?.asset) bases.add(String(s.asset));
    }
  }
  for (const base of bases) {
    const r = resolveMt5Symbol(base, state, mt5);
    if (!r) continue;
    const spread = mt5?.spreads?.[r.symbol];
    out[base] = { symbol: r.symbol, basisPct: Number.isFinite(Number(spread?.basisPct)) ? Number(spread.basisPct) : null, fresh: Boolean(fresh) };
  }
  return NextResponse.json({ ok: true, ts: now, symbols: out });
}

export async function POST(req: NextRequest) {
  // same-origin guard, same as /api/desk/punch
  const origin = req.headers.get("origin");
  const host = req.headers.get("host");
  if (origin) {
    try {
      if (new URL(origin).host !== host) {
        return NextResponse.json({ ok: false, error: "cross-origin API calls are not allowed" }, { status: 403 });
      }
    } catch {
      return NextResponse.json({ ok: false, error: "bad origin" }, { status: 403 });
    }
  }

  let body: Mt5PunchBody;
  try {
    body = (await req.json()) as Mt5PunchBody;
  } catch {
    return NextResponse.json({ ok: false, error: "invalid JSON body" }, { status: 400 });
  }
  const card = body?.card;
  if (!card || !card.engine || !card.sym || !["long", "short"].includes(card.side)
      || !Number.isFinite(card.entry) || !Number.isFinite(card.stop)
      || card.entry <= 0 || card.stop <= 0) {
    return NextResponse.json({ ok: false, error: "card missing engine/sym/side/entry/stop" }, { status: 400 });
  }
  if (card.status === "armed" || !Array.isArray(card.targets) || !card.targets.some((t) => t > 0)) {
    return NextResponse.json({ ok: false, error: "armed card — punch enabled once the confirmation close prints" }, { status: 400 });
  }

  const now = Date.now();
  const state = readJson(path.join(ROOT, "desk", "state.json")) ?? {};
  const mt5 = readJson(path.join(ROOT, "desk", "mt5.json"));
  const daemon = readJson(path.join(ROOT, "desk", "daemon.json"));
  const pythonCmd = daemon?.mt5?.python_cmd ?? "python";

  const base = baseAsset(card.sym);
  const resolved = resolveMt5Symbol(base, state, mt5);
  if (!resolved) {
    return NextResponse.json(
      { ok: false, error: `no MT5 symbol for ${base} — run scripts/list_all_mt5_symbols.py and map it in desk/state.json config.symbol_map` },
      { status: 400 }
    );
  }

  // level translation: perp -> MT5 CFD via live basis (if mt5.json is fresh)
  const spread = mt5?.spreads?.[resolved.symbol];
  const basisPct = Number(spread?.basisPct);
  const fresh = mt5?.ts && now - mt5.ts < 10 * 60_000;
  const tr = (lvl: number) => (fresh && Number.isFinite(basisPct) ? lvl * (1 + basisPct / 100) : lvl);
  const entry = tr(card.entry);
  const stop = tr(card.stop);
  const direction = card.side === "long" ? 1 : -1;
  const stopDist = direction * (card.entry - card.stop);
  if (stopDist <= 0) {
    return NextResponse.json({ ok: false, error: "Stop must be on the adverse side of entry" }, { status: 400 });
  }
  const targetLevel = card.targets.find((t) =>
    Number.isFinite(t) && t > 0 && direction * (t - card.entry) >= 2 * stopDist
  );
  if (targetLevel === undefined) {
    return NextResponse.json({ ok: false, error: "No supplied target delivers at least 2.00R" }, { status: 400 });
  }
  const tp = tr(targetLevel);

  const payload = {
    symbol: resolved.symbol,
    side: card.side,
    kind: card.kind === "limit" ? "limit" : "market",
    entry,
    stop,
    tp,
    risk_usd: Number.isFinite(body.riskUsd) ? body.riskUsd : undefined,
    order_id: `mt5-${now}`,
  };

  const r = await sh(pythonCmd, ["scripts/mt5_punch.py"], JSON.stringify(payload), 60_000);
  let placed: any = null;
  try {
    placed = JSON.parse(r.out.trim().split("\n").pop() || "null");
  } catch {
    placed = null;
  }
  if (r.code !== 0 || !placed?.ok) {
    return NextResponse.json(
      { ok: false, error: placed?.error ?? r.err?.slice(0, 300) ?? `python exited ${r.code} (is the MT5 terminal + MetaTrader5 pip package installed on this PC?)`, resolved: resolved.symbol },
      { status: 502 }
    );
  }

  // mirror into desk/state.json + WAKE so the desk files stay the ledger
  let ledgerWarning: string | undefined;
  const order = {
    id: payload.order_id,
    round: "R548",
    sym: card.sym,
    side: card.side,
    action: card.side,
    type: card.kind === "limit" ? "limit" : "market",
    status: "placed-mt5",
    source: "terminal-mt5-punch",
    engine: card.engine,
    entry: card.entry,
    stop: card.stop,
    targets: card.targets,
    riskR: card.rPlanned,
    riskPct: null,
    regime: `playbook:${card.engine}`,
    mode: "terminal-mt5-punch",
    rationale: card.note,
    mt5Symbol: resolved.symbol,
    mt5Lots: placed.lots,
    mt5RiskUsd: placed.risk_usd,
    mt5BasisPct: fresh && Number.isFinite(basisPct) ? basisPct : null,
    ticket: placed.ticket,
    createdTs: now,
  };
  try {
    const statePath = path.join(ROOT, "desk", "state.json");
    const latestState = readJson(statePath);
    if (!latestState || typeof latestState !== "object") throw new Error("Desk ledger is unavailable");
    const ordersAny = latestState.orders;
    if (Array.isArray(ordersAny)) {
      ordersAny.push(order);
    } else {
      latestState.orders = [order];
    }
    mkdirSync(path.dirname(statePath), { recursive: true });
    writeFileSync(statePath, JSON.stringify(latestState, null, 2) + "\n");
    const wakePath = path.join(ROOT, "desk", "inbox", "WAKE.md");
    appendFileSync(
      wakePath,
      [
        "",
        `## ${new Date(now).toISOString()} — terminal-mt5-punch: ${card.sym} ${card.side.toUpperCase()} (${card.engine})`,
        `- Punched STRAIGHT to MT5 from the terminal Playbook panel: ${resolved.symbol} ${placed.lots} lots, ticket ${placed.ticket}, risk $${placed.risk_usd}.`,
        `- perp levels: entry ${card.entry} · SL ${card.stop} · TP ${targetLevel}${fresh && Number.isFinite(basisPct) ? ` (translated to MT5 at basis ${basisPct}%)` : " (untranslated — MT5 basis unavailable)"}`,
        `- on fill: mirror into positions[], manage auto-BE + scale-outs per desk SOP.`,
        "",
      ].join("\n")
    );
  } catch {
    // The broker has accepted the order. Keep the ticket in the response so
    // a receipt failure cannot make the client resubmit it as a failed punch.
    ledgerWarning = "MT5 accepted the order, but the desk receipt could not be fully recorded";
  }

  return NextResponse.json({
    ok: true,
    orderId: payload.order_id,
    ticket: placed.ticket,
    lots: placed.lots,
    riskUsd: placed.risk_usd,
    price: placed.price,
    mt5Symbol: resolved.symbol,
    symbolSource: resolved.source,
    basisApplied: fresh && Number.isFinite(basisPct),
    ledgerWarning,
  });
}
