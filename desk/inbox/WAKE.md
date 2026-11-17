# WAKE — active tasks and directives for atg-exec (ephemeral beacon)

## ACTIVE DESK DIRECTIVES
- **VENUE & ACCOUNT**: Delta Exchange India (`india_prod` | Account `26902927`).
- **CANONICAL SOP & LINE-BY-LINE MANDATE**: `desk/TRADE_FORMULATION_MANUAL.md` calibrated by `desk/SWARM_MASTER_PROMPT.md` and `.gemini/rules/SWARM_EXECUTION.md`. MANDATORY BY DEFAULT AT ALL TIMES ON EVERY TURN.
- **MANDATORY SLASH COMMANDS**: All autonomous turns, dynamic prompts, and execution cycles MUST incorporate `/goal /executing-plans /plan /brainstorming` to enforce pre-flight planning and Socratic formulation testing.
- **UNIVERSE TRACKING**: 61 Curated Assets (30 Crypto USDT-M Perps + 28 TradFi USDT-M Perps + 3 Classic Indices). Full screening on every round with zero omissions.
- **SHARED ACCOUNT ISOLATION (P5-01b)**: Two separate chats run on this Delta account. Track orders strictly via internal order numbers. Never touch or cancel orders from the external chat (`FIB4H_*`, `SOLVUSD`, `TACUSD`).
- **EXECUTION CADENCE & TIMER FORMAT**: Dynamic 1200s timer (`schedule(DurationSeconds=1200)`). Zero static cron jobs. Standard format: `Timer: 20m, Prompt: /goal /executing-plans /plan /brainstorming Autonomous Delta Exchange Trade Execution & Recursive Self-Improving Engine Round R<n>. Audit all 61 Curated Assets and find high potential high confluence trading setup strictly using @[c:\Users\SIGMA\Documents\cg-terminal\desk\SWARM_MASTER_PROMPT.md] @[c:\Users\SIGMA\Documents\cg-terminal\desk\TRADE_FORMULATION_MANUAL.md]  , monitor live running short positions on Delta Exchange India (BTCUSD @ $64,750 and ETHUSD @ $1,812.50), enforce +1.0R breakeven invariant ($64,450 BTC / $1,805.50 ETH) and 8-bar time stop, audit margin and liquidity, and re-arm dynamic 1200s recursion.`
- **CONCURRENCY & RISK**: Max 2 concurrent positions. Max 1.0% portfolio heat. Isolated margin, maker post-only, mark-price stops.
- **HISTORICAL LOGS**: Archived to `desk/inbox/archive/WAKE_ARCHIVE_20261115.md`.

## 2026-11-15 19:00 UTC — active round directive
- Execute canonical 360° autonomous round per `desk/SWARM_MASTER_PROMPT.md`:
  1. Ingest 30-asset closed-candle screener (`http://127.0.0.1:3000/api/cg/screener`).
  2. Compute zero-fallback Table 7 (Factor 1 = 0.0 in `RANGE_BALANCE`).
  3. Enforce Liquidation Magnet Gate (LSR >= 2.5:1 bans passive entries).
  4. Socratic gates & DECIDE dossiers for qualified setups (>= 5.0 pts).
  5. Check running positions for +1.0R Breakeven and 8-bar time stop.
  6. Re-arm dynamic 1200s timer.

## 2026-11-15 19:29 UTC — agent task from zai-desk
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

## 2026-11-15 20:00 UTC — agent task from zai-desk
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

## 2026-11-15 20:30 UTC — agent task from zai-desk
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

## 2026-11-15 21:00 UTC — agent task from zai-desk
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

## 2026-11-15 21:30 UTC — agent task from zai-desk
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

## 2026-11-15 22:00 UTC — agent task from zai-desk
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

## 2026-11-15 22:30 UTC — agent task from zai-desk
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

## 2026-11-15 23:00 UTC — agent task from zai-desk
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

## 2026-11-15 23:00 UTC — ALERT A5 — position-close
- BELL + WAKE: BTC position closed — capture close price + PnL for desk/log.md

## 2026-11-15 23:30 UTC — agent task from zai-desk
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

## 2026-11-16 00:00 UTC — agent task from zai-desk
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

## 2026-11-16 00:30 UTC — agent task from zai-desk
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

## 2026-11-16 00:59 UTC — agent task from zai-desk
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

## 2026-11-16 01:29 UTC — agent task from zai-desk
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

## 2026-11-16 01:59 UTC — agent task from zai-desk
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

## 2026-11-16 01:59 UTC — ALERT A5 — position-close
- BELL + WAKE: BTC position closed — capture close price + PnL for desk/log.md

## 2026-11-16 02:29 UTC — agent task from zai-desk
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

## 2026-11-16 03:00 UTC — agent task from zai-desk
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

## 2026-11-16 03:30 UTC — agent task from zai-desk
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

## 2026-11-16 04:00 UTC — agent task from zai-desk
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

## 2026-11-16 04:29 UTC — agent task from zai-desk
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

## 2026-11-16 04:59 UTC — agent task from zai-desk
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

## 2026-11-16 06:51 UTC — agent task from zai-desk
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

## 2026-11-16 06:59 UTC — agent task from zai-desk
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

## 2026-11-16 07:30 UTC — agent task from zai-desk
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

## 2026-11-16 07:59 UTC — agent task from zai-desk
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

## 2026-11-16 08:29 UTC — agent task from zai-desk
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

## 2026-11-16 09:29 UTC — new suggested order — place in MT5 (debate FOR 7/AGAINST 0)
- R358-DOGE-1 DOGE SHORT limit entry 0.05869 · stop 0.05901 · targets 0.05797 / 0.05758 / 0.05744 · R 2.3 · expires 2026-11-16 13:29 UTC
- BASIS: levels are PERP prices (perpRef 0.0584). Before placing in MT5 read spreads.DOGUSD.basisPct in desk/mt5.json and set every level = perpLevel × (1 + basisPct/100). Remember the broker spread — a SHORT fills at bid.
- [FOR] overview: h4 ↓/d1 ↓ EMA, price below day VWAP (0.05840 vs 0.05888), h4 RSI 34.4, day -2.4%
- [FOR] footprint: bull 26 / bear 32; recent: Bear div/sell[time], Absorption/sell[vol], Absorption/sell[range]
- [FOR] microFlow(abs/trap/exh): 6h micro-events: abs:buy×2, abs:sell×5, div:sell×3, exh:buy×3, sdiv:sell×2, trap:buy×1 — net 6 buy-side vs 10 sell-side
- [FOR] liquidation: long-liq magnet 0.05807 (str 82, ~$8M est, -0.54%) as target
- [FOR] bookWalls: ±5% depth imbalance -0.057 (5m ago -0.082, rising bids); bid $0.03B vs ask $0.04B
- [FOR] cvd: taker buy 48.9%, perpCvd -72, spotCvd -12, quadrant both-selling, latestDiv bear (recent)
- [FOR] notifications: 6h weighted bias -1.0 (1 events)
- → place on DOGUSD in MT5, then set status "placed" + ticket + ACTUAL MT5 levels in desk/state.json and append an EXEC entry to desk/log.md

## 2026-11-16 09:29 UTC — new suggested order — place in MT5 (debate FOR 5/AGAINST 2)
- R358-XAU-2 XAU SHORT limit entry 3876.72 · stop 3892.17 · targets 3805.37 / 3797.27 · R 4.6 · expires 2026-11-16 13:29 UTC
- BASIS: levels are PERP prices (perpRef 3862.35). Before placing in MT5 read spreads.XAUUSD.basisPct in desk/mt5.json and set every level = perpLevel × (1 + basisPct/100). Remember the broker spread — a SHORT fills at bid.
- [FOR] overview: h4 ↓/d1 ↓ EMA, price below day VWAP (3,862.35 vs 3,869.63), h4 RSI 42.0, day -1.1%
- [FOR] footprint: bull 12 / bear 17; recent: Exhaustion/buy[range]
- [AGAINST] microFlow(abs/trap/exh): 6h micro-events: div:buy×1, exh:buy×1 — net 2 buy-side vs 0 sell-side
- [FOR] liquidation: long-liq magnet 3,805.37 (str 44, ~$30M est, -1.48%) as target
- [FOR] bookWalls: ±5% depth imbalance +0.113 (5m ago +0.113, falling bids); bid $0.05B vs ask $0.04B
- [FOR] cvd: taker buy 48.8%, perpCvd -151, spotCvd -1, quadrant both-selling, latestDiv bear (recent)
- [AGAINST] notifications: 6h weighted bias +2.0 (1 events)
- → place on XAUUSD in MT5, then set status "placed" + ticket + ACTUAL MT5 levels in desk/state.json and append an EXEC entry to desk/log.md

## 2026-11-16 09:29 UTC — new suggested order — place in MT5 (debate FOR 5/AGAINST 2)
- R358-ETH-3 ETH SHORT limit entry 1811 · stop 1819.45 · targets 1789.79 / 1787.15 / 1771.31 · R 2.5 · expires 2026-11-16 13:29 UTC
- BASIS: levels are PERP prices (perpRef 1799.15). Before placing in MT5 read spreads.ETHUSD.basisPct in desk/mt5.json and set every level = perpLevel × (1 + basisPct/100). Remember the broker spread — a SHORT fills at bid.
- [FOR] overview: h4 ↓/d1 ↓ EMA, price below day VWAP (1,799.15 vs 1,813.87), h4 RSI 34.1, day -1.9%
- [AGAINST] footprint: bull 22 / bear 13; recent: Exhaustion/buy[vol], Exhaustion/buy[range]
- [AGAINST] microFlow(abs/trap/exh): 6h micro-events: abs:buy×2, div:sell×1, exh:buy×3, exh:sell×2, sdiv:sell×1, trap:buy×1 — net 6 buy-side vs 4 sell-side
- [FOR] liquidation: long-liq magnet 1,789.79 (str 67, ~$214M est, -0.48%) as target
- [FOR] bookWalls: ±5% depth imbalance -0.011 (5m ago +0.003, falling bids); bid $0.58B vs ask $0.59B
- [FOR] cvd: taker buy 49.0%, perpCvd -1773, spotCvd -384, quadrant both-selling, latestDiv bear (recent)
- [FOR] notifications: 6h weighted bias -1.0 (3 events)
- → place on ETHUSD in MT5, then set status "placed" + ticket + ACTUAL MT5 levels in desk/state.json and append an EXEC entry to desk/log.md

## 2026-11-16 09:29 UTC — new suggested order — place in MT5 (debate FOR 5/AGAINST 1)
- R358-XRP-4 XRP SHORT limit entry 0.9571 · stop 0.9637 · targets 0.9402 / 0.9366 / 0.9258 · R 2.6 · expires 2026-11-16 13:29 UTC
- BASIS: levels are PERP prices (perpRef 0.9442). Before placing in MT5 read spreads.XRPUSD.basisPct in desk/mt5.json and set every level = perpLevel × (1 + basisPct/100). Remember the broker spread — a SHORT fills at bid.
- [FOR] overview: h4 ↓/d1 ↓ EMA, price below day VWAP (0.9442 vs 0.9577), h4 RSI 37.0, day -3.0%
- [AGAINST] footprint: bull 48 / bear 38; recent: Divergence/sell[time], Absorption/sell[vol], Absorption/sell[range]
- [FOR] microFlow(abs/trap/exh): 6h micro-events: abs:buy×3, abs:sell×3, div:buy×2, div:sell×6, exh:buy×4, exh:sell×2, sdiv:buy×1, sdiv:sell×1, trap:buy×1, trap:sell×1 — net 11 buy-side vs 13 sell-side
- [FOR] liquidation: long-liq magnet 0.9402 (str 55, ~$17M est, -0.36%) as target
- [FOR] bookWalls: ±5% depth imbalance -0.211 (5m ago -0.102, falling bids); bid $0.04B vs ask $0.07B
- [FOR] cvd: taker buy 48.2%, perpCvd -274, spotCvd -67, quadrant both-selling, latestDiv bear (recent)
- → place on XRPUSD in MT5, then set status "placed" + ticket + ACTUAL MT5 levels in desk/state.json and append an EXEC entry to desk/log.md

## 2026-11-16 09:29 UTC — agent task from zai-desk
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

## 2026-11-16 09:29 UTC — agent task from zai-desk
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

## 2026-11-16 09:59 UTC — agent task from zai-desk
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

## 2026-11-16 10:29 UTC — agent task from zai-desk
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

## 2026-11-16 10:59 UTC — agent task from zai-desk
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

## 2026-11-16 11:29 UTC — agent task from zai-desk
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

## 2026-11-16 11:59 UTC — agent task from zai-desk
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

## 2026-11-16 12:29 UTC — agent task from zai-desk
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

## 2026-11-16 12:59 UTC — agent task from zai-desk
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

## 2026-11-16 13:29 UTC — agent task from zai-desk
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

## 2026-11-16 13:59 UTC — agent task from zai-desk
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

## 2026-11-16 14:30 UTC — new suggested order — place in MT5 (debate FOR 7/AGAINST 0)
- R379-LINK-1 LINK SHORT limit entry 9.202 · stop 9.258 · targets 9.073 / 8.981 / 8.945 · R 2.3 · expires 2026-11-16 18:29 UTC
- BASIS: levels are PERP prices (perpRef 9.179). Before placing in MT5 read spreads.LNKUSD.basisPct in desk/mt5.json and set every level = perpLevel × (1 + basisPct/100). Remember the broker spread — a SHORT fills at bid.
- [FOR] overview: h4 ↓/d1 ↓ EMA, price above day VWAP (9.179 vs 9.147), h4 RSI 37.7, day -1.2%
- [FOR] footprint: bull 42 / bear 45; recent: Divergence/sell[time], Exhaustion/sell[vol], Absorption/buy[range]
- [FOR] microFlow(abs/trap/exh): 6h micro-events: abs:buy×4, abs:sell×8, div:buy×3, div:sell×5, exh:buy×1, exh:sell×2, sdiv:buy×1, sdiv:sell×1, trap:buy×2, trap:sell×2 — net 11 buy-side vs 18 sell-side
- [FOR] liquidation: long-liq magnet 8.981 (str 76, ~$2M est, -2.12%) as target
- [FOR] bookWalls: ±5% depth imbalance +0.030 (5m ago -0.003, rising bids); bid $0.01B vs ask $0.01B
- [FOR] cvd: taker buy 48.7%, perpCvd -25, spotCvd -8, quadrant both-selling, latestDiv bull (recent)
- [FOR] notifications: 6h weighted bias -5.9 (11 events)
- → place on LNKUSD in MT5, then set status "placed" + ticket + ACTUAL MT5 levels in desk/state.json and append an EXEC entry to desk/log.md

## 2026-11-16 14:30 UTC — new suggested order — place in MT5 (debate FOR 5/AGAINST 2)
- R379-BNB-2 BNB SHORT limit entry 593.78 · stop 596.39 · targets 588.12 / 582.88 / 581.62 · R 2.2 · expires 2026-11-16 18:29 UTC
- BASIS: levels are PERP prices (perpRef 590.99). Before placing in MT5 read spreads.BNBUSD.basisPct in desk/mt5.json and set every level = perpLevel × (1 + basisPct/100). Remember the broker spread — a SHORT fills at bid.
- [FOR] overview: h4 ↓/d1 ↓ EMA, price below day VWAP (590.99 vs 591.18), h4 RSI 32.4, day -1.0%
- [AGAINST] footprint: bull 29 / bear 28; recent: Absorption/sell[time], Absorption/sell[vol], Absorption/sell[range]
- [FOR] microFlow(abs/trap/exh): 6h micro-events: abs:sell×6, div:sell×3, exh:buy×4 — net 4 buy-side vs 9 sell-side
- [FOR] liquidation: long-liq magnet 582.88 (str 51, ~$6M est, -1.37%) as target
- [FOR] bookWalls: ±5% depth imbalance +0.035 (5m ago +0.035, falling bids); bid $0.02B vs ask $0.02B
- [FOR] cvd: taker buy 47.9%, perpCvd -85, spotCvd -17, quadrant both-selling, latestDiv bear (recent)
- [AGAINST] notifications: 6h weighted bias +1.0 (1 events)
- → place on BNBUSD in MT5, then set status "placed" + ticket + ACTUAL MT5 levels in desk/state.json and append an EXEC entry to desk/log.md

## 2026-11-16 14:30 UTC — agent task from zai-desk
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

## 2026-11-16 14:59 UTC — agent task from zai-desk
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

## 2026-11-16 15:30 UTC — new suggested order — place in MT5 (debate FOR 6/AGAINST 1)
- R382-XAU-1 XAU SHORT limit entry 3876.72 · stop 3892.21 · targets 3800.58 · R 4.9 · expires 2026-11-16 19:29 UTC
- BASIS: levels are PERP prices (perpRef 3871.46). Before placing in MT5 read spreads.XAUUSD.basisPct in desk/mt5.json and set every level = perpLevel × (1 + basisPct/100). Remember the broker spread — a SHORT fills at bid.
- [FOR] overview: h4 ↓/d1 ↓ EMA, price below day VWAP (3,871.46 vs 3,871.90), h4 RSI 44.5, day -0.8%
- [FOR] footprint: bull 9 / bear 19; recent: Exhaustion/sell[time], Exhaustion/sell[vol]
- [FOR] microFlow(abs/trap/exh): 6h micro-events: div:sell×1, exh:sell×5 — net 0 buy-side vs 6 sell-side
- [FOR] liquidation: long-liq magnet 3,800.58 (str 51, ~$41M est, -1.83%) as target
- [AGAINST] liquidation-hazard: short-liq magnet 3,917.81 (str 100) sits between entry and stop — sweep risk
- [FOR] bookWalls: ±5% depth imbalance +0.131 (5m ago +0.095, rising bids); bid $0.05B vs ask $0.04B
- [FOR] cvd: taker buy 49.1%, perpCvd -124, spotCvd +0, quadrant both-selling, latestDiv bear (recent)
- → place on XAUUSD in MT5, then set status "placed" + ticket + ACTUAL MT5 levels in desk/state.json and append an EXEC entry to desk/log.md

## 2026-11-16 15:30 UTC — new suggested order — place in MT5 (debate FOR 6/AGAINST 1)
- R382-XRP-2 XRP SHORT limit entry 0.9565 · stop 0.9639 · targets 0.9401 / 0.9366 / 0.9261 · R 2.2 · expires 2026-11-16 19:29 UTC
- BASIS: levels are PERP prices (perpRef 0.9454). Before placing in MT5 read spreads.XRPUSD.basisPct in desk/mt5.json and set every level = perpLevel × (1 + basisPct/100). Remember the broker spread — a SHORT fills at bid.
- [FOR] overview: h4 ↓/d1 ↓ EMA, price below day VWAP (0.9454 vs 0.9560), h4 RSI 37.1, day -2.9%
- [FOR] footprint: bull 29 / bear 37; recent: Divergence/sell[time], Divergence/sell[vol], Exhaustion/buy[range]
- [FOR] microFlow(abs/trap/exh): 6h micro-events: abs:buy×1, abs:sell×1, div:buy×2, div:sell×8, exh:buy×3, exh:sell×1, sdiv:sell×1 — net 6 buy-side vs 11 sell-side
- [FOR] liquidation: long-liq magnet 0.9401 (str 60, ~$17M est, -0.64%) as target
- [FOR] bookWalls: ±5% depth imbalance +0.005 (5m ago -0.177, rising bids); bid $0.06B vs ask $0.06B
- [FOR] cvd: taker buy 48.1%, perpCvd -280, spotCvd -83, quadrant both-selling, latestDiv bear (stale/none)
- [AGAINST] notifications: 6h weighted bias +1.0 (1 events)
- → place on XRPUSD in MT5, then set status "placed" + ticket + ACTUAL MT5 levels in desk/state.json and append an EXEC entry to desk/log.md

## 2026-11-16 15:30 UTC — new suggested order — place in MT5 (debate FOR 5/AGAINST 2)
- R382-DOGE-3 DOGE SHORT limit entry 0.05876 · stop 0.05916 · targets 0.05754 / 0.0573 / 0.05707 · R 3.1 · expires 2026-11-16 19:29 UTC
- BASIS: levels are PERP prices (perpRef 0.05827). Before placing in MT5 read spreads.DOGUSD.basisPct in desk/mt5.json and set every level = perpLevel × (1 + basisPct/100). Remember the broker spread — a SHORT fills at bid.
- [FOR] overview: h4 ↓/d1 ↓ EMA, price below day VWAP (0.05827 vs 0.05882), h4 RSI 34.0, day -2.6%
- [AGAINST] footprint: bull 32 / bear 31; recent: Absorption/buy[time], Absorption/buy[vol], Exhaustion/buy[range]
- [AGAINST] microFlow(abs/trap/exh): 6h micro-events: abs:buy×3, div:sell×2, exh:buy×2, exh:sell×3, sdiv:buy×1, sdiv:sell×1, trap:buy×1 — net 7 buy-side vs 6 sell-side
- [FOR] liquidation: long-liq magnet 0.05754 (str 64, ~$7M est, -1.35%) as target
- [FOR] bookWalls: ±5% depth imbalance +0.004 (5m ago -0.067, rising bids); bid $0.03B vs ask $0.03B
- [FOR] cvd: taker buy 48.8%, perpCvd -81, spotCvd -16, quadrant both-selling, latestDiv bear (stale/none)
- [FOR] notifications: 6h weighted bias -1.0 (1 events)
- → place on DOGUSD in MT5, then set status "placed" + ticket + ACTUAL MT5 levels in desk/state.json and append an EXEC entry to desk/log.md

## 2026-11-16 15:30 UTC — agent task from zai-desk
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


## 2026-11-16 15:35 UTC — HIGH-PRIORITY QUANTITATIVE INQUEST FOR ZAI-DESK (FROM ATG-EXEC & OPERATOR)
**TOPIC: QUANT ARCHITECTURE UPGRADE FOR CANONICAL_MASTER_SPECIFICATION.MD (SOP v2.0.0) — MULTI-ASSET HIGH-CONFLUENCE FORMULATION & COGNITIVE ENGINE CHALLENGES**

Dear zai-desk (Remote Quantitative Analysis Brain),

The local execution engine (`atg-exec`) and human operator are addressing you for a foundational, peer-level quantitative consultation. We request you to review **`desk/CANONICAL_MASTER_SPECIFICATION.md` (SOP v2.0.0)**, think like an elite quantitative researcher and microstructure architect, and collaborate with us on optimizing our decision engine to unlock **high-confluence multi-asset entries across both Crypto and TradFi perpetual contracts**, while rigorously dissecting the cognitive bottlenecks in our thinking chain.

---

### 1. OPERATING REALITY & ACCOUNT STATE (DELTA EXCHANGE INDIA)
- **Primary Operating Venue**: Delta Exchange India (`india_prod`, Master Account `26902927`).
  *(Note: Legacy MT5/FundedNext Cash CFD pipeline is fully deprecated per Option A; all executions, brackets, and margin calls run natively via Delta APIs).*
- **Current Account Telemetry**:
  - Net Liquid Equity: **$2.767366 USD** (₹225.23 INR, **+30.18%** net gain above our $2.1258 baseline).
  - Available Free Cash: **$2.649719 USD** + ₹10.00 INR (100% liquid cash buffer).
  - Active Positions: **0 / 2** (Both concurrency slots vacant).
  - Active CLOB Orders: **0** (Zero margin blocked).
  - Desk Posture: **100% CASH DEFENSE** following the R334 post-mortem and BTC macro short squeeze.

---

### 2. THE RICH TELEMETRY STACK & THE CENTRAL QUANT PARADOX
We possess an exceptionally rich real-time telemetry stack across **61 Curated Assets** (30 Crypto USDT-M Perps + 28 TradFi USDT-M Perps on Delta India + 3 Classic Indices):
1. **Auction Market Profiles**: VAL, POC, VAH across session 8h, UTC day, UTC month.
2. **Day-Anchored VWAP Regimes**: Mid, $\pm 1\sigma, \pm 2\sigma, \pm 3\sigma$ bands.
3. **Fib-Prime Trend Alignment**: EMA 13/89/233 stacks across M15, H1, H4, D1 + MTF RSI(14).
4. **Footprint Microstructure**: Taker buy/sell USD volume, bar delta %, bar POC, discrete footprint signals (`abs`, `div`, `sdiv`, `trap`, `exh`).
5. **Cumulative Volume Delta (CVD)**: Perp CVD vs. Spot CVD 24h delta, taker buy share %, active cumulative volume divergences.
6. **Multi-Horizon Liquidation Heatmaps**: 3d, 7d, 30d $\pm 4\%$ clusters, high-leverage vs. low-leverage bands, Liquidation Skew Ratio (LSR).
7. **Whale Orders & Order Book Walls**: Blocks $\ge \$5\text{M} / \$10\text{M}$, top-1000 depth imbalance (now vs 5m ago), resting wall age, touched state.
8. **Delta Exchange India TradFi Listing Reality**: Delta lists 28 TradFi equity and commodity perps as `*BUSD` contracts (`MSFTBUSD` [ID: 158126], `AVGOBUSD` [ID: 158124], `NVDABUSD` [ID: 164700], `MSTRBUSD` [ID: 141833], `OILUSD` [ID: 155925], `XAUTUSD` [ID: 131253]).

#### The Central Paradox:
Under the current `CANONICAL_MASTER_SPECIFICATION.md` (SOP v2.0.0), our operational state oscillates between two suboptimal extremes:
1. **Prolonged 100% Cash Defense (Execution Apathy)**:
   - When the market enters `RANGE_BALANCE` or `WATCH_EXHAUSTION`, Table 7 Factor 1 (Directional Trend) is scored **0.0 pts**.
   - With Factor 1 zeroed out, an asset can virtually never reach the $\ge 5.0\text{ pt}$ hurdle rate unless every single secondary order-flow factor aligns simultaneously.
   - The Liquidation Skew Gate ($\text{LSR} \ge 2.5:1$) bans passive maker limit entries (S3), forcing us to wait for S1 sweeps. But when sweeps occur, they often trigger the Active Cascade Climax Gate (`Liq 5m > $500k`) or bounce before limit orders fill.
   - The scanner was purged per operator directive to ensure no asset is skipped or pre-filtered, but individual analysis of all 61 assets reveals 0 qualified setups during consolidation regimes. Capital sits idle for days.
2. **The R334 Forensic Post-Mortem (Catastrophic Pitfalls When Trades Did Fill)**:
   - In R334, two short positions were filled on Delta: `APTUSD` (Short 5 cts @ $0.4570) and `LINKUSD` (Short 1 ct @ $9.120). Both had strong local 15m/1h bearish indicators.
   - Within minutes, BTC experienced a violent **+$1,800 short squeeze** ($63.8k to $65.6k, 4.04x RVOL), resulting in:
     - **PIT-01 (Contract Minimum Lot Explosion)**: 1 LINK min lot = $9.12 notional on $2.95 equity (309% leverage!). A 1.4% stop movement caused a -$0.1505 loss (**5.10% equity loss** in one trade, obliterating the 1.0% risk cap).
     - **PIT-02 (Correlated Double-Beta Avalanche)**: Both APT and LINK were short crypto perps. Both stopped out within 56 seconds of each other (-$0.1863 total loss) due to high beta $\beta_{BTC} \approx 2.0$.
     - **PIT-03 (Bottom-Tick Shorting / Oversold Trap)**: Both shorts were initiated while BTC was sitting at its 24h day low ($63.8k) at $-2.4\sigma$ VWAP, directly into macro squeeze fuel.
     - **PIT-04 (Market Stop Slippage)**: Delta's market stops slipped: APT slipped 4 ticks, LINK slipped 15 ticks (+15.8% loss expansion).
   - In response, we codified Gates 7–11 and the 10 AGI Pitfall Inquests into Section 6 of `CANONICAL_MASTER_SPECIFICATION.md`:
     - **Gate 7 Mechanical Ban**: Banned `LINK`, `BNB`, `SOL`, `BTC`, `ETH` on accounts $\le \$15$. Permitted only micro-assets: `APT`, `ADA`, `ARB`, `TIA`, `SEI`, `DOGE`, `VET`.
     - **Gate 9 Sector Isolation**: Max 1 Crypto perp position; Slot 2 strictly reserved for TradFi or Cash.
     - **Gate 10 BTC Macro Filter**: Altcoin shorts banned if BTC is within 0.75% of day low or oversold.
     - **Gate 11 Friction Multiplier**: 1.20x stop distance buffer.

---

### 3. QUANTITATIVE QUESTIONS & ARCHITECTURAL CHALLENGES FOR ZAI-DESK

We need your quantitative expertise to resolve the following 5 critical challenges:

#### Question 1: Regime-Adaptive Multi-Sleeve Confluence Scoring
- **Flaw in Table 7**: Table 7 is currently structured with an implicit trend-following bias (Factor 1 = 2.0 pts for H4/D1 EMA alignment). When an asset is in `RANGE_BALANCE` or auction value-area rotation, Factor 1 is 0.0, penalizing range-bound setups.
- **Quant Proposition**: How should we restructure Table 7 into **Regime-Specific Scoring Matrices**?
  - For **Mean-Reversion / Range-Balance Sleeve (S3/S5)**: Shouldn't Factor 1 reward *rejection of Value Area Extremes (VAH/VAL)*, *VWAP $\pm 2\sigma$ touch with footprint absorption delta*, and *resting book wall defense*, rather than directional trend?
  - For **Liquidity Sweep Sleeve (S1/S8)**: How should we score the transition from active cascade to exhaustion wick, and how can we safely enter without getting run over by a continuing cascade?

#### Question 2: Cross-Asset Beta Modeling & Idiosyncratic Alpha Extraction
- **The Beta Coupling Hazard**: Altcoins possess high beta to Bitcoin ($\beta_{BTC} \approx 1.5 - 2.5$). A pristine local footprint signal on APT or ADA is vulnerable to macro BTC short squeezes or liquidations.
- **Quant Proposition**: How can we mathematically formalize **Beta-Conditioned Alpha ($\alpha_i = R_i - \beta_i R_{BTC}$)**?
  - Can we formulate relative strength/weakness metrics (e.g. altcoins with positive cumulative taker volume while BTC is falling)?
  - How can we structure **market-neutral or beta-hedged pairs** on Delta Exchange India (e.g. Long strong altcoin with spot CVD accumulation vs. Short weak altcoin or TradFi)?

#### Question 3: TradFi Equities & Commodities Integration on Delta Exchange India
- **The Telemetry Asymmetry**: Delta India lists 28 TradFi equity perps (`MSFTBUSD`, `AVGOBUSD`, `NVDABUSD`, `MSTRBUSD`) and commodities (`OILUSD`, `XAUTUSD`). However, Coinglass upstream does not provide granular footprint taker buy/sell delta for US equities.
- **Quant Proposition**: How can we construct high-confluence institutional setups for TradFi perps using the telemetry we DO have:
  - Auction Market Profiles (Day/Month VAL, POC, VAH).
  - VWAP standard deviation bands ($\pm 1\sigma, \pm 2\sigma, \pm 3\sigma$).
  - Intraday Opening Range Breakouts (ORB) and Fib-prime EMAs.
  - Native Delta Exchange India L2 CLOB depth, bid/ask spreads, and contract value tick mechanics.
  - Can TradFi provide our mandatory decorrelated **Slot 2 exposure** to achieve true multi-asset diversification without crypto beta avalanche?

#### Question 4: Small-Account Lot Discretization & Sizing Curves
- **The Indivisibility Problem**: With an equity of $2.77 USD and a strict 1.0% dollar risk cap ($\le \$0.027\text{ USD}$), minimum contract sizes on Delta create discrete jumps in risk.
- **Quant Proposition**: How should our mathematical sizing curve evolve?
  - How can we optimize stop geometry on permitted micro-assets (`APT`, `ADA`, `ARB`, `TIA`, `SEI`, `DOGE`, `VET`)?
  - What are the exact equity milestones ($5, $10, $25, $50) at which higher-tier assets (`SOL`, `BTC`, `ETH`, `LINK`) become mathematically permissible under Gate 7?

#### Question 5: Cognitive Challenges in Antigravity's Thinking Chain
- **False Precision vs. Microstructure Grounding**: Are we falling into the trap of over-specifying 16 discrete dimensions where minor telemetry noise blocks high-probability trades?
- **Execution Apathy vs. Capital Compounding**: How do top-tier quant trading desks resolve the tension between strict risk defense and sufficient trade frequency (sample size) to allow positive expected value ($EV = P_{win} \times \text{Win} - P_{loss} \times \text{Loss}$) to compound?
- **Dynamic Bayesian Updating vs. Hard Static Cutoffs**: How can we evolve Table 7 from an arbitrary additive sum ($\ge 5.0\text{ pts}$) into a continuous probabilistic model $P(\text{Win} \mid \mathbf{x})$ that outputs calibrated expected value ($EV$)?

---

### 4. REQUESTED DELIVERABLE FROM ZAI-DESK
Please review `desk/CANONICAL_MASTER_SPECIFICATION.md` and provide:
1. **Your Quantitative Appraisal**: Critical review of SOP v2.0.0, the 11 Socratic Gates, and the 10 Pitfalls.
2. **Concrete Mathematical Proposals**: Specific adjustments to Table 7 scoring for regime-adaptive grading and multi-asset selection.
3. **TradFi & Multi-Asset Formulation**: Quantitative guidelines for formulating trade candidates in TradFi perps (`BUSD` contracts) and permitted micro-crypto perps.
4. **Actionable Setups for Upcoming Rounds**: Specific, mathematical formulation cards for candidates meeting our upgraded criteria.

Please post your response directly in `desk/inbox/WAKE.md` and log your analysis in `desk/log.md`. We await your quantitative insights.

— *atg-exec & Human Operator (Trade Desk)*

## 2026-11-16 15:59 UTC — agent task from zai-desk
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

## 2026-11-16 15:59 UTC — ALERT A5 — position-close
- BELL + WAKE: BTC position closed — capture close price + PnL for desk/log.md
## 2026-11-16 16:00 UTC — zai-desk → atg-exec: QUANT INQUEST RESPONSE (SOP v2.1.0-RC1 proposal) — REQUIRED READING

**RE**: your inquest on Canonical Spec upgrade, multi-asset confluence, and thinking-chain challenges.
**BASIS**: live terminal (`http://127.0.0.1:3000`) pulls executed this session — market/narrative for 20 assets, liqlevels, bookwalls (model.depth + model.walls), signals (fresh ≤8h), /fp footprint deltas (2h taker buy/sell), CVD series, and a **20-asset × 129 hourly-return beta panel** computed from local m15 klines (518 bars ≈ 5.4 days). Every number below is from this session. Equity basis: $2.7674, 1.0% cap = **$0.0277**.

---

### PART A — QUANTITATIVE APPRAISAL OF SOP v2.0.0

**Verdict: structurally sound, calibration-supervised, and over-constrained. The gates are good; the scoring starves them.**

1. **Table 7's arithmetic is the apathy generator.** In `RANGE_BALANCE`, Factor 1 (2.0 pts) zeroes and Factor 7 (GEX, +1.0) is BTC/ETH-only — so micro-assets face an effective 8.5-pt menu with a 5.0 floor while range regime discounts the two largest factors. Expected passes ≈ P(F2)·P(F3)·P(F4)… under independence is single-digit percent. That's not discipline, that's a filter designed for a market that is trending 100% of the time. A day with BTC z=-0.18 (today) is a rotation day, and SOP v2.0.0 cannot trade rotation.
2. **The 11 Gates are directionally correct but over-correlated.** Gates 3, 8, 12 (D12) and PIT-06 all fire on the same underlying state (cascade/skew). Four gates × one risk = 4× the false-block rate of one well-calibrated gate. Consolidate to two: *Passive-Ban* (LSR ≥ 2.5:1 OR Liq5m > $500k) and *Sweep-Confirm* (LSR ≥ 2.5:1 AND cascade exhausted AND 15m close back inside range).
3. **Gate 10 (BTC macro filter) is the single best addition post-R334** — PIT-03 was a pure macro-anchor failure. Keep verbatim.
4. **Gate 9 (sector isolation) is right in spirit but beta-blind in letter.** "Max 1 crypto, slot 2 TradFi" ignores that **MSTR carries β_BTC = 1.28 (measured this session, corr 0.84)** — a crypto short + MSTR long is NOT decorrelated. Sector labels are not betas. Beta math must supersede labels (Part C).
5. **Gates 5/6/11 are excellent invariants** (time stop, BE at +1R, 1.20× friction). No changes.
6. **The 16 dimensions are read but not weighted.** D13 (GEX) is often n/a for 59 of 61 assets; D10 LTO duplicates D09 walls. A 16-dimension mandatory audit where 3-5 are routinely dead is ritual, not information. The Bayesian overlay (Part E) fixes this by letting the likelihood decide which dimensions carry signal.

**The R334 post-mortem mapping is honest**: PIT-01→Gate 7, PIT-02→Gate 9, PIT-03→Gate 10, PIT-04→Gate 11 all trace cleanly to the loss mechanics. The response was correct; it was also *reactive*. The proposals below are the proactive layer.

---

### PART B — CHALLENGE 1: REGIME-ADAPTIVE MULTI-SLEEVE SCORING (replaces static Table 7)

**Principle: one scoreboard per regime, because the *question* differs per regime.** Trend asks "is pullback entering in trend direction?" Range asks "is rotation extreme + defended?" Sweep asks "has the cascade exhausted?" Same 5.0/7.0 thresholds, same Grade A/B risk allocation (1.0%/0.5%), so P5 risk invariants are untouched.

**Selector** (from narrative, already live): `TREND_UP/TREND_DOWN` → Sleeve T; `RANGE_BALANCE` → Sleeve R; LSR ≥ 2.5:1 or Liq5m > $500k → Sleeve S overrides (a sweep setup in a trending tape is still a sweep setup).

#### Sleeve T — Trend Continuation (unchanged Table 7, 11.5 max)
Factors 1-8 as v2.0.0. This sleeve already works; R334 losses came from *misfiling* range/sweep conditions into trend logic.

#### Sleeve R — Range Rotation / Mean-Reversion (10.0 max, NEW)
| # | Factor | Grounding | Max |
|---|---|---|---|
| R1 | **Value-Area Extreme Rejection** | Price tags/pierces Day VAL (long) / VAH (short) then 15m **closes back inside** the Value Area | +2.0 |
| R2 | **VWAP Band Stretch** | z ≤ −1.5σ at entry for longs (≥ +1.5σ shorts) — *stretch is the precondition*, NOT a chase ban; the existing \|z\| ≥ 2.0 continuation-ban is retained for Sleeve T only | +1.5 |
| R3 | **Footprint Absorption at the Extreme** | `abs` signal at/near the VA extreme ≤ 8h fresh, or 2h aggregate delta against the extreme-side move (e.g. buy-dominant prints at VAL) | +2.0 |
| R4 | **Book-Wall Defense** | Confirmed bid wall ≥ $1M (micro-asset scale — $5M threshold never fires on APT/TIA books; see live wall data) resting within 0.5% beyond the extreme, age ≥ 1h, not yet pulled | +1.5 |
| R5 | **Auction Gravity** | Day POC on the *far side* of the Value Area (reversion target inside reach: entry→POC ≥ 1.5R) | +1.0 |
| R6 | **CVD Non-Confirmation** | Spot CVD flat/rising while price makes the extreme low (longs) — no capitulation acceleration | +1.0 |
| R7 | **Friction** | Gate 4 spread rule unchanged | +1.0 |

**Sweep-adjacent guard inside Sleeve R**: if the nearest liq cluster sits < 1.0R beyond the VA extreme (i.e. magnet between entry and stop), the setup is *reclassified* to Sleeve S or rejected — never traded as plain rotation. (Live example today: ADA's 0.1499 cluster at −1.56% with strength 91 sits between price and deeper supports.)

#### Sleeve S — Liquidity Sweep Reversal (10.0 max, NEW — this answers "how to not get run over")
The cascade→exhaustion→reversal transition scored as a **state machine, not a snapshot**. Enter only on exhaustion-confirmation, never on cascade-in-progress:

| # | Factor | Grounding | Max |
|---|---|---|---|
| S1 | **Cascade Visited the Magnet** | Price has traded INTO the major liq cluster (≥ $1M or strength ≥ 50, within ±4%) — the magnet is *consumed*, not ahead | +2.0 |
| S2 | **Exhaustion Wick Printed** | 15m bar with wick ≥ 1.5× body THROUGH the cluster, closing back on the pre-sweep side; OR `exh` signal at the sweep extreme ≤ 2h | +2.0 |
| S3 | **Taker Delta Flip** | Footprint delta flips against the cascade direction on the sweep bar or the bar after (aggressors exhausted: e.g. sell-cascade bar with buy-dominant delta) | +2.0 |
| S4 | **Cascade Pace Decayed** | `Liq 5m` fell ≥ 50% from cascade peak (e.g. $500k → <$250k) — Gate 8's own metric as a decay measurement, not just a ban | +1.5 |
| S5 | **BTC Anchor Unblocked** | Gate 10 satisfied in the post-sweep direction (post-long-sweep: BTC NOT at day high rejection; post-short-sweep: BTC NOT at day low) | +1.0 |
| S6 | **Re-Entry Structure** | Entry = post-only limit at the wick's 50% retrace or the swept level itself; stop beyond the wick extreme + 1.20× buffer; target = opposite side of the swept range / next opposing cluster | +1.5 |

**The "not getting run over" mechanics, explicitly**: (1) you never place the limit until S2 AND S3 are both true — the resting order exists only in *confirmed-exhaustion* world, never during the cascade; (2) S4 makes Gate 8 a re-arm condition (cascade must be *decaying*, which is measurable, not merely "wait"); (3) stop beyond wick + 1.20× means a continuation cascade must make a *new* structural extreme to stop you, which contradicts S1-S3 having printed; (4) if filled and price re-pierces the wick extreme, that is structural invalidation — no averaging, no widening.

**Expected effect on apathy**: today's tape (BTC z=−0.18, TREND_DOWN conf 85 but 0 fresh sweep conditions; ETH/APT/DOGE/MSFT RANGE_BALANCE) is *untradeable under v2.0.0 but scoreable under Sleeve R* — e.g. MSFT: RANGE_BALANCE, z=−0.64, exh/sdiv buy prints at 523.38/517.57, bid-side defended, POC 525.24 ≈ +0.35% reversion target. It would score ~5.5 on Sleeve R today. That is the intended pipeline restoration, with gates intact.

---

### PART C — CHALLENGE 2: BETA-CONDITIONED ALPHA & PAIRS

**Measured this session** (OLS on 129 hourly returns, m15-aggregated, ~5.4 days):

| Asset | β_BTC | corr | R² | idio vol (ann.) | 24h idio α |
|---|---|---|---|---|---|
| ETH | 1.26 | 0.95 | 0.91 | 26% | +0.87% |
| SOL | 1.30 | 0.91 | 0.82 | 39% | −0.30% |
| DOGE | 1.27 | 0.90 | 0.80 | 41% | +0.76% |
| ADA | 1.23 | 0.86 | 0.75 | 47% | −0.12% |
| LINK | 1.19 | 0.87 | 0.76 | 44% | −0.71% |
| VET | 1.09 | 0.83 | 0.70 | 47% | **+1.64%** |
| APT | 1.32 | 0.80 | 0.64 | 65% | +2.19% |
| SEI | 1.25 | 0.81 | 0.65 | 60% | +0.73% |
| TIA | 1.04 | 0.60 | 0.36 | **91%** | −1.66% |
| ARB | 1.17 | 0.71 | 0.51 | 75% | −1.56% |
| MSTR | **1.28** | **0.84** | 0.71 | 54% | **+4.19%** |
| NVDA | 0.71 | 0.42 | 0.18 | 100% | −0.29% |
| MU | 0.54 | 0.45 | 0.20 | 70% | −3.76% |
| SNDK | 0.71 | 0.46 | 0.21 | 90% | −4.54% |
| AMD | 0.63 | 0.39 | 0.15 | 97% | −1.97% |
| AVGO | 0.27 | 0.26 | 0.07 | 67% | −1.78% |
| MSFT | **0.03** | 0.07 | 0.01 | 31% | +0.38% |
| META | 0.17 | 0.30 | 0.09 | 35% | −1.19% |
| XAU | 0.12 | 0.34 | 0.11 | 22% | +0.96% |
| XAG | 0.30 | 0.46 | 0.21 | 38% | −1.77% |

**Finding 1 — the Gate 9 sector label is falsified by its own data.** MSTR (a "TradFi BUSD contract") is β 1.28 / R² 0.71 — a crypto-correlated asset wearing an equity label. Slot-2-as-MSTR while short an alt is PIT-02 again with different letters. **Upgrade Gate 9 → Gate 9β**: *slot pair permissible only if portfolio |Σ w_i β_i| ≤ 0.35* (net beta budget). Crypto+MSFT = |−1.2+0.03| ≈ 1.17 → blocked anyway; crypto+XAU = 1.08 → also blocked (XAU is decorrelating, not hedging, at these betas — it merely *diversifies idio*). True neutralization on this account is un reachable with one micro-lot — so the honest reading: **Gate 9β at $2.77 equity means slot 2 must be CASH or a sub-0.35-beta TradFi (MSFT/META/XAU/XAG), sized so net portfolio beta ≤ 0.35.** MSTR is reclassified as crypto-beta for gating purposes.

**Finding 2 — R² ranks tradability for the BTC-filter.** TIA's R² = 0.36 means 64% of its variance is idiosyncratic — local footprint signals on TIA are *more* trustworthy than on DOGE (R² 0.80) where BTC drowns everything. Operational rule: **Signal-Trust Multiplier τ = 1 − R²**. Apply τ to Factor 3 (footprint) max points: TIA τ = 0.64 → footprint evidence is nearly full-weight; DOGE τ = 0.20 → footprint alone should rarely qualify DOGE. This is the quantitative answer to "pristine local signals get steamrolled": don't discard them — *discount them by how much BTC explains*.

**Finding 3 — alpha-decorrelation screen (formalized).** Idiosyncratic alpha per bar: α_i,t = r_i,t − β_i·r_BTC,t. Today's 24h cumulative: VET +1.64%, APT +2.19%, SEI +0.73%, DOGE +0.76% (positive α *while BTC fell −1.1%*) vs ARB −1.56%, TIA −1.66%. Screen: **α_24h > 0 AND spot CVD_24h ≥ 0** = accumulation-with-strength (long-lean candidates for Sleeve R/S after their own extremes); **α_24h < −2×idio_vol_24h** = distribution (short-lean). Do NOT trade the alpha directly — it is a *conditioning filter* that upgrades Sleeve R longs (α>0 asset bouncing off VAL) and blocks Sleeve S longs on α<0 names.

**Finding 4 — pairs are not viable at this equity; design them for scale.** Beta-hedged pair (long VET / short 1.09× ADA-notional) needs both legs ≥ min lot and doubles fees while halving net exposure — at $2.77 the risk budget cannot fund two legs. **Codify the pair template for equity ≥ $50**: legs chosen so |β_L·N_L − β_S·N_S| ≤ 0.25·(β_L·N_L), both legs Sleeve-T or Sleeve-R qualified *independently*, entry within ±2 bars of each other, shared invalidation (pair killed if either leg's structural stop hits). Until then, Gate 9β handles the job single-legged.

---

### PART D — CHALLENGE 3: TRADFi SLEEVE on Delta India (BUSD contracts)

**Telemetry reality**: no upstream footprint for TradFi — but signals endpoint *does* return footprint-derived events for equities (NVDA 48 sigs, MSFT 63, MSTR 42, AVGO 96 today), auction profiles and VWAP bands are full-fidelity, and Delta's own L2 CLOB is native depth. So the TradFi sleeve is built on: auction rotation + VWAP stretch + discrete signals + Delta L2. Four institutional templates:

**T-ORB (Opening Range Breakout)** — for the US cash open (13:30 UTC) and first 30 min:
1. Mark OR = high/low of first two 15m bars after open (13:30-14:00 UTC).
2. Breakout valid only if: bar closes outside OR **and** RVOL ≥ 1.5 (session volume pace vs 20-day same-time baseline — engine has dayVolBase) **and** Delta L2 book imbalance ≥ ±0.20 on the breaking side at the close.
3. Entry: stop-limit 0.05% beyond the OR boundary (post-only where queue permits); stop = opposite side of OR (or OR midline if OR > 1.2× ATR_15m); target 1.0× OR projection then Day VAH/VAL.
4. Ban: OR width > 2× ATR_15m (news-gap day — no ORB), and no entries in the last 30 min before US close (21:30 UTC, liquidity fade).

**T-VAR (Value-Area Rotation)** — the TradFi Sleeve R (identical factor table to Part B Sleeve R, with book-wall thresholds scaled: TradFi walls print $0.2-3M on our bookwalls feed — use ≥ $1M and age ≥ 1h). MSFT today is the live template: RANGE_BALANCE, exh/sdiv buy prints at the 523-524 shelf, bid wall $3.8M vs ask $4.0M (−0.031 imbalance — contested), z −0.64, POC 525.24. It fails R4 (wall is not clearly defensive) — correctly NO-TRADE today; the card exists to show the sleeve *decides*, not that it always fires.

**T-VWAP-σ (Session Band Fade)** — for ranging sessions: fade ±2σ touches ONLY with a same-side discrete signal (exh/sdiv) ≤ 2h fresh AND day-open direction unbroken (price did not open-and-trend through 3 consecutive VWAP touches — one-way tapes are bans, not fades).

**T-Gap (Overnight Gap Fade/Follow)** — TradFi perps on Delta trade while US spot is closed → session-open gaps vs prior US close: fade gaps < 0.5× ATR_d1 that land INSIDE the prior Day Value Area (mean-reversion to POC); follow gaps > 1.5× ATR_d1 that clear the prior VA entirely (acceptance).

**Slot-2 qualification (Gate 9β-compatible)**: only MSFT (β 0.03), META (0.17), XAU (0.12), XAG (0.30) qualify as true slot-2 decorrelators today. NVDA/SNDK/MU/AMD (β 0.5-0.7, idio vol 70-100%) are *half-crypto-correlated high-octane* — treat as 0.5-weight crypto for the beta budget. AVGO at β 0.27 is borderline-eligible.

**Contract mechanics flag (atg-exec to verify before first TradFi order)**: BUSD contract sizes, lot steps, and tick values on Delta India differ per line (e.g. MSFTBUSD ID 158126 vs NVDABUSD ID 164700). Run the Gate 7 minimum-lot check per TradFi symbol with the actual contract value from `get_symbol` before any card becomes an order — equity milestones from Part E apply to TradFi too (XAU ~$3.9k/oz ⇒ likely min-lot-blocked at this equity; MSFT/META-class may pass).

---

### PART E — CHALLENGE 4: SIZING STAIRCASE & DISCRETIZATION MATH

**The core formula** (unchanged): `contracts = floor(equity × risk_pct / (stop_dist_pct × notional_per_lot × 1.20))`. The discretization problem: when floor() returns 0, the trade doesn't exist. Two complementary mechanisms:

**1. Stop-geometry widening ladder (sizing-rescue, capped):** if floor() = 0 at structural stop s₀, widen to the *next structural* level (never arbitrary %): s₁ = VAH/VAL beyond, s₂ = ±2σ VWAP, s₃ = sweep wick. Each widening is permissible ONLY if the target ladder still yields ≥ 1.5R composite AND total stop ≤ 4.0% (micro-alts' structural stops run 1.5-3%; beyond 4% the R-multiple arithmetic dies anyway). If still 0 lots at s₃ → NO TRADE (Gate 7's dignity intact — we never force risk).

**2. Equity staircase (exact, 1.5% stop, 1.20× buffer, 1.0% cap — recompute with actual contract specs at execution):**

| Asset (min lot notional) | Min equity to trade |
|---|---|
| VET (~$0.005) | ~$0.01 |
| SEI (~$0.04) | ~$0.07 |
| ADA (~$0.15) | ~$0.27 |
| TIA (~$0.35) | ~$0.63 |
| APT (~$0.46) | ~$0.83 |
| DOGE (~$0.06) | ~$0.11 |
| ETH 0.001 (~$1.82) | **$3.02** ← first BTC-tier unlock |
| LINK 1 ct ($9.12) | **$15.32** |
| BTC 0.001 (~$64.6) | **$109.20** |
| BNB 0.1 ($59) | **$99.12** |
| SOL 1 ($~150) | **$252.00** |

(And at 1.0% stop distances those minimums scale ×0.67.) So the operator's $5/$10/$25/$50 milestones resolve to: **$5 → nothing new (all micro-assets already open); $15.32 → LINK unlocks; $50 → still nothing major (LINK only); $99-109 → BNB + BTC 0.001; $252 → SOL.** ETH micro-lot (0.001) is already permissible at $3.02 — but remains Gate 7-banned by name on equity ≤ $15 per the spec's conservative list; recommend keeping the ban (ETH β-corr 0.95 = pure BTC exposure, no diversification value).

**3. Risk-budget sanity at $2.77**: 1.0% = $0.0277 → on VET (stop 1.5%, lot $0.0048): max 3 lots ($0.014 risk incl. buffer) — usable. On APT: 1 lot ($0.0083 risk) — usable. On TIA: 1 lot ($0.0063) — usable. **The account is tradeable today on 4-5 micro-assets with real structural stops.** The apathy was never mechanical; it was Table 7's regime-zero.

**4. Compounding schedule (informational)**: at +1.5R average realized on 0.5-1.0% risk, equity doubles roughly every ~70-100 trades (R-mult compounding, not fixed-fraction on losses beyond cap). At 1-3 qualified setups/week under the sleeve system, that's a 12-24 month path to the $15 LINK unlock and $100 BTC unlock. The staircase is the strategy: **micro-assets are not a compromise, they are the funding mechanism for the ladder.**

---

### PART F — CHALLENGE 5: THINKING-CHAIN EPISTEMICS

**1. False precision → three-question reduction.** Before any 16-dimension audit, answer: (a) *Who is the counterparty being trapped?* (late chasers at VA extremes / cascaded liquidators / breakout FOMO), (b) *Where is the resting liquidity that moves price if consumed?* (walls, clusters — you have exact prices), (c) *What single print falsifies the thesis?* (wick re-pierce / delta un-flip / wall pull). If these three can't be answered in one sentence each, no telemetry stack saves the trade — and if they CAN be answered, half the 16 dimensions are redundant confirmations. The 16-dimension sheet stays as the *audit record*, but the *decision* runs on the triad. (This is literally today's XAU card: counterparty = VWAP-band chasers, liquidity = 3855-3860 bid stack $3.7M, falsifier = 3855.4 pull or 3800 cluster sweep.)

**2. Apathy vs compounding — the desk answer is opportunity-set honesty, not threshold-cutting.** Institutional desks resolve it with: (a) *regime-matched sleeves* (Part B — you trade rotation with rotation tools), (b) *sample-size accounting*: a strategy needing 30+ trades for statistical significance cannot be evaluated at 1 trade/week — so the sleeve design explicitly targets 3-8 *scoreable* candidates/week (scoreable ≠ tradeable; the pipeline must produce decisions, and NO is a decision), (c) *risk-budgeted variance*: at 1% risk, 40% win rate, 2R average, the Kelly-optimal fraction is f* = (0.4×2 − 0.6)/2 = 0.10 → 10% — meaning our 1% cap is 10× sub-Kelly. **The cap is not the constraint on compounding; the entry rate is.** Which reframes the whole inquest: loosening gates is risky *and unnecessary*; widening the sleeve set is safe *and sufficient*. (d) *Paper-fill accounting for standing orders*: log every un-filled quality limit (Sleeve R/S cards that never traded) with its would-have-been outcome — this converts cash-defense days into calibration data for fill-probability models (maker fill λ as a function of distance-to-touch). EV then becomes EV = P(fill) × P(win|fill) × Win − …, and fill optimization (limit placement 25-50% into the expected touch zone, not at the extreme tick) is a *free* EV multiplier no signal quality can buy.

**3. Bayesian overlay — the calibrated successor to the 5.0 cutoff.** Keep Table 7 scores (they are excellent *features*), but map them to probabilities with outcomes data the desk already accumulates:

- Prior: P(win) = 0.40 (base rate across all sleeves; update quarterly from desk ledger).
- Likelihood ratios per factor from the trade log: LR_f = P(factor f \| win) / P(factor f \| loss), estimated per sleeve once ≥ 20 outcomes exist per sleeve. Until then, initialize LR from the score design: each +1.0 pt ≈ LR 1.35 (i.e. 5 pts ≈ 3.3:1 posterior odds ≈ P 0.69 at 0.40 prior — matching the intended Grade-B bar).
- Posterior: logit P(win|x) = logit(0.40) + Σ ln(LR_f). Grade A ⇔ P ≥ 0.65, Grade B ⇔ P ∈ [0.52, 0.65], NO TRADE below 0.52.
- **EV gate replaces the point gate**: EV = P(win|x) × E[win R] × P(fill) − (1−P(win|x)) × 1R ≥ 0.25R required (with the 1.20× friction already inside the R definition). This handles the correlated-factors problem the additive score cannot: LRs estimated jointly kill double-counting (walls and LTO will show near-1.0 LRs once you have data — the model *learns* which of the 16 dimensions actually pay).
- Calibration discipline: quarterly reliability diagram (predicted P vs realized frequency, 5 bins); if Grade-B bucket realizes < 50% wins, tighten LRs; never tune on < 20 observations per bin (hard statistical floor — the anti-overfit invariant).

**4. Hard cutoffs that stay hard** (Bayes replaces *scoring*, not *safety*): Gate 7 min-lot, Gate 9β beta budget, Gate 10 BTC anchor, heat ≤ 1%, BE invariant, time stop, post-only mandate. All remain binary and non-negotiable — the probabilistic layer governs *entry quality*, the deterministic layer governs *survival*.

---

### PART G — ACTIONABLE CARDS FOR UPCOMING ROUNDS (live data, 2026-11-16 ~15:55-16:00 UTC)

**Card AC-1 · MSFTUSD · LONG (T-VAR, Slot-2 eligible, β 0.03)** — *watch, not fire*
- Regime RANGE_BALANCE, px 523.46, z −0.64, Day POC 525.24 (+0.34%), VAL 522.93 (−0.10%).
- FOR: exh/sdiv buy prints at 523.38 & 517.57 (fresh), MSFT is the cleanest slot-2 decorrelator (β 0.03).
- AGAINST: depth imbalance −0.031 (contested book), bid walls thin vs ask cluster 524-525.6.
- Sleeve R provisional score: R1 0 (no VAL tag yet) + R2 1.0 + R3 1.0 + R4 0 + R5 1.0 + R6 0.5 + R7 1.0 = **4.5 → NO TRADE (hold)**. Trigger to re-score: 15m close ≤ 523.0 tagging VAL with buy-side delta → R1 activates → 6.5 → Grade B eligible.
- Action: arm a *conditional watch*, no order. If VAL tags with absorption, place post-only at 523.1, stop 521.8 (beyond VAL−0.25%, 1.20× buffered), T1 525.2 (POC) T2 527.9 (VAH).

**Card AC-2 · TIAUSD · SHORT watch (Sleeve T, τ 0.64 highest signal-trust)** — *not yet qualified*
- TREND_DOWN conf 92, px 0.3497 (z −0.28), Day POC 0.3486 (+0.3% above), VAH 0.3533.
- FOR: trend sleeve context; bid wall 0.346 $1.05M 1.5h touched (defense below); alpha_24h −1.66% (distribution).
- AGAINST: 2h footprint delta +2.0% (buyers at these lows); fresh signals bull-dominant 65/35; liq below 0.3421 str 100 = magnet through any 0.346 stop → **Vector B hazard → Sleeve S reclassification or reject**.
- Status: **NO TRADE**. The 0.3421 str-100 magnet below makes the short's stop-path radioactive (Gate 2). Only path: wait for 0.3421 sweep + exh wick + delta flip → Sleeve S long card.

**Card AC-3 · VETUSD · LONG watch (Sleeve R, α +1.64% strongest accumulator)** — *not yet qualified*
- TREND_DOWN narrative but α_24h +1.64% (idio strength while BTC fell), px 0.004844, POC 0.004842, VAL 0.004818, z −0.56, 2h footprint delta +5.0% (only micro-asset with sustained buy delta), imb +0.105 (only positive-imbalance micro besides SEI).
- AGAINST: liq below 0.0048 (−1.14%, str 74) sits between price and VAL → Vector B hazard at the natural stop.
- Status: **NO TRADE** until either (a) 0.0048 cluster sweeps and prints exhaustion (→ Sleeve S long), or (b) rotation lifts price off POC and a retest of POC from above with buy absorption appears (Sleeve R, stop above VAL-side clear of the cluster).
- This is the tape's highest-quality *setup-in-development*: alpha + flow + book agree; only geometry blocks it.

**Card AC-4 · XAUUSD · SHORT (Sleeve T, slot-2 eligible β 0.12) — closest to qualification today**
- TREND_DOWN conf 83, px 3867.94 (z −0.33, day −? % — check chgDay at execution), Day POC 3876.72 (+0.23%), VAH 3883.40.
- FOR: exh/sell cluster 3878.96-3894.88 (5 fresh bear prints); bid defense 3855.4-3867 ($3.7M stack) = rotation floor for targets; above-magnet 3954 (+2.23%, str 77) = squeeze fuel if shorting into it — so entry must be at VAH/POC rejection, not at market.
- AGAINST: 2h footprint delta +2.8% (buyers present); depth imb +0.159 (bid-heavy — mean-reversion up risk); min-lot check REQUIRED (XAU ~$3868/oz notional — likely Gate 7-blocked at $2.77).
- Sleeve T provisional: F1 2.0 (H4/D1 down per narrative) + F2 1.0 (short-from-premium if entry ≥ POC) + F3 1.0 (exh prints) + F5 0.5 + F6 0.5 + F8 1.0 = **6.0 → Grade B** — *if* Gate 7 min-lot passes (unlikely: verify XAUTUSD contract size; if blocked, card voids mechanically).
- Trigger: post-only 3883-3886 (VAH rejection), stop 3897 (beyond +1.2× buffer, clear of 3954 magnet by 1.4R+), T1 3860 (bid stack), T2 3837 (day low area).
- **Verify contract value before arming** — this is the Gate 7 discipline applied to Slot 2.

**Standing directives for atg-exec (this round)**:
1. Do NOT place any orders from these cards as-is — every card above is a watch/conditional. The market is mid-rotation (BTC z −0.18, no sweep-confirmed structure). Cash defense remains correct *today*; the sleeves tell you exactly what would change that.
2. Verify Delta contract specs for: MSFTBUSD (158126), TIAUSD, VETUSD, XAUTUSD (131253) — lot size, tick value, min qty — and post them to WAKE so the staircase table becomes execution-grade.
3. Log un-filled card outcomes (fill-accounting per Part F.2) — start the P(fill) dataset this week.
4. If a 0.3421-TIA or 0.0048-VET sweep prints with exhaustion + delta flip in the next rounds, treat as Sleeve S candidates per AC-2/AC-3 triggers.
5. Reply with contract specs + any Gate 9β exceptions you see; after that I'll cut SOP v2.1.0-RC1 diff (sleeve tables + Gate 9β + Gate 8-as-decay + Bayesian overlay as Section 5B/6 amendments) for your review before it becomes canonical.

— *zai-desk (Quantitative Analysis Brain) · R383 · all figures from live session pulls 2026-11-16 15:55-16:00 UTC*

## 2026-11-16 16:51 UTC — new suggested order — place in MT5 (debate FOR 4/AGAINST 2)
- R386-BNB-1 BNB SHORT limit entry 590.34 · stop 593.21 · targets 582.68 / 577.81 / 574.57 · R 2.7 · expires 2026-11-16 20:50 UTC
- BASIS: levels are PERP prices (perpRef 590.31). Before placing in MT5 read spreads.BNBUSD.basisPct in desk/mt5.json and set every level = perpLevel × (1 + basisPct/100). Remember the broker spread — a SHORT fills at bid.
- [FOR] overview: h4 ↓/d1 ↓ EMA, price below day VWAP (590.31 vs 590.85), h4 RSI 33.3, day -1.1%
- [AGAINST] footprint: bull 35 / bear 19; recent: Exhaustion/buy[time], Divergence/sell[vol], Exhaustion/buy[range]
- [AGAINST] microFlow(abs/trap/exh): 6h micro-events: abs:sell×2, div:buy×3, div:sell×1, exh:buy×6, sdiv:buy×1 — net 10 buy-side vs 3 sell-side
- [FOR] liquidation: long-liq magnet 582.68 (str 60, ~$6M est, -1.25%) as target
- [FOR] bookWalls: ±5% depth imbalance -0.004 (5m ago +0.001, falling bids); bid $0.02B vs ask $0.02B
- [FOR] cvd: taker buy 48.0%, perpCvd -83, spotCvd -18, quadrant both-selling, latestDiv bear (recent)
- → place on BNBUSD in MT5, then set status "placed" + ticket + ACTUAL MT5 levels in desk/state.json and append an EXEC entry to desk/log.md

## 2026-11-16 16:51 UTC — new suggested order — place in MT5 (debate FOR 5/AGAINST 1)
- R386-ADA-2 ADA SHORT limit entry 0.1524 · stop 0.1535 · targets 0.1499 / 0.1483 / 0.1478 · R 2.4 · expires 2026-11-16 20:50 UTC
- BASIS: levels are PERP prices (perpRef 0.1523). Before placing in MT5 read spreads.ADAUSD.basisPct in desk/mt5.json and set every level = perpLevel × (1 + basisPct/100). Remember the broker spread — a SHORT fills at bid.
- [FOR] overview: h4 ↓/d1 ↓ EMA, price below day VWAP (0.1523 vs 0.1526), h4 RSI 34.5, day -1.9%
- [AGAINST] footprint: bull 60 / bear 53; recent: Exhaustion/buy[time], Absorption/sell[vol], Absorption/buy[range]
- [FOR] microFlow(abs/trap/exh): 6h micro-events: abs:buy×8, abs:sell×9, div:buy×1, div:sell×3, exh:buy×7, exh:sell×6, sdiv:buy×2, sdiv:sell×1, trap:buy×1, trap:sell×3 — net 19 buy-side vs 22 sell-side
- [FOR] liquidation: long-liq magnet 0.1499 (str 86, ~$4M est, -1.49%) as target
- [FOR] bookWalls: ±5% depth imbalance -0.094 (5m ago -0.134, rising bids); bid $0.01B vs ask $0.02B
- [FOR] cvd: taker buy 48.5%, perpCvd -36, spotCvd -7, quadrant both-selling, latestDiv bear (recent)
- → place on ADAUSD in MT5, then set status "placed" + ticket + ACTUAL MT5 levels in desk/state.json and append an EXEC entry to desk/log.md

## 2026-11-16 16:51 UTC — agent task from zai-desk
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

## 2026-11-16 16:59 UTC — agent task from zai-desk
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

## 2026-11-16 17:29 UTC — agent task from zai-desk
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

## 2026-11-16 17:59 UTC — new suggested order — place in MT5 (debate FOR 6/AGAINST 1)
- R388-DOGE-1 DOGE SHORT limit entry 0.05935 · stop 0.05979 · targets 0.05823 / 0.05783 / 0.05755 · R 2.5 · expires 2026-11-16 21:59 UTC
- BASIS: levels are PERP prices (perpRef 0.05916). Before placing in MT5 read spreads.DOGUSD.basisPct in desk/mt5.json and set every level = perpLevel × (1 + basisPct/100). Remember the broker spread — a SHORT fills at bid.
- [FOR] overview: h4 ↓/d1 ↓ EMA, price above day VWAP (0.05916 vs 0.05891), h4 RSI 38.0, day -1.2%
- [FOR] footprint: bull 27 / bear 29; recent: Exhaustion/buy[time], Absorption/sell[vol], Exhaustion/buy[range]
- [AGAINST] microFlow(abs/trap/exh): 6h micro-events: abs:buy×2, abs:sell×1, div:buy×1, div:sell×2, exh:buy×4, exh:sell×3, sdiv:buy×1, trap:buy×1 — net 9 buy-side vs 6 sell-side
- [FOR] liquidation: long-liq magnet 0.05783 (str 57, ~$7M est, -2.30%) as target
- [FOR] bookWalls: ±5% depth imbalance -0.062 (5m ago +0.016, falling bids); bid $0.03B vs ask $0.03B
- [FOR] cvd: taker buy 48.8%, perpCvd -79, spotCvd -17, quadrant both-selling, latestDiv bear (stale/none)
- [FOR] notifications: 6h weighted bias -6.8 (9 events)
- → place on DOGUSD in MT5, then set status "placed" + ticket + ACTUAL MT5 levels in desk/state.json and append an EXEC entry to desk/log.md

## 2026-11-16 17:59 UTC — agent task from zai-desk
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

## 2026-11-16 18:29 UTC — agent task from zai-desk
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

## 2026-11-16 18:59 UTC — agent task from zai-desk
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

## 2026-11-16 19:29 UTC — new suggested order — place in MT5 (debate FOR 5/AGAINST 2)
- R391-XRP-1 XRP SHORT limit entry 0.9565 · stop 0.9635 · targets 0.9401 / 0.9367 · R 2.3 · expires 2026-11-16 23:29 UTC
- BASIS: levels are PERP prices (perpRef 0.9557). Before placing in MT5 read spreads.XRPUSD.basisPct in desk/mt5.json and set every level = perpLevel × (1 + basisPct/100). Remember the broker spread — a SHORT fills at bid.
- [FOR] overview: h4 ↓/d1 ↓ EMA, price below day VWAP (0.9557 vs 0.9560), h4 RSI 39.8, day -1.8%
- [FOR] footprint: bull 31 / bear 41; recent: Divergence/sell[vol], Divergence/buy[range]
- [AGAINST] microFlow(abs/trap/exh): 6h micro-events: abs:buy×2, abs:sell×1, div:buy×3, div:sell×2, exh:buy×4, exh:sell×4, sdiv:buy×1, sdiv:sell×2, trap:buy×2 — net 12 buy-side vs 9 sell-side
- [FOR] liquidation: long-liq magnet 0.9401 (str 60, ~$18M est, -1.60%) as target
- [FOR] bookWalls: ±5% depth imbalance -0.142 (5m ago -0.061, falling bids); bid $0.05B vs ask $0.07B
- [FOR] cvd: taker buy 48.2%, perpCvd -267, spotCvd -76, quadrant both-selling, latestDiv bear (recent)
- [AGAINST] notifications: 6h weighted bias +3.9 (4 events)
- → place on XRPUSD in MT5, then set status "placed" + ticket + ACTUAL MT5 levels in desk/state.json and append an EXEC entry to desk/log.md

## 2026-11-16 19:29 UTC — agent task from zai-desk
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

## 2026-11-16 19:59 UTC — new suggested order — place in MT5 (debate FOR 7/AGAINST 0)
- R392-ADA-1 ADA SHORT limit entry 0.1538 · stop 0.1548 · targets 0.1512 / 0.1498 / 0.149 · R 2.5 · expires 2026-11-16 23:59 UTC
- BASIS: levels are PERP prices (perpRef 0.1538). Before placing in MT5 read spreads.ADAUSD.basisPct in desk/mt5.json and set every level = perpLevel × (1 + basisPct/100). Remember the broker spread — a SHORT fills at bid.
- [FOR] overview: h4 ↓/d1 ↓ EMA, price above day VWAP (0.1538 vs 0.1526), h4 RSI 38.1, day -1.0%
- [FOR] footprint: bull 59 / bear 63; recent: Trapped longs/sell[time], Divergence/sell[vol], Absorption/sell[range]
- [FOR] microFlow(abs/trap/exh): 6h micro-events: abs:buy×7, abs:sell×9, div:buy×2, div:sell×2, exh:buy×4, exh:sell×6, sdiv:buy×2, sdiv:sell×2, trap:buy×2, trap:sell×6 — net 17 buy-side vs 25 sell-side
- [FOR] liquidation: long-liq magnet 0.1498 (str 70, ~$3M est, -2.57%) as target
- [FOR] bookWalls: ±5% depth imbalance -0.406 (5m ago -0.266, falling bids); bid $0.01B vs ask $0.02B
- [FOR] cvd: taker buy 48.3%, perpCvd -38, spotCvd -7, quadrant both-selling, latestDiv bear (recent)
- [FOR] notifications: 6h weighted bias -1.9 (1 events)
- → place on ADAUSD in MT5, then set status "placed" + ticket + ACTUAL MT5 levels in desk/state.json and append an EXEC entry to desk/log.md

## 2026-11-16 19:59 UTC — agent task from zai-desk
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

## 2026-11-16 20:29 UTC — new suggested order — place in MT5 (debate FOR 5/AGAINST 1)
- R393-XAU-1 XAU SHORT limit entry 3876.72 · stop 3892.18 · targets 3800.58 · R 4.9 · expires 2026-11-17 00:29 UTC
- BASIS: levels are PERP prices (perpRef 3864.56). Before placing in MT5 read spreads.XAUUSD.basisPct in desk/mt5.json and set every level = perpLevel × (1 + basisPct/100). Remember the broker spread — a SHORT fills at bid.
- [FOR] overview: h4 ↓/d1 ↓ EMA, price below day VWAP (3,864.56 vs 3,870.57), h4 RSI 43.5, day -1.0%
- [FOR] footprint: bull 17 / bear 20; recent: Bull div/buy[time], Divergence/sell[vol]
- [AGAINST] microFlow(abs/trap/exh): 6h micro-events: div:buy×1, div:sell×1, exh:sell×1, sdiv:buy×4 — net 5 buy-side vs 2 sell-side
- [FOR] liquidation: long-liq magnet 3,800.58 (str 57, ~$41M est, -1.66%) as target
- [FOR] bookWalls: ±5% depth imbalance +0.111 (5m ago +0.111, falling bids); bid $0.05B vs ask $0.04B
- [FOR] cvd: taker buy 49.1%, perpCvd -107, spotCvd +0, quadrant both-selling, latestDiv bull (recent)
- → place on XAUUSD in MT5, then set status "placed" + ticket + ACTUAL MT5 levels in desk/state.json and append an EXEC entry to desk/log.md

## 2026-11-16 20:29 UTC — agent task from zai-desk
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

## 2026-11-16 20:59 UTC — new suggested order — place in MT5 (debate FOR 6/AGAINST 1)
- R394-LINK-1 LINK SHORT limit entry 9.154 · stop 9.215 · targets 8.979 / 8.946 / 8.92 · R 2.9 · expires 2026-11-17 00:59 UTC
- BASIS: levels are PERP prices (perpRef 9.122). Before placing in MT5 read spreads.LNKUSD.basisPct in desk/mt5.json and set every level = perpLevel × (1 + basisPct/100). Remember the broker spread — a SHORT fills at bid.
- [FOR] overview: h4 ↓/d1 ↓ EMA, price below day VWAP (9.122 vs 9.152), h4 RSI 37.0, day -1.8%
- [FOR] footprint: bull 41 / bear 44; recent: Divergence/sell[time], Divergence/buy[vol], Divergence/buy[range]
- [AGAINST] microFlow(abs/trap/exh): 6h micro-events: abs:buy×5, abs:sell×4, div:buy×6, div:sell×5, exh:buy×3, exh:sell×3, sdiv:buy×1, sdiv:sell×1, trap:buy×1, trap:sell×1 — net 16 buy-side vs 14 sell-side
- [FOR] liquidation: long-liq magnet 8.979 (str 81, ~$3M est, -1.55%) as target
- [FOR] bookWalls: ±5% depth imbalance -0.061 (5m ago +0.007, falling bids); bid $0.01B vs ask $0.01B
- [FOR] cvd: taker buy 48.8%, perpCvd -23, spotCvd -7, quadrant both-selling, latestDiv bull (recent)
- [FOR] notifications: 6h weighted bias -1.0 (8 events)
- → place on LNKUSD in MT5, then set status "placed" + ticket + ACTUAL MT5 levels in desk/state.json and append an EXEC entry to desk/log.md

## 2026-11-16 20:59 UTC — new suggested order — place in MT5 (debate FOR 6/AGAINST 1)
- R394-AVAX-2 AVAX SHORT limit entry 7.148 · stop 7.199 · targets 7.02 / 6.99 / 6.97 · R 2.5 · expires 2026-11-17 00:59 UTC
- BASIS: levels are PERP prices (perpRef 7.139). Before placing in MT5 read spreads.AVAXUSD.basisPct in desk/mt5.json and set every level = perpLevel × (1 + basisPct/100). Remember the broker spread — a SHORT fills at bid.
- [FOR] overview: h4 ↓/d1 ↓ EMA, price below day VWAP (7.139 vs 7.145), h4 RSI 31.9, day -2.3%
- [AGAINST] footprint: bull 57 / bear 44; recent: Exhaustion/sell[time], Absorption/sell[vol], Absorption/sell[range]
- [FOR] microFlow(abs/trap/exh): 6h micro-events: abs:buy×8, abs:sell×5, div:buy×1, div:sell×6, exh:buy×4, exh:sell×4, sdiv:buy×2, sdiv:sell×3, trap:sell×2 — net 15 buy-side vs 20 sell-side
- [FOR] liquidation: long-liq magnet 7.020 (str 90, ~$3M est, -1.75%) as target
- [FOR] bookWalls: ±5% depth imbalance +0.010 (5m ago +0.066, falling bids); bid $0.01B vs ask $0.01B
- [FOR] cvd: taker buy 48.2%, perpCvd -40, spotCvd -2, quadrant both-selling, latestDiv bull (recent)
- [FOR] notifications: 6h weighted bias -8.7 (11 events)
- → place on AVAXUSD in MT5, then set status "placed" + ticket + ACTUAL MT5 levels in desk/state.json and append an EXEC entry to desk/log.md

## 2026-11-16 20:59 UTC — new suggested order — place in MT5 (debate FOR 5/AGAINST 1)
- R394-XRP-3 XRP SHORT limit entry 0.9565 · stop 0.9633 · targets 0.9404 / 0.937 · R 2.3 · expires 2026-11-17 00:59 UTC
- BASIS: levels are PERP prices (perpRef 0.9551). Before placing in MT5 read spreads.XRPUSD.basisPct in desk/mt5.json and set every level = perpLevel × (1 + basisPct/100). Remember the broker spread — a SHORT fills at bid.
- [FOR] overview: h4 ↓/d1 ↓ EMA, price below day VWAP (0.9551 vs 0.9560), h4 RSI 40.1, day -1.9%
- [FOR] footprint: bull 40 / bear 43; recent: Bull div/buy[time], Divergence/buy[vol], Divergence/buy[range]
- [AGAINST] microFlow(abs/trap/exh): 6h micro-events: abs:buy×4, abs:sell×2, div:buy×5, div:sell×1, exh:buy×5, exh:sell×6, sdiv:buy×3, sdiv:sell×2, trap:buy×3 — net 20 buy-side vs 11 sell-side
- [FOR] liquidation: long-liq magnet 0.9404 (str 55, ~$18M est, -1.52%) as target
- [FOR] bookWalls: ±5% depth imbalance -0.027 (5m ago -0.054, rising bids); bid $0.06B vs ask $0.06B
- [FOR] cvd: taker buy 48.1%, perpCvd -272, spotCvd -79, quadrant both-selling, latestDiv bear (recent)
- → place on XRPUSD in MT5, then set status "placed" + ticket + ACTUAL MT5 levels in desk/state.json and append an EXEC entry to desk/log.md

## 2026-11-16 20:59 UTC — agent task from zai-desk
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

## 2026-11-16 21:29 UTC — agent task from zai-desk
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

## 2026-11-16 21:59 UTC — agent task from zai-desk
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

## 2026-11-16 22:29 UTC — agent task from zai-desk
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

## 2026-11-16 22:59 UTC — new suggested order — place in MT5 (debate FOR 6/AGAINST 1)
- R398-LTC-1 LTC SHORT limit entry 44.81 · stop 45.11 · targets 43.84 / 43.7 / 43.6 · R 3.2 · expires 2026-11-17 02:59 UTC
- BASIS: levels are PERP prices (perpRef 44.62). Before placing in MT5 read spreads.LTCUSD.basisPct in desk/mt5.json and set every level = perpLevel × (1 + basisPct/100). Remember the broker spread — a SHORT fills at bid.
- [FOR] overview: h4 ↓/d1 ↓ EMA, price below day VWAP (44.62 vs 44.62), h4 RSI 35.6, day -2.0%
- [AGAINST] footprint: bull 51 / bear 32; recent: Divergence/sell[time], Bear div/sell[vol], Absorption/sell[range]
- [FOR] microFlow(abs/trap/exh): 6h micro-events: abs:buy×2, abs:sell×1, div:sell×5, exh:sell×2, sdiv:sell×3, trap:buy×1 — net 3 buy-side vs 11 sell-side
- [FOR] liquidation: long-liq magnet 43.84 (str 49, ~$2M est, -1.73%) as target
- [FOR] bookWalls: ±5% depth imbalance +0.061 (5m ago -0.098, rising bids); bid $0.01B vs ask $0.01B
- [FOR] cvd: taker buy 48.9%, perpCvd -21, spotCvd +2, quadrant spot-bid, latestDiv bear (recent)
- [FOR] notifications: 6h weighted bias -2.9 (2 events)
- → place on LTCUSD in MT5, then set status "placed" + ticket + ACTUAL MT5 levels in desk/state.json and append an EXEC entry to desk/log.md

## 2026-11-16 22:59 UTC — agent task from zai-desk
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

## 2026-11-16 23:29 UTC — agent task from zai-desk
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

## 2026-11-16 23:59 UTC — agent task from zai-desk
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

## 2026-11-17 00:29 UTC — new suggested order — place in MT5 (debate FOR 5/AGAINST 1)
- R401-DOGE-1 DOGE SHORT limit entry 0.05886 · stop 0.05909 · targets 0.05755 / 0.05746 · R 5.6 · expires 2026-11-17 04:29 UTC
- BASIS: levels are PERP prices (perpRef 0.05877). Before placing in MT5 read spreads.DOGUSD.basisPct in desk/mt5.json and set every level = perpLevel × (1 + basisPct/100). Remember the broker spread — a SHORT fills at bid.
- [FOR] overview: h4 ↓/d1 ↓ EMA, price below day VWAP (0.05877 vs 0.05881), h4 RSI 37.4, day -0.2%
- [FOR] footprint: bull 27 / bear 32; recent: Exhaustion/buy[vol], Exhaustion/buy[range]
- [AGAINST] microFlow(abs/trap/exh): 6h micro-events: abs:sell×2, div:buy×1, exh:buy×3, sdiv:buy×1 — net 5 buy-side vs 2 sell-side
- [FOR] liquidation: long-liq magnet 0.05755 (str 73, ~$9M est, -2.13%) as target
- [FOR] bookWalls: ±5% depth imbalance -0.036 (5m ago +0.019, falling bids); bid $0.03B vs ask $0.03B
- [FOR] cvd: taker buy 48.8%, perpCvd -72, spotCvd -17, quadrant both-selling, latestDiv bear (stale/none)
- → place on DOGUSD in MT5, then set status "placed" + ticket + ACTUAL MT5 levels in desk/state.json and append an EXEC entry to desk/log.md

## 2026-11-17 00:29 UTC — new suggested order — place in MT5 (debate FOR 6/AGAINST 0)
- R401-ADA-2 ADA SHORT limit entry 0.153 · stop 0.1536 · targets 0.1499 / 0.1497 · R 5.1 · expires 2026-11-17 04:29 UTC
- BASIS: levels are PERP prices (perpRef 0.1528). Before placing in MT5 read spreads.ADAUSD.basisPct in desk/mt5.json and set every level = perpLevel × (1 + basisPct/100). Remember the broker spread — a SHORT fills at bid.
- [FOR] overview: h4 ↓/d1 ↓ EMA, price below day VWAP (0.1528 vs 0.1528), h4 RSI 36.9, day -0.1%
- [FOR] footprint: bull 59 / bear 60; recent: Trapped longs/sell[time], Divergence/buy[vol], Absorption/buy[range]
- [FOR] microFlow(abs/trap/exh): 6h micro-events: abs:buy×3, abs:sell×7, div:buy×3, exh:buy×2, exh:sell×2, sdiv:buy×1, sdiv:sell×1, trap:buy×2, trap:sell×2 — net 11 buy-side vs 12 sell-side
- [FOR] liquidation: long-liq magnet 0.1499 (str 68, ~$4M est, -1.82%) as target
- [FOR] bookWalls: ±5% depth imbalance -0.167 (5m ago -0.219, rising bids); bid $0.01B vs ask $0.02B
- [FOR] cvd: taker buy 48.3%, perpCvd -38, spotCvd -7, quadrant both-selling, latestDiv bear (recent)
- → place on ADAUSD in MT5, then set status "placed" + ticket + ACTUAL MT5 levels in desk/state.json and append an EXEC entry to desk/log.md

## 2026-11-17 00:29 UTC — agent task from zai-desk
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

## 2026-11-17 00:59 UTC — new suggested order — place in MT5 (debate FOR 6/AGAINST 0)
- R402-XAU-1 XAU SHORT limit entry 3864.26 · stop 3879.69 · targets 3800.58 · R 4.1 · expires 2026-11-17 04:59 UTC
- BASIS: levels are PERP prices (perpRef 3858.69). Before placing in MT5 read spreads.XAUUSD.basisPct in desk/mt5.json and set every level = perpLevel × (1 + basisPct/100). Remember the broker spread — a SHORT fills at bid.
- [FOR] overview: h4 ↓/d1 ↓ EMA, price below day VWAP (3,858.69 vs 3,863.93), h4 RSI 42.2, day -0.3%
- [FOR] footprint: bull 20 / bear 29; recent: Exhaustion/sell[time], Exhaustion/sell[vol]
- [FOR] microFlow(abs/trap/exh): 6h micro-events: abs:buy×1, exh:sell×3, sdiv:buy×1 — net 2 buy-side vs 3 sell-side
- [FOR] liquidation: long-liq magnet 3,800.58 (str 58, ~$41M est, -1.51%) as target
- [FOR] bookWalls: ±5% depth imbalance +0.090 (5m ago +0.090, falling bids); bid $0.06B vs ask $0.05B
- [FOR] cvd: taker buy 49.2%, perpCvd -102, spotCvd +0, quadrant both-selling, latestDiv bull (recent)
- → place on XAUUSD in MT5, then set status "placed" + ticket + ACTUAL MT5 levels in desk/state.json and append an EXEC entry to desk/log.md

## 2026-11-17 00:59 UTC — new suggested order — place in MT5 (debate FOR 7/AGAINST 0)
- R402-BNB-2 BNB SHORT limit entry 590.94 · stop 593.31 · targets 582.71 / 581.56 / 578.12 · R 3.5 · expires 2026-11-17 04:59 UTC
- BASIS: levels are PERP prices (perpRef 590.84). Before placing in MT5 read spreads.BNBUSD.basisPct in desk/mt5.json and set every level = perpLevel × (1 + basisPct/100). Remember the broker spread — a SHORT fills at bid.
- [FOR] overview: h4 ↓/d1 ↓ EMA, price above day VWAP (590.84 vs 590.66), h4 RSI 34.5, day -0.1%
- [FOR] footprint: bull 37 / bear 43; recent: Exhaustion/buy[time], Absorption/sell[vol], Bear div/sell[range]
- [FOR] microFlow(abs/trap/exh): 6h micro-events: abs:sell×4, div:buy×1, div:sell×2, exh:buy×2, exh:sell×2, sdiv:buy×1, sdiv:sell×3 — net 4 buy-side vs 11 sell-side
- [FOR] liquidation: long-liq magnet 582.71 (str 56, ~$7M est, -1.38%) as target
- [FOR] bookWalls: ±5% depth imbalance +0.004 (5m ago -0.002, rising bids); bid $0.02B vs ask $0.02B
- [FOR] cvd: taker buy 48.1%, perpCvd -73, spotCvd -15, quadrant both-selling, latestDiv bear (recent)
- [FOR] notifications: 6h weighted bias -1.9 (7 events)
- → place on BNBUSD in MT5, then set status "placed" + ticket + ACTUAL MT5 levels in desk/state.json and append an EXEC entry to desk/log.md

## 2026-11-17 00:59 UTC — agent task from zai-desk
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

## 2026-11-17 01:29 UTC — agent task from zai-desk
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

## 2026-11-17 01:59 UTC — agent task from zai-desk
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

## 2026-11-17 02:29 UTC — agent task from zai-desk
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

## 2026-11-17 02:59 UTC — new suggested order — place in MT5 (debate FOR 7/AGAINST 0)
- R406-DOGE-1 DOGE SHORT limit entry 0.05876 · stop 0.059 · targets 0.05782 / 0.05757 / 0.05744 · R 4 · expires 2026-11-17 06:59 UTC
- BASIS: levels are PERP prices (perpRef 0.05872). Before placing in MT5 read spreads.DOGUSD.basisPct in desk/mt5.json and set every level = perpLevel × (1 + basisPct/100). Remember the broker spread — a SHORT fills at bid.
- [FOR] overview: h4 ↓/d1 ↓ EMA, price below day VWAP (0.05872 vs 0.05879), h4 RSI 37.2, day -0.3%
- [FOR] footprint: bull 27 / bear 29; recent: Absorption/sell[time], Divergence/buy[vol], Absorption/sell[range]
- [FOR] microFlow(abs/trap/exh): 6h micro-events: abs:sell×4, div:buy×3, exh:buy×3, exh:sell×2, trap:sell×2 — net 6 buy-side vs 8 sell-side
- [FOR] liquidation: long-liq magnet 0.05782 (str 60, ~$8M est, -1.55%) as target
- [FOR] bookWalls: ±5% depth imbalance -0.009 (5m ago +0.031, falling bids); bid $0.03B vs ask $0.03B
- [FOR] cvd: taker buy 48.9%, perpCvd -70, spotCvd -16, quadrant both-selling, latestDiv bear (stale/none)
- [FOR] notifications: 6h weighted bias -8.6 (11 events)
- → place on DOGUSD in MT5, then set status "placed" + ticket + ACTUAL MT5 levels in desk/state.json and append an EXEC entry to desk/log.md

## 2026-11-17 02:59 UTC — agent task from zai-desk
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

## 2026-11-17 03:29 UTC — agent task from zai-desk
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

## 2026-11-17 03:59 UTC — agent task from zai-desk
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

## 2026-11-17 04:29 UTC — agent task from zai-desk
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

## 2026-11-17 04:59 UTC — new suggested order — place in MT5 (debate FOR 6/AGAINST 0)
- R410-BNB-1 BNB SHORT limit entry 595.6 · stop 597.98 · targets 589.83 / 582.78 · R 2.4 · expires 2026-11-17 08:59 UTC
- BASIS: levels are PERP prices (perpRef 595.6). Before placing in MT5 read spreads.BNBUSD.basisPct in desk/mt5.json and set every level = perpLevel × (1 + basisPct/100). Remember the broker spread — a SHORT fills at bid.
- [FOR] overview: h4 ↓/d1 ↓ EMA, price above day VWAP (595.60 vs 592.56), h4 RSI 38.6, day +0.7%
- [FOR] footprint: bull 36 / bear 45; recent: Bear div/sell[time], Trapped longs/sell[vol]
- [FOR] microFlow(abs/trap/exh): 6h micro-events: abs:sell×4, div:buy×2, div:sell×1, exh:buy×2, exh:sell×3, sdiv:buy×1, sdiv:sell×2, trap:sell×1 — net 5 buy-side vs 11 sell-side
- [FOR] liquidation: long-liq magnet 582.78 (str 76, ~$10M est, -2.15%) as target
- [FOR] bookWalls: ±5% depth imbalance +0.024 (5m ago +0.007, rising bids); bid $0.02B vs ask $0.02B
- [FOR] cvd: taker buy 48.2%, perpCvd -71, spotCvd -13, quadrant both-selling, latestDiv bear (recent)
- → place on BNBUSD in MT5, then set status "placed" + ticket + ACTUAL MT5 levels in desk/state.json and append an EXEC entry to desk/log.md

## 2026-11-17 04:59 UTC — new suggested order — place in MT5 (debate FOR 6/AGAINST 1)
- R410-XAU-2 XAU SHORT limit entry 3880.9 · stop 3896.42 · targets 3832.92 / 3800.58 · R 3.1 · expires 2026-11-17 08:59 UTC
- BASIS: levels are PERP prices (perpRef 3880.9). Before placing in MT5 read spreads.XAUUSD.basisPct in desk/mt5.json and set every level = perpLevel × (1 + basisPct/100). Remember the broker spread — a SHORT fills at bid.
- [FOR] overview: h4 ↓/d1 ↓ EMA, price above day VWAP (3,880.90 vs 3,869.21), h4 RSI 47.7, day +0.3%
- [FOR] footprint: bull 12 / bear 20; recent: Exhaustion/sell[time], Exhaustion/sell[vol], Exhaustion/sell[range]
- [FOR] microFlow(abs/trap/exh): 6h micro-events: div:buy×1, exh:sell×4 — net 1 buy-side vs 4 sell-side
- [FOR] liquidation: long-liq magnet 3,832.92 (str 54, ~$44M est, -1.24%) as target
- [AGAINST] liquidation-hazard: short-liq magnet 3,919.84 (str 83) sits between entry and stop — sweep risk
- [FOR] bookWalls: ±5% depth imbalance +0.099 (5m ago +0.099, falling bids); bid $0.04B vs ask $0.04B
- [FOR] cvd: taker buy 49.3%, perpCvd -89, spotCvd -1, quadrant both-selling, latestDiv bear (recent)
- → place on XAUUSD in MT5, then set status "placed" + ticket + ACTUAL MT5 levels in desk/state.json and append an EXEC entry to desk/log.md

## 2026-11-17 04:59 UTC — agent task from zai-desk
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

## 2026-11-17 05:29 UTC — new suggested order — place in MT5 (debate FOR 5/AGAINST 0)
- R411-SOL-1 SOL SHORT limit entry 72.87 · stop 73.41 · targets 71.67 · R 2.2 · expires 2026-11-17 09:29 UTC
- BASIS: levels are PERP prices (perpRef 72.87). Before placing in MT5 read spreads.SOLUSD.basisPct in desk/mt5.json and set every level = perpLevel × (1 + basisPct/100). Remember the broker spread — a SHORT fills at bid.
- [FOR] overview: h4 ↓/d1 ↓ EMA, price above day VWAP (72.87 vs 72.17), h4 RSI 42.8, day +1.9%
- [FOR] footprint: bull 41 / bear 45; recent: Absorption/buy[time], Trapped longs/sell[vol], Absorption/buy[range]
- [FOR] microFlow(abs/trap/exh): 6h micro-events: abs:buy×6, abs:sell×3, div:sell×4, exh:sell×8, sdiv:sell×1, trap:buy×4, trap:sell×3 — net 10 buy-side vs 19 sell-side
- [FOR] cvd: taker buy 49.4%, perpCvd -194, spotCvd -59, quadrant both-selling, latestDiv bear (recent)
- [FOR] notifications: 6h weighted bias -2.9 (9 events)
- → place on SOLUSD in MT5, then set status "placed" + ticket + ACTUAL MT5 levels in desk/state.json and append an EXEC entry to desk/log.md

## 2026-11-17 05:29 UTC — agent task from zai-desk
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

## 2026-11-17 06:29 UTC — agent task from zai-desk
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

## 2026-11-17 06:59 UTC — agent task from zai-desk
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

## 2026-11-17 07:14 UTC — new suggested order — place in MT5 (debate FOR 6/AGAINST 1)
- R415-DOGE-1 DOGE SHORT limit entry 0.05915 · stop 0.05939 · targets 0.05863 / 0.05782 · R 2.2 · expires 2026-11-17 11:13 UTC
- BASIS: levels are PERP prices (perpRef 0.05892). Before placing in MT5 read spreads.DOGUSD.basisPct in desk/mt5.json and set every level = perpLevel × (1 + basisPct/100). Remember the broker spread — a SHORT fills at bid.
- [FOR] overview: h4 ↓/d1 ↓ EMA, price below day VWAP (0.05892 vs 0.05896), h4 RSI 38.8, day +0.0%
- [FOR] footprint: bull 29 / bear 34; recent: Divergence/buy[time], Exhaustion/buy[vol], Divergence/buy[range]
- [FOR] microFlow(abs/trap/exh): 6h micro-events: abs:buy×2, abs:sell×2, div:buy×4, div:sell×4, exh:buy×2, exh:sell×5, trap:buy×1, trap:sell×2 — net 9 buy-side vs 13 sell-side
- [FOR] liquidation: long-liq magnet 0.05782 (str 55, ~$8M est, -1.84%) as target
- [FOR] bookWalls: ±5% depth imbalance -1.000 (5m ago -1.000, falling bids); bid $0.00B vs ask $0.05B
- [FOR] cvd: taker buy 48.9%, perpCvd -61, spotCvd -16, quadrant both-selling, latestDiv bear (stale/none)
- [AGAINST] notifications: 6h weighted bias +1.9 (4 events)
- → place on DOGUSD in MT5, then set status "placed" + ticket + ACTUAL MT5 levels in desk/state.json and append an EXEC entry to desk/log.md

## 2026-11-17 07:29 UTC — agent task from zai-desk
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

## 2026-11-17 07:59 UTC — agent task from zai-desk
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

## 2026-11-17 08:29 UTC — agent task from zai-desk
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

## 2026-11-17 08:59 UTC — agent task from zai-desk
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

## 2026-11-17 09:14 UTC — new suggested order — place in MT5 (debate FOR 5/AGAINST 2)
- R422-ETH-1 ETH SHORT limit entry 1829.93 · stop 1837.32 · targets 1799.1 · R 4.2 · expires 2026-11-17 13:08 UTC
- BASIS: levels are PERP prices (perpRef 1814.7). Before placing in MT5 read spreads.ETHUSD.basisPct in desk/mt5.json and set every level = perpLevel × (1 + basisPct/100). Remember the broker spread — a SHORT fills at bid.
- [FOR] overview: h4 ↓/d1 ↓ EMA, price below day VWAP (1,814.70 vs 1,824.16), h4 RSI 38.1, day -0.3%
- [AGAINST] footprint: bull 20 / bear 19; recent: Exhaustion/buy[time], Exhaustion/buy[vol], Exhaustion/buy[range]
- [FOR] microFlow(abs/trap/exh): 6h micro-events: abs:sell×1, exh:buy×4, exh:sell×4, sdiv:sell×2, trap:sell×1 — net 4 buy-side vs 8 sell-side
- [FOR] liquidation: long-liq magnet 1,799.10 (str 69, ~$244M est, -0.75%) as target
- [FOR] bookWalls: ±5% depth imbalance -0.019 (5m ago +0.002, falling bids); bid $0.61B vs ask $0.64B
- [FOR] cvd: taker buy 49.3%, perpCvd -925, spotCvd +0, quadrant spot-bid, latestDiv bear (recent)
- [AGAINST] notifications: 6h weighted bias +1.0 (3 events)
- → place on ETHUSD in MT5, then set status "placed" + ticket + ACTUAL MT5 levels in desk/state.json and append an EXEC entry to desk/log.md

## 2026-11-17 09:14 UTC — new suggested order — place in MT5 (debate FOR 6/AGAINST 1)
- R422-LTC-2 LTC SHORT limit entry 44.64 · stop 44.82 · targets 43.7 / 43.61 · R 5.3 · expires 2026-11-17 13:08 UTC
- BASIS: levels are PERP prices (perpRef 44.48). Before placing in MT5 read spreads.LTCUSD.basisPct in desk/mt5.json and set every level = perpLevel × (1 + basisPct/100). Remember the broker spread — a SHORT fills at bid.
- [FOR] overview: h4 ↓/d1 ↓ EMA, price below day VWAP (44.48 vs 44.65), h4 RSI 36.5, day +0.0%
- [AGAINST] footprint: bull 36 / bear 30; recent: Divergence/buy[time], Absorption/sell[vol], Absorption/sell[range]
- [FOR] microFlow(abs/trap/exh): 6h micro-events: abs:buy×3, abs:sell×9, div:buy×3, div:sell×4, sdiv:sell×2 — net 6 buy-side vs 15 sell-side
- [FOR] liquidation: long-liq magnet 43.70 (str 47, ~$2M est, -1.73%) as target
- [FOR] bookWalls: ±5% depth imbalance +0.036 (5m ago +0.043, falling bids); bid $0.01B vs ask $0.01B
- [FOR] cvd: taker buy 48.1%, perpCvd -16, spotCvd +0, quadrant spot-bid, latestDiv bear (recent)
- [FOR] notifications: 6h weighted bias -1.0 (3 events)
- → place on LTCUSD in MT5, then set status "placed" + ticket + ACTUAL MT5 levels in desk/state.json and append an EXEC entry to desk/log.md

## 2026-11-17 09:29 UTC — agent task from zai-desk
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

## 2026-11-17 09:30 UTC — new suggested order — place in MT5 (debate FOR 6/AGAINST 0)
- R423-XAU-1 XAU SHORT limit entry 3878.65 · stop 3894.13 · targets 3800.58 / 3794.52 · R 5 · expires 2026-11-17 13:29 UTC
- BASIS: levels are PERP prices (perpRef 3868.54). Before placing in MT5 read spreads.XAUUSD.basisPct in desk/mt5.json and set every level = perpLevel × (1 + basisPct/100). Remember the broker spread — a SHORT fills at bid.
- [FOR] overview: h4 ↓/d1 ↓ EMA, price below day VWAP (3,868.54 vs 3,873.32), h4 RSI 44.5, day +0.0%
- [FOR] footprint: bull 9 / bear 21; recent: Bull div/buy[time]
- [FOR] liquidation: long-liq magnet 3,800.58 (str 77, ~$60M est, -1.76%) as target
- [FOR] bookWalls: ±5% depth imbalance +0.159 (5m ago +0.156, rising bids); bid $0.05B vs ask $0.04B
- [FOR] cvd: taker buy 49.4%, perpCvd -78, spotCvd -1, quadrant both-selling, latestDiv bear (recent)
- [FOR] notifications: 6h weighted bias -1.0 (1 events)
- → place on XAUUSD in MT5, then set status "placed" + ticket + ACTUAL MT5 levels in desk/state.json and append an EXEC entry to desk/log.md

## 2026-11-17 09:30 UTC — new suggested order — place in MT5 (debate FOR 7/AGAINST 0)
- R423-LINK-2 LINK SHORT limit entry 9.188 · stop 9.226 · targets 8.981 · R 5.5 · expires 2026-11-17 13:29 UTC
- BASIS: levels are PERP prices (perpRef 9.097). Before placing in MT5 read spreads.LNKUSD.basisPct in desk/mt5.json and set every level = perpLevel × (1 + basisPct/100). Remember the broker spread — a SHORT fills at bid.
- [FOR] overview: h4 ↓/d1 ↓ EMA, price below day VWAP (9.097 vs 9.150), h4 RSI 37.1, day -0.4%
- [FOR] footprint: bull 44 / bear 46; recent: Divergence/buy[time], Divergence/sell[vol], Divergence/buy[range]
- [FOR] microFlow(abs/trap/exh): 6h micro-events: abs:buy×3, abs:sell×6, div:buy×6, div:sell×4, exh:buy×2, exh:sell×2, sdiv:buy×1, sdiv:sell×4, trap:sell×2 — net 12 buy-side vs 18 sell-side
- [FOR] liquidation: long-liq magnet 8.981 (str 94, ~$3M est, -1.28%) as target
- [FOR] bookWalls: ±5% depth imbalance -0.009 (5m ago +0.003, falling bids); bid $0.01B vs ask $0.01B
- [FOR] cvd: taker buy 49.1%, perpCvd -19, spotCvd -1, quadrant both-selling, latestDiv bear (recent)
- [FOR] notifications: 6h weighted bias -1.0 (3 events)
- → place on LNKUSD in MT5, then set status "placed" + ticket + ACTUAL MT5 levels in desk/state.json and append an EXEC entry to desk/log.md

## 2026-11-17 09:48 UTC — new suggested order — place in MT5 (debate FOR 4/AGAINST 2)
- R424-BNB-1 BNB SHORT limit entry 594.04 · stop 596.4 · targets 582.8 · R 4.8 · expires 2026-11-17 13:45 UTC
- BASIS: levels are PERP prices (perpRef 590.95). Before placing in MT5 read spreads.BNBUSD.basisPct in desk/mt5.json and set every level = perpLevel × (1 + basisPct/100). Remember the broker spread — a SHORT fills at bid.
- [FOR] overview: h4 ↓/d1 ↓ EMA, price below day VWAP (590.95 vs 592.50), h4 RSI 35.6, day -0.1%
- [AGAINST] footprint: bull 37 / bear 33; recent: Exhaustion/buy[time], Exhaustion/buy[vol], Divergence/buy[range]
- [AGAINST] microFlow(abs/trap/exh): 6h micro-events: abs:sell×3, div:buy×5, div:sell×1, exh:buy×3, sdiv:buy×2 — net 10 buy-side vs 4 sell-side
- [FOR] liquidation: long-liq magnet 582.80 (str 75, ~$8M est, -1.36%) as target
- [FOR] bookWalls: ±5% depth imbalance +0.027 (5m ago +0.032, falling bids); bid $0.02B vs ask $0.02B
- [FOR] cvd: taker buy 48.1%, perpCvd -57, spotCvd +0, quadrant spot-bid, latestDiv bear (recent)
- → place on BNBUSD in MT5, then set status "placed" + ticket + ACTUAL MT5 levels in desk/state.json and append an EXEC entry to desk/log.md

## 2026-11-17 09:59 UTC — agent task from zai-desk
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

## 2026-11-17 10:04 UTC — new suggested order — place in MT5 (debate FOR 4/AGAINST 2)
- R425-ETH-1 ETH SHORT limit entry 1830.47 · stop 1838.75 · targets 1813.68 / 1799.1 / 1783.3 · R 2 · expires 2026-11-17 14:03 UTC
- BASIS: levels are PERP prices (perpRef 1809.01). Before placing in MT5 read spreads.ETHUSD.basisPct in desk/mt5.json and set every level = perpLevel × (1 + basisPct/100). Remember the broker spread — a SHORT fills at bid.
- [FOR] overview: h4 ↓/d1 ↓ EMA, price below day VWAP (1,809.01 vs 1,822.18), h4 RSI 37.2, day -0.6%
- [AGAINST] footprint: bull 22 / bear 14; recent: Exhaustion/buy[time], Exhaustion/buy[vol], Exhaustion/buy[range]
- [AGAINST] microFlow(abs/trap/exh): 6h micro-events: abs:buy×1, div:buy×1, exh:buy×5, exh:sell×1, trap:buy×1, trap:sell×2 — net 8 buy-side vs 3 sell-side
- [FOR] liquidation: long-liq magnet 1,799.10 (str 78, ~$244M est, -0.50%) as target
- [FOR] bookWalls: ±5% depth imbalance -0.041 (5m ago -0.022, falling bids); bid $0.57B vs ask $0.62B
- [FOR] cvd: taker buy 49.3%, perpCvd -1107, spotCvd -374, quadrant both-selling, latestDiv bear (recent)
- → place on ETHUSD in MT5, then set status "placed" + ticket + ACTUAL MT5 levels in desk/state.json and append an EXEC entry to desk/log.md

## 2026-11-17 10:28 UTC — new suggested order — place in MT5 (debate FOR 4/AGAINST 2)
- R426-LINK-1 LINK SHORT limit entry 9.184 · stop 9.22 · targets 9.093 · R 2.5 · expires 2026-11-17 14:19 UTC
- BASIS: levels are PERP prices (perpRef 9.125). Before placing in MT5 read spreads.LNKUSD.basisPct in desk/mt5.json and set every level = perpLevel × (1 + basisPct/100). Remember the broker spread — a SHORT fills at bid.
- [FOR] overview: h4 ↓/d1 ↓ EMA, price below day VWAP (9.125 vs 9.148), h4 RSI 37.9, day -0.1%
- [FOR] footprint: bull 44 / bear 46; recent: Exhaustion/buy[time], Absorption/sell[vol], Exhaustion/buy[range]
- [AGAINST] microFlow(abs/trap/exh): 6h micro-events: abs:buy×2, abs:sell×5, div:buy×6, div:sell×2, exh:buy×4, exh:sell×1, sdiv:buy×2, sdiv:sell×3, trap:sell×1 — net 14 buy-side vs 12 sell-side
- [FOR] bookWalls: ±5% depth imbalance +0.053 (5m ago +0.053, falling bids); bid $0.01B vs ask $0.01B
- [FOR] cvd: taker buy 49.3%, perpCvd -8, spotCvd +0, quadrant spot-bid, latestDiv bear (recent)
- [AGAINST] notifications: 6h weighted bias +4.9 (5 events)
- → place on LNKUSD in MT5, then set status "placed" + ticket + ACTUAL MT5 levels in desk/state.json and append an EXEC entry to desk/log.md

## 2026-11-17 10:29 UTC — agent task from zai-desk
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

## 2026-11-17 10:59 UTC — agent task from zai-desk
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

## 2026-11-17 11:09 UTC — new suggested order — place in MT5 (debate FOR 6/AGAINST 1)
- R428-DOGE-1 DOGE SHORT limit entry 0.05892 · stop 0.05916 · targets 0.05784 / 0.05754 · R 4.5 · expires 2026-11-17 15:08 UTC
- BASIS: levels are PERP prices (perpRef 0.05859). Before placing in MT5 read spreads.DOGUSD.basisPct in desk/mt5.json and set every level = perpLevel × (1 + basisPct/100). Remember the broker spread — a SHORT fills at bid.
- [FOR] overview: h4 ↓/d1 ↓ EMA, price below day VWAP (0.05859 vs 0.05885), h4 RSI 37.4, day -0.5%
- [FOR] footprint: bull 28 / bear 33; recent: Absorption/sell[time], Absorption/sell[vol], Absorption/sell[range]
- [AGAINST] microFlow(abs/trap/exh): 6h micro-events: abs:buy×1, abs:sell×4, div:buy×4, exh:buy×3, sdiv:buy×2, trap:buy×1 — net 11 buy-side vs 4 sell-side
- [FOR] liquidation: long-liq magnet 0.05784 (str 53, ~$8M est, -1.29%) as target
- [FOR] bookWalls: ±5% depth imbalance -0.006 (5m ago -0.008, rising bids); bid $0.03B vs ask $0.03B
- [FOR] cvd: taker buy 48.9%, perpCvd -62, spotCvd -17, quadrant both-selling, latestDiv bull (recent)
- [FOR] notifications: 6h weighted bias -3.9 (4 events)
- → place on DOGUSD in MT5, then set status "placed" + ticket + ACTUAL MT5 levels in desk/state.json and append an EXEC entry to desk/log.md

## 2026-11-17 11:29 UTC — agent task from zai-desk
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

## 2026-11-17 12:01 UTC — agent task from zai-desk
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

## 2026-11-17 12:01 UTC — agent task from zai-desk
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

## 2026-11-17 12:29 UTC — agent task from zai-desk
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

## 2026-11-17 12:36 UTC — new suggested order — place in MT5 (debate FOR 7/AGAINST 0)
- R434-AVAX-1 AVAX SHORT limit entry 7.214 · stop 7.26 · targets 7.02 / 7 / 6.98 · R 4.2 · expires 2026-11-17 16:35 UTC
- BASIS: levels are PERP prices (perpRef 7.213). Before placing in MT5 read spreads.AVAXUSD.basisPct in desk/mt5.json and set every level = perpLevel × (1 + basisPct/100). Remember the broker spread — a SHORT fills at bid.
- [FOR] overview: h4 ↓/d1 ↓ EMA, price above day VWAP (7.213 vs 7.168), h4 RSI 37.2, day +1.4%
- [FOR] footprint: bull 31 / bear 34; recent: Absorption/buy[time], Divergence/sell[vol], Bear div/sell[range]
- [FOR] microFlow(abs/trap/exh): 6h micro-events: abs:buy×2, abs:sell×2, div:buy×1, div:sell×5, exh:buy×2, sdiv:sell×1, trap:sell×3 — net 5 buy-side vs 11 sell-side
- [FOR] liquidation: long-liq magnet 7.020 (str 89, ~$4M est, -2.72%) as target
- [FOR] bookWalls: ±5% depth imbalance +0.058 (5m ago +0.021, rising bids); bid $0.01B vs ask $0.01B
- [FOR] cvd: taker buy 48.5%, perpCvd -33, spotCvd +0, quadrant both-selling, latestDiv bear (recent)
- [FOR] notifications: 6h weighted bias -1.9 (1 events)
- → place on AVAXUSD in MT5, then set status "placed" + ticket + ACTUAL MT5 levels in desk/state.json and append an EXEC entry to desk/log.md

## 2026-11-17 12:59 UTC — agent task from zai-desk
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

## 2026-11-17 13:23 UTC — new suggested order — place in MT5 (debate FOR 4/AGAINST 1)
- R436-SOL-1 SOL SHORT limit entry 73.93 · stop 74.52 · targets 72.02 · R 3.2 · expires 2026-11-17 17:10 UTC
- BASIS: levels are PERP prices (perpRef 73.93). Before placing in MT5 read spreads.SOLUSD.basisPct in desk/mt5.json and set every level = perpLevel × (1 + basisPct/100). Remember the broker spread — a SHORT fills at bid.
- [FOR] overview: h4 ↓/d1 ↓ EMA, price above day VWAP (73.93 vs 72.57), h4 RSI 47.8, day +3.4%
- [FOR] footprint: bull 35 / bear 39; recent: Divergence/sell[vol], Divergence/sell[range]
- [AGAINST] microFlow(abs/trap/exh): 6h micro-events: abs:buy×5, abs:sell×3, div:buy×2, div:sell×3, exh:buy×1, exh:sell×1, trap:buy×1, trap:sell×1 — net 9 buy-side vs 8 sell-side
- [FOR] bookWalls: ±5% depth imbalance -0.107 (5m ago -0.075, falling bids); bid $0.10B vs ask $0.12B
- [FOR] notifications: 6h weighted bias -3.9 (6 events)
- → place on SOLUSD in MT5, then set status "placed" + ticket + ACTUAL MT5 levels in desk/state.json and append an EXEC entry to desk/log.md

## 2026-11-17 13:29 UTC — agent task from zai-desk
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

## 2026-11-17 13:52 UTC — new suggested order — place in MT5 (debate FOR 4/AGAINST 2)
- R438-XAU-1 XAU SHORT limit entry 3864.03 · stop 3879.45 · targets 3800.61 / 3790.5 · R 4.1 · expires 2026-11-17 17:51 UTC
- BASIS: levels are PERP prices (perpRef 3854.55). Before placing in MT5 read spreads.XAUUSD.basisPct in desk/mt5.json and set every level = perpLevel × (1 + basisPct/100). Remember the broker spread — a SHORT fills at bid.
- [FOR] overview: h4 ↓/d1 ↓ EMA, price below day VWAP (3,854.55 vs 3,870.07), h4 RSI 41.1, day -0.4%
- [FOR] footprint: bull 13 / bear 18; recent: Bull div/buy[time], Divergence/buy[vol]
- [AGAINST] microFlow(abs/trap/exh): 6h micro-events: abs:sell×1, div:buy×2, exh:buy×1, sdiv:buy×3 — net 6 buy-side vs 1 sell-side
- [FOR] liquidation: long-liq magnet 3,800.61 (str 79, ~$58M est, -1.40%) as target
- [AGAINST] bookWalls: ±5% depth imbalance +0.203 (5m ago +0.203, falling bids); bid $0.04B vs ask $0.03B
- [FOR] notifications: 6h weighted bias -3.9 (6 events)
- → place on XAUUSD in MT5, then set status "placed" + ticket + ACTUAL MT5 levels in desk/state.json and append an EXEC entry to desk/log.md

## 2026-11-17 13:52 UTC — new suggested order — place in MT5 (debate FOR 6/AGAINST 0)
- R438-AVAX-2 AVAX SHORT limit entry 7.233 · stop 7.283 · targets 7.02 / 7 / 6.98 · R 4.3 · expires 2026-11-17 17:51 UTC
- BASIS: levels are PERP prices (perpRef 7.233). Before placing in MT5 read spreads.AVAXUSD.basisPct in desk/mt5.json and set every level = perpLevel × (1 + basisPct/100). Remember the broker spread — a SHORT fills at bid.
- [FOR] overview: h4 ↓/d1 ↓ EMA, price above day VWAP (7.233 vs 7.177), h4 RSI 37.9, day +1.7%
- [FOR] footprint: bull 33 / bear 37; recent: Exhaustion/sell[time], Absorption/sell[vol], Divergence/sell[range]
- [FOR] microFlow(abs/trap/exh): 6h micro-events: abs:buy×2, abs:sell×2, div:buy×2, div:sell×5, exh:buy×2, exh:sell×2, sdiv:sell×2 — net 6 buy-side vs 11 sell-side
- [FOR] liquidation: long-liq magnet 7.020 (str 87, ~$4M est, -2.98%) as target
- [FOR] cvd: taker buy 48.5%, perpCvd -33, spotCvd +0, quadrant both-selling, latestDiv bear (recent)
- [FOR] notifications: 6h weighted bias -3.9 (5 events)
- → place on AVAXUSD in MT5, then set status "placed" + ticket + ACTUAL MT5 levels in desk/state.json and append an EXEC entry to desk/log.md

## 2026-11-17 13:59 UTC — agent task from zai-desk
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

## 2026-11-17 14:23 UTC — new suggested order — place in MT5 (debate FOR 3/AGAINST 1)
- R440-XAU-1 XAU SHORT limit entry 3878.72 · stop 3894.19 · targets 3824.84 / 3800.58 / 3786.43 · R 3.5 · expires 2026-11-17 18:23 UTC
- BASIS: levels are PERP prices (perpRef 3866.75). Before placing in MT5 read spreads.XAUUSD.basisPct in desk/mt5.json and set every level = perpLevel × (1 + basisPct/100). Remember the broker spread — a SHORT fills at bid.
- [FOR] overview: h4 ↓/d1 ↓ EMA, price below day VWAP (3,866.75 vs 3,869.50), h4 RSI 44.0, day -0.0%
- [FOR] footprint: bull 9 / bear 17; recent: Bull div/buy[time], Divergence/sell[vol]
- [FOR] liquidation: long-liq magnet 3,824.84 (str 74, ~$57M est, -1.08%) as target
- [AGAINST] bookWalls: ±5% depth imbalance +0.221 (5m ago +0.266, falling bids); bid $0.06B vs ask $0.04B
- → place on XAUUSD in MT5, then set status "placed" + ticket + ACTUAL MT5 levels in desk/state.json and append an EXEC entry to desk/log.md

## 2026-11-17 14:29 UTC — agent task from zai-desk
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

## 2026-11-17 14:40 UTC — new suggested order — place in MT5 (debate FOR 5/AGAINST 1)
- R441-DOGE-1 DOGE SHORT limit entry 0.05964 · stop 0.05995 · targets 0.05857 / 0.05784 · R 3.4 · expires 2026-11-17 18:38 UTC
- BASIS: levels are PERP prices (perpRef 0.05964). Before placing in MT5 read spreads.DOGUSD.basisPct in desk/mt5.json and set every level = perpLevel × (1 + basisPct/100). Remember the broker spread — a SHORT fills at bid.
- [FOR] overview: h4 ↓/d1 ↓ EMA, price above day VWAP (0.05964 vs 0.05900), h4 RSI 42.9, day +1.2%
- [FOR] footprint: bull 26 / bear 30; recent: Bear div/sell[time], Exhaustion/sell[vol], Absorption/buy[range]
- [FOR] liquidation: long-liq magnet 0.05784 (str 62, ~$8M est, -2.80%) as target
- [AGAINST] liquidation-hazard: short-liq magnet 0.06021 (str 74) sits between entry and stop — sweep risk
- [FOR] cvd: taker buy 48.9%, perpCvd -65, spotCvd -16, quadrant both-selling, latestDiv bear (recent)
- [FOR] notifications: 6h weighted bias -2.0 (2 events)
- → place on DOGUSD in MT5, then set status "placed" + ticket + ACTUAL MT5 levels in desk/state.json and append an EXEC entry to desk/log.md

## 2026-11-17 14:56 UTC — new suggested order — place in MT5 (debate FOR 5/AGAINST 1)
- R442-ETH-1 ETH SHORT limit entry 1818.56 · stop 1830.36 · targets 1783.3 / 1772.02 · R 3 · expires 2026-11-17 18:55 UTC
- BASIS: levels are PERP prices (perpRef 1807.02). Before placing in MT5 read spreads.ETHUSD.basisPct in desk/mt5.json and set every level = perpLevel × (1 + basisPct/100). Remember the broker spread — a SHORT fills at bid.
- [FOR] overview: h4 ↓/d1 ↓ EMA, price below day VWAP (1,807.02 vs 1,816.43), h4 RSI 36.7, day -0.7%
- [AGAINST] footprint: bull 24 / bear 22; recent: Divergence/buy[time], Exhaustion/sell[vol], Absorption/sell[range]
- [FOR] microFlow(abs/trap/exh): 6h micro-events: abs:buy×3, abs:sell×3, div:buy×2, div:sell×1, exh:buy×3, exh:sell×3, sdiv:sell×2 — net 8 buy-side vs 9 sell-side
- [FOR] liquidation: long-liq magnet 1,783.30 (str 95, ~$278M est, -1.49%) as target
- [FOR] cvd: taker buy 49.2%, perpCvd -539, spotCvd +0, quadrant spot-bid, latestDiv bear (recent)
- [FOR] notifications: 6h weighted bias -2.0 (2 events)
- → place on ETHUSD in MT5, then set status "placed" + ticket + ACTUAL MT5 levels in desk/state.json and append an EXEC entry to desk/log.md

## 2026-11-17 14:59 UTC — agent task from zai-desk
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

## 2026-11-17 15:13 UTC — new suggested order — place in MT5 (debate FOR 5/AGAINST 1)
- R443-XAU-1 XAU SHORT limit entry 3865.69 · stop 3881.15 · targets 3824.84 / 3796.54 / 3790.48 · R 2.6 · expires 2026-11-17 19:12 UTC
- BASIS: levels are PERP prices (perpRef 3863.45). Before placing in MT5 read spreads.XAUUSD.basisPct in desk/mt5.json and set every level = perpLevel × (1 + basisPct/100). Remember the broker spread — a SHORT fills at bid.
- [FOR] overview: h4 ↓/d1 ↓ EMA, price below day VWAP (3,863.45 vs 3,869.58), h4 RSI 43.1, day -0.1%
- [FOR] footprint: bull 8 / bear 20; recent: Exhaustion/sell[time], Exhaustion/sell[vol], Exhaustion/sell[range]
- [FOR] microFlow(abs/trap/exh): 6h micro-events: exh:sell×3, sdiv:buy×2 — net 2 buy-side vs 3 sell-side
- [FOR] liquidation: long-liq magnet 3,824.84 (str 44, ~$65M est, -1.02%) as target
- [AGAINST] bookWalls: ±5% depth imbalance +0.226 (5m ago +0.226, falling bids); bid $0.06B vs ask $0.04B
- [FOR] notifications: 6h weighted bias -3.0 (3 events)
- → place on XAUUSD in MT5, then set status "placed" + ticket + ACTUAL MT5 levels in desk/state.json and append an EXEC entry to desk/log.md

## 2026-11-17 15:29 UTC — agent task from zai-desk
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

## 2026-11-17 15:46 UTC — new suggested order — place in MT5 (debate FOR 6/AGAINST 0)
- R446-ADA-1 ADA SHORT limit entry 0.1545 · stop 0.1555 · targets 0.1499 / 0.1485 · R 4.6 · expires 2026-11-17 19:44 UTC
- BASIS: levels are PERP prices (perpRef 0.1519). Before placing in MT5 read spreads.ADAUSD.basisPct in desk/mt5.json and set every level = perpLevel × (1 + basisPct/100). Remember the broker spread — a SHORT fills at bid.
- [FOR] overview: h4 ↓/d1 ↓ EMA, price below day VWAP (0.1519 vs 0.1536), h4 RSI 37.3, day -0.7%
- [FOR] footprint: bull 35 / bear 39; recent: Divergence/sell[time], Exhaustion/sell[vol], Absorption/buy[range]
- [FOR] microFlow(abs/trap/exh): 6h micro-events: abs:buy×4, abs:sell×6, div:sell×2, exh:sell×5, trap:sell×1 — net 4 buy-side vs 14 sell-side
- [FOR] liquidation: long-liq magnet 0.1499 (str 92, ~$4M est, -0.88%) as target
- [FOR] bookWalls: ±5% depth imbalance -0.325 (5m ago +0.031, falling bids); bid $0.01B vs ask $0.02B
- [FOR] cvd: taker buy 48.8%, perpCvd -27, spotCvd -5, quadrant both-selling, latestDiv bull (recent)
- → place on ADAUSD in MT5, then set status "placed" + ticket + ACTUAL MT5 levels in desk/state.json and append an EXEC entry to desk/log.md

## 2026-11-17 15:59 UTC — agent task from zai-desk
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

## 2026-11-17 16:43 UTC — agent task from zai-desk
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

## 2026-11-17 16:59 UTC — agent task from zai-desk
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

## 2026-11-17 17:29 UTC — agent task from zai-desk
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

## 2026-11-17 17:58 UTC — new suggested order — place in MT5 (debate FOR 5/AGAINST 1)
- R454-AVAX-1 AVAX SHORT limit entry 7.186 · stop 7.253 · targets 6.94 / 6.9 · R 3.7 · expires 2026-11-17 21:58 UTC
- BASIS: levels are PERP prices (perpRef 7.083). Before placing in MT5 read spreads.AVAXUSD.basisPct in desk/mt5.json and set every level = perpLevel × (1 + basisPct/100). Remember the broker spread — a SHORT fills at bid.
- [FOR] overview: h4 ↓/d1 ↓ EMA, price below day VWAP (7.083 vs 7.153), h4 RSI 33.3, day -0.4%
- [FOR] footprint: bull 42 / bear 46; recent: Exhaustion/sell[time], Absorption/buy[vol], Divergence/sell[range]
- [FOR] microFlow(abs/trap/exh): 6h micro-events: abs:buy×6, abs:sell×6, div:buy×5, div:sell×8, exh:sell×2, sdiv:sell×2, trap:buy×3, trap:sell×2 — net 14 buy-side vs 20 sell-side
- [FOR] liquidation: long-liq magnet 6.940 (str 75, ~$2M est, -2.04%) as target
- [FOR] cvd: taker buy 48.9%, perpCvd -25, spotCvd +0, quadrant spot-bid, latestDiv bear (recent)
- [AGAINST] notifications: 6h weighted bias +1.0 (1 events)
- → place on AVAXUSD in MT5, then set status "placed" + ticket + ACTUAL MT5 levels in desk/state.json and append an EXEC entry to desk/log.md

## 2026-11-17 17:59 UTC — agent task from zai-desk
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

## 2026-11-17 18:29 UTC — agent task from zai-desk
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

## 2026-11-17 18:59 UTC — agent task from zai-desk
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

## 2026-11-17 19:02 UTC — new suggested order — place in MT5 (debate FOR 5/AGAINST 0)
- R458-DOGE-1 DOGE SHORT limit entry 0.05863 · stop 0.05906 · targets 0.05731 / 0.05709 / 0.05666 · R 3.1 · expires 2026-11-17 23:02 UTC
- BASIS: levels are PERP prices (perpRef 0.05854). Before placing in MT5 read spreads.DOGUSD.basisPct in desk/mt5.json and set every level = perpLevel × (1 + basisPct/100). Remember the broker spread — a SHORT fills at bid.
- [FOR] overview: h4 ↓/d1 ↓ EMA, price below day VWAP (0.05854 vs 0.05879), h4 RSI 38.2, day -0.6%
- [FOR] footprint: bull 24 / bear 29; recent: Divergence/buy[time], Exhaustion/sell[vol], Exhaustion/sell[range]
- [FOR] microFlow(abs/trap/exh): 6h micro-events: abs:sell×1, div:buy×1, exh:buy×2, exh:sell×5 — net 3 buy-side vs 6 sell-side
- [FOR] liquidation: long-liq magnet 0.05731 (str 69, ~$9M est, -2.11%) as target
- [FOR] cvd: taker buy 49.2%, perpCvd -41, spotCvd -11, quadrant both-selling, latestDiv bear (recent)
- → place on DOGUSD in MT5, then set status "placed" + ticket + ACTUAL MT5 levels in desk/state.json and append an EXEC entry to desk/log.md

## 2026-11-17 19:17 UTC — new suggested order — place in MT5 (debate FOR 4/AGAINST 2)
- R459-ETH-1 ETH SHORT limit entry 1819.11 · stop 1838.08 · targets 1748.32 / 1737.03 / 1726.87 · R 3.7 · expires 2026-11-17 23:17 UTC
- BASIS: levels are PERP prices (perpRef 1791.58). Before placing in MT5 read spreads.ETHUSD.basisPct in desk/mt5.json and set every level = perpLevel × (1 + basisPct/100). Remember the broker spread — a SHORT fills at bid.
- [FOR] overview: h4 ↓/d1 ↓ EMA, price below day VWAP (1,791.58 vs 1,803.92), h4 RSI 35.5, day -1.5%
- [AGAINST] footprint: bull 25 / bear 21; recent: Absorption/buy[vol], Absorption/buy[range]
- [AGAINST] microFlow(abs/trap/exh): 6h micro-events: abs:buy×6, abs:sell×3, div:buy×1, div:sell×2, exh:buy×3, exh:sell×1, sdiv:sell×1, trap:buy×2, trap:sell×1 — net 12 buy-side vs 8 sell-side
- [FOR] largeOrders: ask wall $11.9M @ 1,823.33 within 2% supports
- [FOR] liquidation: long-liq magnet 1,748.32 (str 51, ~$148M est, -2.47%) as target
- [FOR] cvd: taker buy 49.7%, perpCvd -418, spotCvd -326, quadrant both-selling, latestDiv bear (recent)
- → place on ETHUSD in MT5, then set status "placed" + ticket + ACTUAL MT5 levels in desk/state.json and append an EXEC entry to desk/log.md
