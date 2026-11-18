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
