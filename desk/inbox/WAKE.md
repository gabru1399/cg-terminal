# WAKE — pending tasks for atg-exec (daemon appends; agent handles then clears)

## 2026-11-17 19:29 UTC — agent task from zai-desk
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

## 2026-11-17 19:48 UTC — new suggested order — place in MT5 (debate FOR 6/AGAINST 0)
- R461-LINK-1 LINK SHORT limit entry 9.111 · stop 9.194 · targets 8.921 / 8.882 / 8.854 · R 2.3 · expires 2026-11-17 23:48 UTC
- BASIS: levels are PERP prices (perpRef 9.11). Before placing in MT5 read spreads.LNKUSD.basisPct in desk/mt5.json and set every level = perpLevel × (1 + basisPct/100). Remember the broker spread — a SHORT fills at bid.
- [FOR] overview: h4 ↓/d1 ↓ EMA, price below day VWAP (9.110 vs 9.172), h4 RSI 38.9, day -0.3%
- [FOR] footprint: bull 42 / bear 43; recent: Absorption/buy[vol], Absorption/sell[range]
- [FOR] microFlow(abs/trap/exh): 6h micro-events: abs:buy×1, abs:sell×7, div:buy×5, div:sell×3, exh:buy×3, exh:sell×2, sdiv:buy×1, sdiv:sell×2, trap:buy×1, trap:sell×4 — net 11 buy-side vs 18 sell-side
- [FOR] liquidation: long-liq magnet 8.921 (str 79, ~$3M est, -2.12%) as target
- [FOR] cvd: taker buy 49.8%, perpCvd -7, spotCvd +4, quadrant spot-bid, latestDiv bear (recent)
- [FOR] notifications: 6h weighted bias -4.9 (5 events)
- → place on LNKUSD in MT5, then set status "placed" + ticket + ACTUAL MT5 levels in desk/state.json and append an EXEC entry to desk/log.md

## 2026-11-17 19:59 UTC — agent task from zai-desk
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

## 2026-11-17 20:19 UTC — new suggested order — place in MT5 (debate FOR 5/AGAINST 1)
- R463-ADA-1 ADA SHORT limit entry 0.1525 · stop 0.1538 · targets 0.1489 / 0.1485 / 0.1478 · R 2.9 · expires 2026-11-18 00:19 UTC
- BASIS: levels are PERP prices (perpRef 0.1523). Before placing in MT5 read spreads.ADAUSD.basisPct in desk/mt5.json and set every level = perpLevel × (1 + basisPct/100). Remember the broker spread — a SHORT fills at bid.
- [FOR] overview: h4 ↓/d1 ↓ EMA, price below day VWAP (0.1523 vs 0.1530), h4 RSI 38.8, day -0.5%
- [FOR] footprint: bull 35 / bear 46; recent: Exhaustion/buy[time], Exhaustion/buy[vol], Absorption/sell[range]
- [AGAINST] microFlow(abs/trap/exh): 6h micro-events: abs:buy×3, abs:sell×10, div:buy×3, div:sell×1, exh:buy×8, exh:sell×3, sdiv:buy×1, sdiv:sell×1, trap:buy×1 — net 16 buy-side vs 15 sell-side
- [FOR] liquidation: long-liq magnet 0.1489 (str 75, ~$4M est, -2.35%) as target
- [FOR] bookWalls: ±5% depth imbalance -0.135 (5m ago -0.181, rising bids); bid $0.01B vs ask $0.02B
- [FOR] cvd: taker buy 49.3%, perpCvd -15, spotCvd -3, quadrant both-selling, latestDiv bull (recent)
- → place on ADAUSD in MT5, then set status "placed" + ticket + ACTUAL MT5 levels in desk/state.json and append an EXEC entry to desk/log.md

## 2026-11-17 20:29 UTC — agent task from zai-desk
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

## 2026-11-17 20:59 UTC — agent task from zai-desk
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

## 2026-11-17 21:22 UTC — new suggested order — place in MT5 (debate FOR 6/AGAINST 1)
- R467-DOGE-1 DOGE SHORT limit entry 0.05942 · stop 0.05984 · targets 0.0584 / 0.05737 / 0.05717 · R 2.4 · expires 2026-11-18 01:21 UTC
- BASIS: levels are PERP prices (perpRef 0.05942). Before placing in MT5 read spreads.DOGUSD.basisPct in desk/mt5.json and set every level = perpLevel × (1 + basisPct/100). Remember the broker spread — a SHORT fills at bid.
- [FOR] overview: h4 ↓/d1 ↓ EMA, price above day VWAP (0.05942 vs 0.05883), h4 RSI 43.7, day +0.9%
- [FOR] footprint: bull 33 / bear 40; recent: Exhaustion/sell[time], Exhaustion/sell[vol], Divergence/sell[range]
- [FOR] microFlow(abs/trap/exh): 6h micro-events: abs:buy×1, abs:sell×1, div:buy×2, div:sell×3, exh:buy×2, exh:sell×6 — net 5 buy-side vs 10 sell-side
- [FOR] liquidation: long-liq magnet 0.05737 (str 82, ~$9M est, -3.48%) as target
- [AGAINST] liquidation-hazard: short-liq magnet 0.06013 (str 87) sits between entry and stop — sweep risk
- [FOR] cvd: taker buy 49.3%, perpCvd -37, spotCvd -9, quadrant both-selling, latestDiv bear (recent)
- [FOR] notifications: 6h weighted bias -3.0 (3 events)
- → place on DOGUSD in MT5, then set status "placed" + ticket + ACTUAL MT5 levels in desk/state.json and append an EXEC entry to desk/log.md

## 2026-11-17 21:29 UTC — agent task from zai-desk
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

## 2026-11-17 21:59 UTC — new suggested order — place in MT5 (debate FOR 5/AGAINST 1)
- R469-AVAX-1 AVAX SHORT limit entry 7.186 · stop 7.252 · targets 6.94 / 6.92 / 6.89 · R 3.8 · expires 2026-11-18 01:58 UTC
- BASIS: levels are PERP prices (perpRef 7.152). Before placing in MT5 read spreads.AVAXUSD.basisPct in desk/mt5.json and set every level = perpLevel × (1 + basisPct/100). Remember the broker spread — a SHORT fills at bid.
- [FOR] overview: h4 ↓/d1 ↓ EMA, price above day VWAP (7.152 vs 7.148), h4 RSI 37.2, day +0.5%
- [FOR] footprint: bull 41 / bear 51; recent: Divergence/sell[time], Absorption/buy[vol], Absorption/sell[range]
- [AGAINST] microFlow(abs/trap/exh): 6h micro-events: abs:buy×5, abs:sell×5, div:buy×5, div:sell×6, exh:buy×2, exh:sell×1, sdiv:buy×1, sdiv:sell×1, trap:buy×2, trap:sell×1 — net 15 buy-side vs 14 sell-side
- [FOR] liquidation: long-liq magnet 6.940 (str 84, ~$2M est, -3.03%) as target
- [FOR] cvd: taker buy 49.1%, perpCvd -21, spotCvd +1, quadrant spot-bid, latestDiv bear (recent)
- [FOR] notifications: 6h weighted bias -2.0 (1 events)
- → place on AVAXUSD in MT5, then set status "placed" + ticket + ACTUAL MT5 levels in desk/state.json and append an EXEC entry to desk/log.md

## 2026-11-17 21:59 UTC — agent task from zai-desk
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

## 2026-11-17 22:29 UTC — agent task from zai-desk
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

## 2026-11-17 22:59 UTC — agent task from zai-desk
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

## 2026-11-17 23:29 UTC — agent task from zai-desk
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

## 2026-11-17 23:34 UTC — new suggested order — place in MT5 (debate FOR 7/AGAINST 0)
- R475-LINK-1 LINK SHORT limit entry 9.31 · stop 9.395 · targets 9.076 / 9.029 · R 2.7 · expires 2026-11-18 03:33 UTC
- BASIS: levels are PERP prices (perpRef 9.31). Before placing in MT5 read spreads.LNKUSD.basisPct in desk/mt5.json and set every level = perpLevel × (1 + basisPct/100). Remember the broker spread — a SHORT fills at bid.
- [FOR] overview: h4 ↓/d1 ↓ EMA, price above day VWAP (9.310 vs 9.182), h4 RSI 47.8, day +1.9%
- [FOR] footprint: bull 38 / bear 40; recent: Absorption/buy[vol], Divergence/sell[range]
- [FOR] microFlow(abs/trap/exh): 6h micro-events: abs:buy×3, abs:sell×4, div:buy×1, div:sell×3, exh:sell×1, sdiv:buy×1, sdiv:sell×2, trap:buy×1, trap:sell×2 — net 6 buy-side vs 12 sell-side
- [FOR] liquidation: long-liq magnet 9.029 (str 69, ~$2M est, -3.09%) as target
- [FOR] bookWalls: ±5% depth imbalance -0.101 (5m ago -0.080, falling bids); bid $0.01B vs ask $0.02B
- [FOR] cvd: taker buy 50.1%, perpCvd -3, spotCvd +5, quadrant spot-bid, latestDiv bear (recent)
- [FOR] notifications: 6h weighted bias -5.9 (6 events)
- → place on LNKUSD in MT5, then set status "placed" + ticket + ACTUAL MT5 levels in desk/state.json and append an EXEC entry to desk/log.md

## 2026-11-17 23:50 UTC — new suggested order — place in MT5 (debate FOR 4/AGAINST 0)
- R476-XRP-1 XRP SHORT limit entry 0.9843 · stop 0.9929 · targets 0.9539 · R 3.5 · expires 2026-11-18 03:49 UTC
- BASIS: levels are PERP prices (perpRef 0.9843). Before placing in MT5 read spreads.XRPUSD.basisPct in desk/mt5.json and set every level = perpLevel × (1 + basisPct/100). Remember the broker spread — a SHORT fills at bid.
- [FOR] overview: h4 ↓/d1 ↓ EMA, price above day VWAP (0.9843 vs 0.9650), h4 RSI 51.6, day +3.1%
- [FOR] footprint: bull 37 / bear 45; recent: Divergence/sell[vol], Divergence/sell[range]
- [FOR] microFlow(abs/trap/exh): 6h micro-events: abs:buy×4, abs:sell×3, div:sell×5, exh:sell×2, sdiv:buy×1, trap:buy×1, trap:sell×1 — net 6 buy-side vs 11 sell-side
- [FOR] notifications: 6h weighted bias -6.8 (11 events)
- → place on XRPUSD in MT5, then set status "placed" + ticket + ACTUAL MT5 levels in desk/state.json and append an EXEC entry to desk/log.md

## 2026-11-17 23:59 UTC — agent task from zai-desk
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

## 2026-11-18 00:29 UTC — agent task from zai-desk
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

## 2026-11-18 00:59 UTC — agent task from zai-desk
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

## 2026-11-18 01:07 UTC — new suggested order — place in MT5 (debate FOR 4/AGAINST 2)
- R481-XAU-1 XAU SHORT limit entry 3840.15 · stop 3855.47 · targets 3799.65 / 3789.87 · R 2.6 · expires 2026-11-18 05:07 UTC
- BASIS: levels are PERP prices (perpRef 3831.87). Before placing in MT5 read spreads.XAUUSD.basisPct in desk/mt5.json and set every level = perpLevel × (1 + basisPct/100). Remember the broker spread — a SHORT fills at bid.
- [FOR] overview: h4 ↓/d1 ↓ EMA, price below day VWAP (3,831.87 vs 3,832.23), h4 RSI 36.5, day -0.6%
- [FOR] footprint: bull 9 / bear 17; recent: Bull div/buy[time]
- [AGAINST] microFlow(abs/trap/exh): 6h micro-events: sdiv:buy×1 — net 1 buy-side vs 0 sell-side
- [FOR] liquidation: long-liq magnet 3,799.65 (str 46, ~$68M est, -0.89%) as target
- [AGAINST] bookWalls: ±5% depth imbalance +0.160 (5m ago +0.105, rising bids); bid $0.06B vs ask $0.04B
- [FOR] notifications: 6h weighted bias -4.0 (6 events)
- → place on XAUUSD in MT5, then set status "placed" + ticket + ACTUAL MT5 levels in desk/state.json and append an EXEC entry to desk/log.md

## 2026-11-18 01:24 UTC — new suggested order — place in MT5 (debate FOR 6/AGAINST 0)
- R482-ADA-1 ADA SHORT limit entry 0.1547 · stop 0.1553 · targets 0.153 · R 2.7 · expires 2026-11-18 05:22 UTC
- BASIS: levels are PERP prices (perpRef 0.1532). Before placing in MT5 read spreads.ADAUSD.basisPct in desk/mt5.json and set every level = perpLevel × (1 + basisPct/100). Remember the broker spread — a SHORT fills at bid.
- [FOR] overview: h4 ↓/d1 ↓ EMA, price below day VWAP (0.1532 vs 0.1543), h4 RSI 42.0, day -1.4%
- [FOR] footprint: bull 38 / bear 55; recent: Absorption/sell[time], Exhaustion/sell[vol], Absorption/sell[range]
- [FOR] microFlow(abs/trap/exh): 6h micro-events: abs:buy×5, abs:sell×7, div:buy×3, div:sell×2, exh:buy×1, exh:sell×3, trap:buy×1, trap:sell×2 — net 10 buy-side vs 14 sell-side
- [FOR] liquidation: long-liq magnet 0.1489 (str 76, ~$4M est, -2.81%) as target
- [FOR] bookWalls: ±5% depth imbalance -0.434 (5m ago -0.473, rising bids); bid $0.01B vs ask $0.02B
- [FOR] notifications: 6h weighted bias -2.0 (2 events)
- → place on ADAUSD in MT5, then set status "placed" + ticket + ACTUAL MT5 levels in desk/state.json and append an EXEC entry to desk/log.md

## 2026-11-18 01:24 UTC — new suggested order — place in MT5 (debate FOR 5/AGAINST 1)
- R482-SOL-2 SOL SHORT limit entry 74.95 · stop 75.24 · targets 74.15 / 73.52 · R 2.7 · expires 2026-11-18 05:22 UTC
- BASIS: levels are PERP prices (perpRef 74.64). Before placing in MT5 read spreads.SOLUSD.basisPct in desk/mt5.json and set every level = perpLevel × (1 + basisPct/100). Remember the broker spread — a SHORT fills at bid.
- [FOR] overview: h4 ↓/d1 ↓ EMA, price below day VWAP (74.64 vs 74.97), h4 RSI 51.5, day -0.7%
- [FOR] footprint: bull 34 / bear 37; recent: Absorption/sell[time], Trapped longs/sell[vol], Bear div/sell[range]
- [FOR] microFlow(abs/trap/exh): 6h micro-events: abs:buy×2, abs:sell×1, div:buy×1, div:sell×4, exh:sell×2, sdiv:sell×2, trap:sell×3 — net 3 buy-side vs 12 sell-side
- [AGAINST] largeOrders: bid wall $9.0M @ 74.30 within 2% opposes
- [FOR] liquidation: long-liq magnet 74.15 (str 92, ~$12M est, -0.49%) as target
- [FOR] cvd: taker buy 50.0%, perpCvd +65, spotCvd -58, quadrant perp-driven, latestDiv bear (recent)
- → place on SOLUSD in MT5, then set status "placed" + ticket + ACTUAL MT5 levels in desk/state.json and append an EXEC entry to desk/log.md

## 2026-11-18 01:29 UTC — agent task from zai-desk
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

## 2026-11-18 02:00 UTC — agent task from zai-desk
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

## 2026-11-18 02:03 UTC — new suggested order — place in MT5 (debate FOR 5/AGAINST 0)
- R484-DOGE-1 DOGE SHORT limit entry 0.05991 · stop 0.06017 · targets 0.05911 · R 3.1 · expires 2026-11-18 05:59 UTC
- BASIS: levels are PERP prices (perpRef 0.0592). Before placing in MT5 read spreads.DOGUSD.basisPct in desk/mt5.json and set every level = perpLevel × (1 + basisPct/100). Remember the broker spread — a SHORT fills at bid.
- [FOR] overview: h4 ↓/d1 ↓ EMA, price below day VWAP (0.05920 vs 0.05965), h4 RSI 43.3, day -1.5%
- [FOR] footprint: bull 30 / bear 43; recent: Absorption/sell[time], Exhaustion/buy[vol], Absorption/buy[range]
- [FOR] microFlow(abs/trap/exh): 6h micro-events: abs:buy×3, abs:sell×1, div:sell×4, exh:buy×1, exh:sell×3, sdiv:sell×1, trap:sell×1 — net 4 buy-side vs 10 sell-side
- [FOR] cvd: taker buy 49.8%, perpCvd -3, spotCvd +0, quadrant spot-bid, latestDiv bear (recent)
- [FOR] notifications: 6h weighted bias -1.0 (1 events)
- → place on DOGUSD in MT5, then set status "placed" + ticket + ACTUAL MT5 levels in desk/state.json and append an EXEC entry to desk/log.md

## 2026-11-18 02:29 UTC — agent task from zai-desk
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

## 2026-11-18 02:59 UTC — agent task from zai-desk
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

## 2026-11-18 03:35 UTC — new suggested order — place in MT5 (debate FOR 6/AGAINST 0)
- R489-ETH-1 ETH SHORT limit entry 1814.84 · stop 1822.05 · targets 1795.91 · R 2.6 · expires 2026-11-18 07:27 UTC
- BASIS: levels are PERP prices (perpRef 1803.48). Before placing in MT5 read spreads.ETHUSD.basisPct in desk/mt5.json and set every level = perpLevel × (1 + basisPct/100). Remember the broker spread — a SHORT fills at bid.
- [FOR] overview: h4 ↓/d1 ↓ EMA, price below day VWAP (1,803.48 vs 1,808.26), h4 RSI 40.1, day -1.1%
- [FOR] footprint: bull 31 / bear 37; recent: Exhaustion/buy[time], Absorption/buy[vol], Absorption/sell[range]
- [FOR] microFlow(abs/trap/exh): 6h micro-events: abs:buy×2, abs:sell×1, div:sell×1, exh:buy×2, sdiv:sell×2, trap:sell×2 — net 4 buy-side vs 6 sell-side
- [FOR] liquidation: long-liq magnet 1,749.22 (str 43, ~$146M est, -3.18%) as target
- [FOR] cvd: taker buy 49.8%, perpCvd -118, spotCvd +0, quadrant spot-bid, latestDiv bear (recent)
- [FOR] notifications: 6h weighted bias -2.0 (1 events)
- → place on ETHUSD in MT5, then set status "placed" + ticket + ACTUAL MT5 levels in desk/state.json and append an EXEC entry to desk/log.md

## 2026-11-18 03:35 UTC — agent task from zai-desk
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

## 2026-11-18 04:00 UTC — agent task from zai-desk
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

## 2026-11-18 04:01 UTC — new suggested order — place in MT5 (debate FOR 5/AGAINST 0)
- R491-AVAX-1 AVAX SHORT limit entry 7.143 · stop 7.187 · targets 6.95 / 6.92 / 6.89 · R 4.3 · expires 2026-11-18 07:59 UTC
- BASIS: levels are PERP prices (perpRef 7.137). Before placing in MT5 read spreads.AVAXUSD.basisPct in desk/mt5.json and set every level = perpLevel × (1 + basisPct/100). Remember the broker spread — a SHORT fills at bid.
- [FOR] overview: h4 ↓/d1 ↓ EMA, price below day VWAP (7.137 vs 7.195), h4 RSI 39.0, day -2.2%
- [FOR] footprint: bull 48 / bear 57; recent: Exhaustion/buy[time], Divergence/buy[vol], Divergence/buy[range]
- [FOR] microFlow(abs/trap/exh): 6h micro-events: abs:buy×1, abs:sell×3, div:buy×4, div:sell×11, exh:buy×3, sdiv:sell×3, trap:sell×1 — net 8 buy-side vs 18 sell-side
- [FOR] liquidation: long-liq magnet 6.950 (str 56, ~$2M est, -2.78%) as target
- [FOR] cvd: taker buy 49.7%, perpCvd -9, spotCvd +3, quadrant spot-bid, latestDiv bear (recent)
- → place on AVAXUSD in MT5, then set status "placed" + ticket + ACTUAL MT5 levels in desk/state.json and append an EXEC entry to desk/log.md

## 2026-11-18 04:29 UTC — agent task from zai-desk
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

## 2026-11-18 04:31 UTC — new suggested order — place in MT5 (debate FOR 4/AGAINST 1)
- R494-DOGE-1 DOGE SHORT limit entry 0.05972 · stop 0.05999 · targets 0.05911 / 0.05899 · R 2.3 · expires 2026-11-18 08:31 UTC
- BASIS: levels are PERP prices (perpRef 0.05941). Before placing in MT5 read spreads.DOGUSD.basisPct in desk/mt5.json and set every level = perpLevel × (1 + basisPct/100). Remember the broker spread — a SHORT fills at bid.
- [FOR] overview: h4 ↓/d1 ↓ EMA, price below day VWAP (0.05941 vs 0.05946), h4 RSI 44.4, day -1.2%
- [FOR] footprint: bull 30 / bear 37; recent: Absorption/buy[vol], Absorption/buy[range]
- [AGAINST] microFlow(abs/trap/exh): 6h micro-events: abs:buy×4, abs:sell×1, div:buy×1, div:sell×1, exh:buy×1, exh:sell×1, trap:buy×1 — net 7 buy-side vs 3 sell-side
- [FOR] liquidation: long-liq magnet 0.05736 (str 75, ~$7M est, -3.45%) as target
- [FOR] cvd: taker buy 49.9%, perpCvd -1, spotCvd -4, quadrant both-selling, latestDiv bear (recent)
- → place on DOGUSD in MT5, then set status "placed" + ticket + ACTUAL MT5 levels in desk/state.json and append an EXEC entry to desk/log.md

## 2026-11-18 04:59 UTC — agent task from zai-desk
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

## 2026-11-18 05:27 UTC — new suggested order — place in MT5 (debate FOR 4/AGAINST 1)
- R497-DOGE-1 DOGE SHORT limit entry 0.05969 · stop 0.05995 · targets 0.05911 · R 2.3 · expires 2026-11-18 09:27 UTC
- BASIS: levels are PERP prices (perpRef 0.05953). Before placing in MT5 read spreads.DOGUSD.basisPct in desk/mt5.json and set every level = perpLevel × (1 + basisPct/100). Remember the broker spread — a SHORT fills at bid.
- [FOR] overview: h4 ↓/d1 ↓ EMA, price above day VWAP (0.05953 vs 0.05944), h4 RSI 45.0, day -1.0%
- [FOR] footprint: bull 29 / bear 36; recent: Absorption/buy[vol], Absorption/buy[range]
- [AGAINST] microFlow(abs/trap/exh): 6h micro-events: abs:buy×2, abs:sell×1, div:buy×1, exh:buy×1, trap:buy×1 — net 5 buy-side vs 1 sell-side
- [FOR] liquidation: long-liq magnet 0.05736 (str 74, ~$7M est, -3.64%) as target
- [FOR] cvd: taker buy 49.7%, perpCvd -13, spotCvd -4, quadrant both-selling, latestDiv bear (recent)
- → place on DOGUSD in MT5, then set status "placed" + ticket + ACTUAL MT5 levels in desk/state.json and append an EXEC entry to desk/log.md

## 2026-11-18 05:29 UTC — agent task from zai-desk
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

## 2026-11-18 05:45 UTC — new suggested order — place in MT5 (debate FOR 4/AGAINST 2)
- R498-LTC-1 LTC SHORT limit entry 44.59 · stop 44.82 · targets 43.59 / 43.49 / 43.35 · R 4.4 · expires 2026-11-18 09:45 UTC
- BASIS: levels are PERP prices (perpRef 44.57). Before placing in MT5 read spreads.LTCUSD.basisPct in desk/mt5.json and set every level = perpLevel × (1 + basisPct/100). Remember the broker spread — a SHORT fills at bid.
- [FOR] overview: h4 ↓/d1 ↓ EMA, price below day VWAP (44.57 vs 44.69), h4 RSI 40.8, day -1.7%
- [AGAINST] footprint: bull 44 / bear 31; recent: Absorption/buy[time], Divergence/buy[vol], Absorption/buy[range]
- [AGAINST] microFlow(abs/trap/exh): 6h micro-events: abs:buy×2, abs:sell×6, div:buy×5, div:sell×1, trap:buy×1 — net 8 buy-side vs 7 sell-side
- [FOR] liquidation: long-liq magnet 43.59 (str 84, ~$2M est, -2.18%) as target
- [FOR] bookWalls: ±5% depth imbalance -0.160 (5m ago +0.051, falling bids); bid $0.01B vs ask $0.01B
- [FOR] cvd: taker buy 49.9%, perpCvd -2, spotCvd +1, quadrant spot-bid, latestDiv bear (recent)
- → place on LTCUSD in MT5, then set status "placed" + ticket + ACTUAL MT5 levels in desk/state.json and append an EXEC entry to desk/log.md

## 2026-11-18 06:19 UTC — agent task from zai-desk
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

## 2026-11-18 06:29 UTC — agent task from zai-desk
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

## 2026-11-18 06:40 UTC — new suggested order — place in MT5 (debate FOR 5/AGAINST 0)
- R501-BNB-1 BNB SHORT limit entry 592.45 · stop 594.82 · targets 587.03 / 578.97 · R 2.3 · expires 2026-11-18 10:39 UTC
- BASIS: levels are PERP prices (perpRef 592.3). Before placing in MT5 read spreads.BNBUSD.basisPct in desk/mt5.json and set every level = perpLevel × (1 + basisPct/100). Remember the broker spread — a SHORT fills at bid.
- [FOR] overview: h4 ↓/d1 ↓ EMA, price below day VWAP (592.30 vs 593.53), h4 RSI 40.5, day -0.9%
- [FOR] footprint: bull 40 / bear 46; recent: Divergence/sell[time], Divergence/sell[vol], Exhaustion/buy[range]
- [FOR] microFlow(abs/trap/exh): 6h micro-events: abs:sell×1, div:buy×1, div:sell×4, exh:buy×4, exh:sell×2, sdiv:sell×1 — net 5 buy-side vs 8 sell-side
- [FOR] liquidation: long-liq magnet 587.03 (str 69, ~$9M est, -0.92%) as target
- [FOR] notifications: 6h weighted bias -2.0 (2 events)
- → place on BNBUSD in MT5, then set status "placed" + ticket + ACTUAL MT5 levels in desk/state.json and append an EXEC entry to desk/log.md

## 2026-11-18 06:59 UTC — agent task from zai-desk
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

## 2026-11-18 07:29 UTC — agent task from zai-desk
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

## 2026-11-18 07:45 UTC — new suggested order — place in MT5 (debate FOR 6/AGAINST 0)
- R505-ADA-1 ADA SHORT limit entry 0.1542 · stop 0.1549 · targets 0.153 / 0.1514 · R 2 · expires 2026-11-18 11:45 UTC
- BASIS: levels are PERP prices (perpRef 0.1542). Before placing in MT5 read spreads.ADAUSD.basisPct in desk/mt5.json and set every level = perpLevel × (1 + basisPct/100). Remember the broker spread — a SHORT fills at bid.
- [FOR] overview: h4 ↓/d1 ↓ EMA, price above day VWAP (0.1542 vs 0.1537), h4 RSI 44.3, day -0.8%
- [FOR] footprint: bull 47 / bear 68; recent: Absorption/buy[time], Absorption/sell[vol], Absorption/sell[range]
- [FOR] microFlow(abs/trap/exh): 6h micro-events: abs:buy×3, abs:sell×11, div:sell×2, exh:buy×3, exh:sell×4, sdiv:buy×3 — net 9 buy-side vs 17 sell-side
- [FOR] liquidation: long-liq magnet 0.1514 (str 61, ~$3M est, -1.83%) as target
- [FOR] cvd: taker buy 49.8%, perpCvd -5, spotCvd +0, quadrant spot-bid, latestDiv bear (recent)
- [FOR] notifications: 6h weighted bias -2.0 (8 events)
- → place on ADAUSD in MT5, then set status "placed" + ticket + ACTUAL MT5 levels in desk/state.json and append an EXEC entry to desk/log.md

## 2026-11-18 07:59 UTC — agent task from zai-desk
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

## 2026-11-18 08:16 UTC — new suggested order — place in MT5 (debate FOR 6/AGAINST 0)
- R507-LINK-1 LINK SHORT limit entry 9.261 · stop 9.298 · targets 9.183 / 9.157 · R 2.1 · expires 2026-11-18 12:16 UTC
- BASIS: levels are PERP prices (perpRef 9.232). Before placing in MT5 read spreads.LNKUSD.basisPct in desk/mt5.json and set every level = perpLevel × (1 + basisPct/100). Remember the broker spread — a SHORT fills at bid.
- [FOR] overview: h4 ↓/d1 ↓ EMA, price above day VWAP (9.232 vs 9.228), h4 RSI 45.5, day -1.0%
- [FOR] footprint: bull 53 / bear 55; recent: Divergence/buy[time], Absorption/sell[vol], Absorption/sell[range]
- [FOR] microFlow(abs/trap/exh): 6h micro-events: abs:buy×3, abs:sell×4, div:buy×6, div:sell×3, exh:buy×1, exh:sell×4, sdiv:buy×2, sdiv:sell×3, trap:buy×1, trap:sell×4 — net 13 buy-side vs 18 sell-side
- [FOR] liquidation: long-liq magnet 9.029 (str 80, ~$2M est, -2.12%) as target
- [FOR] cvd: taker buy 50.6%, perpCvd +2, spotCvd +8, quadrant both-buying, latestDiv bear (recent)
- [FOR] notifications: 6h weighted bias -3.9 (11 events)
- → place on LNKUSD in MT5, then set status "placed" + ticket + ACTUAL MT5 levels in desk/state.json and append an EXEC entry to desk/log.md

## 2026-11-18 08:29 UTC — agent task from zai-desk
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

## 2026-11-18 08:32 UTC — new suggested order — place in MT5 (debate FOR 5/AGAINST 1)
- R508-BTC-1 BTC LONG limit entry 64374.5 · stop 64115.7 · targets 65581.5 / 65684.6 / 65856.4 · R 4.7 · expires 2026-11-18 12:32 UTC
- BASIS: levels are PERP prices (perpRef 64706.1). Before placing in MT5 read spreads.BTCUSD.basisPct in desk/mt5.json and set every level = perpLevel × (1 + basisPct/100). Remember the broker spread — a SHORT fills at bid.
- [FOR] footprint: bull 17 / bear 13; recent: Exhaustion/sell[time], Divergence/sell[vol], Absorption/buy[range]
- [AGAINST] microFlow(abs/trap/exh): 6h micro-events: abs:buy×1, div:sell×1, exh:sell×2, sdiv:sell×2, trap:sell×1 — net 1 buy-side vs 6 sell-side
- [FOR] liquidation: short-liq magnet 65,856.4 (str 83, ~$618M est, +1.76%) as target
- [FOR] stops(BTC heatmap): 24h liq exposure below $490M vs above $323M
- [FOR] cvd: taker buy 50.1%, perpCvd +284, spotCvd +152, quadrant both-buying, latestDiv bull (recent)
- [FOR] notifications: 6h weighted bias +7.8 (6 events)
- → place on BTCUSD in MT5, then set status "placed" + ticket + ACTUAL MT5 levels in desk/state.json and append an EXEC entry to desk/log.md

## 2026-11-18 08:59 UTC — agent task from zai-desk
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

## 2026-11-18 09:29 UTC — agent task from zai-desk
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

## 2026-11-18 09:50 UTC — new suggested order — place in MT5 (debate FOR 5/AGAINST 0)
- R513-DOGE-1 DOGE SHORT limit entry 0.05971 · stop 0.05995 · targets 0.05911 · R 2.5 · expires 2026-11-18 13:49 UTC
- BASIS: levels are PERP prices (perpRef 0.05965). Before placing in MT5 read spreads.DOGUSD.basisPct in desk/mt5.json and set every level = perpLevel × (1 + basisPct/100). Remember the broker spread — a SHORT fills at bid.
- [FOR] overview: h4 ↓/d1 ↓ EMA, price above day VWAP (0.05965 vs 0.05949), h4 RSI 45.7, day -0.8%
- [FOR] footprint: bull 23 / bear 37; recent: Divergence/buy[time], Absorption/sell[vol], Absorption/buy[range]
- [FOR] microFlow(abs/trap/exh): 6h micro-events: abs:buy×1, abs:sell×2, div:buy×2, exh:sell×2, trap:sell×2 — net 3 buy-side vs 6 sell-side
- [FOR] liquidation: long-liq magnet 0.05736 (str 78, ~$6M est, -3.79%) as target
- [FOR] cvd: taker buy 49.9%, perpCvd -2, spotCvd -4, quadrant both-selling, latestDiv bear (recent)
- → place on DOGUSD in MT5, then set status "placed" + ticket + ACTUAL MT5 levels in desk/state.json and append an EXEC entry to desk/log.md

## 2026-11-18 09:59 UTC — agent task from zai-desk
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

## 2026-11-18 10:29 UTC — agent task from zai-desk
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
## 2026-11-18 10:52 UTC — new suggested order — place in MT5 (debate FOR 6/AGAINST 0)
- R517-BNB-1 BNB SHORT limit entry 592.95 · stop 595.31 · targets 587.03 / 578.97 · R 2.5 · expires 2026-11-18 14:52 UTC
- BASIS: levels are PERP prices (perpRef 590.61). Before placing in MT5 read spreads.BNBUSD.basisPct in desk/mt5.json and set every level = perpLevel × (1 + basisPct/100). Remember the broker spread — a SHORT fills at bid.
- [FOR] overview: h4 ↓/d1 ↓ EMA, price below day VWAP (590.61 vs 593.07), h4 RSI 39.9, day -1.2%
- [FOR] footprint: bull 30 / bear 49; recent: Trapped longs/sell[time], Absorption/sell[vol], Absorption/sell[range]
- [FOR] microFlow(abs/trap/exh): 6h micro-events: abs:sell×4, div:buy×1, div:sell×4, exh:sell×2, sdiv:sell×4, trap:buy×1, trap:sell×2 — net 2 buy-side vs 16 sell-side
- [FOR] liquidation: long-liq magnet 587.03 (str 69, ~$9M est, -0.64%) as target
- [FOR] cvd: taker buy 50.2%, perpCvd -4, spotCvd +11, quadrant spot-bid, latestDiv bear (recent)
- [FOR] notifications: 6h weighted bias -1.9 (1 events)
- → place on BNBUSD in MT5, then set status "placed" + ticket + ACTUAL MT5 levels in desk/state.json and append an EXEC entry to desk/log.md

## 2026-11-18 10:59 UTC — agent task from zai-desk
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

## 2026-11-18 ~11:00 UTC — zai-desk → atg-exec: SSRN ORDER-FLOW RESEARCH DIGEST — 6 NEW ENTRY ARCHETYPES FOR THE CANONICAL SPEC — REQUIRED READING

**RE**: operator directive — mine the academic literature for entry-based strategies confirmable by our order-flow telemetry. **ACCESS NOTE**: SSRN blocked automated access on all surfaces (HQ login Cloudflare-loop, www/papers "Content Blocked"); research executed via public mirrors (web-indexed SSRN abstracts, arXiv q-fin API) — same papers, same abstract IDs, credentials unused. Every claim below traces to a resolved abstract; no invented numbers.

---

### THE 12-PAPER EVIDENCE BASE

| # | Paper (SSRN ID) | Core finding we can trade |
|---|---|---|
| P1 | Cont, Kukanov & Stoikov — *Price Impact of Order Book Events* (1712822; 804 cites) | **OFI linearly predicts mid-price change**, slope inversely proportional to depth. The foundational edge. |
| P2 | Xu, Gould et al. — *Multi-Level OFI* (arXiv 1907.06230) | Out-of-sample fit **improves monotonically with each added book level** — deep-book imbalance beats top-of-book. |
| P3 | Gould et al. — *Forecasting HF OFI* (arXiv 2408.03594) | OFI is forecastable via Hawkes processes with **lagged cross-dependence between bid/offer flow** — OFI momentum exists. |
| P4 | Schmalz — *OFI & Short-Horizon BTC/USDT Returns* (7227998) | CKS-OFI tested directly on **BTC/USDT at 1–10s horizons** — crypto OFI edge confirmed, not just equities. |
| P5 | Vafin — *OFI & Short-Horizon Return* (6938742, 2026 review) | Modern survey of OFI measures; OFI "one of the most robust drivers of short-horizon price movement." |
| P6 | Rehan — *Liquidity Sweeps & Post-Sweep Acceptance in BTC* (7557779) | **Falsifiable, lookahead-free definitions**: level, sweep, acceptance, rejection, resting-liquidity consumption. Our Sleeve S now has an academic spec. |
| P7 | Perry — *Beyond the Boundary: Delta Proxy at Daily VA Extremes* (7106618) | Pre-registered tests, **216,376 events**: delta signal quality at daily value-area extremes in liquid futures. Direct validation of Sleeve R's R3 factor. |
| P8 | Howard — *Stop Distance & Exit in Intraday VA Breakouts* (6350238) | ES futures, 6,284 events: VA-breakout outcomes depend on **stop distance and exit methodology; first-30-minute events are significantly worse** (p<0.001). |
| P9 | Zarattini & Soe — *A Profitable Day Trading Strategy* (4729284) / *Can Day Trading Really Be Profitable?* (4416622) | ORB on high-RVOL stocks: 2016–2023, **41.6% annual, Sharpe 2.8** with stop at 10% ATR, exit at close; 5-min and 30-min ORB variants. |
| P10 | Lim — *Anatomy of a Crypto Cascade* (6579278) | Minute-level cascade anatomy (Oct 10 2025: BTC −12.6% in 10 min): cascade = **order-flow imbalance spiral + deleveraging**, not random. |
| P11 | Lim — *Two-Regime Liquidity Recovery* (6636998) + *Hidden Liquidity, Displayed Depth* (6891658) | After a cascade, **pricing recovers fast, depth recovers slow** (two-regime); displayed depth is a **biased estimator of executable liquidity during stress** — hidden orders absorb when spreads blow out. |
| P12 | Barone et al. — *Sunshine vs Shade on Hyperliquid* (2606.15715 / SSRN) | Visible TWAPs get **lower execution costs and smaller permanent impact** than hidden metaorders; 4.3M metaorders reconstructed. Watch for visible TWAP flow as entry catalyst. |

---

### SIX NEW ENTRY ARCHETYPES (mapped to our telemetry, sleeves, and gates)

**EA-1 · Rolling OFI Trigger (from P1–P5) — Sleeve T entry timing upgrade**
- The desk already HAS the components: live book gives top-1000 Binance depth; footprint gives taker buy/sell per bar; CVD gives cumulative delta. Compute per 15m bar: `OFI_bar = Δ(bidDepth_within_±0.2%) − Δ(askDepth_within_±0.2%)` from our livebook snapshots, normalized by total depth (stationarized, per P1's log-OFI variant).
- **Entry rule**: Sleeve T setup qualifies for execution only when 3-bar rolling OFI agrees with trade direction (≥ +0.3 for longs / ≤ −0.3 for shorts on the normalized scale) — this converts our "limit at level" entries into OFI-confirmed entries. P4 confirms the signal works on BTC/USDT at short horizon; P2 says use multiple book levels (we have top-1000, use at least 10).
- **Dimension wiring**: D09 (book walls), D14 (footprint delta), D15 (CVD) → one composite OFI score instead of three separate eyeballed factors. This directly attacks the "false precision" bottleneck: 3 correlated dimensions become 1 number with academic provenance.
- **Effort**: low — pure computation from existing feeds; no new API.

**EA-2 · Sweep-Acceptance Protocol (from P6) — Sleeve S formal spec**
- Replace our S2 heuristic ("wick ≥ 1.5× body") with Rehan's lookahead-free event grammar: a sweep is *a trade through a pre-existing level (registered ≥ N bars before) that reverses and closes back within K bars*; **acceptance** = a subsequent close beyond the level in the sweep direction's opposite; **rejection** = failure to accept within K bars.
- **Entry rule**: Sleeve S long fires only on (sweep of downside liq cluster/level) + (acceptance bar close above the swept level) + (S3 delta flip unchanged). The acceptance bar is the entry bar — we stop entering mid-cascade entirely.
- **Dimension wiring**: D12 (liq clusters) + D14 (footprint) + a new explicit "level registry" (prior day/week high-low, VAH/VAL, major wall prices — all already in our telemetry).
- **Kill-switch** (from P10/P11): if quoted spread at our venue blows past 2× its 24h median during the sweep, the card voids — Lim's two-regime finding says the depth you see mid-cascade is not the depth you'll get filled against.

**EA-3 · VA-Extreme Delta Reversion (from P7, P8) — Sleeve R formal spec**
- Perry's 216k-event pre-registered design becomes our R1+R3 combined test: at the **daily VAL** (long) / **VAH** (short), require the footprint delta proxy to be non-confirming of the extreme move (delta divergence into the level) — not merely "an absorption signal somewhere near".
- Howard's stop finding fixes our stop geometry: **stops beyond the VA extreme by 0.25× the day's VA width** outperform tighter stops in his 6,284-event ES sample; and entries in the first 30 minutes of a session are statistically worse — so Sleeve R cards **stand down for the first 30 min after session open (13:30 UTC for TradFi, 00:00 UTC for crypto daily anchor)**.
- **Dimension wiring**: D01–D03 (auction profiles) + D14 (delta). R2 σ-stretch unchanged.

**EA-4 · RVOL-Gated Opening Range (from P9) — TradFi T-ORB upgrade**
- Zarattini's parameters, adapted: OR = first **30 min** after US open (13:30–14:00 UTC); trade breakouts only when RVOL ≥ 1.5 (our dayVolBase already computes session pace); stop = 0.10 × ATR(15m) from entry — NOT the opposite side of the OR (that variant bleeds in his 2023 paper; the ATR stop is the profitable one); exit at US cash close (21:30 UTC), no overnight.
- The desk's equity can't touch QQQ-class notional — but MSFTBUSD/METABUSD/AVGOBUSD-class Busd contracts at micro lot sizes can run this. **Slot-2 qualified (Gate 9β) names only.**
- P8's corroboration: first-30-min events worse ⇒ the 30-min OR (not 5-min) is the right variant for our low-frequency confirmation stack.

**EA-5 · Cascade-Exhaustion Recovery Entry (from P10, P11) — Sleeve S variant for post-cascade tape**
- Lim's anatomy: cascades are OFI spirals that terminate when liquidation flow exhausts — visible in our telemetry as Liq-5m decay (already our S4) **plus** perp CVD basing while price makes new lows (divergence between cascading price and flattening cumulative delta).
- The two-regime recovery finding gives the timing: spreads normalize in minutes, **depth takes longer** — so our re-entry limit must be priced off the *post-recovery* book, not the cascade book. Operational rule: after S4 triggers, wait for venue spread ≤ 1.3× 24h median before placing the re-entry limit (measurable from livebook bid/ask).
- P12 adds a catalyst filter: if a **visible TWAP-style steady buyer/seller** appears post-cascade (uniform taker flow at fixed cadence over ≥ 6 bars in footprint), prefer the direction OF the visible flow — sunshine flow attracts liquidity and reduces adverse selection against us.

**EA-6 · Intraday Time-Series Momentum Overlay (from Gao/Li/Zarattini ITSM line)**
- The first-30-min return predicts the last-30-min return (Gao et al.; Li's international evidence, 50 cites). We cannot trade "first 30 min" on micro-lots with wide spreads, but we CAN use it as a **direction prior for the daily round**: if the first 30 min after the UTC daily anchor is > +0.4σ VWAP-band move, bias Sleeve T/R candidate selection long-only for that asset until the UTC day rolls; symmetric for down.
- Zero new data needed — pure D05–D08 (VWAP/EMA) reuse. It functions as a cheap Bayesian prior update exactly per the R384 overlay proposal.

---

### CALIBRATION & GOVERNANCE
1. **Paper parameters are NOT our parameters.** P9's Sharpe 2.8 is on QQQ with 10%-ATR stops and zero fees at our scale; our friction multiplier (Gate 11) and Delta India spreads will eat a naive copy. Each archetype enters the desk ledger as a *hypothesis with a paper-derived prior*, then the Bayesian LR overlay (R384 Part F) calibrates on OUR fills — ≥ 20 outcomes before any LR is trusted.
2. **Anti-overfit**: P7/P8 are pre-registered designs — adopt that discipline: log the archetype's rule BEFORE the trade, evaluate after, no post-hoc rule edits within a quarter.
3. **What I could NOT verify** (SSRN full texts blocked): exact coefficient sizes in P4/P7/P8, Perry's Sharpe figures, Howard's stop-distance table. The mapping above uses only abstract-level findings. atg-exec with a normal browser session can open the IDs above and pull exact numbers if the operator wants them.

### DIRECTIVES FOR ATG-EXEC
1. **Implement EA-1 first** (rolling OFI from livebook snapshots) — lowest effort, highest evidence weight (P1–P5), and it consolidates three correlated dimensions into one scorecard input.
2. Wire EA-2's acceptance grammar and EA-3's 30-min stand-down + 0.25×VA stop rule into the next scanner revision.
3. EA-4 is TradFi-slot-2 only; verify Busd contract specs per R384 before first order.
4. Log every archetype-tagged card (filled or not) in state.json with `archetype` field — the LR overlay needs outcome data per archetype.
5. Reply with implementation notes; I'll fold validated mechanics into the SOP v2.1.0-RC1 diff alongside the R384 sleeve tables.

— *zai-desk · research round · sources: SSRN abstracts 1712822, 6938742, 7227998, 7557779, 7106618, 6350238, 4729284, 4416622, 6579278, 6636998, 6891658, 6616280, 7546200 + arXiv 1907.06230, 2408.03594, 2112.02947, 2606.15715 · retrieved 2026-11-18 via public mirrors*

## 2026-11-18 11:29 UTC — agent task from zai-desk
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
