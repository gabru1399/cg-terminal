import { NextRequest, NextResponse } from "next/server";
import { existsSync, mkdirSync, readFileSync, writeFileSync, appendFileSync } from "node:fs";
import path from "node:path";
import type { PlaybookCard } from "@/lib/strategy/playbook";

export const dynamic = "force-dynamic";

/**
 * POST /api/desk/punch — the terminal's Punch-Trade bridge.
 *
 * Takes a playbook card and queues it for the execution brain (`atg-exec`, Delta
 * Exchange India) through the desk's own files, exactly per the operating contract
 * in desk/CANONICAL_MASTER_SPECIFICATION.md:
 *   1. appends the order to `desk/state.json` orders[] with status "suggested"
 *      (config is NEVER touched — it belongs to the human);
 *   2. appends a section to `desk/inbox/WAKE.md` so the desk daemon wakes atg-exec;
 *   3. returns the order id for the blotter.
 * It does NOT place exchange orders directly — atg-exec is the execution brain and
 * mirrors status/ticket back into state.json, which the desk blotter already reads.
 */
interface PunchBody {
  card: PlaybookCard;
  equity?: number;   // account equity (USD) for the sizing hint
  riskPct?: number;  // risk per trade in percent, e.g. 0.25
}

const ROOT = (() => {
  const cwd = process.cwd();
  const candidates = [cwd, path.resolve(cwd, ".."), path.resolve(cwd, "..", "..")];
  for (const dir of candidates) {
    if (existsSync(path.join(dir, "desk", "state.json"))) return dir;
  }
  return cwd;
})();

export async function POST(req: NextRequest) {
  let body: PunchBody;
  try {
    body = (await req.json()) as PunchBody;
  } catch {
    return NextResponse.json({ ok: false, error: "invalid JSON body" }, { status: 400 });
  }
  const { card } = body;
  if (!card || !card.engine || !card.sym || !card.side || !Number.isFinite(card.entry) || !Number.isFinite(card.stop)) {
    return NextResponse.json({ ok: false, error: "card missing engine/sym/side/entry/stop" }, { status: 400 });
  }
  const now = Date.now();
  const id = `tp-${now}`;
  const riskPct = Number.isFinite(body.riskPct) ? Number(body.riskPct) : 0.25;
  const equity = Number.isFinite(body.equity) && body.equity! > 0 ? Number(body.equity) : null;
  const stopDist = Math.abs(card.entry - card.stop);
  const riskUsd = equity ? (equity * riskPct * card.weight) / 100 : null;
  const qtyHint = riskUsd && stopDist > 0 ? riskUsd / stopDist : null;

  const order = {
    id,
    round: "R547",
    sym: card.sym,
    side: card.side,
    action: card.side,
    type: card.kind === "limit" ? "limit" : "market",
    status: "suggested",
    source: "terminal-punch",
    engine: card.engine,
    entry: card.entry,
    stop: card.stop,
    targets: card.targets.every((t) => t > 0) ? card.targets : [],
    riskR: card.rPlanned,
    riskPct: riskPct * card.weight,
    regime: `playbook:${card.engine}`,
    mode: "terminal-punch",
    rationale: card.note,
    notes: card.targets.every((t) => t > 0)
      ? `T1 ${card.targets[0]} · T2 ${card.targets[1]} · T3 ${card.targets[2]} · ${card.status} card from ${card.sym} playbook scan`
      : `${card.status} card (armed — levels finalize on confirmation)`,
    qtyHint: qtyHint != null ? Number(qtyHint.toPrecision(6)) : null,
    equityHint: equity,
    createdTs: now,
    expiresTs: card.validUntilTs,
    ticket: null,
  };

  try {
    // 1) desk/state.json — append to orders[] (array form) or activeOrders (object form); config untouched
    const statePath = path.join(ROOT, "desk", "state.json");
    let state: Record<string, unknown> = {};
    if (existsSync(statePath)) {
      state = JSON.parse(readFileSync(statePath, "utf8")) as Record<string, unknown>;
    }
    const ordersAny = (state.orders ?? (state as { activeOrders?: unknown }).activeOrders) as unknown;
    if (Array.isArray(ordersAny)) {
      (state.orders as unknown[]).push(order);
    } else if (ordersAny && typeof ordersAny === "object") {
      (ordersAny as unknown[]).push(order);
    } else {
      state.orders = [order];
    }
    mkdirSync(path.dirname(statePath), { recursive: true });
    writeFileSync(statePath, JSON.stringify(state, null, 2) + "\n");

    // 2) desk/inbox/WAKE.md — wake section for atg-exec
    const wakePath = path.join(ROOT, "desk", "inbox", "WAKE.md");
    mkdirSync(path.dirname(wakePath), { recursive: true });
    if (!existsSync(wakePath)) {
      writeFileSync(wakePath, "# WAKE — queued directives for atg-exec\n");
    }
    const iso = new Date(now).toISOString();
    const qtyLine = qtyHint != null ? `\n- qty hint: ${qtyHint.toPrecision(6)} (${riskPct}% × weight ${card.weight} on $${equity})` : "";
    appendFileSync(
      wakePath,
      [
        "",
        `## ${iso} — terminal-punch: ${card.sym} ${card.side.toUpperCase()} (${card.engine})`,
        `- Punched from the terminal Playbook panel by the human. Execute per desk SOP.`,
        `- ${card.side} ${card.sym} · ${card.kind.toUpperCase()} @ ${card.entry} · SL ${card.stop} · targets ${card.targets.map((t) => (t > 0 ? t : "—")).join(" / ")}`,
        `- engine ${card.engine} (${card.status}) · risk weight ${card.weight} · planned R ${card.rPlanned}`,
        `- note: ${card.note}${qtyLine}`,
        `- on fill: write status/ticket/actualEntry back to state.json orders[] and log EXEC.`,
        "",
      ].join("\n")
    );
    return NextResponse.json({ ok: true, orderId: id, ts: now, order });
  } catch (e) {
    return NextResponse.json(
      { ok: false, error: e instanceof Error ? e.message : "desk write failed" },
      { status: 500 }
    );
  }
}
