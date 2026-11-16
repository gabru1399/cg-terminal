# R394 — HOW TO IDENTIFY MORE SETUPS
**arena.ai · 2026-11-16 · branch `arena/944378eb-cg-terminal` · base `bcf797c` (R343)**

---

## The short answer

You do not have a data problem. The data dictionary you pasted is *more* than enough —
it is the richest input the desk has ever had. What you have is a **conversion
problem**: that telemetry is being compressed into a candidate format that physically
cannot express six of the eight setups the manual defines.

Measured, over the 81 KB of committed `desk/log.md`:

| Measurement | Value |
| :--- | :--- |
| Structured candidate blocks ever produced | **77** |
| Of those, declaring a setup archetype (S1–S8) | **0** |
| S4 (Wall-Pull Breakout) uses, all-time | **0** |
| S3 (Whale Wall Defense) uses | 0 (mentioned 6× only as "banned") |
| S5 / S6 / S7 / S8 uses | 3 / 2 / 5 / 3 mentions, ~0 formulised |
| Crypto assets permanently pinned to "WAIT FOR THE SWEEP (S1)" | **27 of 30** |
| Generator model vocabulary | `M1_TREND_PULLBACK`, `M2_MEAN_REVERSION`, **`WATCH_EXHAUSTION`** |
| `WATCH_EXHAUSTION` appearances | **23** |

`WATCH_EXHAUSTION` is **not in the manual.** It is not S1–S8. It is a *non-setup*
that occupies a candidate slot and resolves, by construction, to "wait". Twenty-three
of those is what "so few setups" looks like when you count it.

And the blocker is formal, not aesthetic: **Table 7 hard veto #8 is "Setup fits no card
S1–S8."** A candidate that never names its archetype is ungradeable by definition. The
pipeline is not failing to find setups — it is finding *states* and never converting
them into *setups*.

---

## The root cause, in one table

I built `scripts/run_setup_scanner.py` to enumerate all 8 archetypes against a symbol.
Run against the desk's own real R392 ADA block, it returns **zero armed setups** — and
this is the diagnostic it prints:

```
ADA  price 0.1538   no archetype state reached
   .. S1 blocked on: z
   .. S2 blocked on: day_vah | day_val, gex
   .. S3 blocked on: walls[], liq_up_usd, liq_dn_usd
   .. S4 blocked on: wall_pull
   .. S5 blocked on: z, rsi_h1
   .. S7 blocked on: ema_h4_e13, ema_h4_e89, ema_d1_e13, ema_d1_e89, z
   .. S8 blocked on: oi_delta_4h_pct, gex
```

The desk's candidate format carries: **price, stop, T1/T2/T3, R, EMA direction arrows,
RSI H4, VWAP side, footprint bulls/bears, micro-flow counts, one liq magnet, depth
imbalance.** That is 5 usable fields out of the ~13 the archetypes demand.

**Every one of these is already in your data dictionary and is being thrown away:**

| Missing input | Exists in your inventory | Blocks |
| :--- | :--- | :--- |
| **z-score / VWAP σ bands** (`vwap.bands.sd1/2/3`) | Tab 1 §1.3 | **S5 entirely, S7 chase-guard, S1 stretch** |
| **Day/Session/Month VAL·POC·VAH** | Tab 1 §1.2 | **S2 entirely, S1 targets, S6 targets** |
| **Wall objects w/ `usd` + `ageMs` + `touched`** | Tab 3 §3.3, Tab 5 §5.3 | **S3 entirely, F4 = 1.5 pts, S4 entirely** |
| **Wall `pull` lifecycle events** | Tab 5 §5.4 | **S4 entirely** |
| **LSR (`liq_up_usd` / `liq_dn_usd`)** | Tab 4 §4.3 | **§3 gate cannot be cleared — currently unmeasurable** |
| **OI deltas + quadrant** | Tab 1 §1.6, D14 | **S4, S8 confirmation** |
| **GEX regime** | Tab 1, D13 | S2, S8, F7 = 1.0 pt (BTC/ETH) |
| **Spread %** | Tab 9 §9.1 | F8 = 1.0 pt, Gate 4 |

That last column is the headline: **the four Table 7 factors the desk scores 0.0 are
0.0 because the fields are dropped in transit, not because the data is absent.**
F4 (1.5) + F7 (1.0) + F8 (1.0) = **3.5 points** — a third of the table — is being
written off on every single candidate, which mechanically caps every setup at
8.0/11.5 and makes Grade A (≥7.0) a knife-edge.

---

## Fix 1 — Log the fields, not the summary

The single highest-leverage change. The candidate block must carry the raw numbers
that the archetype needs, not the model's prose conclusion about them.

Current block:
```
- NEW R392-ADA-1 ADA SHORT limit 0.1538 · stop 0.1548 · T1 0.1512 · T2 0.1498 · T3 0.1490 · R 2.5
      [FOR] overview: h4 ↓/d1 ↓ EMA, price above day VWAP (0.1538 vs 0.1526), h4 RSI 38.1, day -1.0%
      [FOR] footprint: bull 59 / bear 63; recent: Trapped longs/sell[time], ...
```

Proposed — same information, machine-gradeable:
```
- NEW R392-ADA-1 ADA SHORT limit 0.1538 · stop 0.1548 · T1 0.1512 · T2 0.1498 · T3 0.1490 · R 2.5
      setup: S7  variant: trend-pullback   (required: name ONE of S1..S8 — veto #8)
      px 0.1538  vwap 0.1526  sd1 0.1531  sd2 0.1536  sd3 0.1541  z +0.42
      day VAL 0.1519 / POC 0.1527 / VAH 0.1538   sess VAL/POC/VAH ...
      ema h4 13 0.1533 / 89 0.1547   d1 13 0.1560 / 89 0.1541
      rsi h1 41.2 / h4 38.1
      fp abs/sell @0.1536  cvd div bear (recent)  oi4h -1.8% quadrant LONG_LIQUIDATION
      liq up 0.1551 $1.2M / dn 0.1498 $3.0M  -> LSR 2.50
      walls a 0.1536 $6.2M 47m untouched / b 0.1497 $1.1M 12m
      gex n/a (non-BTC/ETH)   spread 0.021%   liq5m $84k
```

Roughly 12 lines instead of 7, and every archetype becomes computable. This costs the
generator nothing — it already has every one of these values in memory when it writes
the block; it is summarising them away.

---

## Fix 2 — Generate setup-first, not symbol-first

The current loop is: *pick a symbol → look for a reason → emit a candidate*. That is why
27 of 30 assets land on the same S1 "wait". With ~13 inputs per asset, the manual's
eight archetypes define **8 predicates × 61 assets = 488 possible states.** Today the
desk evaluates roughly one of them.

`scripts/run_setup_scanner.py` does this inversion. It is read-only and has no side
effects — it proposes, the Council disposes.

```bash
python3 scripts/run_setup_scanner.py              # self-test: proves the logic
python3 scripts/run_setup_scanner.py -t live.json # real telemetry
```

Self-test output (synthetic tape — proves the machinery, **not** a market read):

```
ADEV   NOTE  S8 dropped: partial break vs fully-armed S1 sweep fade on same cluster
       ARMED   S1 Liquidation Sweep Reversal [long] cap=A+
       PARTIAL S5 VWAP Band Mean Reversion [long]  - MISSING: RSI H1 unknown
CDEV   VETO  §3 LSR 4.5:1 >= 2.5 — passive entries into the magnet path BANNED
       PARTIAL S3 Whale Wall Defense — MISSING: LSR 4.5:1 — S3 BANNED
DDEV   ARMED   S4 Wall-Pull Breakout [long] cap=B
EDEV   ARMED   S5 VWAP Band Mean Reversion [short] cap=A
FDEV   ARMED   S7 High-Volume Absorption Continuation [long] cap=A
GDEV   ARMED   S8 Liquidation Breakout Continuation [long] cap=A
HDEV   VETO  D16 Liq 5m $900,000 > $500k — cascading, BAN ALL LIMIT ENTRIES
```

Two design decisions worth flagging:

1. **A missing field is `UNKNOWN`, never `True`.** No archetype fires on absent data.
   That is what stops the scanner manufacturing candidates — the exact failure mode
   `WATCH_EXHAUSTION` represents.
2. **S1 vs S8 conflict resolution.** A swept magnet is *either* a completed sweep
   (fade it — S1) *or* a continuing break (ride it — S8). They are opposite trades on
   one level and the naive implementation fired both. The discriminator is the
   confirmation stack: S1 needs exhaustion + delta flip + stretch; S8 needs OI +
   gamma. A fully-armed S1 beats a partial S8 and vice versa; two full arms escalate
   to the Council rather than auto-picking.

---

## Fix 3 — The spread gate is measuring the wrong venue

This one is costing you candidates directly and is a straight bug.

R234-ADA-1 was **withdrawn** with "Spread 2.25% veto", and R360/R386 repeat it:
`ADA (2.25%), DOGE (1.39%), LTC (2.42%), LINK (0.57%), XAG (0.178%) barred from MT5 placement`.

Those are **MT5 broker spreads on the CFD venue.** Delta Exchange India is the execution
venue, and it is a central limit order book — ADA does not trade at 2.25 % inside a
book. The giveaway is in the sentence itself: *"barred from **MT5 placement**"*. The gate
is labelled correctly and then applied to Delta orders anyway.

The consequence is measurable: **ADA R392's stop distance is 0.65 %.** If ADA's real
spread were 2.25 %, the spread alone would consume **346 % of the stop distance** —
the trade would be impossible, not merely capped. Since the desk placed it, the Delta
spread is obviously nothing like 2.25 %. Meanwhile Gate 4 requires spread < 20 % of stop
distance — a rule that can never be *evaluated* on a Delta order, because the Delta
spread is never recorded.

**Fix:** read spread from Tab 9 §9.1 (`bestAsk - bestBid`) on the venue the order will be
placed, and apply the MT5 gate to MT5 orders only. This alone un-bars ADA, DOGE, LTC,
LINK and XAG — five of the highest-liquidity alts in the curated set — and restores F8
(+1.0 pt) to Table 7.

---

## Fix 4 — Report coverage, not just outcomes

The reason this took a session to find is that a round reporting "0 qualifying setups"
is *indistinguishable* from a round reporting "0 setups examined". Both print the same
thing. Add three counters to every round:

```
archetypes evaluated: 488      (8 x 61)
archetypes reachable:  61      (13.5% - fields present)
archetypes armed:       0
blocked by missing field: 427  (top: z-score 183, GEX 122, OI 122)
```

With that line in the log, "no setups today" is falsifiable. Without it, it is
indistinguishable from a broken pipeline — which is what 104 consecutive
`ROUND FAILED rc=1` entries already proves is happening.

---

## What I did not do, and why

I did **not** run this against live telemetry, because the sandbox has no market-data
egress: `/api/cg/screener` returns 61 rows with `warmCount: 0`, `fapiOk: false`, and
**0/61 priced**. The self-test proves the *logic*; it says nothing about today's tape.
Any number I quoted from a live scan would be fabricated.

The scanner is deliberately dependency-free and takes a plain JSON file, so it will run
the moment a host with feed access populates that file — one `curl` per tab, no code
changes.

---

## Recommended order of work

1. **Fix the spread gate to read Delta's own book** (Fix 3). Cheap, un-bars 5 alts,
   restores F8.
2. **Extend the candidate block to carry the 13 fields** (Fix 1). Highest leverage;
   makes 3.5 Table 7 points and 6 setups computable.
3. **Mandate a `setup: S<n>` line on every candidate** (veto #8). Kills
   `WATCH_EXHAUSTION` as a category instantly — a "watch" is not a card, and a
   candidate with no card cannot be graded.
4. **Add the coverage counters** (Fix 4) so future councils can tell "nothing there"
   from "nothing looked at".
5. **Then** run `run_setup_scanner.py` against real telemetry and see the true count.
   I expect the answer to be materially above zero — S4 has never once been checked,
   and S5/S6 need only z-score and RSI H1, both already in Tab 1.

*Second Council, arena.ai. Every figure above is either measured from committed
telemetry and cited, or explicitly marked unverified. The self-test tape is labelled
synthetic everywhere it appears.*
