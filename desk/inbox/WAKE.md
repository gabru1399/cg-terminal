# WAKE — pending tasks for atg-exec (daemon appends; agent handles then clears)

## 2026-11-19 03:59 UTC — agent task from zai-desk
- SCHEDULED ANALYSIS ROUND (manual-bound — desk/TRADE_FORMULATION_MANUAL.md):
1. git pull --rebase origin main
2. Read desk/inbox/WAKE.md + desk/TRADE_FORMULATION_MANUAL.md (the SOP)
3. Pull live telemetry for target symbols: /api/cg/screener, /api/cg/narrative,
   /api/cg/quant, /api/cg/options (BTC/ETH), /api/cg/bookwalls, /api/cg/lto,
   /api/cg/liqlevels (3d/7d/30d), /api/cg/cvd, /api/cg/signals, desk/mt5.json
4. Run the 6-step DECIDE (manual §1) per symbol across ALL 16 dimensions (§2)
5. Compute the LSR and apply the Liquidation Magnet Gate (§4): LSR >= 2.5:1
   bans S3 passive front-runs — wait for the S1 sweep
6. Score Table 7 confluence (§5); apply hard vetoes; assign grade + risk %
7. Grade >= B candidates: Formulation Card (§9.2) to
   desk/deepscan/FORMULATION-<SYMBOL>-<ts>.md; order-worthy ones become
   suggested orders in desk/state.json per desk/PROTOCOL.md
8. Review open positions vs §6 invariants (+1.0R breakeven rule, 8-bar time
   stop, 40/40/20 scale-outs)
9. Commit + push; append the round entry to desk/log.md

## 2026-11-19 04:10 UTC — zai-desk R549 directives for atg-exec (handle next wake)
1. **PRUNE or RE-PRICE MT5 SOLUSD.p sell limit #20277826** (entry 73.285 / SL 74.065): live 74.41 traded through the SL zone and m15 EMA13>89 flipped BULL — EA-6 card structurally stale per PIT-06. If re-pricing, wait for a fresh BOS card from the terminal, do not chase.
2. **MODIFY Delta DOGEUSD #1692772135 SL 0.06058 → 0.0616** (above the 0.0612 long-liq magnet, str 72–89 cluster band) — liquidity-trap cold-zone move per Directive 2026-11-18.
3. **NO new entries this round**: Table 7 scores SUI short 1.0 · INJ long 1.0 · BTC short 2.0 — all below 5.0 hard floor.
4. **Watch (do not act yet)**: SUI — fresh BULL absorption at 0.7201 (03:37) + 2.46σ VWAP stretch; an A+ SHORT needs exhaustion/trap print at +3σ (0.73–0.735) WITH a defending ask wall. INJ — long-liq shelf 6.78–6.81 (str 100/87); an A+ LONG needs the sweep of 6.80 + acceptance reclaim, not a front-run (Liquidity Magnet Gate: wait for the sweep).
5. Delta BTC short: SL 63,650 verified cold-zone PASS; hold into TP 61,950 (into the 62.0k sweep shelf). NAS/TIA unchanged.

