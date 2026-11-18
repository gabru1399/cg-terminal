/**
 * Playbook Engine — live detector for the VALIDATED entry archetypes.
 *
 * Ported 1:1 from the real-data backtests (data/backtest/, scripts/backtest_ea.py +
 * scripts/backtest_portfolio.py; validated 2026-05-01 → 11-17 on Binance USDT-M 15m):
 *   EA-2 sweep-acceptance      PRIMARY   all crypto perps   PF 1.51 · +113.1R · n 433
 *   EA-5 cascade-exhaustion    SECONDARY ETH/SOL only       PF 1.69 · +104.2R · n 367 (ETH/SOL)
 *   EA-6 SMC BOS + FVG retest  TERTIARY  all crypto perps   PF 1.40 · +206.9R · n 945
 *   EA-1 / EA-3 / EA-4 / EA-7 / EA-8 are SUSPENDED — never emitted here.
 *
 * Portfolio weights (inverse-maxDD risk parity, data/backtest/portfolio.json):
 *   EA-5 0.467 · EA-2 0.300 · EA-6 0.233  (Grade B, 0.5% risk/trade; live-start 0.25%)
 *
 * The function is PURE: same candles in → same cards out. Signals are evaluated
 * on CLOSED 15m bars only (the forming bar never triggers). A card's stop and
 * targets are frozen at signal time exactly as the backtest froze them.
 */

export interface PlaybookCandle {
  t: number; // open time ms
  o: number; h: number; l: number; c: number;
  v: number;
  tbb: number; // taker buy base volume (Binance klines field 9)
}

export type PlaybookEngine = "EA2" | "EA5" | "EA6";

export interface PlaybookCard {
  id: string;                 // deterministic: engine-sym-signalTs
  engine: PlaybookEngine;
  sym: string;
  side: "long" | "short";
  kind: "market" | "limit";
  entry: number;
  stop: number;
  targets: [number, number, number]; // T1/T2/T3 ladder (40/40/20)
  rPlanned: number;           // planned R of T3 from entry
  status: "confirmed" | "armed" | "pending-fill";
  signalTs: number;           // open time of the triggering (confirmation) bar
  validUntilTs: number;       // after this the card is stale (entry window closed)
  note: string;
  weight: number;             // portfolio risk weight
}

export interface PlaybookContext {
  sym: string;
  price: number;
  vwap: number | null;
  sigma: number | null;
  rPOC: number | null;
  rVAH: number | null;
  rVAL: number | null;
  pdh: number | null;
  pdl: number | null;
  pwh: number | null;
  pwl: number | null;
  atr: number | null;
  biasUp: boolean | null;     // h4 EMA13 × EMA89
}

export const ENGINE_WEIGHTS: Record<PlaybookEngine, number> = { EA2: 0.3, EA5: 0.467, EA6: 0.233 };
export const ENGINE_EVIDENCE: Record<PlaybookEngine, string> = {
  EA2: "PF 1.51 · +113.1R · n433 · 6/7 months (R546)",
  EA5: "PF 1.69 · +104.2R · n367 · ETH/SOL only, BTC banned (R546)",
  EA6: "PF 1.40 · +206.9R · n945 · all syms (R547)",
};
export const EA5_SYMS = new Set(["ETH", "SOL"]);

const DAY = 86_400_000;

function sma(xs: number[], n: number, i: number): number {
  if (i + 1 < n) return NaN;
  let s = 0;
  for (let k = i - n + 1; k <= i; k++) s += xs[k];
  return s / n;
}
function atr14(cs: PlaybookCandle[], i: number): number {
  if (i < 14) return NaN;
  let s = 0;
  for (let k = i - 13; k <= i; k++) {
    const pc = cs[k - 1]?.c ?? cs[k].o;
    s += Math.max(cs[k].h - cs[k].l, Math.abs(cs[k].h - pc), Math.abs(cs[k].l - pc));
  }
  return s / 14;
}

/** Session volume area from a bar slice (70% coverage around POC, 48 bins). */
function volumeArea(bars: PlaybookCandle[]): { poc: number; vah: number; val: number } | null {
  if (bars.length < 8) return null;
  const loP = Math.min(...bars.map((b) => b.l));
  const hiP = Math.max(...bars.map((b) => b.h));
  if (!(hiP > loP)) return null;
  const bins = new Float64Array(48);
  for (const b of bars) {
    const tp = (b.h + b.l + b.c) / 3;
    const idx = Math.min(47, Math.max(0, Math.floor(((tp - loP) / (hiP - loP)) * 48)));
    bins[idx] += b.v;
  }
  let total = 0, p = 0;
  for (let k = 0; k < 48; k++) total += bins[k];
  if (total <= 0) return null;
  for (let k = 1; k < 48; k++) if (bins[k] > bins[p]) p = k;
  let va = bins[p] / total, loI = p, hiI = p;
  while (va < 0.7 && (loI > 0 || hiI < 47)) {
    const up = hiI < 47 ? bins[hiI + 1] : -1;
    const dn = loI > 0 ? bins[loI - 1] : -1;
    if (up >= dn && hiI < 47) { hiI++; va += bins[hiI] / total; }
    else if (loI > 0) { loI--; va += bins[loI] / total; }
    else { hiI++; va += bins[hiI] / total; }
  }
  const bw = (hiP - loP) / 48;
  return { poc: loP + (p + 0.5) * bw, vah: loP + (hiI + 1) * bw, val: loP + loI * bw };
}

/** h4 EMA13/89 bias as of bar i (forming bucket included, as in the backtest). */
function h4Bias(cs: PlaybookCandle[], i: number): boolean | null {
  const buckets = new Map<number, { c: number; t: number }>();
  for (let k = 0; k <= i; k++) {
    const bt = Math.floor(cs[k].t / (4 * 3_600_000)) * 4 * 3_600_000;
    buckets.set(bt, { c: cs[k].c, t: bt });
  }
  const closes = [...buckets.entries()].sort((a, b) => a[0] - b[0]).map(([, b]) => b.c);
  if (closes.length < 90) return null;
  let e13 = closes[0], e89 = closes[0];
  const k13 = 2 / 14, k89 = 2 / 90;
  for (let k = 1; k < closes.length; k++) {
    e13 = closes[k] * k13 + e13 * (1 - k13);
    e89 = closes[k] * k89 + e89 * (1 - k89);
  }
  return e13 > e89;
}

function levels(cs: PlaybookCandle[]): {
  vwap: number | null; sigma: number | null; poc: number | null; vah: number | null; val: number | null;
  pdh: number | null; pdl: number | null; pwh: number | null; pwl: number | null;
  pdVAH: number | null; pdVAL: number | null; pdPOC: number | null;
} {
  const n = cs.length;
  const curDay = Math.floor(cs[n - 1].t / DAY);
  const cur: PlaybookCandle[] = [];
  const prev: PlaybookCandle[] = [];
  const weekBars = new Map<number, PlaybookCandle[]>();
  for (const b of cs) {
    const d = Math.floor(b.t / DAY);
    if (d === curDay) cur.push(b);
    else if (d === curDay - 1) prev.push(b);
    const wk = Math.floor((b.t - 4 * DAY) / (7 * DAY)); // Monday-anchored weeks (Thu 1970 epoch offset)
    if (!weekBars.has(wk)) weekBars.set(wk, []);
    weekBars.get(wk)!.push(b);
  }
  // running session (current day, bars so far)
  let vwap: number | null = null, sigma: number | null = null;
  let va: { poc: number; vah: number; val: number } | null = null;
  if (cur.length) {
    let cv = 0, ctpv = 0, dev2 = 0;
    for (const b of cur) {
      const tp = (b.h + b.l + b.c) / 3;
      cv += b.v; ctpv += tp * b.v;
    }
    const vw = ctpv / Math.max(cv, 1e-12);
    for (const b of cur) {
      const tp = (b.h + b.l + b.c) / 3;
      dev2 += (tp - vw) * (tp - vw) * b.v;
    }
    vwap = vw;
    sigma = Math.sqrt(Math.max(dev2 / Math.max(cv, 1e-12), 0));
    va = volumeArea(cur);
  }
  const pva = volumeArea(prev);
  const weekKeys = [...weekBars.keys()].sort((a, b) => b - a);
  const curWeek = Math.floor((cs[n - 1].t - 4 * DAY) / (7 * DAY));
  const prevWeekBars = weekBars.get(curWeek - 1) ?? weekBars.get(weekKeys[1] ?? curWeek) ?? [];
  return {
    vwap, sigma,
    poc: va?.poc ?? null, vah: va?.vah ?? null, val: va?.val ?? null,
    pdh: prev.length ? Math.max(...prev.map((b) => b.h)) : null,
    pdl: prev.length ? Math.min(...prev.map((b) => b.l)) : null,
    pwh: prevWeekBars.length ? Math.max(...prevWeekBars.map((b) => b.h)) : null,
    pwl: prevWeekBars.length ? Math.min(...prevWeekBars.map((b) => b.l)) : null,
    pdVAH: pva?.vah ?? null, pdVAL: pva?.val ?? null, pdPOC: pva?.poc ?? null,
  };
}

export function runPlaybook(cs: PlaybookCandle[], sym: string): { cards: PlaybookCard[]; ctx: PlaybookContext } {
  const n = cs.length;
  const empty: PlaybookCard[] = [];
  if (n < 220) return { cards: empty, ctx: { sym, price: cs[n - 1]?.c ?? NaN, vwap: null, sigma: null, rPOC: null, rVAH: null, rVAL: null, pdh: null, pdl: null, pwh: null, pwl: null, atr: null, biasUp: null } };
  const L = levels(cs);
  const last = cs[n - 1];
  const atrArr = new Array<number>(n);
  const volSma = new Array<number>(n);
  const dp = new Array<number>(n); // delta_pct
  const vz = new Array<number>(n);
  for (let i = 0; i < n; i++) {
    atrArr[i] = atr14(cs, i);
    volSma[i] = sma(cs.map((x) => x.v), 20, i);
    dp[i] = cs[i].v > 0 ? (2 * cs[i].tbb - cs[i].v) / cs[i].v : 0;
  }
  for (let i = 20; i < n; i++) {
    let m = 0, s2 = 0;
    for (let k = i - 19; k <= i; k++) m += cs[k].v;
    m /= 20;
    for (let k = i - 19; k <= i; k++) s2 += (cs[k].v - m) * (cs[k].v - m);
    const sd = Math.sqrt(s2 / 20);
    vz[i] = sd > 0 ? (cs[i].v - m) / sd : 0;
  }
  const base = sym.replace(/USDT$/i, "").toUpperCase();
  const cards: PlaybookCard[] = [];
  const NOW = last.t + 15 * 60_000; // close time of the last closed bar

  // ---------- EA-2: sweep-acceptance (evaluate the last 12 bars for live windows) ----------
  if (atrArr[n - 1] > 0 && L.pdh != null) {
    const lvls: [string, number][] = [];
    if (L.pdh != null) lvls.push(["PDH", L.pdh]);
    if (L.pdl != null) lvls.push(["PDL", L.pdl]);
    if (L.pwh != null) lvls.push(["PWH", L.pwh]);
    if (L.pwl != null) lvls.push(["PWL", L.pwl]);
    if (L.pdVAH != null) lvls.push(["PD-VAH", L.pdVAH]);
    if (L.pdVAL != null) lvls.push(["PD-VAL", L.pdVAL]);
    const sweptDays = new Map<string, number>(); // level name -> day already swept (approx: skip if same level produced a card today)
    for (let j = Math.max(30, n - 14); j < n; j++) {
      const d = Math.floor(cs[j].t / DAY);
      for (const [name, Lv] of lvls) {
        if (sweptDays.get(name) === d) continue;
        const isSweepVol = cs[j].v >= 1.5 * volSma[j];
        if (!isSweepVol || !(atrArr[j] > 0)) continue;
        // downside sweep -> long
        if (cs[j].c < Lv && cs[j].l < Lv && cs[j].h >= Lv && (Lv - cs[j].l) / atrArr[j] <= 1.5) {
          let accepted: number | null = null;
          for (let m = j + 1; m <= Math.min(j + 3, n - 1); m++) {
            if (cs[m].c > Lv && dp[m] > 0.15 && cs[m].c > cs[m].o) { accepted = m; break; }
          }
          if (accepted != null) {
            const m = accepted;
            const stop = Math.min(...cs.slice(j, m + 1).map((b) => b.l)) - 0.05 * atrArr[m];
            const t1 = L.poc != null && L.poc > cs[m].c ? L.poc : cs[m].c + 2 * (cs[m].c - stop);
            const t2 = L.vah != null && L.vah > t1 ? L.vah : cs[m].c + 2.5 * (cs[m].c - stop);
            const t3 = cs[m].c + 3 * (cs[m].c - stop);
            cards.push({
              id: `EA2-${sym}-${cs[m].t}`, engine: "EA2", sym, side: "long", kind: "market",
              entry: cs[m].c, stop, targets: [t1, t2, t3], rPlanned: 3,
              status: m === n - 1 ? "confirmed" : "armed",
              signalTs: cs[m].t, validUntilTs: cs[m].t + 8 * 15 * 60_000,
              note: `${name} sweep accepted (delta +${(dp[m] * 100).toFixed(0)}%) — stop beyond sweep wick`,
              weight: ENGINE_WEIGHTS.EA2,
            });
            sweptDays.set(name, d);
          } else if (n - 1 - j < 3) {
            cards.push({
              id: `EA2-ARM-${sym}-${cs[j].t}-${name}`, engine: "EA2", sym, side: "long", kind: "market",
              entry: Lv, stop: cs[j].l - 0.05 * atrArr[j], targets: [0, 0, 0], rPlanned: 3,
              status: "armed", signalTs: cs[j].t, validUntilTs: cs[j].t + 4 * 15 * 60_000,
              note: `${name} sweep detected — awaiting acceptance close back above ${name}`,
              weight: ENGINE_WEIGHTS.EA2,
            });
          }
        }
        // upside sweep -> short
        if (cs[j].c > Lv && cs[j].h > Lv && cs[j].l <= Lv && (cs[j].h - Lv) / atrArr[j] <= 1.5) {
          let accepted: number | null = null;
          for (let m = j + 1; m <= Math.min(j + 3, n - 1); m++) {
            if (cs[m].c < Lv && dp[m] < -0.15 && cs[m].c < cs[m].o) { accepted = m; break; }
          }
          if (accepted != null) {
            const m = accepted;
            const stop = Math.max(...cs.slice(j, m + 1).map((b) => b.h)) + 0.05 * atrArr[m];
            const t1 = L.poc != null && L.poc < cs[m].c ? L.poc : cs[m].c - 2 * (stop - cs[m].c);
            const t2 = L.val != null && L.val < t1 ? L.val : cs[m].c - 2.5 * (stop - cs[m].c);
            const t3 = cs[m].c - 3 * (stop - cs[m].c);
            cards.push({
              id: `EA2-${sym}-${cs[m].t}`, engine: "EA2", sym, side: "short", kind: "market",
              entry: cs[m].c, stop, targets: [t1, t2, t3], rPlanned: 3,
              status: m === n - 1 ? "confirmed" : "armed",
              signalTs: cs[m].t, validUntilTs: cs[m].t + 8 * 15 * 60_000,
              note: `${name} sweep accepted (delta ${(dp[m] * 100).toFixed(0)}%) — stop beyond sweep wick`,
              weight: ENGINE_WEIGHTS.EA2,
            });
            sweptDays.set(name, d);
          } else if (n - 1 - j < 3) {
            cards.push({
              id: `EA2-ARM-${sym}-${cs[j].t}-${name}`, engine: "EA2", sym, side: "short", kind: "market",
              entry: Lv, stop: cs[j].h + 0.05 * atrArr[j], targets: [0, 0, 0], rPlanned: 3,
              status: "armed", signalTs: cs[j].t, validUntilTs: cs[j].t + 4 * 15 * 60_000,
              note: `${name} sweep detected — awaiting acceptance close back below ${name}`,
              weight: ENGINE_WEIGHTS.EA2,
            });
          }
        }
      }
    }
  }

  // ---------- EA-5: cascade exhaustion (ETH/SOL only) ----------
  if (EA5_SYMS.has(base) && L.vwap != null) {
    for (let j = Math.max(30, n - 12); j < n; j++) {
      if (!(vz[j] >= 3)) continue;
      const prior12Low = Math.min(...cs.slice(Math.max(0, j - 12), j).map((b) => b.l));
      const prior12High = Math.max(...cs.slice(Math.max(0, j - 12), j).map((b) => b.h));
      // long: cascade down + exhaustion flip
      if (cs[j].c < prior12Low && cs[j].c < L.vwap) {
        for (let m = j + 1; m <= Math.min(j + 5, n - 1); m++) {
          const dp3 = dp[m - 2] + dp[m - 1] + dp[m];
          const rng = cs[m].h - cs[m].l;
          if (dp3 > 0.05 && rng > 0 && cs[m].c > cs[m].l + 0.5 * rng && cs[m].c > cs[m - 1].c) {
            const stop = Math.min(...cs.slice(j, m + 1).map((b) => b.l)) - 0.1 * atrArr[m];
            const t1 = L.vwap;
            const t2 = L.poc != null && L.poc > L.vwap ? L.poc : L.vwap + 1.5 * (L.vwap - stop);
            const t3 = cs[m].c + 2 * (cs[m].c - stop);
            cards.push({
              id: `EA5-${sym}-${cs[m].t}`, engine: "EA5", sym, side: "long", kind: "market",
              entry: cs[m].c, stop, targets: [t1, t2, t3], rPlanned: 2,
              status: m === n - 1 ? "confirmed" : "armed",
              signalTs: cs[m].t, validUntilTs: cs[m].t + 8 * 15 * 60_000,
              note: `cascade vol z=${vz[j].toFixed(1)} exhausted, delta flip +${(dp3 * 100).toFixed(0)}%`,
              weight: ENGINE_WEIGHTS.EA5,
            });
            break;
          }
        }
        if (cards.every((c) => c.signalTs < cs[j].t) && n - 1 - j < 5) {
          cards.push({
            id: `EA5-ARM-${sym}-${cs[j].t}`, engine: "EA5", sym, side: "long", kind: "market",
            entry: L.vwap, stop: cs[j].l - 0.1 * atrArr[j], targets: [0, 0, 0], rPlanned: 2,
            status: "armed", signalTs: cs[j].t, validUntilTs: cs[j].t + 6 * 15 * 60_000,
            note: `cascade bar (vol z=${vz[j].toFixed(1)}) — awaiting delta-flip exhaustion close`,
            weight: ENGINE_WEIGHTS.EA5,
          });
        }
      }
      // short: cascade up
      if (cs[j].c > prior12High && cs[j].c > L.vwap) {
        for (let m = j + 1; m <= Math.min(j + 5, n - 1); m++) {
          const dp3 = dp[m - 2] + dp[m - 1] + dp[m];
          const rng = cs[m].h - cs[m].l;
          if (dp3 < -0.05 && rng > 0 && cs[m].c < cs[m].h - 0.5 * rng && cs[m].c < cs[m - 1].c) {
            const stop = Math.max(...cs.slice(j, m + 1).map((b) => b.h)) + 0.1 * atrArr[m];
            const t1 = L.vwap;
            const t2 = L.poc != null && L.poc < L.vwap ? L.poc : L.vwap - 1.5 * (stop - L.vwap);
            const t3 = cs[m].c - 2 * (stop - cs[m].c);
            cards.push({
              id: `EA5-${sym}-${cs[m].t}`, engine: "EA5", sym, side: "short", kind: "market",
              entry: cs[m].c, stop, targets: [t1, t2, t3], rPlanned: 2,
              status: m === n - 1 ? "confirmed" : "armed",
              signalTs: cs[m].t, validUntilTs: cs[m].t + 8 * 15 * 60_000,
              note: `cascade vol z=${vz[j].toFixed(1)} exhausted, delta flip ${(dp3 * 100).toFixed(0)}%`,
              weight: ENGINE_WEIGHTS.EA5,
            });
            break;
          }
        }
      }
    }
  }

  // ---------- EA-6: SMC BOS + FVG retest (limit entries) ----------
  {
    let LSH: number | null = null, LSL: number | null = null;
    let fvg: { side: "L" | "S"; lo: number; hi: number } | null = null;
    for (let i = 30; i < n; i++) {
      if (i >= 2 && cs[i - 2].h > cs[i - 3]?.h && cs[i - 2].h > cs[i - 1].h && cs[i - 2].h > cs[i - 4]?.h && cs[i - 2].h > cs[i]?.h) LSH = cs[i - 2].h;
      if (i >= 2 && cs[i - 2].l < cs[i - 3]?.l && cs[i - 2].l < cs[i - 1].l && cs[i - 2].l < cs[i - 4]?.l && cs[i - 2].l < cs[i]?.l) LSL = cs[i - 2].l;
      if (i >= 2 && cs[i].l > cs[i - 2].h) fvg = { side: "L", lo: cs[i - 2].h, hi: cs[i].l };
      if (i >= 2 && cs[i].h < cs[i - 2].l) fvg = { side: "S", lo: cs[i].h, hi: cs[i - 2].l };
      if (!(atrArr[i] > 0)) continue;
      const bias = h4Bias(cs, i);
      // bullish BOS -> limit at FVG mid
      if (LSH != null && cs[i].c > LSH && fvg && fvg.side === "L" && bias === true) {
        const mid = (fvg.lo + fvg.hi) / 2;
        if (i >= n - 12) {
          const stop = Math.min(fvg.lo, LSL ?? fvg.lo) - 0.05 * atrArr[i];
          const risk = mid - stop;
          const t1 = LSH + 0.5 * atrArr[i];
          const t2 = mid + 2 * risk, t3 = mid + 3 * risk;
          const touched = cs.slice(i + 1).some((b) => b.l <= mid);
          cards.push({
            id: `EA6-${sym}-${cs[i].t}`, engine: "EA6", sym, side: "long", kind: "limit",
            entry: mid, stop, targets: [t1, t2, t3], rPlanned: 3,
            status: touched ? "confirmed" : "pending-fill",
            signalTs: cs[i].t, validUntilTs: cs[i].t + 8 * 15 * 60_000,
            note: `bullish BOS → FVG retest limit @ mid (zone ${fvg.lo.toFixed(2)}–${fvg.hi.toFixed(2)})`,
            weight: ENGINE_WEIGHTS.EA6,
          });
        }
        LSH = null;
      }
      // bearish BOS -> limit at FVG mid
      if (LSL != null && cs[i].c < LSL && fvg && fvg.side === "S" && bias === false) {
        const mid = (fvg.lo + fvg.hi) / 2;
        if (i >= n - 12) {
          const stop = Math.max(fvg.hi, LSH ?? fvg.hi) + 0.05 * atrArr[i];
          const risk = stop - mid;
          const t1 = LSL - 0.5 * atrArr[i];
          const t2 = mid - 2 * risk, t3 = mid - 3 * risk;
          const touched = cs.slice(i + 1).some((b) => b.h >= mid);
          cards.push({
            id: `EA6-${sym}-${cs[i].t}`, engine: "EA6", sym, side: "short", kind: "limit",
            entry: mid, stop, targets: [t1, t2, t3], rPlanned: 3,
            status: touched ? "confirmed" : "pending-fill",
            signalTs: cs[i].t, validUntilTs: cs[i].t + 8 * 15 * 60_000,
            note: `bearish BOS → FVG retest limit @ mid (zone ${fvg.lo.toFixed(2)}–${fvg.hi.toFixed(2)})`,
            weight: ENGINE_WEIGHTS.EA6,
          });
        }
        LSL = null;
      }
    }
  }

  const ctx: PlaybookContext = {
    sym, price: last.c, vwap: L.vwap, sigma: L.sigma, rPOC: L.poc, rVAH: L.vah, rVAL: L.val,
    pdh: L.pdh, pdl: L.pdl, pwh: L.pwh, pwl: L.pwl, atr: atrArr[n - 1] > 0 ? atrArr[n - 1] : null,
    biasUp: h4Bias(cs, n - 1),
  };
  // freshness gate: drop armed/pending cards whose window expired; confirmed cards older than 2 bars are stale
  const live = cards.filter((c) => c.validUntilTs >= NOW);
  return { cards: live, ctx };
}
