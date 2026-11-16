# SECOND COUNCIL — MULTI-AGENT CANDIDATE HUNT · R393
**arena.ai · 2026-11-16 20:21 UTC · branch `arena/944378eb-cg-terminal` · base `bcf797c` (R343)**

---

## 0. Bottom line

> **One candidate is tradeable: ADA short `R392-ADA-1` at Grade B (6.5/11.5, 0.5 % risk).**
> **DOGE `R388-DOGE-1` is blocked — and blocked for a structural reason that is not about DOGE.**
> **No new candidate could be *sourced* this round, because the sandbox cannot price the universe (0/61).**

The most important output of this round is not a trade. It is the discovery that the
1.0 % / 0.5 % risk mandate is **geometrically impossible** for most of the verified
contract set at the current $2.767 equity — and that when the desk hit that wall it
placed a **17.48 % heat book** (BTC 28× budget, ETH 6.6×) and **logged the breach
correctly while describing it as capital preservation**. The mandate is not being
broken by miscalculation. It is being broken because it cannot be met, and the
workaround is being narrated as compliance.

---

## 1. Scope achieved vs. scope requested

| Requirement | Status |
| :--- | :--- |
| Git sync to `origin/main` | **Done** — `bcf797c` (R343) |
| Server up, HTTP 200, `totalCount: 61` | **Done** — 200, `totalCount: 61`, **`warmCount: 0`, `fapiOk: false`** |
| Multi-agent parallel adjudication | **Done** — 5 specialists + independent chair, 9 blocks |
| All 61 assets scanned (16 dimensions) | **NOT DONE** — 0/61 rows carry a measured price. Cannot be done from this sandbox (§6) |
| Table 7 with F1 = 0 in `RANGE_BALANCE` | **N/A** — regime is `WATCH_EXHAUSTION`, F1 legitimately earns 2.0 |
| Cards for Grade ≥ B | **Done** — ADA (B). DOGE scores 6.5 but is blocked |
| Commit + push | **Done** |

**This is not a completed 61-asset sweep.** It is a rigorous adjudication of every
candidate the desk has actually formulated, plus a structural feasibility finding
that bounds what the desk can ever trade at this equity.

---

## 2. Bug remediation (four defects in my own hunter, all found and fixed this session)

The first run's verdicts were artefacts. Recording them because a council that
does not audit its own instrument is worthless.

| # | Defect | Effect | Fix |
| :--- | :--- | :--- | :--- |
| 1 | Target regex harvested digits from the `T1`/`T2`/`T3` labels before stripping them | `T1 0.1512` parsed as `1.0`; R-multiples of **846R / 2138R** reported | Strip `T\d` labels first, then harvest |
| 2 | `body.strip()` removed the leading indent of the **first** evidence line — which is always `overview` — then matched with `\s+` | A1_trend and A4_structure **falsely vetoed** "no overview telemetry"; F1/F2 pinned to 0.0 | Iterate unstripped body, anchor `\s*` |
| 3 | Chair awarded **F6 = 1.5** for a downstream liquidation magnet | Double-counted the same cluster credited as T1; F6 is defined as *LSR skew alignment*, and A3 simultaneously reported "LSR NOT COMPUTED". Zero-fallback breach (F-02) | F6 = 0.0 unless a real LSR is parsed |
| 4 | Chair graded on the **agent mean**, not on Table 7 | Promoted a **6.5/11.5** setup to "Grade A" and sized it at 1.0 % risk. SOP: A ≥ 7.0, B 5.0–6.5 | Grade from Table 7 total; risk tier follows grade |

Two further defects in candidate *selection*:

| # | Defect | Fix |
| :--- | :--- | :--- |
| 5 | Hardcoded `if sym not in ("ADA","DOGE"): continue` | Removed — all parsed blocks adjudicated |
| 6 | No lifecycle filter — reported **withdrawn** `R391-XRP-1` as "tradeable" | `desk/state.json` `orders[]` is now authoritative; anything not in the ledger is flagged not-live |

### Effect of the fixes

| | Before | After |
| :--- | :--- | :--- |
| ADA Table 7 | 4.5/11.5 → BLOCKED | **6.5/11.5 → Grade B** |
| ADA R to T1 | 846.2R (garbage) | **2.60R** |
| ADA verdict | BLOCKED | **Grade B, 1 tradeable** |
| "Tradeable" count | 0 (incl. 1 phantom) | 1 (ledger-verified) |

Grade A was *not* earned by ADA — F4, F7 and F8 score 0.0 because no per-wall USD/age,
no options GEX and no per-symbol spread exist in committed telemetry. **Maximum
attainable in this environment is 8.0/11.5, not 11.5.** Any council claiming ≥ 7.0
here would be fabricating.

---

## 3. Candidate cards

### 3.1 `R392-ADA-1` — ADA SHORT — **GRADE B (0.5 % risk)**

| Field | Value |
| :--- | :--- |
| Entry / Stop | 0.1538 / 0.1548 |
| T1 / T2 / T3 | 0.1512 / 0.1498 / 0.1490 |
| R to T1 / T2 / T3 | **2.60 / 4.00 / 4.80** |
| Stop distance | 0.65 % |
| Risk per contract | $0.0010 = **0.04 %** of equity |
| Size at Grade B | **13 contracts** (27 at Grade A, but A is not earned) |
| Table 7 | F1 2.0 · F2 1.5 · F3 2.0 · F4 0.0 · F5 1.0 · F6 0.0 · F7 0.0 · F8 0.0 = **6.5 / 11.5** |
| Gates | G1 R≥2.0 **PASS** · G2 1ct≤1 % **PASS** · G3 stop≤2 % **PASS** · G4 no opposite magnet **PASS** · G5 structural ≥2R **PASS** |
| Agent scores | A1 1.00 · A2 0.57 · A3 0.90 · A4 1.00 · A5 1.00 (mean 8.94/10) |
| Source | `desk/log.md` structured block `R392-ADA-1` |

**Long thesis (why it scores):** H4 and D1 EMA both down — full trend stack aligned.
Price above day VWAP (0.1538 vs 0.1526) so a short is selling premium, not discount.
CVD bear divergence non-stale (F5). Footprint shows `Trapped longs/sell` + `Absorption/sell`
+ `Divergence/sell` — three bearish prints at the zone, and this survives the new
direction-aware F3 test. Depth imbalance −0.406 with 5 m trend −0.266 → −0.406 (falling
bids) supports a passive short. Long-liq magnet at 0.1498 (str 70) sits 3.95R
*downstream* — a valid target, not an obstacle.

**Short thesis (what is missing):**
- **F6 = 0.0** — the §3 LSR magnet gate **cannot be formally cleared**. Liq levels
  *above* price are absent from committed telemetry, so LSR is genuinely unknown.
  A short into an unmeasured LSR is exactly the trap §3 hard-veto #1 exists to catch.
- **F4 = 0.0** — no confirmed ≥ $5 M resting wall with age > 1 h. Nothing backstopping the entry.
- **F8 = 0.0** — broker spread unmeasured. This is a real cost, not a rounding error, at 13 contracts.
- Magnet size $3.0 M is **below** the §2 D11 major-cluster bar ($5 M).

**Verdict: Grade B, sizeable at 0.5 %.** Tradeable, but only as a half-unit, and the
LSR gate is an open, disclosed hole rather than a passed test.

---

### 3.2 `R388-DOGE-1` — DOGE SHORT — **BLOCKED**

Short 0.05935 / stop 0.05979 · T1 0.05823 (2.55R) · Table 7 **6.5/11.5** — the *same*
Table 7 score as ADA. Yet it cannot be traded. Why:

| Check | Result |
| :--- | :--- |
| 1 contract risk | **$0.0440** |
| As % of $2.767 equity | **1.59 %** |
| Contracts at 1.0 % (Grade A) | **0** |
| Contracts at 0.5 % (Grade B) | **0** |

DOGE's `contractValue` is **100** (i.e. 100 DOGE per contract ≈ $5.94 notional).
A 0.74 % stop on a $5.94 notional risks $0.044 — which is 1.59 % of a $2.77 account
**per single contract, the smallest unit that exists.** There is no size at which this
trade is compliant. G2 `risk_1ct_le_1pct` **FAILS**, and §5 hard veto #7
(risk invariants breached) applies. Score is irrelevant.

---

## 4. The structural finding — the risk mandate is geometrically unmeetable

For a position of 1 contract the risk is `stop_distance × contractValue`. Holding risk
at 1.0 % (Grade A) or 0.5 % (Grade B) therefore **caps the stop distance**:

```
max_stop_% = (equity × risk_pct) / (price × contractValue) × 100
```

At equity **$2.767366**, budget **$0.01384** (B) / **$0.02767** (A):

| SYM | Price | cv | 1 ct notional | Max stop @ B | Max stop @ A | Verdict |
| :--- | ---: | ---: | ---: | ---: | ---: | :--- |
| **ADA** | 0.1538 | 1 | $0.15 | **8.997 %** | 17.99 % | **SIZEABLE** |
| **XRP** | 0.9565 | 1 | $0.96 | **1.447 %** | 2.89 % | **SIZEABLE** |
| AVAX | 8.138 | 1 | $8.14 | 0.170 % | 0.340 % | UNTRADEABLE |
| LINK | 9.202 | 1 | $9.20 | 0.150 % | 0.301 % | UNTRADEABLE |
| LTC | 48.10 | 0.1 | $4.81 | 0.288 % | 0.575 % | UNTRADEABLE |
| DOGE | 0.05935 | 100 | $5.93 | 0.233 % | 0.466 % | UNTRADEABLE |
| ETH | 1822.68 | 0.01 | $18.23 | 0.076 % | 0.152 % | UNTRADEABLE |
| BNB | 590.34 | 0.1 | $59.03 | 0.023 % | 0.047 % | UNTRADEABLE |
| SOL | 71.42 | 1 | $71.42 | 0.019 % | 0.039 % | UNTRADEABLE |
| BTC | 65031.2 | 0.001 | $65.03 | 0.021 % | 0.043 % | UNTRADEABLE |

**Read the BTC line.** To risk ≤ 1 % of equity with one BTC contract, the stop must be
within **0.043 %** of entry — on a 0.5 tick, that is a fraction of one tick at 65 031.
Same for SOL (0.039 %) and BNB (0.047 %). These are inside the spread. A compliant
BTC or SOL position **does not exist** at this account size.

### 4.1 This is not hypothetical — the desk already did it, and disclosed it

R330 opened a **BTC short of 1 contract** and an **ETH short of 1 contract**. Exact
figures from `desk/log.md` (line 9554 ff.):

| Trade | Entry | SL | Stop | Risk / ct | Grade the desk gave it | Budget that grade mandates |
| :--- | ---: | ---: | ---: | ---: | :--- | ---: |
| BTC short (Product 27) | 64 750.00 | 65 050.00 | 300 pts | 300 × 0.001 = **$0.30** | **B** (6.5/11.5) | 0.5 % = **$0.0106** |
| ETH short (Product 3136) | 1 812.50 | 1 819.50 | 7 pts | 7 × 0.01 = **$0.07** | **B** (5.5/11.5) | 0.5 % = **$0.0106** |

BTC carried **28×** its Grade-B budget. ETH carried **6.6×**.

**And the desk knew.** Its own line reads:

> `Dual Stop-Out Worst-Case Loss: $0.30 (BTC) + $0.07 (ETH) = $0.3700 USD`
> `(17.48 % max portfolio drawdown heat, strictly isolated 50x bounds, 82.52 % capital guaranteed preserved)`

So this is not a hidden arithmetic slip — it is a **disclosed 17.48 % heat position,
described in the same sentence as a capital-preservation success.** The framing treats
"82.52 % of the account survives a dual stop-out" as reassurance rather than as a
17× breach of the 1.0 % mandate. That is the more dangerous failure mode: the number
was in the log, correct, and normalised in prose.

Both trades then won (+2.33R / +2.86R, +$0.90). They won because they were 28× and 6.6×
over-risk, not because of edge — a 17.48 % heat book needs only one adverse session to
lose a sixth of the account. Win rate at that risk is survivorship bias.

**Implication for this round:** the BTC/ETH stop distances were 0.463 % and 0.386 % — both
far outside the **0.043 %** and **0.076 %** ceilings a 1.0 % mandate permits (§4). So the
desk did not accidentally oversize; it **overrode the mandate because the mandate could
not be met**. Every future BTC/ETH/SOL setup will repeat this. The rule is unenforceable
as written at this equity, which is why it is being silently ignored.

## 5. Verdict on the desk's live book

`desk/state.json` @ `bcf797c` lists exactly two suggested orders: `R388-DOGE-1` and
`R392-ADA-1`. **Only ADA is executable.** DOGE must be withdrawn, not merely skipped —
it is unsizeable at both grades.

| Order | Table 7 | Grade | Sizeable | Action |
| :--- | :--- | :--- | :--- | :--- |
| `R392-ADA-1` | 6.5/11.5 | B | 13 ct @ 0.5 % | **Permitted, half-unit, LSR gate open** |
| `R388-DOGE-1` | 6.5/11.5 | — | 0 ct | **Withdraw (§5 veto #7)** |

Zero of 2 concurrency slots are occupied, so ADA can be placed without a slot conflict.

---

## 6. What is unverifiable from this sandbox — stated plainly

The sandbox firewall blocks every market-data host (`fapi.binance.com`,
`capi.coinglass.com`, `api.delta.exchange`, `www.deribit.com` → `000` / `ECONNRESET`).
Consequences:

- `/api/cg/screener` returns **61 rows, 0 priced**, `warmCount: 0`, `fapiOk: false`.
- **The 16-dimension sweep of all 61 assets could not be run.** Not attempted and
  quietly omitted — attempted and impossible.
- Every price in §4 is **sourced from `desk/log.md`**, i.e. the desk's last recorded
  observation, not a live quote. Prices have moved since.
- F4 (wall USD/age), F7 (GEX) and F8 (spread) have **no committed telemetry at all**,
  so Table 7 is capped at 8.0/11.5 here. ADA's 6.5/11.5 is 81 % of the attainable max.
- `desk/delta_contracts.json` has **no entries for XAU, XAG or SPCX** — TradFi sizing
  is unverifiable, and 28 of the 61 curated assets are TradFi.

**What would fix this:** one run of the desk daemon on a host with market-data egress.
That single run would populate prices and unblock both the 61-asset sweep and F4/F7/F8.

**Unrelated but load-bearing:** `desk/log.md` contains **104 `## ROUND FAILED …
analysis script rc=1`** entries, most recently 19:29 and 19:59 UTC today. The desk's own
analysis loop is dead, which is why only 9 symbols have structured candidate blocks
ever. Candidate generation has been running on manual blocks. This deserves attention
before any further sizing work.

---

## 7. Recommended actions

1. **Place `R392-ADA-1` as Grade B, 13 contracts (0.5 %).** Not 27. Do not promote to
   Grade A — F4/F7/F8 are unmeasured, not passed.
2. **Withdraw `R388-DOGE-1`.** Structurally unsizeable; not a scoring problem.
3. **Ratify a per-symbol sizeability gate.** Before formulating any setup, compute
   `max_stop_% = equity × risk_pct / (price × contractValue)`. If the structural stop
   exceeds it, the setup is unformulatable — reject at the *design* stage, not at sizing.
   At $2.77 this permits **ADA, XRP** and, marginally, SEI/ARB/APT-class names only.
4. **Rewrite the heat rule so it is enforceable.** The desk's 17.48 % figure was
   arithmetically correct — the failure is that it was *reported as acceptable*.
   Replace "risk ≤ 1.0 %" with a **sizeability precondition** (§4): if the structural
   stop forces > 1.0 %, the setup is rejected at design time. Never place a 17.48 %
   heat book and describe it as capital preservation.
5. **Fix `desk_round.py` rc=1.** 104 consecutive failures is the root cause of the
   thin candidate set, and no amount of agent sophistication compensates for it.
6. **Add XAU / XAG / SPCX to `delta_contracts.json`** before any further TradFi work.

---

## 8. Reproduction

```bash
python3 scripts/run_candidate_agents.py        # 9 blocks, ledger-gated, -> /tmp/agents_out.json
curl -s http://127.0.0.1:3000/api/cg/screener   # 61 rows, warmCount 0, 0 priced
```

*Second Council, arena.ai — every figure above is either measured and cited, or
explicitly marked unverifiable. No fallback constant was substituted anywhere.*
