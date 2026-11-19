import { NextRequest, NextResponse } from "next/server";
import { cgGet } from "@/lib/cg/client";
import { buildLiqModel, liqStats, type LiqModel, type RawLiqPayload } from "@/lib/cg/liq-model";
import { liqVenues, symDecs } from "@/lib/cg/assets";
import { anyTerminalSym, knownSym } from "@/lib/cg/sym-gate";
import { getLivePrice } from "@/lib/live/server-price";
import { fetchBinCandles } from "@/lib/cg/fallbacks";
import { BoundedMap } from "@/lib/cg/bounded";
import type { LiquidationLevel } from "@/lib/cg/types";

export const dynamic = "force-dynamic";

const FRESH_MS = 60_000;
const STALE_MS = 5 * 60_000;
const RETRY_MS = 15_000;

interface Snapshot {
  at: number;
  model: LiqModel;
  perVenue: Record<string, number>;
  venues: string[];
  partial: boolean;
}

const snapshots = new BoundedMap<Snapshot>(32);
const failures = new BoundedMap<{ at: number; error: string }>(32);
const pending = new Map<string, Promise<Snapshot>>();

function unwrapPayload(value: unknown): RawLiqPayload | null {
  for (let depth = 0; depth < 3; depth++) {
    if (!value || typeof value !== "object") return null;
    const payload = value as { prices?: unknown; data?: unknown };
    if (Array.isArray(payload.prices) && Array.isArray(payload.data)) {
      const valid = payload.prices.length >= 10 && payload.prices.every((row) =>
        Array.isArray(row) && [0, 2, 3, 4].every((i) => Number.isFinite(Number(row[i])) && Number(row[i]) > 0)
        && Number(row[2]) >= Number(row[3])
      );
      return valid ? (payload as RawLiqPayload) : null;
    }
    value = payload.data;
  }
  return null;
}

async function loadSnapshotFromDisk(sym: string, range: string, limit: number): Promise<Snapshot | null> {
  try {
    const fs = await import("fs/promises");
    const path = await import("path");
    const candidates = [
      path.join(process.cwd(), "data", "cg-series", `liqlevels_${sym}_${range}.jsonl`),
      path.join(process.cwd(), "data", "cg-series", `liqlevels_${sym}_3d.jsonl`),
      ...(sym === "BTC" ? [
        path.join(process.cwd(), "data", "cg-series", `liqlevels_${range}.jsonl`),
        path.join(process.cwd(), "data", "cg-series", "liqlevels_3d.jsonl"),
      ] : []),
    ];
    let filePath: string | null = null;
    for (const c of candidates) {
      try {
        await fs.access(c);
        filePath = c;
        break;
      } catch {}
    }
    if (!filePath) return null;

    const raw = await fs.readFile(filePath, "utf8");
    const lines = raw.trim().split("\n");
    if (!lines.length) return null;
    const rows = lines.slice(-limit).map((l) => {
      try { return JSON.parse(l); } catch { return null; }
    }).filter((r) => r && typeof r === "object");
    if (!rows.length) return null;

    let candles = await fetchBinCandles(sym, "15m", 100).catch(() => []);
    if (!candles.length) {
      const now = Date.now();
      const avgP = rows.reduce((acc, r) => acc + (Number(r.p) || 0), 0) / rows.length || 1;
      candles = Array.from({ length: 96 }, (_, i) => ({
        t: now - (96 - i) * 900_000,
        o: avgP, h: avgP * 1.005, l: avgP * 0.995, c: avgP, v: 1000,
      }));
    }
    const prices: [number, number, number, number, number, number][] = candles.map((b) => [
      Math.floor(b.t / 1000), b.o, b.h, b.l, b.c, b.v,
    ]);

    const venuesMap = new Map<string, RawLiqLevel[]>();
    let maxAt = 0;
    for (const r of rows) {
      if (r.at && r.at > maxAt) maxAt = r.at;
      const vKey = String(r.v || "");
      const vName = vKey.split("_")[0] || vKey || "Aggregated";
      if (!venuesMap.has(vName)) venuesMap.set(vName, []);
      venuesMap.get(vName)!.push({
        price: Number(r.p),
        size: Number(r.s),
        level2: r.l2,
        side: r.side,
        beginDate: Math.floor((r.at || Date.now()) / 1000),
      });
    }

    const available: { name: string; payload: RawLiqPayload }[] = [];
    const perVenue: Record<string, number> = {};
    for (const [vName, data] of venuesMap.entries()) {
      available.push({ name: vName, payload: { prices, data } });
      perVenue[vName] = data.length;
    }
    const model = buildLiqModel(available);
    if (!model) return null;
    return {
      at: maxAt || Date.now(),
      model,
      perVenue,
      venues: Array.from(venuesMap.keys()),
      partial: true,
    };
  } catch (err) {
    console.error("[liqlevels] loadSnapshotFromDisk error for", sym, err);
    return null;
  }
}

async function loadSnapshot(sym: string, range: string, limit: number): Promise<Snapshot> {
  const requested = liqVenues(sym);
  const results = await Promise.allSettled(requested.map(async (venue, i) => {
    if (i > 0) await new Promise((r) => setTimeout(r, i * 50));
    const query = new URLSearchParams({ symbol: venue.key, limit: String(limit), range });
    // Aggregate freshness with client-level caching: 30s TTL keeps the
    // endpoint polite and allows staleDuringCooldown to serve recent payloads
    // during transient upstream 429 rate-limit windows.
    const data = await cgGet("/api/liquidationLevels/v2?" + query, 30_000);
    const payload = unwrapPayload(data);
    if (!payload) throw new Error("Unusable liquidation snapshot");
    return { name: venue.name, payload };
  }));
  const available = results.flatMap((result) => (result.status === "fulfilled" ? [result.value] : []));
  let model = buildLiqModel(available);
  if (!model) {
    // Upstream throttled or returned no data — fall back to local on-disk series
    const diskSnapshot = await loadSnapshotFromDisk(sym, range, limit);
    if (diskSnapshot) return diskSnapshot;

    const throttled = results.some((r) => r.status === "rejected" && String(r.reason).includes("429"));
    throw new Error(throttled
      ? "Coinglass is rate limiting liquidation data. Try again shortly."
      : "Coinglass did not return a usable liquidation snapshot. Try again shortly.");
  }
  const perVenue = Object.fromEntries(requested.map((v) => [v.name, 0]));
  for (const venue of available) perVenue[venue.name] = venue.payload.data.length;
  return {
    at: Date.now(), model, perVenue, venues: available.map((v) => v.name),
    partial: available.length < requested.length,
  };
}

function refreshSnapshot(key: string, sym: string, range: string, limit: number) {
  const current = pending.get(key);
  if (current) return current;
  const refresh = loadSnapshot(sym, range, limit)
    .then((snapshot) => {
      snapshots.set(key, snapshot);
      return snapshot;
    })
    .catch((error: Error) => {
      failures.set(key, { at: Date.now(), error: error.message });
      throw error;
    })
    .finally(() => pending.delete(key));
  pending.set(key, refresh);
  return refresh;
}

async function referencePrice(sym: string): Promise<number | null> {
  // The snapshot has a candle close to fall back on if the quote is slow.
  let timer: ReturnType<typeof setTimeout> | undefined;
  try {
    return await Promise.race([
      getLivePrice(sym).then((quote) => quote.price, () => null),
      new Promise<null>((resolve) => { timer = setTimeout(() => resolve(null), 1500); }),
    ]);
  } finally {
    clearTimeout(timer);
  }
}

export async function GET(req: NextRequest) {
  const sp = req.nextUrl.searchParams;
  const sym = (sp.get("sym") ?? "BTC").trim().toUpperCase();
  if (!(await anyTerminalSym(sym))) {
    return NextResponse.json({ ok: false, error: "unknown asset " + sym }, { status: 400 });
  }
  const rangeRaw = sp.get("range") ?? "3d";
  const range = ["3d", "7d", "30d"].includes(rangeRaw) ? rangeRaw : "3d";
  const lvR = Math.min(Math.max(Number(sp.get("lvR") ?? 4) || 4, 1), 8);
  const limit = Math.max(1, Math.min(Math.floor(Number(sp.get("limit") ?? 4000) || 4000), 6000));
  if (!(await knownSym(sym))) {
    return NextResponse.json({
      ok: true, supported: false, sym, range, lvR, venues: [], perVenue: {}, stats: null,
      livePrice: await referencePrice(sym),
      reason: "Coinglass estimated liquidation clusters apply only to multi-venue perpetual futures",
      updatedAt: Date.now(),
    });
  }

  const key = [sym, range, limit].join("|");
  let snapshot = snapshots.get(key);
  const now = Date.now();
  const failure = failures.get(key);
  let stale = false;
  try {
    if (!snapshot || now - snapshot.at >= (snapshot.partial ? RETRY_MS : FRESH_MS)) {
      if (failure && now - failure.at < RETRY_MS) throw new Error(failure.error);
      snapshot = await refreshSnapshot(key, sym, range, limit);
    }
  } catch (error) {
    // If we have an existing snapshot (even if older than STALE_MS), serve it as stale
    // rather than throwing a hard 503 error. Only throw 503 if no snapshot exists at all.
    if (!snapshot) {
      return NextResponse.json(
        { ok: false, sym, range, lvR, error: error instanceof Error ? error.message : "Liquidation data unavailable" },
        { status: 503, headers: { "Retry-After": String(RETRY_MS / 1000) } },
      );
    }
    stale = true;
  }
  const livePrice = await referencePrice(sym);
  const stats = liqStats(snapshot.model, lvR, {
    livePrice,
    priceDecs: symDecs(sym, livePrice ?? snapshot.model.c.at(-1) ?? null),
  });
  return NextResponse.json({
    ok: true, supported: true, sym, range, lvR,
    venues: snapshot.venues, perVenue: snapshot.perVenue, stats, livePrice,
    stale, partial: snapshot.partial, updatedAt: snapshot.at,
  });
}

export type { LiquidationLevel };
