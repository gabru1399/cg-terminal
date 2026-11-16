# CG Order-Flow Terminal — Canonical Telemetry Data Point Inventory
**Specification Version**: 2.1.0  
**Coverage**: CURATED 61 Assets (30 Crypto USDT-M + 28 TradFi Perps + 3 Classic Indices)  
**Execution Venue**: Delta Exchange India (`india_prod`, Account #26902927)

---

## Architecture: The Real-Time 3-Tier Ladder
Every displayed data point originates from the fastest reliable tier:
* **Tier 0 · Live WebSocket (sub-100ms)**: Browser direct connection to `wss://fstream.binance.com` (`<sym>usdt@bookTicker` and `<sym>usdt@trade`). Single connection with dynamic subscribe/unsubscribe, 5s watchdog, 10 Hz render throttle.
* **Tier 1 · REST Engine (250ms–1.2s)**: Server-side poller to `fapi.binance.com` for L2 order book top-1000 depth, ticker fallbacks, and wall change scanners.
* **Tier 2 · Coinglass Aggregator (3s–30s)**: Multi-exchange aggregates across Binance, OKX, Bybit, Coinbase, and Hyperliquid.

---

## 1. TAB 1: OVERVIEW (`Overview`)
Provides the macro structural auction profile, multi-timeframe trend context, volatility regime, and aggregate funding metrics.

### 1.1 Header & Ticker Telemetry
* `symbol` / `market`: Standardized ticker identifier (e.g., `BTCUSDT`, `MSFTBUSD`).
* `lastPrice`: Real-time mid/trade price from Tier 0 WebSocket (Binance lead).
* `change24h` & `change24hPercent`: 24-hour nominal and percentage price displacement.
* `high24h` / `low24h`: 24-hour absolute session boundaries.
* `volume24hUsd`: 24-hour aggregated taker volume across all covered exchanges (in USD).
* `turnover24h`: Nominal base asset turnover.
* `tierActiveBadge`: Visual latency indicator confirming active data tier (`WS 0`, `REST 1`, `CG 2`).

### 1.2 Multi-Timeframe Auction Profiler (AMT)
Computed for three distinct anchor sessions: **Session 8h**, **UTC Day (24h)**, and **UTC Month**:
* `VAL` (Value Area Low): 70% volume distribution lower boundary.
* `POC` (Point of Control): Exact price tick containing the maximum executed volume.
* `VAH` (Value Area High): 70% volume distribution upper boundary.
* `VA_WidthPercent`: Value Area spread `(VAH - VAL) / POC * 100` (determines compression vs expansion regime).
* `profileType`: Auction shape classification (`D-shape` = balanced, `P-shape` = short covering/buying climax, `b-shape` = liquidation/long liquidation, `B-shape` = dual balance).

### 1.3 Day VWAP & Volatility Bands
* `vwap`: Volume-Weighted Average Price anchored to 00:00:00 UTC.
* `vwapUpper1`, `vwapUpper2`, `vwapUpper3`: +1.0σ, +2.0σ, +3.0σ standard deviation bands.
* `vwapLower1`, `vwapLower2`, `vwapLower3`: -1.0σ, -2.0σ, -3.0σ standard deviation bands.
* `zScore`: Statistical distance `(lastPrice - vwap) / stdDev` (flags mean-reversion extensions when $|z| \ge 2.0\sigma$).
* `regime`: `PREMIUM` (Price > VWAP), `DISCOUNT` (Price < VWAP), or `EXTREME_EXTENSION` ($|z| \ge 2.5\sigma$).

### 1.4 Multi-Timeframe Trend & Momentum Matrix
Calculated across 4 standard intervals (`15m`, `1h`, `4h`, `1d`):
* `ema13`: 13-period Exponential Moving Average (tactical micro-trend).
* `ema89`: 89-period Exponential Moving Average (structural macro-trend).
* `ema233`: 233-period Exponential Moving Average (institutional cycle baseline).
* `trendState`: `BULLISH_STACK` ($EMA13 > EMA89 > EMA233$), `BEARISH_STACK` ($EMA13 < EMA89 < EMA233$), or `CHOP_COMPRESSION`.
* `rsi14`: 14-period Relative Strength Index (evaluates oversold $< 30$ and overbought $> 70$).

### 1.5 Derivatives Context & Funding
* `openInterestUsd`: Total open contracts multiplied by mark price across all venues.
* `oiChange24hPercent`: 24-hour expansion or contraction in open commitments.
* `fundingRate`: Current 8-hour predicted funding rate (annualized % equivalent).
* `longShortRatio`: Taker volume / account ratio of accounts net long vs net short.

---

## 2. TAB 2: FOOTPRINT (`Footprint`)
Provides microstructural inside-the-bar order execution analysis, decomposing candle volume into executed buyer and seller aggression.

### 2.1 Per-Bar Footprint Metrics
* `barTimestamp` / `interval`: Timestamp and time-bucket duration (15m standard, auto-volume, auto-range).
* `open`, `high`, `low`, `close`: Classical OHLC candle boundaries.
* `totalVolumeUsd`: Cumulative executed notional inside the candle.
* `buyVolumeUsd`: Aggressive taker buying volume (executed at ask).
* `sellVolumeUsd`: Aggressive taker selling volume (executed at bid).
* `deltaUsd`: Net taker flow `buyVolumeUsd - sellVolumeUsd`.
* `deltaPercent`: Relative imbalance `(deltaUsd / totalVolumeUsd) * 100`.
* `barPOC`: Price level within the specific candle that traded the largest volume.
* `barVAL` / `barVAH`: Intra-bar 70% value boundaries.

### 2.2 Microstructure Signal Engine
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

## 3. TAB 3: LARGE ORDERS (`Large Orders`)
Tracks resting institutional liquidity and executed block trades across the aggregated venue books.

### 3.1 Resting Whale Limit Walls
* `orderId` / `hash`: Unique identifier of the resting order.
* `exchange`: Originating exchange (`Binance`, `OKX`, `Bybit`, etc.).
* `side`: `BID` (resting support) or `ASK` (resting resistance).
* `price`: Exact limit price where the wall is posted.
* `notionalUsd`: Total USD size of the resting order.
* `distancePercent`: Percentage distance from current mark price `(orderPrice - lastPrice) / lastPrice * 100`.
* `wallAge`: Duration the order has rested on the book without being cancelled.
* `wallStatus`: `RESTING`, `PARTIALLY_FILLED`, or `TOUCHED` (tested by market price).

### 3.2 Executed Block Trades (Tape Whales)
* `tradeTimestamp`: Millisecond execution timestamp.
* `tradeSizeUsd`: Notional value of the single executed trade (filtered $\ge \$100\text{k}$ alts, $\ge \$500\text{k}$ BTC).
* `executionSide`: `BUY` (aggressed into ask) or `SELL` (aggressed into bid).
* `executionPrice`: Executed trade price.
* `executedImbalance`: Rolling ratio of whale buy notional vs whale sell notional over 1h, 4h, and 24h.

---

## 4. TAB 4: LIQUIDATION LEVELS (`Liq Levels`)
Tracks the liquidation landscape, modeling forced liquidation price clusters that act as market magnets.

### 4.1 Liquidation Clusters (3d / 7d / 30d Lookbacks)
* `timeHorizon`: Historical accumulation window (`3-Day`, `7-Day`, `30-Day`).
* `clusterPrice`: Price level where liquidation exposure is concentrated.
* `clusterNotionalUsd`: Estimated total forced liquidation value (USD millions) at that price.
* `liquidationSide`:
  * `LONG_LIQUIDATION`: Trapped long traders whose forced selling creates a downside magnet.
  * `SHORT_LIQUIDATION`: Trapped short traders whose forced buying creates an upside magnet.
* `distanceToClusterPercent`: Distance from current mark price.
* `clusterDensityRatio`: Notional density relative to local 24-hour volume.

### 4.2 Liquidation Skew & Magnet Gate
* `longLiqTotalUsd`: Total estimated long liquidation exposure within $\pm 4\%$.
* `shortLiqTotalUsd`: Total estimated short liquidation exposure within $\pm 4\%$.
* `liquidationSkewRatio`: Ratio of dominant side to minority side (e.g., $Short / Long$).
* `magnetGateStatus`: When Skew $\ge 2.5:1$, passive front-running is prohibited; execution must await cluster sweep.

---

## 5. TAB 5: BOOK WALLS (`Book Walls`)
Depth-of-book telemetry quantifying order book imbalances, depth migration, and spoofing detection.

### 5.1 Order Book Depth & Imbalance
* `bandInterval`: Depth calculation band ($\pm 0.5\%$, $\pm 1.0\%$, $\pm 2.0\%$, $\pm 5.0\%$).
* `bidDepthUsd`: Total resting bid notional within the band.
* `askDepthUsd`: Total resting ask notional within the band.
* `depthImbalanceRatio`: `(bidDepth - askDepth) / (bidDepth + askDepth)`.
* `imbalanceDelta5m`: Net shift in imbalance compared to 5 minutes ago (detects wall loading/pulling).

### 5.2 Dynamic Wall Scanner & Event Feed
* `confirmedWallList`: Active institutional walls verified across multiple polling cycles.
* `wallAddEvents`: New large orders injected into the order book within the last 5 minutes.
* `wallPullEvents`: Cancelled or pulled orders (identifies spoofing liquidity).
* `wallFillEvents`: Order depth consumed by active market orders.

---

## 6. TAB 6: CUMULATIVE VOLUME DELTA (`CVD`)
Cumulative volume delta engine isolating spot market accumulation from leveraged perp market aggression.

### 6.1 Multi-Venue CVD Streams
* `perpCvd`: Cumulative Taker Delta for perpetual futures contracts.
* `spotCvd`: Cumulative Taker Delta for physical spot markets (Binance, Coinbase).
* `takerBuySharePercent`: Percentage of total volume driven by aggressive buyers.
* `cvdAnchor`: Accumulation anchor period (`Session`, `UTC Day`, `Rolling 7-Day`).

### 6.2 Structural Divergence Telemetry
* `divergenceType`:
  * `BULLISH_ABSORPTION`: Spot CVD rising while Perp CVD and Price are falling or flat.
  * `BEARISH_EXHAUSTION`: Perp CVD aggressively surging into new highs while Spot CVD fails to confirm.
  * `LEVERAGE_DRIVEN`: Rapid price expansion accompanied exclusively by Perp CVD spike and OI surge (fragile).
* `cvdSlope`: Rate of change ($\Delta CVD / \Delta t$) over 5m, 15m, and 1h intervals.

---

## 7. TAB 7: BACKTEST (`Backtest`)
Historical strategy evaluation engine validating playbook setups against archival tick and footprint data.

### 7.1 Playbook Strategy Configurations
* `strategyId`: Target playbook setup (`S1_SWEEP_REVERSAL`, `S2_TREND_POC_RETEST`, `S3_VWAP_EXTENSION`).
* `assetCohort`: Curated 61 asset selection or sector filter.
* `testWindow`: Historical backtest date range.
* `riskPerTrade`: Fixed percentage risk model ($\le 1.0\%$).

### 7.2 Performance & Risk Metrics
* `winRate`: Percentage of completed trades hitting Take Profit.
* `profitFactor`: Gross profits divided by gross losses.
* `sharpeRatio`: Risk-adjusted excess return over standard deviation.
* `maxDrawdownPercent`: Maximum peak-to-trough equity decline.
* `averageRMultiple`: Average realized $R$ return per trade.
* `expectancy`: Statistical edge $EV = (Win\% \times R_{win}) - (Loss\% \times 1.0R)$.

---

## 8. TAB 8: ALERTS & NOTIFICATIONS (`Alerts`)
Real-time asynchronous notification and cursor-based event queue.

### 8.1 Event Telemetry Fields
* `eventId`: Unique monotonic event UUID.
* `timestamp`: ISO-8601 event generation timestamp.
* `source`: Telemetry generator (`footprint`, `indicators`, `whale-orders`, `liqlevels`, `cvd`, `engine`).
* `severity`: `HIGH` (trade-formulation trigger), `MEDIUM`, or `INFO`.
* `symbol`: Triggering ticker symbol.
* `message`: Human- and agent-readable event description.
* `cursorPosition`: Monotonic cursor sequence saved in `data/mcp-cursor.json`.

---

## 9. TAB 9: LIVE L2 & TICKET WS (`Live L2 & Ticket WS`)
Real-time microstructural order book visualizer and execution venue bridge.

### 9.1 Live L2 Depth Ladder
* `bids`: Top 1,000 bids sorted descending by price `[price, size, cumulativeNotional]`.
* `asks`: Top 1,000 asks sorted ascending by price `[price, size, cumulativeNotional]`.
* `spreadUsd`: Absolute difference between best bid and best ask `(bestAsk - bestBid)`.
* `spreadBps`: Bid-Ask spread expressed in basis points `(spreadUsd / midPrice) * 10,000`.
* `midPrice`: Computed midpoint `(bestBid + bestAsk) / 2`.
* `bookDepthCoveragePercent`: Nominal price coverage range captured by top-1,000 levels ($\approx \pm 0.2\%$ on BTC).

### 9.2 Execution Ticket Bridge (Delta Exchange India)
* `orderType`: Post-Only Limit (`limit`, `post_only: true`). Zero taker execution allowed.
* `contractSize`: Minimum order increment and lot multiplier (Delta specification).
* `marginRequiredUsd`: Initial margin required to open order.
* `bracketStopLoss`: Stop loss trigger price (evaluates against `mark_price`).
* `bracketTakeProfit`: Take profit limit/market price.
* `executionStatus`: Live state on Delta Exchange India CLOB (`open`, `filled`, `cancelled`).
