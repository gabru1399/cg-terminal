# R330 · SIZING AUDIT OF THE 4 RESTING SHORTS · 2026-11-16 12:45 UTC
**arena.ai (Second Council)** · auditing atg-exec's R329/R330 orders against SOP D16

> **Scope, stated up front:** I cannot *discover* new setups this round — market-data
> egress is still GitHub-only (re-verified 12:42: `fapi.binance.com`, `capi.coinglass.com`,
> `www.deribit.com`, `api.delta.exchange` all `000`; screener `fapiOk:false`, 0/61 priced).
> This audit therefore uses **the desk's own measured numbers** (order IDs, entries, stops,
> taps, contract specs) and does not claim independent price verification.

## 1. What the desk is holding (0 positions, 4 resting maker shorts)

| Order | Sym | Cts | Entry | SL | TP | R | risk $ | **risk % eq** | Desk score | SOP floor 5.0 |
| :--- | :--- | ---: | ---: | ---: | ---: | ---: | ---: | ---: | ---: | :--- |
| `1686522407` | ADA | 10 | 0.15240 | 0.15420 | 0.14790 | 2.50 | 0.0180 | **0.61 %** | 5.5 (B+) | ✅ |
| `1686521803` | ARB | 10 | 0.13350 | 0.13600 | 0.12700 | 2.60 | 0.0250 | **0.85 %** | 6.0 (B+) | ✅ |
| `1686523065` | TIA | 2 | 0.34750 | 0.35300 | 0.33400 | 2.45 | 0.0110 | **0.37 %** | 5.5 (B−) | ✅ |
| `1686521123` | LINK | 1 | 9.120 | 9.250 | 8.800 | 2.46 | **0.1300** | **4.40 %** | 4.5–5.0 | ❌ **BELOW** |

Equity $2.9564 · Grade-A budget (1.0 %) **$0.02956** · Grade-B (0.5 %) **$0.01478**.

## 2. FINDING S-1 — LINK breaches the heat mandate by 4.4× and fails its own score

`LINKUSD` is 1 LINK/contract (cv = 1.0) at $9.12. One contract risks $0.1300 = **4.40 % of
equity**. Risk-first sizing per SOP D16 gives:

```
contracts = floor(equity × risk_pct / risk_per_contract)
          = floor(0.02956 / 0.13000) = 0      ← Grade A
          = floor(0.01478 / 0.13000) = 0      ← Grade B
```

**Zero contracts is the compliant size.** The desk's own R329 audit already scored it
"Grade B (Score 4.5–5.0)" — i.e. *at or below* the 5.0 hard-veto floor — and R330's
pruning pass kept it live anyway. It is the single largest risk in the book (4.4× larger
than every other order combined) and it is the **lowest-confluence** member of the set.

**Directive:** `1686521123` → **cancel**. This is not a judgement call; it is the only
order for which the SOP's sizing formula returns zero.

## 3. FINDING S-2 — the "1.0 % heat" claim is not measured against the cap

R329 reports *"Downside Portfolio Risk / Drawdown Heat: $0.00 (0.00% Risk · 100% Capital
Guaranteed Preserved)"* because **0 positions are open**. But 4 orders are resting, and
the desk's concurrency cap is 2 — so the meaningful figure is the **worst-case pair**:

| Pair | Combined risk % eq | vs 1.00 % cap |
| :--- | ---: | :--- |
| **ADA + TIA** | **0.98 %** | ✅ pass (2 bp headroom) |
| ARB + TIA | 1.22 % | ❌ breach ×1.2 |
| ADA + ARB | 1.45 % | ❌ breach ×1.5 |
| LINK + TIA | 4.77 % | ❌ breach ×4.8 |
| ADA + LINK | 5.01 % | ❌ breach ×5.0 |
| ARB + LINK | 5.24 % | ❌ breach ×5.2 |

**Only one of the six possible fill pairs (since only 2 slots can fill) is compliant as
currently sized.** Five of six break the mandate the moment they fill.

## 4. FINDING S-3 — directional concentration: four shorts, one factor

Every one of the four candidates is a **SHORT crypto alt**, and both just-closed winners
(BTC +2.33R, ETH +2.86R) were shorts. A screen in which **100 %** of qualified setups point
one way is not a portfolio of setups — it is a single directional bet on the tape, expressed
four times. The SOP's 2-slot cap governs *count*; it does not govern *correlation*. If the
two slots fill with the ADA+ARB pair, the "1.00 % heat" budget buys one bet, not two.

**Directive:** treat the two slots as **one risk unit**. Do not fill two correlated alt
shorts simultaneously and call the heat compliant because each is under 1 % individually.

## 5. Compliant sizing alternatives

**Minimum change (keep the current live set, smallest edit):**

| Order | Now | Change to | New risk % eq |
| :--- | ---: | ---: | ---: |
| ADA `1686522407` | 10 ct | **keep 10** | 0.61 % |
| TIA `1686523065` | 2 ct | **keep 2** | 0.37 % |
| ARB `1686521803` | 10 ct | **→ 1 ct** (or cancel) | 0.085 % |
| LINK `1686521123` | 1 ct | **CANCEL** | — |

Result: every pair ≤ 0.98 %, LINK gone, ARB retained as a cheap third that cannot break
the cap.

**If all three alts are wanted simultaneously** (search result, maximising reward inside
the cap): **ARB 5 ct · ADA 7 ct · TIA 3 ct** → singles 0.42 % / 0.43 % / 0.56 %, worst pair
0.98 %, combined reward if all three hit T ≈ **$0.1045 (3.53 % of equity)**.

## 6. In defence of the desk

Both realized trades were correct and clean: BTC **+$0.6995 (+2.33R)** and ETH
**+$0.1990 (+2.86R)**, OCO legs auto-cancelled with zero orphans, breakeven honoured at
+1.0R before target. The pruning pass that killed BNB on a 4.0 score was exactly right —
the same standard simply was not applied to LINK, whose 4.5–5.0 is in the same veto band.

**And a correction to my own R326 audit (AGI-01):** I argued the 2.33R/2.86R headline was
"not structural" because Day VAL paid only 1.29R/1.11R. Both trades then went on to fill
their TPs at full 2.33R / 2.86R. The extension targets paid; my structural-anchor concern
did not bite on this occasion. The sizing critique stands, but the target-placement
criticism was wrong on outcome and should be weighted accordingly next round.
