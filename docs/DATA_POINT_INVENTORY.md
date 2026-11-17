# CG Order-Flow Terminal — Canonical Telemetry Data Point Inventory
## Comprehensive Telemetry Dictionary & Retail Setup Order-Flow Confirmation Engine

```text
Specification Version: 2.2.0 · Comprehensive Telemetry & Setup Mapping
Coverage: CURATED 61 Assets (30 Crypto USDT-M + 28 TradFi Perps + 3 Classic Indices)
Execution Venue: Delta Exchange India (india_prod, Account #26902927)
Architecture: Real-Time 3-Tier Ladder (Tier 0 WS · Tier 1 REST · Tier 2 CG)
```

---

## PART 1. THE REAL-TIME 3-TIER PERCEPTION ARCHITECTURE

Every displayed data point originates from the fastest reliable tier:
* **Tier 0 · Live WebSocket (sub-100ms)**: Browser direct connection to `wss://fstream.binance.com` (`<sym>usdt@bookTicker` and `<sym>usdt@trade`). Single connection with dynamic subscribe/unsubscribe, 5s watchdog, 10 Hz render throttle.
* **Tier 1 · REST Engine (250ms–1.2s)**: Server-side poller to `fapi.binance.com` for L2 order book top-1000 depth, ticker fallbacks, and wall change scanners.
* **Tier 2 · Coinglass Aggregator (3s–30s)**: Multi-exchange aggregates across Binance, OKX, Bybit, Coinbase, and Hyperliquid.

---

## PART 2. THE COMPLETE 9-TAB TELEMETRY PARAMETER DICTIONARY

### 1. TAB 1: OVERVIEW (`Overview` — `/api/cg/market?sym=`)
Provides the macro structural auction profile, multi-timeframe trend context, volatility regime, and aggregate funding metrics.

#### 1.1 Header & Ticker Telemetry
* `symbol` / `market`: Standardized ticker identifier (e.g., `BTCUSDT`, `MSFTBUSD`).
* `lastPrice`: Real-time mid/trade price from Tier 0 WebSocket (Binance lead).
* `change24h` & `change24hPercent`: 24-hour nominal and percentage price displacement.
* `high24h` / `low24h`: 24-hour absolute session boundaries.
* `volume24hUsd`: 24-hour aggregated taker volume across all covered exchanges (in USD).
* `turnover24h`: Nominal base asset turnover.
* `tierActiveBadge`: Visual latency indicator confirming active data tier (`WS 0`, `REST 1`, `CG 2`).

#### 1.2 Multi-Timeframe Auction Profiler (AMT)
Computed for three distinct anchor sessions: **Session 8h**, **UTC Day (24h)**, and **UTC Month**:
* `VAL` (Value Area Low): 70% volume distribution lower boundary.
* `POC` (Point of Control): Exact price tick containing the maximum executed volume.
* `VAH` (Value Area High): 70% volume distribution upper boundary.
* `VA_WidthPercent`: Value Area spread `(VAH - VAL) / POC * 100` (determines compression vs expansion regime).
* `profileType`: Auction shape classification (`D-shape` = balanced, `P-shape` = short covering/buying climax, `b-shape` = liquidation/long liquidation, `B-shape` = dual balance).

#### 1.3 Day VWAP & Volatility Bands
* `vwap`: Volume-Weighted Average Price anchored to 00:00:00 UTC.
* `vwapUpper1`, `vwapUpper2`, `vwapUpper3`: +1.0σ, +2.0σ, +3.0σ standard deviation bands.
* `vwapLower1`, `vwapLower2`, `vwapLower3`: -1.0σ, -2.0σ, -3.0σ standard deviation bands.
* `zScore`: Statistical distance `(lastPrice - vwap) / stdDev` (flags mean-reversion extensions when $|z| \ge 2.0\sigma$).
* `regime`: `PREMIUM` (Price > VWAP), `DISCOUNT` (Price < VWAP), or `EXTREME_EXTENSION` ($|z| \ge 2.5\sigma$).

#### 1.4 Multi-Timeframe Trend & Momentum Matrix
Calculated across 4 standard intervals (`15m`, `1h`, `4h`, `1d`):
* `ema13`: 13-period Exponential Moving Average (tactical micro-trend).
* `ema89`: 89-period Exponential Moving Average (structural macro-trend).
* `ema233`: 233-period Exponential Moving Average (institutional cycle baseline).
* `trendState`: `BULLISH_STACK` ($EMA13 > EMA89 > EMA233$), `BEARISH_STACK` ($EMA13 < EMA89 < EMA233$), or `CHOP_COMPRESSION`.
* `rsi14`: 14-period Relative Strength Index (evaluates oversold $< 30$ and overbought $> 70$).

#### 1.5 Derivatives Context & Funding
* `openInterestUsd`: Total open contracts multiplied by mark price across all venues.
* `oiChange24hPercent`: 24-hour expansion or contraction in open commitments.
* `fundingRate`: Current 8-hour predicted funding rate (annualized % equivalent).
* `longShortRatio`: Taker volume / account ratio of accounts net long vs net short.

---

### 2. TAB 2: FOOTPRINT (`Footprint` — `/api/cg/signals?sym=` & `/api/cg/fp?sym=`)
Provides microstructural inside-the-bar order execution analysis, decomposing candle volume into executed buyer and seller aggression.

#### 2.1 Per-Bar Footprint Metrics
* `barTimestamp` / `interval`: Timestamp and time-bucket duration (15m standard, auto-volume, auto-range).
* `open`, `high`, `low`, `close`: Classical OHLC candle boundaries.
* `totalVolumeUsd`: Cumulative executed notional inside the candle.
* `buyVolumeUsd`: Aggressive taker buying volume (executed at ask).
* `sellVolumeUsd`: Aggressive taker selling volume (executed at bid).
* `deltaUsd`: Net taker flow `buyVolumeUsd - sellVolumeUsd`.
* `deltaPercent`: Relative imbalance `(deltaUsd / totalVolumeUsd) * 100`.
* `barPOC`: Price level within the specific candle that traded the largest volume.
* `barVAL` / `barVAH`: Intra-bar 70% value boundaries.

#### 2.2 Microstructure Signal Engine
* `signalType`:
  * `ABSORPTION`: Heavy taker volume failed to advance price (passive limit wall absorbed aggression).
  * `DIVERGENCE`: Price printed a new extreme (high/low), but bar delta printed a reverse extreme.
  * `STRONG_DIVERGENCE`: Multi-bar sustained price-delta divergence confirmed at VWAP bands.
  * `TRAP`: Aggressive breakout buyers/sellers trapped as price promptly re-enters prior Value Area.
  * `EXHAUSTION`: Sudden drop in taker volume at key swing structural highs/lows.
* `signalSeverity`: `HIGH` (actionable setup trigger) or `INFO` (contextual telemetry).
* `signalPrice`: Exact price where the structural anomaly printed.
* `imbalanceRatios`: Diagonal Bid/Ask imbalance ticks where buy volume $\ge 300\%$ sell volume (or vice versa).

---

### 3. TAB 3: LARGE ORDERS (`Large Orders` — `/api/cg/largeorder?sym=` & `/api/cg/lto?sym=`)
Tracks resting institutional liquidity and executed block trades across the aggregated venue books.

#### 3.1 Resting Whale Limit Walls & Liquidity-Calibrated Thresholds
* `orderId` / `hash`: Unique identifier of the resting order.
* `exchange`: Originating exchange (`Binance`, `OKX`, `Bybit`, etc.).
* `side`: `BID` (resting support) or `ASK` (resting resistance).
* `price`: Exact limit price where the wall is posted.
* `notionalUsd`: Total USD size of the resting order.
* `distancePercent`: Percentage distance from current mark price `(orderPrice - lastPrice) / lastPrice * 100`.
* `wallAge`: Duration the order has rested on the book without being cancelled.
* `wallStatus`: `RESTING`, `PARTIALLY_FILLED`, or `TOUCHED` (tested by market price).
* **Dynamic Whale Wall Tiering (Calibrated by Asset Class)**:
  * *Tier 1 Mega-Cap (BTC, ETH)*: Whale Wall $\ge \$5.0\text{M}$ (Alerts $\ge \$10.0\text{M}$).
  * *Tier 2 Large-Cap (SOL, XRP, DOGE, BNB, TradFi Indices SPX500/NDX100, Gold/Oil XAU/UKO)*: Whale Wall $\ge \$1.0\text{M}$.
  * *Tier 3 Mid-Cap Alts & Equities (ADA, LINK, AVAX, SUI, NEAR, APT, ARB, TIA, SEI, INJ, NVDA, MSFT, AAPL, MSTR)*: Whale Wall $\ge \$250\text{k} - \$500\text{k}$.
  * *Tier 4 Micro-Cap Alts & Tokenized Equities (VET, 1000PEPE, 1000SHIB, CRCL, TSM)*: Whale Wall $\ge \$50\text{k} - \$100\text{k}$.
  * *Relative Depth Invariant*: Any resting limit order representing $\ge 15\% - 20\%$ of the total resting book depth within $\pm 1.0\%$ (Tab 5 `depthImbalanceRatio`) or $\ge 2.5\times$ rolling 15m bar volume qualifies as a confirmed institutional wall.

#### 3.2 Executed Block Trades (Tape Whales)
* `tradeTimestamp`: Millisecond execution timestamp.
* `tradeSizeUsd`: Notional value of the single executed trade (filtered $\ge \$100\text{k}$ alts, $\ge \$500\text{k}$ BTC).
* `executionSide`: `BUY` (aggressed into ask) or `SELL` (aggressed into bid).
* `executionPrice`: Executed trade price.
* `executedImbalance`: Rolling ratio of whale buy notional vs whale sell notional over 1h, 4h, and 24h.

---

### 4. TAB 4: LIQUIDATION LEVELS (`Liq Levels` — `/api/cg/liqlevels?sym=` & `/api/cg/stopmap?sym=`)
Tracks the liquidation landscape, modeling forced liquidation price clusters that act as market magnets.

#### 4.1 Liquidation Clusters (3d / 7d / 30d Lookbacks)
* `timeHorizon`: Historical accumulation window (`3-Day`, `7-Day`, `30-Day`).
* `clusterPrice`: Price level where liquidation exposure is concentrated.
* `clusterNotionalUsd`: Estimated total forced liquidation value (USD millions) at that price.
* `liquidationSide`:
  * `LONG_LIQUIDATION`: Trapped long traders whose forced selling creates a downside magnet.
  * `SHORT_LIQUIDATION`: Trapped short traders whose forced buying creates an upside magnet.
* `distanceToClusterPercent`: Distance from current mark price.
* `clusterDensityRatio`: Notional density relative to local 24-hour volume.

#### 4.2 Liquidation Skew & Magnet Gate
* `longLiqTotalUsd`: Total estimated long liquidation exposure within $\pm 4\%$.
* `shortLiqTotalUsd`: Total estimated short liquidation exposure within $\pm 4\%$.
* `liquidationSkewRatio`: Ratio of dominant side to minority side (e.g., $Short / Long$).
* `magnetGateStatus`: When Skew $\ge 2.5:1$, passive front-running is prohibited; execution must await cluster sweep.

---

### 5. TAB 5: BOOK WALLS (`Book Walls` — `/api/cg/bookwalls?sym=`)
Depth-of-book telemetry quantifying order book imbalances, depth migration, and spoofing detection.

#### 5.1 Order Book Depth & Imbalance
* `bandInterval`: Depth calculation band ($\pm 0.5\%$, $\pm 1.0\%$, $\pm 2.0\%$, $\pm 5.0\%$).
* `bidDepthUsd`: Total resting bid notional within the band.
* `askDepthUsd`: Total resting ask notional within the band.
* `depthImbalanceRatio`: `(bidDepth - askDepth) / (bidDepth + askDepth)`.
* `imbalanceDelta5m`: Net shift in imbalance compared to 5 minutes ago (detects wall loading/pulling).

#### 5.2 Dynamic Wall Scanner & Event Feed
* `confirmedWallList`: Active institutional walls verified across multiple polling cycles.
* `wallAddEvents`: New large orders injected into the order book within the last 5 minutes.
* `wallPullEvents`: Cancelled or pulled orders (identifies spoofing liquidity).
* `wallFillEvents`: Order depth consumed by active market orders.

---

### 6. TAB 6: CUMULATIVE VOLUME DELTA (`CVD` — `/api/cg/cvd?sym=`)
Cumulative volume delta engine isolating spot market accumulation from leveraged perp market aggression.

#### 6.1 Multi-Venue CVD Streams
* `perpCvd`: Cumulative Taker Delta for perpetual futures contracts.
* `spotCvd`: Cumulative Taker Delta for physical spot markets (Binance, Coinbase).
* `takerBuySharePercent`: Percentage of total volume driven by aggressive buyers.
* `cvdAnchor`: Accumulation anchor period (`Session`, `UTC Day`, `Rolling 7-Day`).

#### 6.2 Structural Divergence Telemetry
* `divergenceType`:
  * `BULLISH_ABSORPTION`: Spot CVD rising while Perp CVD and Price are falling or flat.
  * `BEARISH_EXHAUSTION`: Perp CVD aggressively surging into new highs while Spot CVD fails to confirm.
  * `LEVERAGE_DRIVEN`: Rapid price expansion accompanied exclusively by Perp CVD spike and OI surge (fragile).
* `cvdSlope`: Rate of change ($\Delta CVD / \Delta t$) over 5m, 15m, and 1h intervals.

---

### 7. TAB 7: STRATEGY NARRATIVE & BACKTEST (`Narrative` — `/api/cg/narrative?sym=`)
Historical strategy evaluation and live narrative formulation engine validating playbook setups against archival tick and footprint data.

#### 7.1 Playbook Strategy Configurations
* `strategyId`: Target playbook setup (`S1_SWEEP_REVERSAL`, `S2_TREND_POC_RETEST`, `S3_VWAP_EXTENSION`, `S7_ABSORPTION_CONTINUATION`).
* `assetCohort`: Curated 61 asset selection or sector filter.
* `testWindow`: Historical backtest date range.
* `riskPerTrade`: Fixed percentage risk model ($\le 1.0\% - 2.5\%$).

#### 7.2 Performance & Risk Metrics
* `winRate`: Percentage of completed trades hitting Take Profit.
* `profitFactor`: Gross profits divided by gross losses.
* `sharpeRatio`: Risk-adjusted excess return over standard deviation.
* `maxDrawdownPercent`: Maximum peak-to-trough equity decline.
* `averageRMultiple`: Average realized $R$ return per trade.
* `expectancy`: Statistical edge $EV = (Win\% \times R_{win}) - (Loss\% \times 1.0R)$.

---

### 8. TAB 8: ALERTS & NOTIFICATIONS (`Alerts` — `/api/cg/notifications`)
Real-time asynchronous notification and cursor-based event queue.

#### 8.1 Event Telemetry Fields
* `eventId`: Unique monotonic event UUID.
* `timestamp`: ISO-8601 event generation timestamp.
* `source`: Telemetry generator (`footprint`, `indicators`, `whale-orders`, `liqlevels`, `cvd`, `engine`).
* `severity`: `HIGH` (trade-formulation trigger), `MEDIUM`, or `INFO`.
* `symbol`: Triggering ticker symbol.
* `message`: Human- and agent-readable event description.
* `cursorPosition`: Monotonic cursor sequence saved in `data/mcp-cursor.json`.

---

### 9. TAB 9: LIVE L2 & TICKET WS (`Live L2` — `/api/cg/livebook?sym=` & Delta MCP)
Real-time microstructural order book visualizer and execution venue bridge.

#### 9.1 Live L2 Depth Ladder
* `bids`: Top 1,000 bids sorted descending by price `[price, size, cumulativeNotional]`.
* `asks`: Top 1,000 asks sorted ascending by price `[price, size, cumulativeNotional]`.
* `spreadUsd`: Absolute difference between best bid and best ask `(bestAsk - bestBid)`.
* `spreadBps`: Bid-Ask spread expressed in basis points `(spreadUsd / midPrice) * 10,000`.
* `midPrice`: Computed midpoint `(bestBid + bestAsk) / 2`.
* `bookDepthCoveragePercent`: Nominal price coverage range captured by top-1,000 levels ($\approx \pm 0.2\%$ on BTC).

#### 9.2 Execution Ticket Bridge (Delta Exchange India)
* `orderType`: Post-Only Limit (`limit`, `post_only: true`). Zero taker execution allowed.
* `contractSize`: Minimum order increment and lot multiplier (Delta specification).
* `marginRequiredUsd`: Initial margin required to open order.
* `bracketStopLoss`: Stop loss trigger price (evaluates against `mark_price`).
* `bracketTakeProfit`: Take profit limit/market price.
* `executionStatus`: Live state on Delta Exchange India CLOB (`open`, `filled`, `cancelled`).

---

### 10. TAB 10: ATHENA ORACLE (`Oracle` — `/api/cg/oracle?sym=`)
The mythological quantitative confluence engine synthesizing 6 distinct order-flow and structural dimensions into a unified 0–100 score.

#### 10.1 The 6 Microstructure Gods
* `apollo` (Weight 25% — Trend & Momentum): Binance 15m/1h klines, EMA20/50/200 stack, RSI(14) regime, EMA50 3h slope, 1h HTF confirmation, and ATR volatility regime (`trend`, `range`, `squeeze`).
* `poseidon` (Weight 20% — Order-Flow Tide): Multi-venue CVD slope over 24 bars (~6h), Spot vs Perp CVD divergence, taker buy volume ratio, and flow grid momentum.
* `hades` (Weight 15% — Liquidation Gravity): 7-day liquidation clusters, distance & notional of long cluster below vs short cluster above (magnet pull effect), Liquidation Skew Ratio ($LSR$).
* `zeus` (Weight 15% — Whale Strikes): Large Resting Orders ($LTO \ge \$1\text{M}$) net notional (bid vs ask), resting institutional order clusters.
* `atlas` (Weight 15% — Wall Pressure): Order-book depth within $\pm 2\%$ of price, dominant wall side, 5m depth imbalance delta.
* `nemesis` (Weight 10% — Funding Reversion): Annualized funding APR percentile vs historical baseline (crowded long liquidation risk vs crowded short squeeze fuel).

#### 10.2 Composite Metrics & Regimes
* `score`: 0–100 composite score (higher = more bullish).
* `verdict`: Plain English narrative synthesis (e.g. `Cautious bearish lean 38/100 — trend broken`).
* `regime`: Structural market regime (`trend`, `range`, `squeeze`).
* `partial`: Array of degraded factors (if an upstream source fails, factor defaults to neutral 50 with tag; never mocked).

---

## PART 3. THE RETAIL SETUP $\longleftrightarrow$ ORDER-FLOW CONFIRMATION ENGINE

Retail traders rely on visual chart patterns that treat price as a continuous geometric drawing. In reality, **price moves only when market orders consume resting limit depth**, and institutions exploit retail chart patterns to harvest liquidity.

Below is the exhaustive mapping of **8 Popular Retail Setups**, explaining the underlying retail flaw, the exact order-flow telemetry required to validate or fade the setup, and the data-driven entry design.

---

### Setup R-01: Classical Support / Resistance Bounce (Horizontal Levels)

```text
Retail Concept: "Price bounced off this horizontal support 3 times; buy the 4th touch with a market order."
Microstructure Reality: Each touch weakens resting limit liquidity. By the 3rd or 4th touch, bids are exhausted.
Institutions know retail stops are clustered 10-20 bps below the line.
```

#### Order-Flow Confirmation Checklist (Data Points Required):
1. **Tab 5 (Book Walls)**: Is there a **confirmed resting bid wall $\ge \$5\text{M}$** at the support price? (If the wall was pulled or is $< \$1\text{M}$, the support is hollow).
2. **Tab 2 (Footprint)**: Look for **Absorption (`abs`)** or **Divergence (`div`)** on the test of support. Taker sell volume must spike into the level with zero downside price progress (passive buyer absorbing aggression).
3. **Tab 6 (CVD)**: Spot CVD must be flat or rising while price tests support. If Spot CVD is dumping violently with Perp CVD, smart money is liquidating $\implies$ **DO NOT BUY**.
4. **Tab 4 (Liq Levels)**: Check `longLiqTotalUsd` below the support. If a massive liquidation cluster sits 0.5% below support, the market **WILL SWEEP IT** before any bounce.
5. **Tab 1 (Auction POC)**: Does support coincide with the **Day POC or Session POC**? (If yes, volume acceptance confirms the level; if support is in a low-volume node, it will slice right through).

#### Data-Driven Entry Formulation:
* **Entry Mode**: NEVER buy the first touch. Wait for the test wick.
* **Trigger**: Post-Only Limit order rested at the top of the **Absorption Footprint Zone** or front-running the **confirmed Whale Wall by +0.05%** (Setup S3).
* **Stop Loss**: 0.5% below the structural absorption wick + behind the resting wall (Gate 1 & Gate 2 clear).
* **Target (Drive)**: Day POC / Day VAH (T1 40%, T2 40%, T3 20% Runner).

---

### Setup R-02: Classical S/R Breakout (Momentum Chasing)

```text
Retail Concept: "Price broke above horizontal resistance with a big green candle; buy market on the breakout."
Microstructure Reality: 75% of breakouts in perpetual markets are fakeouts designed to trigger retail breakout buys
into institutional limit sell walls (exit liquidity).
```

#### Order-Flow Confirmation Checklist (Data Points Required):
1. **Tab 3 & Tab 5 (Whale Walls)**: Is there an **Ask Wall $\ge \$5\text{M}$** immediately above the breakout price? If YES, the breakout is running directly into a brick wall $\implies$ **VETO LONG / PREPARE TO FADE**.
2. **Tab 4 (Liq Levels / LSR)**: Was the breakout driven by a **Short Liquidation Cascade**? If `shortLiqTotalUsd` wiped $\ge \$5\text{M}$ and `Liq 5m > $500k`, the buying was forced stop-outs. Once liquidations clear, fuel vanishes.
3. **Tab 1 & Tab 4 (OI Dynamics)**:
   - **True Breakout**: Price Breaking Out + **Rising Open Interest** + Rising Spot CVD $\implies$ Institutional aggressive long accumulation (Setup S8).
   - **Fakeout (Trap)**: Price Breaking Out + **Falling Open Interest** $\implies$ Short covering only. As soon as stops are cleared, price collapses back into value.
4. **Tab 2 (Footprint)**: Look for **Trap (`trap`)** signal at the breakout candle. If high buy volume traded at the candle extreme but closed in the lower 50% of the bar, buyers are trapped.

#### Data-Driven Entry Formulation:
* **To Trade the Breakout (Continuation — S8)**:
  * Only when: OI is expanding, Spot CVD is leading, and price closes a full 15m bar outside the Day Value Area (`VAH`).
  * Entry: Limit order on the **retest of broken VAH / old resistance**.
* **To Fade the Breakout (The Trap Trade — S6)**:
  * Only when: Footprint prints `trap` or `exh`, OI drops, and 15m candle closes back inside the prior Value Area.
  * Entry: Limit sell at the failure bar close or 50% wick retest.
  * Target: Value Area Midline (Day POC).

---

### Setup R-03: Double Top / Double Bottom (W & M Patterns)

```text
Retail Concept: "Price printed a 'W' double bottom; enter long when price breaks above the middle neckline."
Microstructure Reality: Waiting for the neckline break sacrifices 50%–70% of the trade's R-multiple.
Order flow detects the bottom AT THE EXACT SECOND TAP via delta divergence.
```

#### Order-Flow Confirmation Checklist (Data Points Required):
1. **Tab 2 (Footprint Bar Delta)**: On Tap 1, aggressive selling drives price down (large negative delta). On Tap 2, price reaches the same price or slightly lower, but **Bar Delta is significantly less negative or flips positive** (`div` or `sdiv` signal).
2. **Tab 6 (Cumulative Volume Delta)**: **Bullish Absorption Divergence** — Price made an equal low, but Spot CVD printed a higher low. Passive buyers absorbed all aggressive market sell orders.
3. **Tab 1 (Day VWAP Z-Score)**: Double bottom occurs at an extreme statistical discount: **$z \le -2.0\sigma$ or $-3.0\sigma$ VWAP lower band**.
4. **Tab 1 (RSI Divergence)**: H1/M15 RSI prints higher low while price prints equal/lower low.
5. **Tab 4 (Liquidation Heatmap)**: Was Tap 2 a deliberate sweep of Tap 1's low? If Tap 2 swept the long liquidation stops by 10-20 ticks and instantly rejected, it is a textbook **Liquidation Sweep Reversal (S1)**.

#### Data-Driven Entry Formulation:
* **Entry**: Do not wait for the neckline. Enter at the **close of the 15m divergence bar** at Tap 2, or place a Post-Only Limit at 50% of the sweep wick.
* **Stop Loss**: 0.3% below the lowest sweep wick.
* **Target (Drive)**:
  * T1: Day POC (Value Area center).
  * T2: Prior neckline / Day VAH.
  * T3: Upper short liquidation cluster.
* **Expected R-Multiple**: Increases from retail 1.2R (neckline entry) to **3.5R–5.0R** (order-flow tap entry).

---

### Setup R-04: Trendline / Flag / Channel Retest (Trend Pullback)

```text
Retail Concept: "Price is in an uptrend channel and pulled back to the diagonal trendline / bull flag support; buy."
Microstructure Reality: Diagonal trendlines have zero exchange order book reality.
Price reacts to horizontal volume profiles and VWAP bands, not diagonal geometry.
```

#### Order-Flow Confirmation Checklist (Data Points Required):
1. **Tab 1 (Auction Confluence)**: Does the retail trendline or flag boundary align with a **structural horizontal node**?
   - Confluence with **Day POC**, **Session POC**, or **Day VWAP $-1\sigma$ band**.
   - If the trendline is floating in low-volume air, it has zero structural support and will fail.
2. **Tab 1 (Trend Alignment)**: Check **H4 & D1 Fib-Prime EMA Stacks**:
   - $EMA13 > EMA89 > EMA233$ on H4 and D1. Both slopes must be upward.
3. **Tab 2 (Footprint Exhaustion)**: On the pullback to the trendline, **selling volume must dry up** (`exh` signal, volume $< 50\%$ 10-bar average). Aggressive sellers are exhausted.
4. **Tab 5 (Book Walls)**: Depth Imbalance Ratio within $\pm 1\%$ must show **bids loading (+5m delta positive)** in front of the zone.
5. **Tab 1 (Regime)**: Market must be in `TREND_UP` (Tab 7). In `RANGE_BALANCE`, bull flags fail $\approx 68\%$ of the time.

#### Data-Driven Entry Formulation (Setup S7):
* **Entry Ladder**: 3-tier limit ladder across the confluence node:
  * $L_1$ (40%): At the Day/Session POC.
  * $L_2$ (40%): At the Day VWAP $-1\sigma$ band.
  * $L_3$ (20%): At the structural absorption low.
* **Stop Loss**: 0.5% below the absorption low / beyond the $-2\sigma$ VWAP band.
* **Target (Drive)**: T1 Day VAH $\to$ T2 Month POC $\to$ T3 Upper Liquidation Cluster.

---

### Setup R-05: RSI / Oscillator Oversold / Overbought Reversal

```text
Retail Concept: "RSI is 22 (oversold); buy immediately because price is cheap and due for a bounce."
Microstructure Reality: In strong trending or cascading markets, RSI can stay < 30 for days while price drops 20%.
Buying purely on oversold oscillator readings is the #1 knife-catching account killer.
```

#### Order-Flow Confirmation Checklist (Data Points Required):
1. **Tab 8 & Tab 4 (Cascade Climax Gate — Gate 8)**:
   - Check `Liq 5m`. If **`Liq 5m > $500k`**, a liquidation cascade is actively raging. **BUYING IS BANNED**. You must wait for the cascade to exhaust.
2. **Tab 1 (VWAP Extension)**: Price must be at least **$|z| \ge 2.0\sigma$ or $3.0\sigma$** away from Day VWAP.
3. **Tab 1 (Crowded Funding APR)**:
   - Funding APR must be heavily negative ($< -20\%$ to $-50\%$), indicating shorts are aggressively paying longs to hold positions (short squeeze fuel).
4. **Tab 2 (Footprint Reversal Proof)**:
   - **MANDATORY**: There MUST be a footprint confirmation: **Absorption (`abs`)**, **Strong Divergence (`sdiv`)**, or an **Exhaustion Wick (`exh`)** where the candle closed in the upper half with positive delta.
   - *Zero Proof = Zero Trade* (Watching only).
5. **Tab 6 (CVD Divergence)**: Perp CVD continuing down while Spot CVD flattens or ticks up (smart money accumulating).

#### Data-Driven Entry Formulation (Setup S5):
* **Entry**: Limit order placed at the **confirmation bar close** or 50% retrace of the exhaustion wick.
* **Stop Loss**: $0.5\times$ ATR beyond the extreme wick low.
* **Target (Drive)**: Day VWAP Mean (mean-reversion magnet). Must yield at least $\ge 1.50\text{R}$ to VWAP.

---

### Setup R-06: Moving Average Crossover (Golden Cross / 9×21 EMA Pullback)

```text
Retail Concept: "9 EMA crossed 21 EMA bullishly; enter long on the next bar open."
Microstructure Reality: Moving averages lag price. By the time a crossover prints on M15/H1, price is already
overextended into resistance and retail buys the top tick.
```

#### Order-Flow Confirmation Checklist (Data Points Required):
1. **Tab 1 & Tab 7 (Regime Filter)**:
   - Check `regime`. If regime is `RANGE_BALANCE`, **ALL MA CROSSOVERS ARE DISCARDED** (whipsaw rate is $> 80\%$).
   - MA setups are authorized ONLY in `TREND_UP` or `TREND_DOWN`.
2. **Tab 1 (Z-Score Chase Guard)**:
   - If $|z| \ge 2.0\sigma$, **CHASING IS BANNED**. Even if MA crossed, price is statistically overextended. Must wait for pullback to VWAP.
3. **Tab 3 & Tab 5 (Whale Wall Clearance)**:
   - Check nearest opposing whale wall. There must be NO opposing wall $\ge \$5\text{M}$ within $1.5\text{R}$ of entry.
4. **Tab 9 (Delta Basis & Spread)**:
   - Check Delta Exchange India CLOB spread ($< 0.05\%$) and basis offset ($|basisPct| < 0.5\%$). Ensure high spread does not consume MA profit margin.

#### Data-Driven Entry Formulation:
* **Entry**: Never buy the crossover market bar. Wait for the **pullback to the EMA13 / Day VWAP mean** (Setup S7).
* **Stop Loss**: Structural invalidation below the EMA89 structural baseline.
* **Target**: Same-direction liquidation pool (Tab 4).

---

### Setup R-07: Liquidity Sweep / "Smart Money Concept" (SMC / CHoCH / Stop Hunt)

```text
Retail Concept: "Previous Day High was swept, price broke structure (CHoCH) on 1m chart; short the fair value gap."
Microstructure Reality: 1-minute CHoCH is random market noise. Real institutional sweeps happen on 3d/7d
liquidation pools and can be measured in exact millions of dollars on Coinglass telemetry.
```

#### Order-Flow Confirmation Checklist (Data Points Required):
1. **Tab 4 (Liq Levels / LSR Magnet Gate — D12 & Gate 3)**:
   - Quantify the swept pool: Was it a genuine cluster? **Cluster Notional must be $\ge \$5\text{M}$** or Strength $\ge 50$.
   - **Liquidation Skew Ratio (LSR)**: Prior to the sweep, LSR was $\ge 2.5:1$.
2. **Tab 2 (Footprint Delta Flip)**:
   - The sweep candle prints massive green taker volume (retail stops triggering at market ask), but **closes back below the swept high**.
   - The immediate follow-up candle prints **aggressive negative delta** (institutional short re-injection).
3. **Tab 1 (Auction Re-entry)**:
   - Price must close a full 15m candle back inside the Day Value Area (`VAH`).
4. **Tab 6 (CVD Delta Confirmation)**:
   - Perp CVD surges to a new high (trapped long retail), while Spot CVD fails to make a new high $\implies$ **Bearish Exhaustion Divergence**.

#### Data-Driven Entry Formulation (Setup S1 — Pristine Institutional Archetype):
* **Entry**:
  * Limit order placed at the **15m close back inside value**, or limit at **50% retrace of the sweep wick**.
* **Stop Loss**:
  * 0.3%–0.5% above the absolute high of the sweep wick (structural invalidation).
* **Target (Drive)**:
  * T1: Day POC (Value Area center — 40% scale).
  * T2: Opposite Day VAL (40% scale).
  * T3: Lower long liquidation cluster (20% runner).
* **Quality Grade**: **Grade A+** eligible. Provides the highest win rate ($> 68\%$) and highest asymmetric R-multiples ($> 3.0\text{R}$).

---

### Setup R-08: Range Breakout / Opening Range Breakout (ORB)

```text
Retail Concept: "Mark high and low of the first 30 minutes of session; buy if price breaks high, sell if breaks low."
Microstructure Reality: Over 60% of opening range breakouts are false expansions that re-enter the range,
chopping up retail breakout orders.
```

#### Order-Flow Confirmation Checklist (Data Points Required):
1. **Tab 5 (Wall-Pull Detection — Setup S4)**:
   - Did the breakout occur because a **confirmed resting whale wall was PULLED**? (`wallPullEvents`). When a wall pulls, an order book vacuum opens, allowing price to surge effortlessly.
2. **Tab 4 & Tab 1 (Open Interest & Volume Expansion)**:
   - Volume on the breakout candle must be **$\ge 1.5\times$ 10-bar average**.
   - Open Interest must be **EXPANDING** (+1% to +5% on 4H). Breakouts with falling OI are fakeouts.
3. **Tab 6 (CVD Alignment)**:
   - Both Spot CVD and Perp CVD must slope aggressively in the breakout direction.
4. **Tab 13 (Options Gamma Regime — BTC/ETH)**:
   - **Negative Gamma**: Market makers amplify moves $\implies$ Breakout succeeds (favors S4/S8).
   - **Positive Gamma**: Market makers suppress volatility $\implies$ Breakout fails (favors mean reversion S2).

#### Data-Driven Entry Formulation:
* **Entry**:
  * Conservative: Wait for the breakout bar to close, then place a limit order on the **retest of the broken range boundary**.
* **Stop Loss**:
  * Inside edge of the broken boundary (if price re-enters the range, thesis is immediately invalidated).
* **Target (Drive)**:
  * Next major liquidation cluster or $\pm 2.0\sigma$ VWAP band.

---

## PART 4. MASTER SYNTHESIS: RETAIL vs. ORDER-FLOW DECISION MATRIX

| Retail Setup Name | Primary Retail Indicator | Fatal Retail Failure Mode | Terminal Order-Flow Confirmation Telemetry | Institutional Setup Code | Minimum Required Confluence |
| :--- | :--- | :--- | :--- | :---: | :---: |
| **S/R Bounce** | Horizontal Line touch | Liquidity already exhausted; stops wiped | Tab 5 Confirmed Bid Wall $\ge \$5\text{M}$ + Tab 2 `abs` + Tab 1 POC | **S3 / S2** | $\ge 5.0\text{ pts}$ (Grade B) |
| **S/R Breakout** | Green breakout bar | Buying into institutional Ask Wall | Tab 5 Wall-Pull + Tab 1 Expanding OI + Spot CVD Lead | **S4 / S8** | $\ge 6.5\text{ pts}$ (Grade A) |
| **Double Bottom (W)**| Neckline breakout | Terrible R-multiple; late entry | Tab 2 Footprint Delta Divergence + Tab 6 Spot CVD Absorption | **S1 / S6** | $\ge 7.0\text{ pts}$ (Grade A+) |
| **Trendline Retest** | Diagonal trendline touch | Floating in low-volume air | Tab 1 Day/Session POC + VWAP $-1\sigma$ + Tab 2 `exh` | **S7** | $\ge 6.0\text{ pts}$ (Grade A) |
| **RSI Oversold** | RSI $< 30$ | Buying into raging liquidation cascade | Tab 4 `Liq 5m < $500k` + Tab 1 $|z| \ge 2.0\sigma$ + Tab 2 `abs`/`trap` | **S5** | $\ge 5.5\text{ pts}$ (Grade B/A) |
| **MA Crossover** | 9 EMA crosses 21 EMA | Lagging indicator; buying top of chop | Tab 7 `TREND_UP` regime + Tab 1 Pullback to VWAP ($|z| < 1.0$) | **S7** | $\ge 5.0\text{ pts}$ (Grade B) |
| **SMC Liquidity Sweep**| 1m CHoCH market structure | 1m noise; swept level had zero liquidity | Tab 4 Cluster $\ge \$5\text{M}$ swept + 15m close back in value + Delta flip | **S1** | $\ge 7.5\text{ pts}$ (Grade A+) |
| **Range Breakout (ORB)**| High/Low session break | Whipsaw false breakout in positive GEX | Tab 5 Wall-Pull + Tab 14 Negative GEX + Retest of boundary | **S4** | $\ge 6.0\text{ pts}$ (Grade A) |

---
*END OF DATA POINT INVENTORY & RETAIL CONFIRMATION SPECIFICATION (v2.2.0)*
