# WAKE — active tasks and directives for atg-exec (ephemeral beacon)

## ACTIVE DESK DIRECTIVES
- **VENUE & ACCOUNT**: Delta Exchange India (`india_prod` | Account `26902927`).
- **CANONICAL SOP**: `desk/TRADE_FORMULATION_MANUAL.md` calibrated by `desk/SWARM_MASTER_PROMPT.md` and `.gemini/rules/SWARM_EXECUTION.md`.
- **SHARED ACCOUNT ISOLATION (P5-01b)**: Two separate chats run on this Delta account. Track orders strictly via internal order numbers. Never touch or cancel orders from the external chat (`FIB4H_*`, `SOLVUSD`, `TACUSD`).
- **EXECUTION CADENCE**: Dynamic 1200s timer (`schedule(DurationSeconds=1200)`). Zero static cron jobs.
- **CONCURRENCY & RISK**: Max 2 concurrent crypto positions. Max 1.0% portfolio heat. Isolated margin, maker post-only, mark-price stops.
- **HISTORICAL LOGS**: Archived to `desk/inbox/archive/WAKE_ARCHIVE_20261115.md`.

## 2026-11-15 19:00 UTC — active round directive
- Execute canonical 360° autonomous round per `desk/SWARM_MASTER_PROMPT.md`:
  1. Ingest 30-asset closed-candle screener (`http://127.0.0.1:3000/api/cg/screener`).
  2. Compute zero-fallback Table 7 (Factor 1 = 0.0 in `RANGE_BALANCE`).
  3. Enforce Liquidation Magnet Gate (LSR >= 2.5:1 bans passive entries).
  4. Socratic gates & DECIDE dossiers for qualified setups (>= 5.0 pts).
  5. Check running positions for +1.0R Breakeven and 8-bar time stop.
  6. Re-arm dynamic 1200s timer.
