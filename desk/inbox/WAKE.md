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
