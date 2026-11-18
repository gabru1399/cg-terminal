/**
 * Playbook Engine — live detector for the VALIDATED entry archetypes.
 *
 * 1:1 port of the real-data backtests (scripts/backtest_ea.py, backtest_portfolio.py,
 * backtest_ea6_fix.py — R546/R547/R548, Binance USDT-M 15m, 2026-05-01→11-17,
 * net of fees/slippage, stop-first worst-case fills):
 *   EA-2 sweep-acceptance      PRIMARY   all crypto perps   PF 1.51 · +113.1R · n 432
 *   EA-5 cascade-exhaustion    SECONDARY ETH/SOL only       PF 1.69 · +104.2R · n 367 (ETH/SOL)
 *   EA-6 SMC BOS + FVG retest  TERTIARY  all crypto perps   PF 1.38 · +195.3R · n 953 (R548 no-lookahead)
 *   EA-1 / EA-3 / EA-4 / EA-7 / EA-8 are SUSPENDED — structurally never emitted.
 *
 * Portfolio weights (inverse-maxDD risk parity, data/backtest/portfolio.json):
 *   EA-5 0.467 · EA-2 0.300 · EA-6 0.233  (live-start 0.25% risk/trade, 50-fill gate to 0.5%)
 *
 * PARITY CONTRACT (verified by scripts/parity_check.mjs):
 * - Signals evaluate CLOSED 15m bars only; stops/targets freeze at signal time.
 * - h4 EMA13/89 bias uses the forming 4h bucket's close-so-far (NO lookahead —
 *   the R548 correction; the original R547 backtest leaked the bucket's final close).
 * - Running session VWAP/σ/POC/VAH/VAL and prior-day/week levels are computed
 *   per bar exactly like backtest_ea.running_session()/prior_levels().
 * - vz is ddof=1 (pandas rolling.std semantics).
 * - EA-6 uses the WIDE FVG zone (l[i-2] … h[i]) that the validated rules used,
 *   targets anchored at the BOS close, 23:30 UTC emission cutoff, BOS re-arm
 *   throttle, opposite-swing requirement, swing consumption on any close-through.
 * - Engine state (swing highs/lows, last FVG, BOS throttle, per-day/level sweep
 *   dedupe, cascade caps) runs over the whole fetched window so per-day caps
 *   match the backtest; only the last 12 bars emit cards.
 * - Known divergence (documented): EMA warmup starts at the window head
 *   (~1500 bars ≈ 94 4h buckets) instead of the backtest's full history.
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
  pdVAH: number | null;
  pdVAL: number | null;
  pdPOC: number | null;
  pwh: number | null;
  pwl: number | null;
  atr: number | null;
  biasUp: boolean | null;     // h4 EMA13 × EMA89 (no-lookahead)
}

export const ENGINE_WEIGHTS: Record<PlaybookEngine, number> = { EA2: 0.3, EA5: 0.467, EA6: 0.233 };
export const ENGINE_EVIDENCE: Record<PlaybookEngine, string> = {
  EA2: "PF 1.51 · +113.1R · n432 · 6/7 months (R546)",
  EA5: "PF 1.69 · +104.2R · n367 · ETH/SOL only, BTC banned (R546)",
  EA6: "PF 1.38 · +195.3R · n953 · no-lookahead re-validation (R548)",
};
export const PORTFOLIO_EVIDENCE = "PF 1.50 · +128.1R weighted · maxDD 26.2R · corr ≤ 0.12";
export const EA5_SYMS = new Set(["ETH", "SOL"]);

const DAY = 86_400_000;
const BAR = 15 * 60_000;
const H4 = 4 * 3_600_000;
const K13 = 2 / 14;
const K89 = 2 / 90;
const EMIT_WINDOW = 8; // bars back that may emit cards (== card validity window, == backtest pending-limit lifetime)

interface SessionArrays {
  vwap: Float64Array; sigma: Float64Array;
  poc: Float64Array; vah: Float64Array; val: Float64Array;
}
interface DayLevels {
  pdh: number; pdl: number; pdVAH: number; pdVAL: number; pdPOC: number; pwh: number; pwl: number;
}

/** Running per-bar VWAP/σ/POC/VAH/VAL of the current session — backtest_ea.running_session() semantics. */
function runningSession(cs: PlaybookCandle[]): SessionArrays {
  const n = cs.length;
  const vwap = new Float64Array(n).fill(NaN);
  const sigma = new Float64Array(n).fill(NaN);
  const poc = new Float64Array(n).fill(NaN);
  const vah = new Float64Array(n).fill(NaN);
  const val = new Float64Array(n).fill(NaN);
  let i = 0;
  while (i < n) {
    let j = i;
    const d0 = Math.floor(cs[i].t / DAY);
    while (j < n && Math.floor(cs[j].t / DAY) === d0) j++;
    let cv = 0, ctpv = 0, s2 = 0;
    let loP = Infinity, hiP = -Infinity;
    for (let k = i; k < j; k++) {
      const tp = (cs[k].h + cs[k].l + cs[k].c) / 3;
      cv += cs[k].v; ctpv += tp * cs[k].v;
      const vw = ctpv / Math.max(cv, 1e-12);
      const dev = tp - vw;
      s2 += dev * dev * cs[k].v;
      vwap[k] = vw;
      sigma[k] = Math.sqrt(Math.max(s2 / Math.max(cv, 1e-12), 0));
      loP = Math.min(loP, cs[k].l); hiP = Math.max(hiP, cs[k].h);
      if (hiP > loP && cv > 0) {
        // running volume profile over bars so far (48 bins, expand from POC to 70%)
        const bins = new Float64Array(48);
        for (let m = i; m <= k; m++) {
          const mtp = (cs[m].h + cs[m].l + cs[m].c) / 3;
          const idx = Math.min(47, Math.max(0, Math.floor(((mtp - loP) / (hiP - loP)) * 47)));
          bins[idx] += cs[m].v;
        }
        let p = 0;
        for (let b = 1; b < 48; b++) if (bins[b] > bins[p]) p = b;
        let total = 0;
        for (let b = 0; b < 48; b++) total += bins[b];
        let va = bins[p] / total, loI = p, hiI = p;
        while (va < 0.7 && (loI > 0 || hiI < 47)) {
          const up = hiI < 47 ? bins[hiI + 1] : -1;
          const dn = loI > 0 ? bins[loI - 1] : -1;
          if (up >= dn && hiI < 47) { hiI++; va += bins[hiI] / total; }
          else if (loI > 0) { loI--; va += bins[loI] / total; }
          else { hiI++; va += bins[hiI] / total; }
        }
        const bw = (hiP - loP) / 48;
        poc[k] = loP + (p + 0.5) * bw;
        vah[k] = loP + (hiI + 1) * bw;
        val[k] = loP + loI * bw;
      } else {
        poc[k] = vah[k] = val[k] = tp;
      }
    }
    i = j;
  }
  return { vwap, sigma, poc, vah, val };
}

/** h4 EMA13/89 per bar with the forming bucket's close-so-far (no lookahead) — R548 corrected. */
function h4BiasArrays(cs: PlaybookCandle[]): { e13: Float64Array; e89: Float64Array } {
  const n = cs.length;
  const e13 = new Float64Array(n);
  const e89 = new Float64Array(n);
  let e13c: number | null = null;
  let e89c: number | null = null;
  let curBt: number | null = null;
  for (let i = 0; i < n; i++) {
    const bt = Math.floor(cs[i].t / H4);
    if (curBt === null) {
      curBt = bt;
    } else if (bt !== curBt) {
      const cc = cs[i - 1].c; // previous bucket completed with its final close
      if (e13c === null || e89c === null) { e13c = cc; e89c = cc; }
      else { e13c = cc * K13 + e13c * (1 - K13); e89c = cc * K89 + e89c * (1 - K89); }
      curBt = bt;
    }
    e13[i] = e13c === null ? cs[i].c : cs[i].c * K13 + e13c * (1 - K13);
    e89[i] = e89c === null ? cs[i].c : cs[i].c * K89 + e89c * (1 - K89);
  }
  return { e13, e89 };
}

export function runPlaybook(cs: PlaybookCandle[], sym: string): { cards: PlaybookCard[]; ctx: PlaybookContext } {
  const n = cs.length;
  const emptyCtx: PlaybookContext = {
    sym, price: cs[n - 1]?.c ?? NaN, vwap: null, sigma: null, rPOC: null, rVAH: null, rVAL: null,
    pdh: null, pdl: null, pdVAH: null, pdVAL: null, pdPOC: null, pwh: null, pwl: null, atr: null, biasUp: null,
  };
  if (n < 220) return { cards: [], ctx: emptyCtx };

  // ---- feature arrays (backtest parity) ----
  const o = new Float64Array(n), h = new Float64Array(n), l = new Float64Array(n), c = new Float64Array(n), v = new Float64Array(n);
  for (let i = 0; i < n; i++) { o[i] = cs[i].o; h[i] = cs[i].h; l[i] = cs[i].l; c[i] = cs[i].c; v[i] = cs[i].v; }
  const atr = new Float64Array(n).fill(NaN);
  for (let i = 13; i < n; i++) {
    let s = 0;
    for (let k = i - 13; k <= i; k++) {
      // pandas: pc = close.shift(1) is NaN on the first row -> TR = h - l
      s += k > 0 ? Math.max(h[k] - l[k], Math.abs(h[k] - cs[k - 1].c), Math.abs(l[k] - cs[k - 1].c)) : h[k] - l[k];
    }
    atr[i] = s / 14;
  }
  const volSma = new Float64Array(n).fill(NaN);
  for (let i = 19; i < n; i++) {
    let s = 0;
    for (let k = i - 19; k <= i; k++) s += v[k];
    volSma[i] = s / 20;
  }
  const dp = new Float64Array(n); // delta_pct = (2*tbb - v)/v
  for (let i = 0; i < n; i++) dp[i] = v[i] > 0 ? (2 * cs[i].tbb - v[i]) / v[i] : NaN;
  const vz = new Float64Array(n).fill(NaN); // pandas rolling(20).std ddof=1
  for (let i = 19; i < n; i++) {
    let m = 0;
    for (let k = i - 19; k <= i; k++) m += v[k];
    m /= 20;
    let s2 = 0;
    for (let k = i - 19; k <= i; k++) s2 += (v[k] - m) * (v[k] - m);
    const sd = Math.sqrt(s2 / 19);
    vz[i] = sd > 0 ? (v[i] - m) / sd : NaN;
  }
  const sess = runningSession(cs);
  const { e13, e89 } = h4BiasArrays(cs);

  // per-day aggregates -> prior-day/week levels per day (prior_levels semantics)
  const dayOf = new Int32Array(n);
  for (let i = 0; i < n; i++) dayOf[i] = Math.floor(cs[i].t / DAY);
  const dayAgg = new Map<number, { hi: number; lo: number; lastPoc: number; lastVah: number; lastVal: number }>();
  for (let i = 0; i < n; i++) {
    const d = dayOf[i];
    let a = dayAgg.get(d);
    if (!a) { a = { hi: -Infinity, lo: Infinity, lastPoc: NaN, lastVah: NaN, lastVal: NaN }; dayAgg.set(d, a); }
    a.hi = Math.max(a.hi, h[i]); a.lo = Math.min(a.lo, l[i]);
    a.lastPoc = sess.poc[i]; a.lastVah = sess.vah[i]; a.lastVal = sess.val[i];
  }
  const weekHi = new Map<number, number>();
  const weekLo = new Map<number, number>();
  for (const [d, a] of dayAgg) {
    const wk = Math.floor((d * DAY - 4 * DAY) / (7 * DAY));
    weekHi.set(wk, Math.max(weekHi.get(wk) ?? -Infinity, a.hi));
    weekLo.set(wk, Math.min(weekLo.get(wk) ?? Infinity, a.lo));
  }
  const levelsOf = (d: number): DayLevels => {
    const prev = dayAgg.get(d - 1) ?? null;
    const wk = Math.floor((d * DAY - 4 * DAY) / (7 * DAY));
    return {
      pdh: prev?.hi ?? NaN, pdl: prev?.lo ?? NaN,
      pdVAH: prev?.lastVah ?? NaN, pdVAL: prev?.lastVal ?? NaN, pdPOC: prev?.lastPoc ?? NaN,
      pwh: weekHi.get(wk - 1) ?? NaN, pwl: weekLo.get(wk - 1) ?? NaN,
    };
  };

  const base = sym.replace(/USDT$/i, "").toUpperCase();
  const NOW = cs[n - 1].t + BAR; // close time of the last closed bar
  const cards: PlaybookCard[] = [];

  // ---------- EA-2: sweep-acceptance (gen_signals EA-2 block, 1:1) ----------
  {
    const lvls: [string, (d: number) => number][] = [
      ["PDH", (d) => levelsOf(d).pdh], ["PDL", (d) => levelsOf(d).pdl],
      ["PD-VAH", (d) => levelsOf(d).pdVAH], ["PD-VAL", (d) => levelsOf(d).pdVAL],
      ["PWH", (d) => levelsOf(d).pwh], ["PWL", (d) => levelsOf(d).pwl],
    ];
    const lastSweep = new Map<string, number>(); // level name -> day of the sweep that fired
    // NOTE: no data-edge guard here (the backtest's `range(30, n-3)` only existed to
    // keep confirmation windows from running off the DATASET end; the m-loops clamp
    // themselves, so the live engine scans every closed bar).
    for (let j = 30; j <= n - 1; j++) {
      if (!Number.isFinite(atr[j]) || !Number.isFinite(volSma[j]) || v[j] < 1.5 * volSma[j]) continue;
      const dj = dayOf[j];
      for (const [name, getL] of lvls) {
        const L = getL(dj);
        if (!Number.isFinite(L)) continue;
        if (lastSweep.get(name) === dj) continue; // one sweep per level per day
        // downside sweep -> long
        if (c[j] < L && l[j] < L && h[j] >= L && (L - l[j]) / atr[j] <= 1.5) {
          for (let m = j + 1; m <= Math.min(j + 3, n - 1); m++) {
            if (c[m] > L && dp[m] > 0.15 && c[m] > o[m]) {
              let lo = Infinity;
              for (let k = j; k <= m; k++) lo = Math.min(lo, l[k]);
              const stop = lo - 0.05 * atr[m];
              const t1 = sess.poc[m] > c[m] ? sess.poc[m] : c[m] + 2 * (c[m] - stop);
              const t2 = sess.vah[m] > t1 ? sess.vah[m] : c[m] + 2.5 * (c[m] - stop);
              const t3 = c[m] + 3 * (c[m] - stop);
              if (m >= n - EMIT_WINDOW) {
                cards.push({
                  id: `EA2-${sym}-${cs[m].t}`, engine: "EA2", sym, side: "long", kind: "market",
                  entry: c[m], stop, targets: [t1, t2, t3], rPlanned: 3,
                  status: "confirmed", signalTs: cs[m].t, validUntilTs: cs[m].t + 8 * BAR,
                  note: `${name} sweep accepted (delta +${(dp[m] * 100).toFixed(0)}%) — stop beyond sweep wick`,
                  weight: ENGINE_WEIGHTS.EA2,
                });
              }
              lastSweep.set(name, dj);
              break;
            }
          }
        }
        // upside sweep -> short
        if (c[j] > L && h[j] > L && l[j] <= L && (h[j] - L) / atr[j] <= 1.5) {
          for (let m = j + 1; m <= Math.min(j + 3, n - 1); m++) {
            if (c[m] < L && dp[m] < -0.15 && c[m] < o[m]) {
              let hi = -Infinity;
              for (let k = j; k <= m; k++) hi = Math.max(hi, h[k]);
              const stop = hi + 0.05 * atr[m];
              const t1 = sess.poc[m] < c[m] ? sess.poc[m] : c[m] - 2 * (stop - c[m]);
              const t2 = sess.val[m] < t1 ? sess.val[m] : c[m] - 2.5 * (stop - c[m]);
              const t3 = c[m] - 3 * (stop - c[m]);
              if (m >= n - EMIT_WINDOW) {
                cards.push({
                  id: `EA2-${sym}-${cs[m].t}`, engine: "EA2", sym, side: "short", kind: "market",
                  entry: c[m], stop, targets: [t1, t2, t3], rPlanned: 3,
                  status: "confirmed", signalTs: cs[m].t, validUntilTs: cs[m].t + 8 * BAR,
                  note: `${name} sweep accepted (delta ${(dp[m] * 100).toFixed(0)}%) — stop beyond sweep wick`,
                  weight: ENGINE_WEIGHTS.EA2,
                });
              }
              lastSweep.set(name, dj);
              break;
            }
          }
        }
      }
    }
    // armed previews (UI affordance only — never punchable, not a backtest concept)
    const dNow = dayOf[n - 1];
    for (let j = Math.max(30, n - 3); j <= n - 1; j++) {
      if (!Number.isFinite(atr[j]) || !Number.isFinite(volSma[j]) || v[j] < 1.5 * volSma[j]) continue;
      const dj = dayOf[j];
      if (dj !== dNow) continue;
      for (const [name, getL] of lvls) {
        const L = getL(dj);
        if (!Number.isFinite(L) || lastSweep.get(name) === dj) continue;
        if (c[j] < L && l[j] < L && h[j] >= L && (L - l[j]) / atr[j] <= 1.5) {
          cards.push({
            id: `EA2-ARM-${sym}-${cs[j].t}-${name}`, engine: "EA2", sym, side: "long", kind: "market",
            entry: L, stop: l[j] - 0.05 * atr[j], targets: [0, 0, 0], rPlanned: 3,
            status: "armed", signalTs: cs[j].t, validUntilTs: cs[j].t + 4 * BAR,
            note: `${name} sweep detected — awaiting acceptance close back above ${name}`,
            weight: ENGINE_WEIGHTS.EA2,
          });
        }
        if (c[j] > L && h[j] > L && l[j] <= L && (h[j] - L) / atr[j] <= 1.5) {
          cards.push({
            id: `EA2-ARM-${sym}-${cs[j].t}-${name}`, engine: "EA2", sym, side: "short", kind: "market",
            entry: L, stop: h[j] + 0.05 * atr[j], targets: [0, 0, 0], rPlanned: 3,
            status: "armed", signalTs: cs[j].t, validUntilTs: cs[j].t + 4 * BAR,
            note: `${name} sweep detected — awaiting acceptance close back below ${name}`,
            weight: ENGINE_WEIGHTS.EA2,
          });
        }
      }
    }
  }

  // ---------- EA-5: cascade exhaustion (gen_signals EA-5 block, 1:1; ETH/SOL only) ----------
  if (EA5_SYMS.has(base)) {
    const cascadeDay = new Map<string, number>(); // "L|day" / "S|day" -> count
    // NOTE: no data-edge guard (backtest's `range(30, n-5)` was dataset-edge only;
    // the m-loops clamp themselves — scanning to the last closed bar is correct live).
    for (let j = 30; j <= n - 1; j++) {
      if (!Number.isFinite(vz[j]) || vz[j] < 3.0) continue;
      const dj = dayOf[j];
      if (!Number.isFinite(sess.vwap[j])) continue;
      // long: cascade down bar
      let prior12Low = Infinity;
      for (let k = Math.max(0, j - 12); k < j; k++) prior12Low = Math.min(prior12Low, l[k]);
      if (c[j] < prior12Low && c[j] < sess.vwap[j]) {
        const key = `L|${dj}`;
        if ((cascadeDay.get(key) ?? 0) >= 1) continue;
        for (let m = j + 1; m <= Math.min(j + 5, n - 1); m++) {
          const dp3 = dp[m - 2] + dp[m - 1] + dp[m];
          const rng = h[m] - l[m];
          if (dp3 > 0.05 && c[m] > l[m] + 0.5 * rng && c[m] > c[m - 1]) {
            let lo = Infinity;
            for (let k = j; k <= m; k++) lo = Math.min(lo, l[k]);
            const stop = lo - 0.1 * atr[m];
            const t1 = sess.vwap[m];
            const t2 = sess.poc[m] > t1 ? sess.poc[m] : t1 + (t1 - stop) * 1.5;
            const t3 = c[m] + 2 * (c[m] - stop);
            if (m >= n - EMIT_WINDOW) {
              cards.push({
                id: `EA5-${sym}-${cs[m].t}`, engine: "EA5", sym, side: "long", kind: "market",
                entry: c[m], stop, targets: [t1, t2, t3], rPlanned: 2,
                status: "confirmed", signalTs: cs[m].t, validUntilTs: cs[m].t + 8 * BAR,
                note: `cascade vol z=${vz[j].toFixed(1)} exhausted, delta flip +${(dp3 * 100).toFixed(0)}%`,
                weight: ENGINE_WEIGHTS.EA5,
              });
            }
            cascadeDay.set(key, (cascadeDay.get(key) ?? 0) + 1);
            break;
          }
        }
      }
      // short: cascade up bar
      let prior12High = -Infinity;
      for (let k = Math.max(0, j - 12); k < j; k++) prior12High = Math.max(prior12High, h[k]);
      if (c[j] > prior12High && c[j] > sess.vwap[j]) {
        const key = `S|${dj}`;
        if ((cascadeDay.get(key) ?? 0) >= 1) continue;
        for (let m = j + 1; m <= Math.min(j + 5, n - 1); m++) {
          const dp3 = dp[m - 2] + dp[m - 1] + dp[m];
          const rng = h[m] - l[m];
          if (dp3 < -0.05 && c[m] < h[m] - 0.5 * rng && c[m] < c[m - 1]) {
            let hi = -Infinity;
            for (let k = j; k <= m; k++) hi = Math.max(hi, h[k]);
            const stop = hi + 0.1 * atr[m];
            const t1 = sess.vwap[m];
            const t2 = sess.poc[m] < t1 ? sess.poc[m] : t1 - (stop - t1) * 1.5;
            const t3 = c[m] - 2 * (stop - c[m]);
            if (m >= n - EMIT_WINDOW) {
              cards.push({
                id: `EA5-${sym}-${cs[m].t}`, engine: "EA5", sym, side: "short", kind: "market",
                entry: c[m], stop, targets: [t1, t2, t3], rPlanned: 2,
                status: "confirmed", signalTs: cs[m].t, validUntilTs: cs[m].t + 8 * BAR,
                note: `cascade vol z=${vz[j].toFixed(1)} exhausted, delta flip ${(dp3 * 100).toFixed(0)}%`,
                weight: ENGINE_WEIGHTS.EA5,
              });
            }
            cascadeDay.set(key, (cascadeDay.get(key) ?? 0) + 1);
            break;
          }
        }
      }
    }
  }

  // ---------- EA-6: SMC BOS + FVG retest (backtest_portfolio.gen_ea6, 1:1, wide zone) ----------
  {
    let LSH: number | null = null;   // last confirmed swing high
    let LSL: number | null = null;   // last confirmed swing low
    let fvg: { side: "L" | "S"; lo: number; hi: number } | null = null; // last FVG (WIDE zone)
    let bosArmed: number | null = null; // bar index of the last emitted BOS signal
    for (let i = 30; i < n; i++) {
      // state updates first (swing pivots confirmed 2 bars later; FVG on this bar)
      const k = i - 2;
      if (cs[k].h > cs[k - 1].h && cs[k].h > cs[k - 2].h && cs[k].h > cs[k + 1].h && cs[k].h > cs[k + 2].h) LSH = cs[k].h;
      if (cs[k].l < cs[k - 1].l && cs[k].l < cs[k - 2].l && cs[k].l < cs[k + 1].l && cs[k].l < cs[k + 2].l) LSL = cs[k].l;
      if (cs[i].l > cs[i - 2].h) fvg = { side: "L", lo: cs[i - 2].l, hi: cs[i].h };
      if (cs[i].h < cs[i - 2].l) fvg = { side: "S", lo: cs[i].l, hi: cs[i - 2].h };
      if (!Number.isFinite(atr[i])) continue;
      const minutesIntoDay = (cs[i].t % DAY) / 60000;
      if (minutesIntoDay >= 23 * 60 + 30) continue; // 23:30 UTC cutoff (signal emission only)
      // bullish BOS
      if (LSH !== null && c[i] > LSH && (bosArmed === null || bosArmed < i - 1)) {
        if (LSL !== null && e13[i] > e89[i] && fvg && fvg.side === "L") {
          const mid = (fvg.lo + fvg.hi) / 2;
          const stop = Math.min(fvg.lo, LSL) - 0.05 * atr[i];
          const t1 = LSH + 0.5 * atr[i];
          const t2Local = c[i] + 2 * (mid - stop);
          const t3Local = mid + 3 * (mid - stop);
          const T2 = Math.max(t2Local, t1);
          const T3 = Math.max(t3Local, t2Local);
          if (i >= n - EMIT_WINDOW) {
            const touched = cs.slice(i + 1).some((b) => b.l <= mid);
            cards.push({
              id: `EA6-${sym}-${cs[i].t}`, engine: "EA6", sym, side: "long", kind: "limit",
              entry: mid, stop, targets: [t1, T2, T3], rPlanned: 3,
              status: touched ? "confirmed" : "pending-fill",
              signalTs: cs[i].t, validUntilTs: cs[i].t + 8 * BAR,
              note: `bullish BOS → FVG retest limit @ mid (zone ${fvg.lo.toFixed(2)}–${fvg.hi.toFixed(2)})`,
              weight: ENGINE_WEIGHTS.EA6,
            });
          }
          bosArmed = i;
        }
        LSH = null; // consumed on any close-through
      }
      // bearish BOS
      if (LSL !== null && c[i] < LSL && (bosArmed === null || bosArmed < i - 1)) {
        if (LSH !== null && e13[i] < e89[i] && fvg && fvg.side === "S") {
          const mid = (fvg.lo + fvg.hi) / 2;
          const stop = Math.max(fvg.hi, LSH) + 0.05 * atr[i];
          const t1 = LSL - 0.5 * atr[i];
          const t2Local = c[i] - 2 * (stop - mid);
          const t3Local = mid - 3 * (stop - mid);
          const T2 = Math.min(t2Local, t1);
          const T3 = Math.min(t3Local, t2Local);
          if (i >= n - EMIT_WINDOW) {
            const touched = cs.slice(i + 1).some((b) => b.h >= mid);
            cards.push({
              id: `EA6-${sym}-${cs[i].t}`, engine: "EA6", sym, side: "short", kind: "limit",
              entry: mid, stop, targets: [t1, T2, T3], rPlanned: 3,
              status: touched ? "confirmed" : "pending-fill",
              signalTs: cs[i].t, validUntilTs: cs[i].t + 8 * BAR,
              note: `bearish BOS → FVG retest limit @ mid (zone ${fvg.lo.toFixed(2)}–${fvg.hi.toFixed(2)})`,
              weight: ENGINE_WEIGHTS.EA6,
            });
          }
          bosArmed = i;
        }
        LSL = null; // consumed on any close-through
      }
    }
  }

  const last = n - 1;
  const lastLevels = levelsOf(dayOf[last]);
  const ctx: PlaybookContext = {
    sym, price: c[last], vwap: num(sess.vwap[last]), sigma: num(sess.sigma[last]),
    rPOC: num(sess.poc[last]), rVAH: num(sess.vah[last]), rVAL: num(sess.val[last]),
    pdh: num(lastLevels.pdh), pdl: num(lastLevels.pdl), pdVAH: num(lastLevels.pdVAH),
    pdVAL: num(lastLevels.pdVAL), pdPOC: num(lastLevels.pdPOC),
    pwh: num(lastLevels.pwh), pwl: num(lastLevels.pwl),
    atr: num(atr[last]), biasUp: e13[last] > e89[last] ? true : e13[last] < e89[last] ? false : null,
  };
  const live = cards.filter((cd) => cd.validUntilTs >= NOW);
  return { cards: live, ctx };
}

function num(x: number): number | null {
  return Number.isFinite(x) ? x : null;
}
