# PLAYBOOK — EA Archetypes VALIDATED on Real Data (Round R546)

**Status: VALIDATED · 2026-11-18 · zai-desk**
**Data: real Binance USDT-M futures 15m klines, 2026-05-01 → 2026-11-17 (201 days, 57,819 bars × BTC/ETH/SOL)**
**Engine: conservative fills (stop-first worst case), maker 0.02% / taker 0.05% / stop slippage 0.02% — ALL stats NET of costs.**
**Scripts: scripts/backtest_ea.py, scripts/diag_ea.py, scripts/charts_ea.py · Results: data/backtest/results.json, trades.csv**

---

## POOLED RESULTS (net R, 201 days)

| Engine | Verdict | n | Net R | WR | PF | MaxDD | Notes |
|---|---|---|---|---|---|---|---|
| **EA-2 Sweep-Acceptance** | **LIVE — PRIMARY** | 433 | **+113.1** | 45.5% | 1.51 | 19.9R | Positive on BTC/ETH/SOL, 6/7 months, both sides |
| **EA-5 Cascade-Exhaustion** | **LIVE — ETH/SOL ONLY** | 568 | +70.5 | 39.3% | 1.27 | 50.2R | ETH+SOL: **+104.2R, PF 1.69, 367 trades**; BTC **−33.8R → banned on BTC** |
| EA-1 OFI Trend Pullback | SUSPENDED | 179 | −19.6 | 37.4% | 0.75 | — | Fails conservative fills; ablation confirms |
| EA-3 VA-Extreme Reversion | SUSPENDED | 130 | −14.9 | 43.8% | 0.82 | — | Edge absent in this regime |
| EA-4 UTC ORB | SUSPENDED (crypto) | 88 | −31.7 | 51.1% | 0.45 | — | No session-close structure in 24/7 crypto |
| **LIVE SET (EA-2 all + EA-5 ETH/SOL)** | — | 800 | **+217.3** | 43.4% | **1.58** | 45.1R | ≈ 4 trades/day, avg +0.27R/trade |

---

## ENGINE A — EA-2 SWEEP-ACCEPTANCE (primary; all liquid majors)

1. **Levels (pre-registered, from kline_series/d1 + session VA):** prior-day high/low, prior-week high/low, prior-day VAH/VAL.
2. **Sweep event:** a bar CLOSES through the level after touching it, volume ≥ 1.5 × SMA20(volume), sweep depth ≤ 1.5 × ATR14(15m). Depth > 1.5 ATR = cascade, not sweep → hand to Engine B / stand down.
3. **Entry (confirmation, within 3 bars of sweep):** a bar closes back through the level with taker-delta skew ≥ 15% in the reversal direction AND a reversal-direction body. Enter at that close.
4. **Stop:** beyond the sweep wick extreme ± 0.05 ATR. DATA-DRIVEN, never a %.
5. **Targets (40/40/20 ladder):** T1 = running session POC · T2 = running VAH/VAL (or next prior-day extreme) · T3 = +3R runner.
6. **Invariants (already enforced in engine):** BE stop at +1R excursion · time-stop 8 bars (2h) if < +0.5R · one sweep per level per day · one position per archetype per symbol.
7. **Evidence:** 433 trades · +113.1R net · PF 1.51 · shorts +96.2R / longs +16.9R (both tradeable) · runners (T3) produce +185.8R — hold the runner, it IS the engine · BE-stop exits add +93.8R · monthly: May +2.1 Jun +16.0 Jul +36.6 Aug −12.5 Sep +47.1 Oct +3.0 Nov +20.7.

## ENGINE B — EA-5 CASCADE-EXHAUSTION (secondary; ETH, SOL ONLY — banned on BTC)

1. **Cascade bar:** volume z-score ≥ 3.0 AND close makes a 12-bar low (long) / high (short) beyond the running day VWAP.
2. **Entry (within 5 bars):** 3-bar cumulative delta flips sign (> ±0.05) AND closing body ≥ 50% in the reversal direction AND close beyond prior bar's close. Enter at that close.
3. **Stop:** cascade extreme ± 0.1 ATR.
4. **Targets:** T1 = running day VWAP · T2 = running POC · T3 = +2R (quick reversion — do not over-hold).
5. **One setup per day per side** · spec time-stop (8 bars) applies · max hold 96 bars.
6. **Evidence:** ETH+SOL: 367 trades · +104.2R net · Sep–Nov streak +91.4R · BTC: −33.8R (cascade continuation venue) — **do not run on BTC** until regime flag exists.

## SUSPENDED RULES — DO NOT TRADE

- **EA-1** (trend + OFI pullback): pooled PF 0.75; the OFI≥0.25 filter did not rescue it (ablation EA-1A PF 0.98, BTC −275.5R). Re-arm ONLY after hftbacktest fill-rate validation (P1) shows pullback limits actually fill where assumed.
- **EA-3** (VA-extreme reversion): PF 0.82. Re-test next quarter with looser delta-confirmation gate on a different regime window.
- **EA-4** (ORB): PF 0.45 on crypto — structurally inapplicable (no cash close). Revisit ONLY for TradFi sleeves on equities-hours products.

## RISK GOVERNANCE (unchanged from Canonical Spec §risk)

- **Grade B engine (live-set PF 1.58):** **0.5% risk per trade**. Live-start recommendation: **0.25% for the first 50 real fills**, then scale to 0.5% only if realized distribution matches backtest (LR overlay, pre-registered).
- Max 2 same-direction crypto positions · total heat ≤ 1.0% · metals/commodities slot 3.
- Funding cost not modeled (~±0.01%/8h typical) — long holds in positive-funding regimes shave ~0.3R per 24h; prefer maker entries where Delta fees allow.
- Every live fill logged to `desk/log.md` with archetype tag; outcome feeds the per-archetype LR ledger (≥20 outcomes before any parameter edit).

## TERMINAL WIRING (how each rule reads the live terminal)

| Rule input | Terminal source |
|---|---|
| Sweep levels (PDH/PDL/PWH/PWL/VAH/VAL) | `market_snapshot` (auction session/day/month) + `kline_series` d1 |
| Sweep depth vs ATR | `kline_series` 15m (ATR14) |
| Taker-delta skew / delta flip | `footprint` (interval 15m, per-bar delta %) + CVD `cvd_state` |
| Cascade volume z-score | `footprint` per-bar volume vs 20-bar baseline |
| Running POC/VAH/VAL/VWAP | `market_snapshot` (session 8h / UTC day) |
| Walls/clusters for target sanity | `liquidation_levels`, `whale_orders`, `book_walls` |

**atg-exec directive:** generate candidate cards ONLY from Engine A / Engine B rules above; tag each card `EA2` or `EA5-ETHSOL`; cards from suspended archetypes are rejected at intake. zai-desk runs the same rules per 15-min round and posts suggested orders to WAKE.md as usual.
