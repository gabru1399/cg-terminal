## SECTION 5. THE 16 TELEMETRY DATA DIMENSIONS (DATA CONTRACT)

[DIM-00] [MANDATORY] [DATA_CONTRACT]: Every candidate setup MUST explicitly evaluate, extract, and log all 16 dimensions before order generation:

| Dimension | Telemetry Field | Source Endpoint | Invariant Rule & Threshold |
| :--- | :--- | :--- | :--- |
| **D01** | **Spot/Broker Basis Offset** | `/api/cg/market` & Delta `get_ticker` | `basisPct = (Price_Delta - Price_Perp) / Price_Perp * 100`. Must be $|basisPct| \le 0.5\%$. |
| **D02** | **Auction Profile (VAL/POC/VAH)** | `/api/cg/narrative` `market.auction` | Fade Value Area extremes back to POC (S2); target VAL/VAH on continuations (S7). Mid-value entries score 0.0. |
| **D03** | **Day VWAP & Z-Score Bands** | `/api/cg/narrative` `market.vwap` | Price > VWAP = Premium; Price < VWAP = Discount. $|z| \ge 2.0\sigma$ **BANS** continuation entries in direction of extension. |
| **D04** | **Trend Momentum Alignment** | `/api/cg/narrative` `market.ema` | H4 & D1 EMA 13×89 alignment. 3-TF stack alignment required for Grade A continuation setups. |
| **D05** | **Multi-TF RSI(14) Divergence** | `/api/cg/narrative` `market.rsi` | H1/H4 RSI > 70 or < 30 warns of exhaustion. Regular divergence across $\ge 2$ timeframes confirms reversals. |
| **D06** | **Footprint Bar Delta & POC** | `/api/cg/fp` | Bar delta %, taker buy/sell USD, intra-bar POC acceptance. High volume + small progress = absorption. |
| **D07** | **Discrete Footprint Signals** | `/api/cg/signals` | Signals: `abs`, `div`, `sdiv`, `trap`, `exh` printed inside entry zone within $\le 8\text{h}$ recency. |
| **D08** | **Cumulative Volume Delta** | `/api/cg/cvd` | Perp vs Spot CVD. Spot buying while Perp selling = smart money absorption $\implies$ **HARD VETO on shorts**. |
| **D09** | **Book Walls & Lifecycle** | `/api/cg/bookwalls` | Confirmed resting walls (Tier 1 $\ge \$5\text{M}$, Tier 2 $\ge \$1.0\text{M}$, Tier 3 $\ge \$250\text{k}-\$500\text{k}$, Tier 4 $\ge \$50\text{k}-\$100\text{k}$, or $\ge 20\%$ depth), age $> 1\text{h}$. Opposing wall within 1.5R = **HARD VETO**. |
| **D10** | **Large Resting Orders (LTO)** | `/api/cg/lto` | Resting institutional blocks ($\ge \$500\text{k}$ BTC/ETH, $\ge \$100\text{k}$ large alts, $\ge \$25\text{k}$ micro alts). Queue priority placement 0.05% in front. |
| **D11** | **Liquidation Clusters & Stopmap**| `/api/cg/liqlevels` & `/api/cg/stopmap` | Multi-venue clusters are sweep magnets. Take profit INTO clusters; never hold through them. |
| **D12** | **Liquidation Magnet Gate (LSR)**| `/api/cg/liqlevels` | If $\text{LSR} \ge 2.5:1$, **BAN ALL PASSIVE ENTRIES INTO MAGNET PATH**. Switch strictly to S1 sweep reversal. |
| **D13** | **Options GEX & Gamma Flip** | `/api/cg/options` | Positive Gamma favors mean reversion (S2/S5); Negative Gamma favors expansion (S1/S8) — BTC/ETH only. |
| **D14** | **4H Open Interest Quadrants** | `/api/cg/oi` | Falling Price + Falling OI = Long Liquidation (do not short tail end); Rising Price + Falling OI = Short Covering. |
| **D15** | **Annualized Funding APR** | `/api/cg/market` | Negative funding when shorting = Crowded Trade / Short Squeeze Hazard. |
| **D16** | **5m Liquidation Pace (`Liq 5m`)** | Screener `Liq 5m` | If `Liq 5m > $500k`, active cascade raging $\implies$ **BAN PASSIVE LIMIT ENTRIES**. Wait for exhaustion wick. |

---

## SECTION 6. THE 9 STANDARDIZED PLAYBOOK STRATEGY ARCHETYPES (S1 TO S9)

[ARCH-00] [MANDATORY] [PLAYBOOK_CANON]: These are the ONLY permitted trade archetypes. Every opportunity that fits no archetype is strictly NO TRADE:

| Code | Setup Name | Best Regime | Entry Trigger | Stop Invalidation | Target |
| :--- | :--- | :--- | :--- | :--- | :--- |
| **S1** | **Liquidation Sweep Reversal** | Over-extended / high LSR ($\ge 2.5:1$) | 15m close back inside value after stops wiped + delta flip | Beyond sweep wick high/low (+ 0.3–0.5 ATR buffer) | Opposite Day VAL/VAH & POC (40/40/20) |
| **S2** | **Value Area Edge Fade** | Range Balance / High Gamma | Touch of Day VAH (short) / VAL (long) with footprint divergence | Beyond Day VWAP $\pm 2\sigma$ band | Day POC (mean reversion) |
| **S3** | **Whale Wall Defense / Front-Run** | Trend Pullback (LSR < 2.0) | 0.05%–0.1% in front of confirmed wall (Tiered / $\ge 20\%$ depth) | Behind whale wall + 0.5 ATR buffer | Next opposing wall / POC |
| **S4** | **Wall-Pull Breakout** | Momentum Expansion | Breakout candle through pulled wall with rising OI | Retest of broken level | +2σ or +3σ VWAP band |
| **S5** | **VWAP Band Mean Reversion** | Extreme Extension ($|z| \ge 2.0\sigma$) | Touch of Day VWAP $\pm 3\sigma$ with RSI divergence & proof | 0.5 ATR beyond $\pm 3\sigma$ band | Day VWAP mean |
| **S6** | **Trapped Traders Fade** | False Breakout | High volume cluster at extreme with failed progress | Beyond trapped candle wick | POC / Value Area midline |
| **S7** | **High-Volume Absorption Continuation** | Strong Trend (M1) | Retest of absorbed high-volume node in trend direction | Other side of absorption bar | Same-direction liquidation pool |
| **S8** | **Liquidation Breakout Continuation** | Negative Gamma Expansion | Clean 15m close beyond major liquidation shelf with rising volume | Inside edge of broken shelf | Next liquidity pocket |
| **S9** | **Dynamic Trend Rejection Candle** | Macro Trend Pullback (Stage 2/4) | 15m/1H spike into EMA 89 or EMA 233 with rejection wick $\ge 2:1$ & volume surge | Beyond tip of rejection wick + 0.1% buffer | Value Area boundary & 100% liquidation pool |

[ARCH-S1] [INVARIANT] [S1_DETAIL]: When LSR >= 2.5:1, wait for cluster to be wiped, wait for exhaustion print (`exh`), wait for taker delta flip, enter on 15m confirmation close back inside value. Grade A+ eligible.
[ARCH-S2] [INVARIANT] [S2_DETAIL]: Fade value boundaries back to POC; Grade cap: Grade B unless absorption cluster >= $5M; banned when LSR >= 2.5:1.
[ARCH-S3] [INVARIANT] [S3_DETAIL]: Front-run large resting walls only when LSR < 2.0:1; size tiered by liquidity ($5M BTC/ETH, $1M SOL/large, $250k-$500k alts/equities); Grade cap: Grade B (0.5% risk) always.
[ARCH-S4] [INVARIANT] [S4_DETAIL]: Enter on retest of pulled wall level with expanding OI; Grade B on break, Grade A on retest.
[ARCH-S5] [INVARIANT] [S5_DETAIL]: Requires stretch ($|z| \ge 2.0\sigma$), crowding (RSI >70/<30, funding extreme), and footprint reversal proof (`abs`, `div`, `sdiv`, `trap`, `exh`). Stretch without proof is WATCH, not trade.
[ARCH-S6] [INVARIANT] [S6_DETAIL]: Fade trapped breakout volume; stop placed beyond trapped volume wick.
[ARCH-S7] [INVARIANT] [S7_DETAIL]: M1 trend pullback; 3-tier limit ladder: 40% at POC, 40% at trend-side +-1σ VWAP, 20% at absorption high/low; stop beyond absorption bar.
[ARCH-S8] [INVARIANT] [S8_DETAIL]: Continuation through broken liquidation shelf; stop at inside edge of shelf.
[ARCH-S9] [INVARIANT] [S9_DETAIL]: Spikes into declining EMA 89 or 233 with rejection wick >= 2.0x body on heavy volume (>= 1.5x 20-MA) with footprint exhaustion/trap; enter on 50% wick retest or candle close; stop tightly beyond rejection wick in cold zone. Grade A+ eligible.

---

## SECTION 7. RETAIL SETUP ⟷ ORDER-FLOW CONFIRMATION ENGINE

[RET-00] [AXIOM] [ORDER_FLOW_REALITY]: Retail chart patterns treat price as continuous geometric drawings; price moves ONLY when market orders consume resting limit depth; institutions exploit retail chart patterns to harvest liquidity.

[RET-R01] [SETUP] [SR_BOUNCE]:
  - Retail Concept: "Price bounced 3 times; buy 4th touch with market order."
  - Microstructure Reality: Each touch consumes resting limit bids; by 4th touch bids are exhausted; retail stops clustered 10-20 bps below line.
  - Telemetry Checklist: Tab 5 Confirmed resting bid wall + Tab 2 `abs`/`div` on test bar + Tab 6 Spot CVD flat/rising + Tab 1 POC alignment.
  - Data-Driven Entry: Post-Only limit +0.05% in front of whale wall (S3) or at absorption zone (S2); stop 0.5% below absorption low.

[RET-R02] [SETUP] [SR_BREAKOUT]:
  - Retail Concept: "Price broke resistance with green candle; buy market on breakout."
  - Microstructure Reality: 75% of breakouts in perpetual markets are fakeouts triggering retail buy market orders into institutional limit sells.
  - Telemetry Checklist: Tab 3/5 No opposing ask wall above + Tab 5 `wallPullEvent` opens air pocket + Tab 1/4 Expanding OI (+1% to +5% on 4H) + Tab 2 Trap fade check.
  - Data-Driven Entry: Limit order on retest of broken Day VAH / resistance (S8/S4), or fade trap back to Day POC (S6).

[RET-R03] [SETUP] [DOUBLE_BOTTOM]:
  - Retail Concept: "Price printed W double bottom; enter long when price breaks neckline."
  - Microstructure Reality: Waiting for neckline sacrifices 50%-70% of R-multiple (< 1.2R).
  - Telemetry Checklist: Tab 2 Bar delta positive (`div`/`sdiv`) + Tab 6 Spot CVD higher low + Tab 1 $|z| \le -2.0\sigma$ or $-3.0\sigma$ VWAP + Tab 4 Sweep of stops below first low.
  - Data-Driven Entry: Enter at close of 15m divergence candle at Tap 2 (S1); stop 0.3% below lowest sweep wick; EV 3.5R-5.0R.

[RET-R04] [SETUP] [TRENDLINE_PULLBACK]:
  - Retail Concept: "Price pulled back to diagonal trendline / bull flag; buy."
  - Microstructure Reality: Diagonal trendlines have zero exchange matching engine reality; price reacts to horizontal volume profiles and VWAP bands.
  - Telemetry Checklist: Tab 1 Day/Session POC or Day VWAP -1σ band + Tab 1 H4/D1 EMA stacks + Tab 2 Footprint seller exhaustion (`exh`) + Tab 5 Bid depth loading.
  - Data-Driven Entry: 3-tier ladder (40% POC, 40% -1σ VWAP, 20% absorption low); stop beyond -2σ VWAP (S7).

[RET-R05] [SETUP] [RSI_OVERSOLD]:
  - Retail Concept: "RSI < 25 oversold; buy the dip."
  - Microstructure Reality: In strong cascades, RSI stays < 30 indefinitely while price drops another 15%.
  - Telemetry Checklist: Tab 4/8 Rolling `Liq 5m < $500k` (cascade halted) + Tab 1 Touch of -2σ/-3σ VWAP + Tab 1 Funding APR heavily negative (< -20%) + Tab 2 Footprint `abs`/`trap`/`sdiv`.
  - Data-Driven Entry: Limit at confirmation bar close; stop 0.5x ATR beyond extreme wick; target Day VWAP mean (S5).

[RET-R06] [SETUP] [MA_CROSSOVER]:
  - Retail Concept: "9 EMA crossed 21 EMA bullishly; buy next bar."
  - Microstructure Reality: Moving averages lag; price is at resistance; whipsaws 80% of time in chop.
  - Telemetry Checklist: Tab 7 Explicit `TREND_UP` regime (veto in `RANGE_BALANCE`) + Tab 1 $|z| < 1.0\sigma$ (no chasing) + Tab 3/5 Zero opposing wall within 1.5R.
  - Data-Driven Entry: Never buy crossover bar; wait for pullback to EMA13 / Day VWAP mean; stop below EMA89 (S7).

[RET-R07] [SETUP] [SMC_LIQUIDITY_SWEEP]:
  - Retail Concept: "Asian high swept, 1m CHoCH printed; short FVG."
  - Microstructure Reality: 1m market structure breaks are random noise; real sweeps require multi-million dollar liquidation clusters.
  - Telemetry Checklist: Tab 4 Cluster swept >= $5M (Tier 1/2) or >= $500k (Tier 3/4), pre-sweep LSR >= 2.5:1 + Tab 2 Sweep bar high volume close below high, next bar delta flip + Tab 1 15m close back inside Day VAH.
  - Data-Driven Entry: Limit on 15m close back inside Value Area or 50% retrace of sweep wick (S1 Grade A+).

[RET-R08] [SETUP] [RANGE_BREAKOUT_ORB]:
  - Retail Concept: "Price broke 30m OR high; buy breakout."
  - Microstructure Reality: Breakouts fail > 60% of time when Market Makers dampen volatility in Positive Gamma.
  - Telemetry Checklist: Tab 5 Confirmed wall was pulled (`wallPullEvent`) + Tab 1/4 Breakout volume >= 1.5x 10-bar avg + expanding OI + Tab 13 Negative Gamma confirmed.
  - Data-Driven Entry: Limit order placed on retest of broken range boundary; stop inside broken boundary (S4).

[RET-MATRIX] [MANDATORY] [MASTER_DECISION_MATRIX]:

| Retail Setup Name | Primary Retail Indicator | Fatal Retail Failure Mode | Terminal Order-Flow Confirmation Telemetry | Institutional Setup Code | Minimum Required Confluence |
| :--- | :--- | :--- | :--- | :---: | :---: |
| **S/R Bounce** | Horizontal Line touch | Liquidity already exhausted; stops wiped | Tab 5 Confirmed Bid Wall + Tab 2 `abs` + Tab 1 POC | **S3 / S2** | $\ge 5.0\text{ pts}$ (Grade B) |
| **S/R Breakout** | Green breakout bar | Buying into institutional Ask Wall | Tab 5 Wall-Pull + Tab 1 Expanding OI + Spot CVD Lead | **S4 / S8** | $\ge 6.5\text{ pts}$ (Grade A) |
| **Double Bottom (W)**| Neckline breakout | Terrible R-multiple; late entry | Tab 2 Footprint Delta Divergence + Tab 6 Spot CVD Absorption | **S1 / S6** | $\ge 7.0\text{ pts}$ (Grade A+) |
| **Trendline Retest** | Diagonal trendline touch | Floating in low-volume air | Tab 1 Day/Session POC + VWAP $-1\sigma$ + Tab 2 `exh` | **S7** | $\ge 6.0\text{ pts}$ (Grade A) |
| **RSI Oversold** | RSI $< 30$ | Buying into raging liquidation cascade | Tab 4 `Liq 5m < $500k` + Tab 1 $|z| \ge 2.0\sigma$ + Tab 2 `abs`/`trap` | **S5** | $\ge 5.5\text{ pts}$ (Grade B/A) |
| **MA Crossover** | 9 EMA crosses 21 EMA | Lagging indicator; buying top of chop | Tab 7 `TREND_UP` regime + Tab 1 Pullback to VWAP ($|z| < 1.0$) | **S7** | $\ge 5.0\text{ pts}$ (Grade B) |
| **SMC Liquidity Sweep**| 1m CHoCH structure | 1m noise; swept level had zero liquidity | Tab 4 Cluster swept + 15m close back in value + Delta flip | **S1** | $\ge 7.5\text{ pts}$ (Grade A+) |
| **Range Breakout (ORB)**| Session high/low break | Whipsaw false breakout in positive GEX | Tab 5 Wall-Pull + Tab 13 Negative GEX + Retest of boundary | **S4** | $\ge 6.0\text{ pts}$ (Grade A) |

---

## SECTION 8. THE 6-STEP DECIDE FRAMEWORK

[DEC-00] [MANDATORY] [DECIDE_PIPELINE]: Every trade formulation must execute the DECIDE framework sequentially:

[DEC-D1] [DECIDE] [DIRECTION_BIAS]: Establish macro and intraday bias via 2-of-3 confluence:
  - 1. Footprint signal direction (D7)
  - 2. 4H/D1 EMA 13×89 trend alignment (D4)
  - 3. Price position vs Day VWAP (D3)

[DEC-E1] [DECIDE] [ENTRY_ZONE]:
  - Passive maker limit orders rested at structural anchors: Day VWAP mean, Day/Session POC, or post-sweep exhaustion wick.
  - Front-running confirmed whale walls ONLY when $\text{LSR} < 2.5:1$.

[DEC-C1] [DECIDE] [CONFLUENCE_SCORING]: Score against Table 7 (11.5 pts max). Minimum 5.0 points required to trade.

[DEC-I1] [DECIDE] [INVALIDATION_STOP]:
  - Data-driven structural invalidation only: Beyond Day VAH/VAL, beyond auction POC + 0.5 ATR buffer, or beyond sweep wick in the Cold Zone.
  - MUST pass Auction Clearance Gate 1 (>= 0.5% cushion) and Hazard Gate 2 (0 liquidation pools in Vector B).

[DEC-D2] [DECIDE] [DRIVE_TARGETS]:
  - 40% @ T1: Nearest Value Area edge (Day VAH for longs, Day VAL for shorts).
  - 40% @ T2: High-volume node (Month POC / Session POC / Primary Liquidation Cluster).
  - 20% Runner @ T3: Extended macro target trailed by Structure-Based Trailing Stop (15m Swing Pivot / 15m EMA 20).
  - Hard Floor: $\ge 2.00\text{R}$ composite hurdle across all setups; setups under 2.00R are vetoed.

[DEC-E2] [DECIDE] [EXECUTION_SIZING]:
  - Compute exact contract sizing from structural stop distance: capped at <= 1.0% Dollar Risk of Net Liquid Equity (or Gate 7 exception).
  - Post-Only Maker limit execution (P5-03) with zero taker fees.

---

## SECTION 9. TABLE 7 ZERO-FALLBACK CONFLUENCE MATRIX (MAX 11.5 PTS)

[TAB7-00] [MANDATORY] [SCORING_TABLE]: Every point must originate strictly from live API telemetry; missing or counter-regime feature scores 0.0 pts (labeled `n/a`):

| # | Factor | Grounding Condition | Max Score |
| :--- | :--- | :--- | :---: |
| **1** | **Directional Trend** | H4 AND D1 EMA 13×89 aligned in trade direction AND compatible with active regime (Scores 0.0 in `RANGE_BALANCE` where slope is flat). | **+2.0** |
| **2** | **Auction / VWAP Regime** | Long in Discount (below VWAP, $|z| \le 1.0$) / Short in Premium (above VWAP, $|z| \le 1.0$) or at exact POC/VWAP mean retest. | **+1.5** |
| **3** | **Footprint Order-Flow** | Strong Divergence or Absorption at the entry zone ($\le 8\text{h}$ recency) = +2.0; Divergence/Exhaustion = +1.0. | **+2.0** |
| **4** | **Whale Wall Backstop** | Entry defended by confirmed resting wall (Tier 1 $\ge \$5\text{M}$, Tier 2 $\ge \$1.0\text{M}$, Tier 3 $\ge \$250\text{k}-\$500\text{k}$, Tier 4 $\ge \$50\text{k}-\$100\text{k}$, or $\ge 20\%$ depth within $\pm 1\%$) AND age $> 1\text{h}$. | **+1.5** |
| **5** | **CVD Alignment** | Spot and Perp CVD delta confirming price swing or showing absorption divergence. | **+1.0** |
| **6** | **Liquidity Magnet Gate** | Liquidation skew favors trade direction; LSR $< 2.5:1$; Vector B risk zone clear of hazard pools. | **+1.5** |
| **7** | **Options GEX Context** | Gamma regime confirms setup type (Positive for S2/S5, Negative for S1/S8 — BTC/ETH only). | **+1.0** |
| **8** | **Broker Spread & Friction** | Delta CLOB spread $< 0.05\%$, consumes $< 20\%$ of planned stop-loss distance, maker post-only. | **+1.0** |
| **TOTAL**| **CANONICAL SCORE** | **MAXIMUM CONFLUENCE POINTS** | **11.5 pts** |

[TAB7-GATE] [MANDATORY] [CONFLUENCE_DECISION_GATES]:

| Score | Grade | Leverage Cap | Risk Allocation | Operational Action |
| :--- | :---: | :---: | :---: | :--- |
| **$\ge 7.0\text{ pts}$** | **Grade A** | **Up to 25X** | **1.0% equity cap** | Pristine Institutional Setup. Authorizes full standard position unit with up to 25X isolated leverage (Dollar Risk strictly $\le 1.0\%$ of Net Liquid Equity, e.g. $\le \$0.028\text{ USD}$ on $\approx \$2.77$ equity). |
| **$5.0 - 6.5\text{ pts}$** | **Grade B** | **Up to 20X** | **0.5% equity cap** | Standard Setup. Authorizes half-unit risk allocation ($\le 0.5\%$ of equity). |
| **$< 5.0\text{ pts}$** | **NO TRADE** | **0X** | **0.0% equity** | **HARD VETO. Capital Preserved.** Never enter sub-threshold setups. |

---

## SECTION 10. THE 11 SOCRATIC SELF-AUDIT GATES & THE 10 IMMUTABLE AGI PITFALL INQUESTS

### 10.1 The 11 Socratic Self-Audit Gates

[GATE-01] [GATE] [AUCTION_CLEARANCE]: SL MUST be separated from Session/Day POC and Day VWAP by >= 0.5% cushion (or 1.0x ATR); stops inside high-volume nodes are strictly vetoed.
[GATE-02] [GATE] [VECTOR_B_HAZARDS]: Zero liquidation hazard pools permitted inside the risk path ($P_{\text{entry}} \to \text{SL}$).
[GATE-03] [GATE] [LSR_MAGNET]: If LSR >= 2.5:1, all passive limit entries into the magnet path are banned; wait for the sweep (S1).
[GATE-04] [GATE] [SPREAD_DRAG]: CLOB spread MUST be < 0.15% and consume < 20% of planned stop-loss distance.
[GATE-05] [GATE] [TIME_STOP]: If price fails to reach +0.5R within 8 bars (2 hours), exit or tighten stop (P5-05).
[GATE-06] [GATE] [BREAKEVEN_INVARIANT]: Move SL to entry immediately upon reaching >= +1.0R favorable excursion (P5-04); downside risk strictly $0.00 USD.
[GATE-07] [GATE] [HIGH_POTENTIAL_CONVICTION]:
  - Operator Risk Expansion Directive (2026-11-18): If a slight risk increase captures an A+ high-confluence trade ($EV \ge 2.0\text{R}$), opt for it.
  - Blueberry MT5 (`#5126976`, Balance ~$2,607 USD): Where broker min lot (0.01 lot) produces risk of $7.00-$15.00 USD (<= 0.6% equity), risk is authorized up to $10.00-$15.00 USD max per trade for Grade A/A+ setups with structural stops beyond cold zones; standard Grade B capped at $5.00-$6.00 USD.
  - Delta Exchange India (`#26902927`, Equity ~$3.92 USD): Pristine Grade A/A+ setups (Table 7 >= 7.0, Oracle <= 35 or >= 65, Best R >= 2.50R) authorized high isolated leverage (25x-50x) to size 1 min lot with initial margin <= $1.50 USD; structural stop placed beyond liquidation clusters (<= 0.8% distance, risk $0.35-$0.65 USD).
  - Standard Grade B setups: Restricted to micro-crypto (`SEI`, `ADA`, `ARB`, `DOGE`, `TIA`, `VET`) and TradFi fractionals with margin <= $0.30 USD and $5.00-$6.00 MT5 risk cap.
[GATE-08] [GATE] [CASCADE_CLIMAX]: If `Liq 5m > $500k`, no limit orders into the cascade; wait for the exhaustion wick.
[GATE-09] [GATE] [DYNAMIC_MULTI_SLOT]: Grade B setups restricted to max 2 concurrent slots; Grade A/A+ setups UNLOCKED to punch concurrent setups across available liquid margin while enforcing +1.0R Breakeven.
[GATE-10] [GATE] [BTC_MACRO_ANCHOR]: Altcoin shorts strictly banned if BTC is within 0.75% of daily low, oversold (<-2.0σ VWAP), or testing major multi-day liquidity support.
[GATE-11] [GATE] [SLIPPAGE_MULTIPLIER]: All stop risk budgeting MUST multiply calculated stop distance by 1.20x for execution slippage and exit fees.

### 10.2 The 10 Immutable AGI Pitfall Inquests

| Pitfall ID | Name | Failure Mechanism | Empirical Case Study | Immutable Invariant Enforced |
| :--- | :--- | :--- | :--- | :--- |
| **PIT-01** | **Contract Lot Explosion** | Minimum exchange lot forces position notional far beyond equity. | **LINKUSD (R334)**: 1 LINK min lot = $9.12 notional on $2.95 equity (309% leverage). A 1.4% stop movement caused a -$0.1505 loss (**5.10% equity loss**). | **Gate 7 Mechanical Ban**: Strict veto on any asset where 1 min lot exceeds 1.0%–2.5% equity risk. LINK/BNB/SOL banned on small equity. |
| **PIT-02** | **Double-Beta Avalanche** | 2 same-direction crypto assets create 100% correlated beta to Bitcoin. | **APT + LINK Shorts (R334)**: Both shorts filled together. BTC bounced +$1,800, stopping out both altcoins in 56s (-$0.1863 loss). | **Gate 9 Sector Isolation**: Max 1 crypto position per direction. Slot 2 is TradFi or Cash. |
| **PIT-03** | **Bottom-Tick Shorting** | Shorting altcoin pullbacks while BTC is at day lows or sweep support. | **R334 Altcoin Shorts**: Entered while BTC was -2.5% at $64.1k near day low ($63.8k), directly preceding violent short squeeze. | **Gate 10 BTC Macro Filter**: Altcoin shorts banned when BTC is at day lows or <-2.0σ VWAP. |
| **PIT-04** | **Altcoin Market Slippage** | Market stop-loss orders in thin books slip heavily. | **APT & LINK (R334)**: APT slipped 4 ticks; LINK slipped 15 ticks, expanding losses by +15.8%. | **Gate 11 1.20x Multiplier**: Risk models must incorporate 20% friction buffer on all stop distance calculations. |
| **PIT-05** | **HVN Stop Collision** | Stops placed on high-volume profile nodes get hit during normal Value Area rotation. | Stops hit during normal Value Area rotation rather than structural invalidation. | **Gate 1 Clearance**: Stops placed $\ge 0.5\%$ beyond Session/Day POC and outside Value Area extremes. |
| **PIT-06** | **Passive Front-Run in High Skew**| Limit orders front-running clusters when LSR $\ge 2.5:1$ get steamrolled. | Cascades blast straight through resting limit orders before reversing. | **Gate 3 LSR Sweep Gate**: If LSR $\ge 2.5:1$, maker front-running banned. Must wait for sweep wick. |
| **PIT-07** | **Spread Drag & Fee Asymmetry** | Tight targets where fees and spread consume $> 25\%$ of profit. | Commission drag turns positive gross EV into negative net realized PnL. | **Gate 4 Spread Drag**: Spread must consume $< 20\%$ of SL distance; all entries post-only maker. |
| **PIT-08** | **Time Decay / Stale Execution** | Stagnant position chopping around entry exposes capital to overnight gap risk. | Chop consumes time and eventually breaks against trader. | **Gate 5 Time Stop (P5-05)**: Hard exit or stop tightening after 8 15m bars (2 hours) if price $< +0.5\text{R}$. |
| **PIT-09** | **Premature BE vs Late Trailing**| Moving stop to BE too early (chopped out) or too late (turning winners into losses). | Winning trade at +1.5R swings back to -1.0R loss because stop was never trailed. | **Gate 6 Invariant (P5-04)**: Non-discretionary move to exact entry at $\ge +1.0\text{R}$ excursion. |
| **PIT-10** | **Asymmetric Taker Panic Liquidation** | Manually market-exiting during temporary pullbacks due to emotional loss aversion. | Exiting at exact bottom tick right before price rotates to target. | **P5-01 Rule**: Execution 100% mechanical via pre-set CLOB bracket orders. No manual panic closes. |

---

## SECTION 11. DELTA EXCHANGE INDIA OPERATIONAL INVARIANTS

[P5-01b] [INVARIANT] [SHARED_ACCOUNT_ISOLATION]: Track exclusively via internal order/client IDs recorded in `desk/state.json`; never cancel, edit, or touch external/algo positions (`FIB4H_*`, `SOLVUSD`, `TACUSD`).
[P5-02] [INVARIANT] [MAX_POSITIONS]: Maximum 2 active positions total; MAXIMUM 1 CRYPTO POSITION in any direction (Gate 9); Slot 2 strictly reserved for TradFi/Metals (XAU, XAG, Oil, Equities) or 100% Cash; total portfolio heat <= 1.0% - 2.5% equity.
[P5-03] [INVARIANT] [POST_ONLY_MAKER]: All new entries MUST be Post-Only Maker Limit orders (`post_only: true`); zero taker fees on entry.
[P5-04] [INVARIANT] [BREAKEVEN_RATCHET]: Move SL to entry immediately upon reaching >= +1.0R favorable excursion; downside risk strictly $0.00 USD.
[P5-05] [INVARIANT] [TIME_STOP]: If price fails to reach +0.5R within 8 15-minute bars (2 hours), exit or tighten the stop.
[P5-06] [INVARIANT] [FIRST_TWO_FILLS]: When resting maker orders are standing for multiple assets, the moment ANY 2 fill into active positions, immediately cancel all remaining open candidate orders.
[P5-07] [INVARIANT] [VACANT_SLOT_HUNTER]: Maintain high-confluence standing maker orders at key structural nodes only when portfolio slots are vacant; respect Gate 7 micro-asset constraint.
[P5-08] [INVARIANT] [PRUNING_DISCIPLINE]: Instantly cancel any order that falls below 5.0 confluence points, becomes overextended ($|z| \ge 2.0\sigma$), or violates margin solvency.
[P5-09] [INVARIANT] [CANONICAL_TIMER_PROTOCOL]: Re-arm dynamic recursion using `schedule(DurationSeconds=1200)` with the canonical prompt string. Strictly 1 background timer; zero duplicate timers, zero cron.

```text
Canonical Structured Timer Prompt Format:
Timer: 20m, Prompt: # INVOCATION (load first, uncached)
@[plugin:persistent-memory]  @[plugin:coderabbit]  @[plugin:superpowers]  @[plugin:trading-skills] 
/gravitas  /goal  /executing-plans  /plan  /brainstorming  /karpathy-guidelines  /thinking-model-router 
@[plugin:trading-skills] 
# ENGINE: Autonomous Dual-Venue Trade Execution & Recursive Self-Improving Engine
# ROUND: R<n>

## RULES OF ENGAGEMENT
- Every numbered step below is MANDATORY and must be executed in order.
- Each step must end with a status line: `[STEP n: DONE | FAILED | N/A + reason]`.
- No step may be merged, skipped, or summarized away.
- If any step FAILS, state why and fix it before proceeding.

---

## STEP 0: META-COGNITIVE REVIEW (FIRST ACTION, BEFORE ANYTHING ELSE)
0.1 Review the previous thinking chain.
0.2 Identify what was missed or omitted.
0.3 Measure execution latency.
0.4 Apply continuous self-improvement lessons to this round.
Output: list of misses + lessons applied.

## STEP 1: PRE-FLIGHT VERIFICATION CHECKLIST (RESPONSE MUST OPEN WITH THIS)
Confirm each item explicitly:
- [ ] Fresh, individual audit of ALL assets from scratch (no cached results)
- [ ] Audit covers all 10 modules
- [ ] Universe covered: 234 Delta Exchange India + 156 MT5 Blueberry assets
- [ ] All skills loaded fresh/uncached
- [ ] All plugins loaded fresh/uncached
- [ ] All MCPs loaded fresh/uncached

## STEP 2: OPERATOR INQUEST (ASK AND ANSWER EVERY ROUND)
Question: "What are potential high confluence A+ setups for Delta and MT5 that can be punched right away?"
Output: explicit answer, per venue.

## STEP 3: SPECIFICATION AUDIT
- Audit BOTH venues strictly against:
  @[c:\Users\SIGMA\Documents\cg-terminal\desk\CANONICAL_MASTER_SPECIFICATION.md]
- Report any deviation found.

## STEP 4: 4-VOICE QUANTITATIVE DESK DEBATE
Run all four voices, each with a written position:
1. Alpha Strategist
2. Red Team
3. Quant
4. Arbiter (final ruling)

## STEP 5: MENTAL MODELS + KARPATHY GUIDELINES
Apply and show evidence of each:
- First principles
- Pre-mortem
- Probabilistic thinking
- Red-team
- Margin of safety
- Karpathy guidelines

## STEP 6: GATE ENFORCEMENT (GATES 1-11, EACH WITH PASS/FAIL)
- Gates 1-6, 8: enforce per canonical spec
- Gate 7: High-Potential Conviction Sizing with Structural Stops
- Gate 9: Dynamic Multi-Slot Expansion
- Gate 10: BTC Macro Filter
- Gate 11: 1.20x Slippage Multiplier
- Target: >= 2.0R trades, with Trailing SL Runner Extension

## STEP 7: RESTING LIMIT ORDER RE-ANALYSIS (PIT-06)
For every resting limit order on both venues:
- Re-validate ongoing structural validity
- Prune if stale
- Output: KEEP / PRUNE per order, with reason

## STEP 8: AUDIT OF ALL RUNNING TRADES (BOTH VENUES)
Scope: ALL running trades on Delta and MT5, including co-located algo trades on MT5.

8.1 Liquidity trap check (Directive 2026-11-18)
- Use rich orderflow, stopmap, and liquidation data.
- Verify no SL sits inside a liquidity sweep or heatmap cluster.
- If trapped, move the SL into a structural cold zone, even if risk increases slightly.

8.2 Optimization
- SL breakeven ratchet at +1.0R
- Structure-based trailing stops
- Dynamically adapt TP targets into high-density liquidity clusters
- Enforce the 8-bar time stop

Output: per-trade table (venue, symbol, SL action, TP action, time-stop status).

## STEP 9: NEW OPPORTUNITY HUNT & EXECUTION (CORE GOAL)
- Hunt across the entire universe (234 Delta + 156 MT5).
- Qualify only A+ Grade setups: score >= 7.0 pts AND EV >= 2.0R, with high confluence and high potential.
- For each qualifying setup, produce a pristine execution card:
  - Venue, symbol, direction
  - Maker limit entry
  - Structural stop
  - High-density liquidity target(s)
  - Score, EV, R-multiple
  - Gate 1-11 results
- Punch maker limit orders on both platforms for qualifying setups.
- If none qualify, state so explicitly, with the best near-miss and what it lacks.

## STEP 10: MARGIN & LIQUIDITY AUDIT
- Audit margin usage and available liquidity on both venues.
- Confirm new orders fit within limits.

## STEP 11: RECURSION
- Re-arm the dynamic 1200s recursion for the next round.
- Carry forward this round's lessons to Step 0 of the next round.

---

## FINAL COMPLIANCE GATE (RESPONSE IS INVALID WITHOUT THIS)
End the response with this table, every row marked DONE / FAILED / N/A:

| Step | Requirement | Status |
|------|-------------|--------|
| 0 | Meta-cognitive review | |
| 1 | Pre-flight checklist | |
| 2 | Operator inquest | |
| 3 | Canonical spec audit | |
| 4 | 4-voice debate | |
| 5 | Mental models + Karpathy | |
| 6 | Gates 1-11 | |
| 7 | Resting orders (PIT-06) | |
| 8 | Running-trade audit + SL cold-zone check | |
| 9 | A+ hunt + execution cards + orders | |
| 10 | Margin & liquidity | |
| 11 | 1200s recursion re-armed | |
```

[P5-10] [INVARIANT] [MARGIN_SOLVENCY]: Compute sizing: `contracts = floor((net_equity * risk_pct) / (stop_distance * contract_value))`; verify `order_margin <= available_balance * 0.8`.

---

## SECTION 12. DUAL-AGENT COORDINATION & DESK OPERATING PROTOCOL

[COORD-01] [ROLES] [CADENCE_MATRIX]:
  - `zai-desk` (Remote Sandbox Brain): 3 scheduled wakes/day (01:00, 09:00, 17:00 IST) + on message; market structure analysis, confluence synthesis, order suggestions, trade reviews; NEVER places live trades or edits `positions[]`.
  - `atg-exec` (Local Delta Execution Brain): Continuous 15-min rounds driven by daemon / 1200s timer; audits CLOB, punches Delta orders, manages brackets, enforces invariants; NEVER edits `analysis` or invents arbitrary levels.

[COORD-02] [DAEMON] [LOCAL_DESK_DAEMON]: Process `scripts/desk_daemon.mjs` runs local event loop: git pull --rebase, runs `scripts/desk_round.sh` every 15 min, processes inbox instructions, queues suggested orders in `desk/inbox/WAKE.md`, refreshes CLOB in `desk/state.json`, commits and pushes.
[COORD-03] [SECURITY] [SAFE_EXECUTION]: Commands run WITHOUT A SHELL (`spawn(file, argv)` with `shell:false`); zero metacharacter escape, no variable expansion, no pipes/redirects.
[COORD-04] [CHANNEL] [INBOX_VOCABULARY]: `PING`, `CLOB_SNAPSHOT`, `ROUND_NOW`, `REPORT`, `AGENT_TASK`.
[COORD-05] [OWNERSHIP] [FILE_FIELD_MATRIX]:
  - `desk/state.json`: `config` owned strictly by Human; `analysis` written only by `zai-desk`; `orders[]` appended by `zai-desk` as suggested, updated by `atg-exec` to placed/filled/cancelled; `positions[]` written only by `atg-exec`; `closed[]` appended by `atg-exec`.
  - `desk/log.md`: Append-only journal; `## R<n>` per round; `EXEC`, `DIALOG` per execution action. Older entries never edited or deleted.

[COORD-06] [STATE_MACHINE] [ORDER_LIFECYCLE]:
```text
suggested ──(atg places on Delta)──► placed ──(fill)──► filled ──(close)──► closed
    │                                    │                  │
    ├──(expiry ts passed)─────────────► expired             ├──(SL/TP hit on CLOB)──► closed
    └──(confluence invalidated)───────► withdrawn           └──(review: CLOSE rec)──► closed
```

[COORD-07] [DIRECTIVE] [REASONING_MANDATE]: `atg-exec` NEVER executes directives on blind trust:
  - 1. Re-derive every number itself (live quote, basis offset, lot sizing, risk cap).
  - 2. Re-verify validity (order suggested, Table 7 >= 5.0 pts, not expired).
  - 3. Form its own opinion: "Would I take this trade?" If NO -> reply COUNTER with alternative and reasoning.
  - Reply contract: Output to `desk/outbox/<basename>.reply.md` with `VERDICT: EXECUTED | COUNTER | REJECTED | DEFERRED`.

[COORD-08] [REVIEW] [RUNNING_TRADE_VERDICTS]:
  - `HOLD`: Trade progressing within normal parameters.
  - `MOVE_STOP_TO_BREAKEVEN`: Position reached >= +1.0R excursion (P5-04).
  - `TIGHTEN_STOP`: Position reached >= +1.5R excursion.
  - `TAKE_PARTIAL`: Price within 0.3x stop-distance of T1.
  - `CLOSE_RECOMMENDED`: Structural invalidation triggered or regime flipped.
  - `CHECK_EXCHANGE`: Price beyond stop level; verify fill status on Delta India.

[COORD-09] [GIT] [CONFLICT_AVOIDANCE]: Always `git pull --rebase origin main` before editing; keep edit windows short; commit and push immediately; prefixes: `desk(round):` (`zai-desk`) and `desk(exec):` (`atg-exec`); NEVER force push.

---
