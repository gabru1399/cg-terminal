---
description: Autonomous trading execution enforcement — forces sequential SWARM_MASTER_PROMPT execution on every activation
trigger: always
---

# MANDATORY SWARM EXECUTION PROTOCOL (AUTO-INJECTED WORKSPACE RULE)

This rule fires on EVERY activation. It cannot be skipped, summarized, or overridden.

## ACTIVATION DETECTION

If the current prompt contains ANY of: "AUTONOMOUS DELTA EXCHANGE", "SWARM_MASTER_PROMPT", "RECURSIVE ENGINE ROUND", "SOP v1.4.0", or this activation was triggered by a 1200s dynamic timer — then the **Full Execution Protocol** below is MANDATORY.

## FULL EXECUTION PROTOCOL

### 1. READ FIRST, ALWAYS
- **FIRST tool call**: `read_file("C:\\Users\\SIGMA\\Documents\\cg-terminal\\desk\\SWARM_MASTER_PROMPT.md")` — read the FULL file, every line.
- **SECOND tool call**: `read_file("C:\\Users\\SIGMA\\Documents\\cg-terminal\\desk\\TRADE_FORMULATION_MANUAL.md", StartLine=1, EndLine=120)`.
- Do NOT begin any analysis, reporting, or tool calls until both files are loaded.

### 2. SEQUENTIAL PHASE EXECUTION (ZERO SKIPPING)
- Execute Phases 0 through 7 **in strict sequential order**.
- Each phase's EXIT CRITERION must be verified before the next phase begins.
- **Phase 0**: Every step (0.1–0.8) MUST result in an actual tool call. A table row saying "PASS" without a corresponding tool call is a fabrication.
- **Phase 1**: MUST call the screener endpoint or run `node scripts/dump_matrix.mjs`. Output ALL 30 rows uncompressed.
- **Phase 7**: MUST call `schedule(DurationSeconds=1200, ...)` with ZERO `CronExpression` and ZERO `IsDaemon=true`.

### 3. TABLE 7 SCORING INVARIANTS (ANTI-FABRICATION GATE)
- **Every score MUST be itemized**: show each of the 8 factors (Directional Trend, Auction/VWAP, Footprint Signal, Whale Wall, CVD Divergence, Liq Magnet, Options GEX, Spread Drag) with the live data source and points awarded.
- **Factor 1 (Directional Trend) = 0.0 in `RANGE_BALANCE`** — this is non-negotiable. The EMA slope is flat in balance; trend points are structurally invalid.
- **Maximum achievable score in `RANGE_BALANCE` = 9.5** (11.5 minus 2.0 for Factor 1). If you compute > 9.5, you have a bug. HALT.
- **Maximum achievable for non-BTC/ETH assets = 10.5** (Factor 7 Options GEX = 0.0 / n/a). In RANGE_BALANCE: max = 8.5.
- **NEVER output a composite score without showing the 8-factor breakdown first.**

### 4. TIMER IS NON-OPTIONAL
- The **LAST tool call** of every execution round MUST be `schedule(DurationSeconds=1200, Prompt=<LAUNCHER>)`.
- NEVER use `CronExpression`. NEVER use `IsDaemon=true`. One-shot dynamic timer ONLY.
- If you reach the end of your response without having called `schedule()`, you have violated this rule. Go back and call it.

### 5. ANTI-SUMMARY BIAS
- Do NOT output a summary table with "PASS/FAIL" results until the underlying tool calls have been made and their responses processed.
- Tool call FIRST → Process response → THEN write the result row.
- If you catch yourself writing Phase 1's matrix before having called the screener API: STOP. Call the API first.

### 6. LIQUIDATION MAGNET GATE (DIMENSION 12)
- If Liquidation Skew Ratio (LSR) >= 2.5:1 in the Risk Zone [Entry → SL + 0.5 ATR]: **BAN all passive entries (S2/S3)**.
- This gate outranks every other confluence. A 9-point setup of a banned archetype is still NO TRADE.
- NEVER place a sell limit order into a dominant short-liquidation pool above price.

### 7. DATA HONESTY
- Every number quoted must come from a tool response in THIS session.
- If a tool call fails, score that factor 0.0 and label it `n/a` — never guess.
- Liquidation and whale figures are Coinglass estimates — always label them as such.

### 8. SHARED ACCOUNT ISOLATION (EXTERNAL ALGO PROTECTION)
- Another algorithm operates on the same Delta Exchange account (e.g., placing orders with client_order_id like `FIB4H_*`, or positions on symbols like `TACUSD`, `SOLVUSD`).
- **You are ONLY responsible for orders and positions punched by your own desk.**
- **STRICTLY FORBIDDEN**: Never cancel, modify, close, or interfere with orders or positions belonging to the external algorithm.
- Always check available liquid margin to ensure your own orders do not exceed free cash reserves.
