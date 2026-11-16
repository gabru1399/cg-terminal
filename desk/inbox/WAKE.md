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
