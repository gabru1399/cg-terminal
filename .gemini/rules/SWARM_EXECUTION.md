---
description: Autonomous trading execution enforcement — forces sequential CANONICAL_MASTER_SPECIFICATION execution on every activation
trigger: always
---

# MANDATORY SWARM EXECUTION PROTOCOL (AUTO-INJECTED WORKSPACE RULE)

**USER DIRECTIVE (MANDATORY BY DEFAULT):**
Strict line-by-line adherence to `desk/CANONICAL_MASTER_SPECIFICATION.md` (which unifies `SWARM_MASTER_PROMPT.md` and `TRADE_FORMULATION_MANUAL.md` into SOP v2.0.0) is BINDING AND MANDATORY BY DEFAULT AT ALL TIMES.

## 1. UNIVERSE COVERAGE: 61 CURATED ASSETS (ZERO GAPS)
- **30 Crypto USDT-M Perps**: BTC, ETH, BNB, SOL, XRP, ADA, DOGE, TRX, LINK, LTC, AVAX, DOT, NEAR, UNI, ATOM, XLM, ETC, FIL, ICP, HBAR, APT, ARB, OP, SUI, SEI, INJ, TIA, VET, 1000PEPE, 1000SHIB.
- **28 TradFi USDT-M Perps**: XAU, NVDA, SNDK, SOXL, SPCX, GOOGL, MU, SKHY, XAG, CL, INTC, CRCL, MSTR, QQQ, ANTHROPIC, AAPL, TSLA, DRAM, KORU, META, NBIS, MSFT, AMZN, AMD, COIN, NFLX, AVGO, TSM.
- **3 Classic Indices**: SPX500, UKO, NDX100.
- All 61 assets are scanned every cycle without omission.

## 2. LINE-BY-LINE EXECUTION DISCIPLINE (PHASES -1 THROUGH 7)
On every activation and execution turn:
- **Phase -1 (Structural Self-Audit)**: Verify entire prompt read, tool-first commitment, and single-timer constraint.
- **Phase 0 (Pre-Flight SOP & Tool Ingestion)**: Ingest `desk/CANONICAL_MASTER_SPECIFICATION.md`, WAKE inbox, user profile, memory, wallet balances, positions, open orders, and adversarial subagent.
- **Phase 1 (Universe Screening & Tab 7 Routing)**: Fetch 61-asset screener telemetry, route archetypes via Tab 7 regime, output uncompressed screening matrix.
- **Phase 2 (16-Dimension Telemetry Extraction)**: Complete the mandatory 16-point Telemetry Audit Sheet (Section 8) for in-scope assets.
- **Phase 3 (8 Socratic Gates & 10 Pitfall Inquests)**: Calibrated gates (G1-G8, including Gate 7 Dollar Risk Invariant $\le 1.0\%$ and Gate 8 Active Cascade Climax Gate).
- **Phase 4 (6-Step DECIDE Dossier)**: Direction, Entry, Confluence, Invalidation, Drive (T1/T2/T3, R >= 1.5R, T1 >= 2.0R), Execution.
- **Phase 5 (CLOB Execution & Concurrency Hygiene)**: Maker limit orders (`post_only=true`, `mark_price` triggers, isolated leverage). Max 2 positions. Enforce First-Two-Fills circuit (P5-06), +1.0R Breakeven (P5-04), and 8-bar time stop (P5-05).
- **Phase 6 (AGI Meta-Learning Debrief & Persistence)**: Structured post-mortem appended to `desk/log.md`, `desk/state.json` synced, committed and pushed to git.
- **Phase 7 (Dynamic Timer Re-Arm)**: Mandatory LAST CALL: `schedule(DurationSeconds=1200, Prompt=...)`. ZERO static cron, ZERO daemon.

## 3. TABLE 7 SCORING INVARIANTS (ANTI-FABRICATION GATE)
- Every score MUST be itemized showing all 8 factors.
- **Factor 1 (Directional Trend) = 0.0 in `RANGE_BALANCE`** — non-negotiable.
- Score < 5.0 pts = HARD VETO. 100% Cash Defense.

## 4. SHARED ACCOUNT ISOLATION (DELTA INDIA `26902927`)
- Two separate chats run on this Delta account.
- Track trades STRICTLY via internal exchange Order IDs / Ticket Numbers recorded in `desk/state.json`.
- NEVER cancel, modify, or report external algo orders (`FIB4H_*`, `SOLVUSD`, `TACUSD`).

## 5. RECURSIVE TIMER CONTINUITY & MANDATORY FORMAT
- Autonomous propagation is single-turn dynamic 1200s timer (`schedule(DurationSeconds=1200)`).
- Never terminate an execution turn without re-arming the 1200s dynamic wake timer.
- **Mandatory Timer Instruction & Prompt Format:**
  `Timer: 20m, Prompt: /goal /executing-plans /plan /brainstorming Autonomous Delta Exchange Trade Execution & Recursive Self-Improving Engine Round R<n>. Audit all 61 Curated Assets and find high potential high confluence trading setup strictly using @[c:\Users\SIGMA\Documents\cg-terminal\desk\CANONICAL_MASTER_SPECIFICATION.md]  , monitor live standing maker limit orders on Delta Exchange India (APTUSD @ $0.45700, ADAUSD @ $0.15240, ARBUSD @ $0.13350, LINKUSD @ $9.120, TIAUSD @ $0.34750), enforce First-Two-Fills circuit, +1.0R breakeven invariant and 8-bar time stop, audit margin and liquidity, and re-arm dynamic 1200s recursion.`

## 6. CONTINUOUS PLANNING & BRAINSTORMING MANDATE (/plan & /brainstorming)
- Every autonomous prompt, task formulation, and dynamic wakeup must explicitly carry `/goal /executing-plans /plan /brainstorming`.
- **`/plan`**: Enforces structured pre-flight technical design, verification, and artifact documentation before placing or altering exchange orders.
- **`/brainstorming`**: Enforces Socratic exploration of alternative entry models (e.g., session VWAP/POC pullback fades vs. liquidation sweep retests) to prevent entry tightness and execution apathy.
