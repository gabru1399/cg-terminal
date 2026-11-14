# CRYPTO DOMAIN 360° SCREENING & DEEP TELEMETRY REPORT (DELTA EXCHANGE EDITION)

**Round**: `R274`  
**Domain Analyst**: `@delta-crypto-7`  
**Lead Formulator & Executioner**: `@delta-lead-7`  
**Adversarial Auditor**: `@delta-auditor-7`  
**Swarm Sentinel**: `@delta-sentinel-4`  
**Timestamp**: 2026-11-14 17:58:40 UTC  
**Execution Venue**: Delta Exchange India (`api.india.delta.exchange`, Account 26902927, india_prod)  
**Coverage**: All 30 Curated Crypto USDT-M Perps (`src/lib/universe/curated.ts`) · 100% Zero-Mock Coinglass Live API + Delta Exchange CLOB  
**Specification**: `desk/TRADE_FORMULATION_MANUAL.md` v1.1.0 & Canonical Playbook (10 Nov 2026)  

---

## 1. Executive Summary

In Round R274 of the 360° Autonomous Delta Exchange Execution Swarm, `@delta-crypto-7` executed the complete **Tier A Narrative Sweep** across all **30 crypto USDT-M perp assets**, ingested live telemetry across the **16 Telemetry Data Dimensions**, and performed canonical **Table 7 Confluence Scoring** with strict zero-fallback rules grounded directly in Delta Exchange CLOB market microstructure.

- **Total Assets Swept**: 30 / 30 (100% Live Coinglass + Delta Exchange API Telemetry, Zero Mocks)
- **Delta Listed Perpetuals**: **27 / 30 assets** mapped directly to Delta perpetual futures (`BTCUSD`, `ETHUSD`, `BNBUSD`, `SOLUSD`, `XRPUSD`, etc.). Only 3 assets (ATOM, ICP, VET) lack Delta perp listings.
- **Tier B Qualifiers Isolated**: **29 assets** meeting canonical qualification criteria.
- **High-Confluence Delta Trade Candidates (Grade B, Score ≥ 5.0 pts, Spread < 0.15%)**: **1 assets** across Delta Exchange.
- **Market Microstructure Posture**: Macro downtrend (`TREND_DOWN`) dominates the crypto universe. Mean-reversion bounces continue to develop toward the desk's resting limit sell levels at Day VAH/POC on ETH, LINK, SUI, and LTC.

---

## 2. Tier A Full-Universe Screening Table (All 30 Crypto Assets)

| Symbol | Sector | Price | Regime | Dir | Grade | Conf % | M1/M2 Status | VWAP z-score | ±2% LSR (Dominant) | Delta Contract (Spread %) | Active Vetoes | Qualifier? |
| :--- | :--- | :--- | :--- | :--- | :--- | :--- | :--- | :--- | :--- | :--- | :--- | :--- |
| **BTC** | Store of Value | $65,763.1000 | `TREND_DOWN` | **SHORT** | `VETO` | 92% | `M1:TRIGGERED` | -0.97σ | **1.7:1 (SA)** | BTCUSD (0.0008%) | Table 7 score 3.0 < 5.0 — HARD V... | **YES** |
| **ETH** | Smart Contract L1 | $1,839.1700 | `TREND_DOWN` | **SHORT** | `VETO` | 88% | `M1:TRIGGERED` | -1.06σ | **1.8:1 (SA)** | ETHUSD (0.0027%) | Table 7 score 3.0 < 5.0 — HARD V... | **YES** |
| **BNB** | Exchange Token | $590.5200 | `TREND_DOWN` | **SHORT** | `VETO` | 92% | `M1:TRIGGERED` | -1.27σ | **1.6:1 (LB)** | BNBUSD (0.0034%) | Table 7 score 4.0 < 5.0 — HARD V... | **YES** |
| **SOL** | Smart Contract L1 | $72.7500 | `TREND_DOWN` | **SHORT** | `VETO` | 92% | `M1:TRIGGERED` | -1.49σ | **1.9:1 (LB)** | SOLUSD (0.0151%) | Table 7 score 4.0 < 5.0 — HARD V... | **YES** |
| **XRP** | Payments | $0.9598 | `TREND_DOWN` | **SHORT** | `VETO` | 92% | `M1:TRIGGERED` | -1.56σ | **1.1:1 (SA)** | XRPUSD (0.0208%) | Table 7 score 3.0 < 5.0 — HARD V... | **YES** |
| **ADA** | Smart Contract L1 | $0.1555 | `TREND_DOWN` | **SHORT** | `VETO` | 92% | `M1:TRIGGERED` | -1.40σ | **1.1:1 (LB)** | ADAUSD (0.1670%) | Delta spread 0.1670% > 0.15% — e... | **YES** |
| **DOGE** | Meme | $0.0603 | `TREND_DOWN` | **SHORT** | `VETO` | 92% | `M1:TRIGGERED` | -1.30σ | **1.7:1 (LB)** | DOGEUSD (0.0331%) | Table 7 score 3.0 < 5.0 — HARD V... | **YES** |
| **TRX** | Smart Contract L1 | $0.3070 | `TREND_DOWN` | **SHORT** | `VETO` | 45% | `M1:WAIT_PULLBACK` | -2.13σ | **10.3:1 (LB)** | TRXUSD (0.0065%) | LSR 10.3:1 (LB) >= 2.5:1 — passi... | **YES** |
| **LINK** | Oracle | $9.1680 | `TREND_DOWN` | **SHORT** | `VETO` | 92% | `M1:TRIGGERED` | -1.27σ | **2.1:1 (SA)** | LINKUSD (0.0218%) | Table 7 score 3.0 < 5.0 — HARD V... | **YES** |
| **LTC** | Payments | $45.6800 | `TREND_DOWN` | **SHORT** | `VETO` | 92% | `M1:TRIGGERED` | -1.35σ | **1.3:1 (SA)** | LTCUSD (0.0437%) | Table 7 score 3.0 < 5.0 — HARD V... | **YES** |
| **AVAX** | Smart Contract L1 | $7.4780 | `TREND_DOWN` | **SHORT** | `VETO` | 92% | `M1:TRIGGERED` | -1.70σ | **5.6:1 (LB)** | AVAXUSD (0.0803%) | LSR 5.6:1 (LB) >= 2.5:1 — passiv... | **YES** |
| **DOT** | Interoperability | $0.7526 | `TREND_DOWN` | **SHORT** | `VETO` | 92% | `M1:TRIGGERED` | -1.44σ | **1.7:1 (LB)** | DOTUSD (0.1328%) | Table 7 score 2.0 < 5.0 — HARD V... | **YES** |
| **NEAR** | Smart Contract L1 | $3.1210 | `TREND_DOWN` | **SHORT** | `VETO` | 92% | `M1:TRIGGERED` | -1.46σ | **83.8:1 (LB)** | NEARUSD (0.0960%) | LSR 83.8:1 (LB) >= 2.5:1 — passi... | **YES** |
| **UNI** | DeFi DEX | $5.0200 | `TREND_DOWN` | **SHORT** | `VETO` | 88% | `M1:TRIGGERED` | -1.33σ | **1.4:1 (SA)** | UNIUSD (0.0597%) | Table 7 score 1.5 < 5.0 — HARD V... | **YES** |
| **ATOM** | Interoperability | $1.2910 | `TREND_DOWN` | **SHORT** | `VETO` | 92% | `M1:TRIGGERED` | -1.79σ | **17.0:1 (LB)** | NOT LISTED | LSR 17.0:1 (LB) >= 2.5:1 — passi... | **YES** |
| **XLM** | Payments | $0.1363 | `TREND_DOWN` | **SHORT** | `VETO` | 92% | `M1:TRIGGERED` | -1.73σ | **4.3:1 (LB)** | XLMUSD (0.0220%) | LSR 4.3:1 (LB) >= 2.5:1 — passiv... | **YES** |
| **ETC** | Smart Contract L1 | $6.0830 | `TREND_DOWN` | **SHORT** | `VETO` | 92% | `M1:TRIGGERED` | -1.02σ | **2.2:1 (SA)** | ETCUSD (0.0492%) | Table 7 score 2.0 < 5.0 — HARD V... | **YES** |
| **FIL** | Storage | $0.6462 | `TREND_DOWN` | **SHORT** | `VETO` | 45% | `M1:WAIT_PULLBACK` | -2.04σ | **69.9:1 (LB)** | FILUSD (0.0309%) | LSR 69.9:1 (LB) >= 2.5:1 — passi... | **YES** |
| **ICP** | Smart Contract L1 | $2.2830 | `TREND_DOWN` | **SHORT** | `VETO` | 92% | `M1:TRIGGERED` | -1.77σ | **11.6:1 (LB)** | NOT LISTED | LSR 11.6:1 (LB) >= 2.5:1 — passi... | **YES** |
| **HBAR** | Enterprise L1 | $0.0581 | `TREND_DOWN` | **SHORT** | `VETO` | 92% | `M1:TRIGGERED` | -1.39σ | **1.0:1 (LB)** | HBARUSD (0.0515%) | Table 7 score 1.5 < 5.0 — HARD V... | **YES** |
| **APT** | Smart Contract L1 | $0.4745 | `TREND_DOWN` | **SHORT** | `VETO` | 92% | `M1:TRIGGERED` | -1.40σ | **24.7:1 (LB)** | APTUSD (0.0420%) | LSR 24.7:1 (LB) >= 2.5:1 — passi... | **YES** |
| **ARB** | Ethereum L2 | $0.1345 | `TREND_DOWN` | **SHORT** | `VETO` | 92% | `M1:TRIGGERED` | -1.59σ | **214.6:1 (LB)** | ARBUSD (0.0148%) | LSR 214.6:1 (LB) >= 2.5:1 — pass... | **YES** |
| **OP** | Ethereum L2 | $0.0840 | `TREND_DOWN` | **SHORT** | `VETO` | 92% | `M1:TRIGGERED` | -1.35σ | **1.1:1 (LB)** | OPUSD (0.3562%) | Delta spread 0.3562% > 0.15% — e... | **YES** |
| **SUI** | Smart Contract L1 | $0.7284 | `TREND_DOWN` | **SHORT** | `VETO` | 92% | `M1:TRIGGERED` | -1.54σ | **2.1:1 (LB)** | SUIUSD (0.0411%) | Table 7 score 4.0 < 5.0 — HARD V... | **YES** |
| **SEI** | Smart Contract L1 | $0.0394 | `TREND_DOWN` | **SHORT** | `VETO` | 92% | `M1:TRIGGERED` | -1.23σ | **1.1:1 (SA)** | SEIUSD (0.0506%) | Table 7 score 1.5 < 5.0 — HARD V... | **YES** |
| **INJ** | DeFi L1 | $7.2480 | `RANGE_BALANCE` | **LONG** | `VETO` | 78% | `M2:TRIGGERED` | -1.40σ | **2.2:1 (LB)** | INJUSD (0.0550%) | Table 7 score 3.0 < 5.0 — HARD V... | No |
| **TIA** | Modular DA | $0.3516 | `TREND_DOWN` | **SHORT** | `VETO` | 92% | `M1:TRIGGERED` | -1.99σ | **9.2:1 (LB)** | TIAUSD (0.0568%) | LSR 9.2:1 (LB) >= 2.5:1 — passiv... | **YES** |
| **VET** | Supply Chain | $0.0047 | `TREND_DOWN` | **SHORT** | `VETO` | 92% | `M1:TRIGGERED` | -1.38σ | **2.8:1 (LB)** | NOT LISTED | LSR 2.8:1 (LB) >= 2.5:1 — passiv... | **YES** |
| **1000PEPE** | Meme | $0.0040 | `RANGE_BALANCE` | **LONG** | `B` | 66% | `M2:TRIGGERED` | -1.19σ | **99.0:1 (SA)** | 1000PEPEUSD (0.0101%) | LSR 99.0:1 (SA) >= 2.5:1 — passi... | **YES** |
| **1000SHIB** | Meme | $0.0040 | `TREND_DOWN` | **SHORT** | `VETO` | 92% | `M1:TRIGGERED` | -1.57σ | **4.9:1 (LB)** | 1000SHIBUSD (0.0756%) | LSR 4.9:1 (LB) >= 2.5:1 — passiv... | **YES** |

---

## 3. Tier B Qualifier Isolation & Synthesis

- **BTC** (Store of Value): Regime `TREND_DOWN` (SHORT) | T7: `3.0 pts` | Grade: `VETO` | Conf: `92%` | LSR: `1.7:1 (SA)` | Delta: `BTCUSD (0.0008%)`
- **ETH** (Smart Contract L1): Regime `TREND_DOWN` (SHORT) | T7: `3.0 pts` | Grade: `VETO` | Conf: `88%` | LSR: `1.8:1 (SA)` | Delta: `ETHUSD (0.0027%)`
- **BNB** (Exchange Token): Regime `TREND_DOWN` (SHORT) | T7: `4.0 pts` | Grade: `VETO` | Conf: `92%` | LSR: `1.6:1 (LB)` | Delta: `BNBUSD (0.0034%)`
- **SOL** (Smart Contract L1): Regime `TREND_DOWN` (SHORT) | T7: `4.0 pts` | Grade: `VETO` | Conf: `92%` | LSR: `1.9:1 (LB)` | Delta: `SOLUSD (0.0151%)`
- **XRP** (Payments): Regime `TREND_DOWN` (SHORT) | T7: `3.0 pts` | Grade: `VETO` | Conf: `92%` | LSR: `1.1:1 (SA)` | Delta: `XRPUSD (0.0208%)`
- **ADA** (Smart Contract L1): Regime `TREND_DOWN` (SHORT) | T7: `1.0 pts` | Grade: `VETO` | Conf: `92%` | LSR: `1.1:1 (LB)` | Delta: `ADAUSD (0.1670%)`
- **DOGE** (Meme): Regime `TREND_DOWN` (SHORT) | T7: `3.0 pts` | Grade: `VETO` | Conf: `92%` | LSR: `1.7:1 (LB)` | Delta: `DOGEUSD (0.0331%)`
- **TRX** (Smart Contract L1): Regime `TREND_DOWN` (SHORT) | T7: `3.5 pts` | Grade: `VETO` | Conf: `45%` | LSR: `10.3:1 (LB)` | Delta: `TRXUSD (0.0065%)`
- **LINK** (Oracle): Regime `TREND_DOWN` (SHORT) | T7: `3.0 pts` | Grade: `VETO` | Conf: `92%` | LSR: `2.1:1 (SA)` | Delta: `LINKUSD (0.0218%)`
- **LTC** (Payments): Regime `TREND_DOWN` (SHORT) | T7: `3.0 pts` | Grade: `VETO` | Conf: `92%` | LSR: `1.3:1 (SA)` | Delta: `LTCUSD (0.0437%)`
- **AVAX** (Smart Contract L1): Regime `TREND_DOWN` (SHORT) | T7: `3.0 pts` | Grade: `VETO` | Conf: `92%` | LSR: `5.6:1 (LB)` | Delta: `AVAXUSD (0.0803%)`
- **DOT** (Interoperability): Regime `TREND_DOWN` (SHORT) | T7: `2.0 pts` | Grade: `VETO` | Conf: `92%` | LSR: `1.7:1 (LB)` | Delta: `DOTUSD (0.1328%)`
- **NEAR** (Smart Contract L1): Regime `TREND_DOWN` (SHORT) | T7: `3.0 pts` | Grade: `VETO` | Conf: `92%` | LSR: `83.8:1 (LB)` | Delta: `NEARUSD (0.0960%)`
- **UNI** (DeFi DEX): Regime `TREND_DOWN` (SHORT) | T7: `1.5 pts` | Grade: `VETO` | Conf: `88%` | LSR: `1.4:1 (SA)` | Delta: `UNIUSD (0.0597%)`
- **ATOM** (Interoperability): Regime `TREND_DOWN` (SHORT) | T7: `2.5 pts` | Grade: `VETO` | Conf: `92%` | LSR: `17.0:1 (LB)` | Delta: `NOT LISTED (0.0000%)`
- **XLM** (Payments): Regime `TREND_DOWN` (SHORT) | T7: `3.5 pts` | Grade: `VETO` | Conf: `92%` | LSR: `4.3:1 (LB)` | Delta: `XLMUSD (0.0220%)`
- **ETC** (Smart Contract L1): Regime `TREND_DOWN` (SHORT) | T7: `2.0 pts` | Grade: `VETO` | Conf: `92%` | LSR: `2.2:1 (SA)` | Delta: `ETCUSD (0.0492%)`
- **FIL** (Storage): Regime `TREND_DOWN` (SHORT) | T7: `2.5 pts` | Grade: `VETO` | Conf: `45%` | LSR: `69.9:1 (LB)` | Delta: `FILUSD (0.0309%)`
- **ICP** (Smart Contract L1): Regime `TREND_DOWN` (SHORT) | T7: `2.5 pts` | Grade: `VETO` | Conf: `92%` | LSR: `11.6:1 (LB)` | Delta: `NOT LISTED (0.0000%)`
- **HBAR** (Enterprise L1): Regime `TREND_DOWN` (SHORT) | T7: `1.5 pts` | Grade: `VETO` | Conf: `92%` | LSR: `1.0:1 (LB)` | Delta: `HBARUSD (0.0515%)`
- **APT** (Smart Contract L1): Regime `TREND_DOWN` (SHORT) | T7: `3.5 pts` | Grade: `VETO` | Conf: `92%` | LSR: `24.7:1 (LB)` | Delta: `APTUSD (0.0420%)`
- **ARB** (Ethereum L2): Regime `TREND_DOWN` (SHORT) | T7: `3.5 pts` | Grade: `VETO` | Conf: `92%` | LSR: `214.6:1 (LB)` | Delta: `ARBUSD (0.0148%)`
- **OP** (Ethereum L2): Regime `TREND_DOWN` (SHORT) | T7: `1.0 pts` | Grade: `VETO` | Conf: `92%` | LSR: `1.1:1 (LB)` | Delta: `OPUSD (0.3562%)`
- **SUI** (Smart Contract L1): Regime `TREND_DOWN` (SHORT) | T7: `4.0 pts` | Grade: `VETO` | Conf: `92%` | LSR: `2.1:1 (LB)` | Delta: `SUIUSD (0.0411%)`
- **SEI** (Smart Contract L1): Regime `TREND_DOWN` (SHORT) | T7: `1.5 pts` | Grade: `VETO` | Conf: `92%` | LSR: `1.1:1 (SA)` | Delta: `SEIUSD (0.0506%)`
- **TIA** (Modular DA): Regime `TREND_DOWN` (SHORT) | T7: `3.0 pts` | Grade: `VETO` | Conf: `92%` | LSR: `9.2:1 (LB)` | Delta: `TIAUSD (0.0568%)`
- **VET** (Supply Chain): Regime `TREND_DOWN` (SHORT) | T7: `2.5 pts` | Grade: `VETO` | Conf: `92%` | LSR: `2.8:1 (LB)` | Delta: `NOT LISTED (0.0000%)`
- **1000PEPE** (Meme): Regime `RANGE_BALANCE` (LONG) | T7: `5.0 pts` | Grade: `B` | Conf: `66%` | LSR: `99.0:1 (SA)` | Delta: `1000PEPEUSD (0.0101%)`
- **1000SHIB** (Meme): Regime `TREND_DOWN` (SHORT) | T7: `3.0 pts` | Grade: `VETO` | Conf: `92%` | LSR: `4.9:1 (LB)` | Delta: `1000SHIBUSD (0.0756%)`

---

## 4. Deep Telemetry Dossier & Strict Table 7 Confluence Scoring

### BTC · Store of Value (SHORT)

- **Live Spot / Perp Price**: $65,763.1000
- **Regime / Model**: `TREND_DOWN` | Active Model: `M1:TRIGGERED` (Conf: 92%)
- **Delta Perpetual Contract**: `BTCUSD` | Contract Value: `0.001` | Tick Size: `0.5` | Mark: `$65,831.0780` | Spread: `0.0008%`
- **Table 7 Confluence Score**: **3.0 / 11.5 pts** → **Grade VETO**
  * Directional Trend (2.0 max): **0.0** — Counter-trend / No alignment (0.0 pts)
  * Auction / VWAP Regime (1.5 max): **0.0** — Discount Short / Premium Long violation (z = -0.97σ -> 0.0 pts)
  * Footprint Signal (2.0 max): **0.0** — No qualifying footprint signal at zone (0.0 pts)
  * Whale Wall Backstop (1.5 max): **1.0** — Delta L2 SELL Wall $297.0k @ 65877.0 -> 1.0 pt
  * CVD Divergence (1.0 max): **1.0** — Active BEAR CVD divergence () -> 1.0 pt
  * Liquidation Magnet Gate (1.5 max): **0.0** — Sub-threshold or unaligned skew (0.0 pts)
  * Options GEX Context (1.0 max): **0.0** — n/a (Non-BTC/ETH perpetual -> 0.0 pts)
  * Broker Spread Drag (1.0 max): **1.0** — Spread 0.0008% < 0.05% -> 1.0 pt

### ETH · Smart Contract L1 (SHORT)

- **Live Spot / Perp Price**: $1,839.1700
- **Regime / Model**: `TREND_DOWN` | Active Model: `M1:TRIGGERED` (Conf: 88%)
- **Delta Perpetual Contract**: `ETHUSD` | Contract Value: `0.01` | Tick Size: `0.05` | Mark: `$1,840.4297` | Spread: `0.0027%`
- **Table 7 Confluence Score**: **3.0 / 11.5 pts** → **Grade VETO**
  * Directional Trend (2.0 max): **0.0** — Counter-trend / No alignment (0.0 pts)
  * Auction / VWAP Regime (1.5 max): **0.0** — Discount Short / Premium Long violation (z = -1.06σ -> 0.0 pts)
  * Footprint Signal (2.0 max): **0.0** — No qualifying footprint signal at zone (0.0 pts)
  * Whale Wall Backstop (1.5 max): **1.0** — Delta L2 SELL Wall $257.1k @ 1841.50 -> 1.0 pt
  * CVD Divergence (1.0 max): **1.0** — Active BEAR CVD divergence () -> 1.0 pt
  * Liquidation Magnet Gate (1.5 max): **0.0** — Sub-threshold or unaligned skew (0.0 pts)
  * Options GEX Context (1.0 max): **0.0** — n/a (Non-BTC/ETH perpetual -> 0.0 pts)
  * Broker Spread Drag (1.0 max): **1.0** — Spread 0.0027% < 0.05% -> 1.0 pt

### BNB · Exchange Token (SHORT)

- **Live Spot / Perp Price**: $590.5200
- **Regime / Model**: `TREND_DOWN` | Active Model: `M1:TRIGGERED` (Conf: 92%)
- **Delta Perpetual Contract**: `BNBUSD` | Contract Value: `0.1` | Tick Size: `0.001` | Mark: `$590.0923` | Spread: `0.0034%`
- **Table 7 Confluence Score**: **4.0 / 11.5 pts** → **Grade VETO**
  * Directional Trend (2.0 max): **0.0** — Counter-trend / No alignment (0.0 pts)
  * Auction / VWAP Regime (1.5 max): **0.0** — Discount Short / Premium Long violation (z = -1.27σ -> 0.0 pts)
  * Footprint Signal (2.0 max): **0.0** — No qualifying footprint signal at zone (0.0 pts)
  * Whale Wall Backstop (1.5 max): **1.0** — Delta L2 SELL Wall $50.2k @ 590.420 -> 1.0 pt
  * CVD Divergence (1.0 max): **1.0** — Active BEAR CVD divergence () -> 1.0 pt
  * Liquidation Magnet Gate (1.5 max): **1.0** — Moderate directional skew (1.6:1 (LB)) -> 1.0 pt
  * Options GEX Context (1.0 max): **0.0** — n/a (Non-BTC/ETH perpetual -> 0.0 pts)
  * Broker Spread Drag (1.0 max): **1.0** — Spread 0.0034% < 0.05% -> 1.0 pt

### SOL · Smart Contract L1 (SHORT)

- **Live Spot / Perp Price**: $72.7500
- **Regime / Model**: `TREND_DOWN` | Active Model: `M1:TRIGGERED` (Conf: 92%)
- **Delta Perpetual Contract**: `SOLUSD` | Contract Value: `1.0` | Tick Size: `0.0001` | Mark: `$72.7568` | Spread: `0.0151%`
- **Table 7 Confluence Score**: **4.0 / 11.5 pts** → **Grade VETO**
  * Directional Trend (2.0 max): **0.0** — Counter-trend / No alignment (0.0 pts)
  * Auction / VWAP Regime (1.5 max): **0.0** — Discount Short / Premium Long violation (z = -1.49σ -> 0.0 pts)
  * Footprint Signal (2.0 max): **0.0** — No qualifying footprint signal at zone (0.0 pts)
  * Whale Wall Backstop (1.5 max): **1.0** — Delta L2 SELL Wall $50.7k @ 72.8200 -> 1.0 pt
  * CVD Divergence (1.0 max): **1.0** — Active BEAR CVD divergence () -> 1.0 pt
  * Liquidation Magnet Gate (1.5 max): **1.0** — Moderate directional skew (1.9:1 (LB)) -> 1.0 pt
  * Options GEX Context (1.0 max): **0.0** — n/a (Non-BTC/ETH perpetual -> 0.0 pts)
  * Broker Spread Drag (1.0 max): **1.0** — Spread 0.0151% < 0.05% -> 1.0 pt

### XRP · Payments (SHORT)

- **Live Spot / Perp Price**: $0.9598
- **Regime / Model**: `TREND_DOWN` | Active Model: `M1:TRIGGERED` (Conf: 92%)
- **Delta Perpetual Contract**: `XRPUSD` | Contract Value: `1.0` | Tick Size: `0.0001` | Mark: `$0.9602` | Spread: `0.0208%`
- **Table 7 Confluence Score**: **3.0 / 11.5 pts** → **Grade VETO**
  * Directional Trend (2.0 max): **0.0** — Counter-trend / No alignment (0.0 pts)
  * Auction / VWAP Regime (1.5 max): **0.0** — Discount Short / Premium Long violation (z = -1.56σ -> 0.0 pts)
  * Footprint Signal (2.0 max): **0.0** — No qualifying footprint signal at zone (0.0 pts)
  * Whale Wall Backstop (1.5 max): **1.0** — Delta L2 SELL Wall $57.7k @ 0.9608 -> 1.0 pt
  * CVD Divergence (1.0 max): **1.0** — Active BEAR CVD divergence () -> 1.0 pt
  * Liquidation Magnet Gate (1.5 max): **0.0** — Sub-threshold or unaligned skew (0.0 pts)
  * Options GEX Context (1.0 max): **0.0** — n/a (Non-BTC/ETH perpetual -> 0.0 pts)
  * Broker Spread Drag (1.0 max): **1.0** — Spread 0.0208% < 0.05% -> 1.0 pt

### ADA · Smart Contract L1 (SHORT)

- **Live Spot / Perp Price**: $0.1555
- **Regime / Model**: `TREND_DOWN` | Active Model: `M1:TRIGGERED` (Conf: 92%)
- **Delta Perpetual Contract**: `ADAUSD` | Contract Value: `1.0` | Tick Size: `1e-05` | Mark: `$0.1557` | Spread: `0.1670%`
- **Table 7 Confluence Score**: **1.0 / 11.5 pts** → **Grade VETO**
  * Directional Trend (2.0 max): **0.0** — Counter-trend / No alignment (0.0 pts)
  * Auction / VWAP Regime (1.5 max): **0.0** — Discount Short / Premium Long violation (z = -1.40σ -> 0.0 pts)
  * Footprint Signal (2.0 max): **0.0** — No qualifying footprint signal at zone (0.0 pts)
  * Whale Wall Backstop (1.5 max): **0.0** — No confirmed wall backstop (0.0 pts)
  * CVD Divergence (1.0 max): **1.0** — Active BEAR CVD divergence () -> 1.0 pt
  * Liquidation Magnet Gate (1.5 max): **0.0** — Sub-threshold or unaligned skew (0.0 pts)
  * Options GEX Context (1.0 max): **0.0** — n/a (Non-BTC/ETH perpetual -> 0.0 pts)
  * Broker Spread Drag (1.0 max): **0.0** — Spread 0.1670% > 0.10% -> 0.0 pts

### DOGE · Meme (SHORT)

- **Live Spot / Perp Price**: $0.0603
- **Regime / Model**: `TREND_DOWN` | Active Model: `M1:TRIGGERED` (Conf: 92%)
- **Delta Perpetual Contract**: `DOGEUSD` | Contract Value: `100.0` | Tick Size: `1e-06` | Mark: `$0.0604` | Spread: `0.0331%`
- **Table 7 Confluence Score**: **3.0 / 11.5 pts** → **Grade VETO**
  * Directional Trend (2.0 max): **0.0** — Counter-trend / No alignment (0.0 pts)
  * Auction / VWAP Regime (1.5 max): **0.0** — Discount Short / Premium Long violation (z = -1.30σ -> 0.0 pts)
  * Footprint Signal (2.0 max): **0.0** — No qualifying footprint signal at zone (0.0 pts)
  * Whale Wall Backstop (1.5 max): **0.0** — No confirmed wall backstop (0.0 pts)
  * CVD Divergence (1.0 max): **1.0** — Active BEAR CVD divergence () -> 1.0 pt
  * Liquidation Magnet Gate (1.5 max): **1.0** — Moderate directional skew (1.7:1 (LB)) -> 1.0 pt
  * Options GEX Context (1.0 max): **0.0** — n/a (Non-BTC/ETH perpetual -> 0.0 pts)
  * Broker Spread Drag (1.0 max): **1.0** — Spread 0.0331% < 0.05% -> 1.0 pt

### TRX · Smart Contract L1 (SHORT)

- **Live Spot / Perp Price**: $0.3070
- **Regime / Model**: `TREND_DOWN` | Active Model: `M1:WAIT_PULLBACK` (Conf: 45%)
- **Delta Perpetual Contract**: `TRXUSD` | Contract Value: `1.0` | Tick Size: `1e-05` | Mark: `$0.3070` | Spread: `0.0065%`
- **Table 7 Confluence Score**: **3.5 / 11.5 pts** → **Grade VETO**
  * Directional Trend (2.0 max): **0.0** — Counter-trend / No alignment (0.0 pts)
  * Auction / VWAP Regime (1.5 max): **0.0** — Discount Short / Premium Long violation (z = -2.13σ -> 0.0 pts)
  * Footprint Signal (2.0 max): **0.0** — No qualifying footprint signal at zone (0.0 pts)
  * Whale Wall Backstop (1.5 max): **0.0** — No confirmed wall backstop (0.0 pts)
  * CVD Divergence (1.0 max): **1.0** — Active BEAR CVD divergence () -> 1.0 pt
  * Liquidation Magnet Gate (1.5 max): **1.5** — Long Liq Below dominates (10.3:1 (LB)) — Target magnet aligned -> 1.5 pts
  * Options GEX Context (1.0 max): **0.0** — n/a (Non-BTC/ETH perpetual -> 0.0 pts)
  * Broker Spread Drag (1.0 max): **1.0** — Spread 0.0065% < 0.05% -> 1.0 pt

### LINK · Oracle (SHORT)

- **Live Spot / Perp Price**: $9.1680
- **Regime / Model**: `TREND_DOWN` | Active Model: `M1:TRIGGERED` (Conf: 92%)
- **Delta Perpetual Contract**: `LINKUSD` | Contract Value: `1.0` | Tick Size: `0.001` | Mark: `$9.1635` | Spread: `0.0218%`
- **Table 7 Confluence Score**: **3.0 / 11.5 pts** → **Grade VETO**
  * Directional Trend (2.0 max): **0.0** — Counter-trend / No alignment (0.0 pts)
  * Auction / VWAP Regime (1.5 max): **0.0** — Discount Short / Premium Long violation (z = -1.27σ -> 0.0 pts)
  * Footprint Signal (2.0 max): **0.0** — No qualifying footprint signal at zone (0.0 pts)
  * Whale Wall Backstop (1.5 max): **1.0** — Delta L2 SELL Wall $80.8k @ 9.154 -> 1.0 pt
  * CVD Divergence (1.0 max): **1.0** — Active BEAR CVD divergence () -> 1.0 pt
  * Liquidation Magnet Gate (1.5 max): **0.0** — Sub-threshold or unaligned skew (0.0 pts)
  * Options GEX Context (1.0 max): **0.0** — n/a (Non-BTC/ETH perpetual -> 0.0 pts)
  * Broker Spread Drag (1.0 max): **1.0** — Spread 0.0218% < 0.05% -> 1.0 pt

### LTC · Payments (SHORT)

- **Live Spot / Perp Price**: $45.6800
- **Regime / Model**: `TREND_DOWN` | Active Model: `M1:TRIGGERED` (Conf: 92%)
- **Delta Perpetual Contract**: `LTCUSD` | Contract Value: `0.1` | Tick Size: `0.01` | Mark: `$45.8099` | Spread: `0.0437%`
- **Table 7 Confluence Score**: **3.0 / 11.5 pts** → **Grade VETO**
  * Directional Trend (2.0 max): **0.0** — Counter-trend / No alignment (0.0 pts)
  * Auction / VWAP Regime (1.5 max): **0.0** — Discount Short / Premium Long violation (z = -1.35σ -> 0.0 pts)
  * Footprint Signal (2.0 max): **0.0** — No qualifying footprint signal at zone (0.0 pts)
  * Whale Wall Backstop (1.5 max): **1.0** — Delta L2 SELL Wall $55.3k @ 45.83 -> 1.0 pt
  * CVD Divergence (1.0 max): **1.0** — Active BEAR CVD divergence () -> 1.0 pt
  * Liquidation Magnet Gate (1.5 max): **0.0** — Sub-threshold or unaligned skew (0.0 pts)
  * Options GEX Context (1.0 max): **0.0** — n/a (Non-BTC/ETH perpetual -> 0.0 pts)
  * Broker Spread Drag (1.0 max): **1.0** — Spread 0.0437% < 0.05% -> 1.0 pt

### AVAX · Smart Contract L1 (SHORT)

- **Live Spot / Perp Price**: $7.4780
- **Regime / Model**: `TREND_DOWN` | Active Model: `M1:TRIGGERED` (Conf: 92%)
- **Delta Perpetual Contract**: `AVAXUSD` | Contract Value: `1.0` | Tick Size: `0.0001` | Mark: `$7.4765` | Spread: `0.0803%`
- **Table 7 Confluence Score**: **3.0 / 11.5 pts** → **Grade VETO**
  * Directional Trend (2.0 max): **0.0** — Counter-trend / No alignment (0.0 pts)
  * Auction / VWAP Regime (1.5 max): **0.0** — Discount Short / Premium Long violation (z = -1.70σ -> 0.0 pts)
  * Footprint Signal (2.0 max): **0.0** — No qualifying footprint signal at zone (0.0 pts)
  * Whale Wall Backstop (1.5 max): **0.0** — No confirmed wall backstop (0.0 pts)
  * CVD Divergence (1.0 max): **1.0** — Active BEAR CVD divergence () -> 1.0 pt
  * Liquidation Magnet Gate (1.5 max): **1.5** — Long Liq Below dominates (5.6:1 (LB)) — Target magnet aligned -> 1.5 pts
  * Options GEX Context (1.0 max): **0.0** — n/a (Non-BTC/ETH perpetual -> 0.0 pts)
  * Broker Spread Drag (1.0 max): **0.5** — Spread 0.0803% [0.05%-0.10%] -> 0.5 pts

### DOT · Interoperability (SHORT)

- **Live Spot / Perp Price**: $0.7526
- **Regime / Model**: `TREND_DOWN` | Active Model: `M1:TRIGGERED` (Conf: 92%)
- **Delta Perpetual Contract**: `DOTUSD` | Contract Value: `1.0` | Tick Size: `0.001` | Mark: `$0.7530` | Spread: `0.1328%`
- **Table 7 Confluence Score**: **2.0 / 11.5 pts** → **Grade VETO**
  * Directional Trend (2.0 max): **0.0** — Counter-trend / No alignment (0.0 pts)
  * Auction / VWAP Regime (1.5 max): **0.0** — Discount Short / Premium Long violation (z = -1.44σ -> 0.0 pts)
  * Footprint Signal (2.0 max): **0.0** — No qualifying footprint signal at zone (0.0 pts)
  * Whale Wall Backstop (1.5 max): **0.0** — No confirmed wall backstop (0.0 pts)
  * CVD Divergence (1.0 max): **1.0** — Active BEAR CVD divergence () -> 1.0 pt
  * Liquidation Magnet Gate (1.5 max): **1.0** — Moderate directional skew (1.7:1 (LB)) -> 1.0 pt
  * Options GEX Context (1.0 max): **0.0** — n/a (Non-BTC/ETH perpetual -> 0.0 pts)
  * Broker Spread Drag (1.0 max): **0.0** — Spread 0.1328% > 0.10% -> 0.0 pts

### NEAR · Smart Contract L1 (SHORT)

- **Live Spot / Perp Price**: $3.1210
- **Regime / Model**: `TREND_DOWN` | Active Model: `M1:TRIGGERED` (Conf: 92%)
- **Delta Perpetual Contract**: `NEARUSD` | Contract Value: `1.0` | Tick Size: `0.0001` | Mark: `$3.1262` | Spread: `0.0960%`
- **Table 7 Confluence Score**: **3.0 / 11.5 pts** → **Grade VETO**
  * Directional Trend (2.0 max): **0.0** — Counter-trend / No alignment (0.0 pts)
  * Auction / VWAP Regime (1.5 max): **0.0** — Discount Short / Premium Long violation (z = -1.46σ -> 0.0 pts)
  * Footprint Signal (2.0 max): **0.0** — No qualifying footprint signal at zone (0.0 pts)
  * Whale Wall Backstop (1.5 max): **0.0** — No confirmed wall backstop (0.0 pts)
  * CVD Divergence (1.0 max): **1.0** — Active BEAR CVD divergence () -> 1.0 pt
  * Liquidation Magnet Gate (1.5 max): **1.5** — Long Liq Below dominates (83.8:1 (LB)) — Target magnet aligned -> 1.5 pts
  * Options GEX Context (1.0 max): **0.0** — n/a (Non-BTC/ETH perpetual -> 0.0 pts)
  * Broker Spread Drag (1.0 max): **0.5** — Spread 0.0960% [0.05%-0.10%] -> 0.5 pts

### UNI · DeFi DEX (SHORT)

- **Live Spot / Perp Price**: $5.0200
- **Regime / Model**: `TREND_DOWN` | Active Model: `M1:TRIGGERED` (Conf: 88%)
- **Delta Perpetual Contract**: `UNIUSD` | Contract Value: `1.0` | Tick Size: `0.0001` | Mark: `$5.0273` | Spread: `0.0597%`
- **Table 7 Confluence Score**: **1.5 / 11.5 pts** → **Grade VETO**
  * Directional Trend (2.0 max): **0.0** — Counter-trend / No alignment (0.0 pts)
  * Auction / VWAP Regime (1.5 max): **0.0** — Discount Short / Premium Long violation (z = -1.33σ -> 0.0 pts)
  * Footprint Signal (2.0 max): **0.0** — No qualifying footprint signal at zone (0.0 pts)
  * Whale Wall Backstop (1.5 max): **0.0** — No confirmed wall backstop (0.0 pts)
  * CVD Divergence (1.0 max): **1.0** — Active BEAR CVD divergence () -> 1.0 pt
  * Liquidation Magnet Gate (1.5 max): **0.0** — Sub-threshold or unaligned skew (0.0 pts)
  * Options GEX Context (1.0 max): **0.0** — n/a (Non-BTC/ETH perpetual -> 0.0 pts)
  * Broker Spread Drag (1.0 max): **0.5** — Spread 0.0597% [0.05%-0.10%] -> 0.5 pts

### ATOM · Interoperability (SHORT)

- **Live Spot / Perp Price**: $1.2910
- **Regime / Model**: `TREND_DOWN` | Active Model: `M1:TRIGGERED` (Conf: 92%)
- **Delta Perpetual Contract**: `NOT LISTED` | Contract Value: `None` | Tick Size: `None` | Mark: `$1.2910` | Spread: `0.0000%`
- **Table 7 Confluence Score**: **2.5 / 11.5 pts** → **Grade VETO**
  * Directional Trend (2.0 max): **0.0** — Counter-trend / No alignment (0.0 pts)
  * Auction / VWAP Regime (1.5 max): **0.0** — Discount Short / Premium Long violation (z = -1.79σ -> 0.0 pts)
  * Footprint Signal (2.0 max): **0.0** — No qualifying footprint signal at zone (0.0 pts)
  * Whale Wall Backstop (1.5 max): **0.0** — No confirmed wall backstop (0.0 pts)
  * CVD Divergence (1.0 max): **1.0** — Active BEAR CVD divergence () -> 1.0 pt
  * Liquidation Magnet Gate (1.5 max): **1.5** — Long Liq Below dominates (17.0:1 (LB)) — Target magnet aligned -> 1.5 pts
  * Options GEX Context (1.0 max): **0.0** — n/a (Non-BTC/ETH perpetual -> 0.0 pts)
  * Broker Spread Drag (1.0 max): **0.0** — NOT LISTED ON DELTA (0.0 pts)

### XLM · Payments (SHORT)

- **Live Spot / Perp Price**: $0.1363
- **Regime / Model**: `TREND_DOWN` | Active Model: `M1:TRIGGERED` (Conf: 92%)
- **Delta Perpetual Contract**: `XLMUSD` | Contract Value: `1.0` | Tick Size: `1e-05` | Mark: `$0.1366` | Spread: `0.0220%`
- **Table 7 Confluence Score**: **3.5 / 11.5 pts** → **Grade VETO**
  * Directional Trend (2.0 max): **0.0** — Counter-trend / No alignment (0.0 pts)
  * Auction / VWAP Regime (1.5 max): **0.0** — Discount Short / Premium Long violation (z = -1.73σ -> 0.0 pts)
  * Footprint Signal (2.0 max): **0.0** — No qualifying footprint signal at zone (0.0 pts)
  * Whale Wall Backstop (1.5 max): **0.0** — No confirmed wall backstop (0.0 pts)
  * CVD Divergence (1.0 max): **1.0** — Active BEAR CVD divergence () -> 1.0 pt
  * Liquidation Magnet Gate (1.5 max): **1.5** — Long Liq Below dominates (4.3:1 (LB)) — Target magnet aligned -> 1.5 pts
  * Options GEX Context (1.0 max): **0.0** — n/a (Non-BTC/ETH perpetual -> 0.0 pts)
  * Broker Spread Drag (1.0 max): **1.0** — Spread 0.0220% < 0.05% -> 1.0 pt

### ETC · Smart Contract L1 (SHORT)

- **Live Spot / Perp Price**: $6.0830
- **Regime / Model**: `TREND_DOWN` | Active Model: `M1:TRIGGERED` (Conf: 92%)
- **Delta Perpetual Contract**: `ETCUSD` | Contract Value: `0.1` | Tick Size: `0.001` | Mark: `$6.0937` | Spread: `0.0492%`
- **Table 7 Confluence Score**: **2.0 / 11.5 pts** → **Grade VETO**
  * Directional Trend (2.0 max): **0.0** — Counter-trend / No alignment (0.0 pts)
  * Auction / VWAP Regime (1.5 max): **0.0** — Discount Short / Premium Long violation (z = -1.02σ -> 0.0 pts)
  * Footprint Signal (2.0 max): **0.0** — No qualifying footprint signal at zone (0.0 pts)
  * Whale Wall Backstop (1.5 max): **0.0** — No confirmed wall backstop (0.0 pts)
  * CVD Divergence (1.0 max): **1.0** — Active BEAR CVD divergence () -> 1.0 pt
  * Liquidation Magnet Gate (1.5 max): **0.0** — Sub-threshold or unaligned skew (0.0 pts)
  * Options GEX Context (1.0 max): **0.0** — n/a (Non-BTC/ETH perpetual -> 0.0 pts)
  * Broker Spread Drag (1.0 max): **1.0** — Spread 0.0492% < 0.05% -> 1.0 pt

### FIL · Storage (SHORT)

- **Live Spot / Perp Price**: $0.6462
- **Regime / Model**: `TREND_DOWN` | Active Model: `M1:WAIT_PULLBACK` (Conf: 45%)
- **Delta Perpetual Contract**: `FILUSD` | Contract Value: `1.0` | Tick Size: `0.0001` | Mark: `$0.6477` | Spread: `0.0309%`
- **Table 7 Confluence Score**: **2.5 / 11.5 pts** → **Grade VETO**
  * Directional Trend (2.0 max): **0.0** — Counter-trend / No alignment (0.0 pts)
  * Auction / VWAP Regime (1.5 max): **0.0** — Discount Short / Premium Long violation (z = -2.04σ -> 0.0 pts)
  * Footprint Signal (2.0 max): **0.0** — No qualifying footprint signal at zone (0.0 pts)
  * Whale Wall Backstop (1.5 max): **0.0** — No confirmed wall backstop (0.0 pts)
  * CVD Divergence (1.0 max): **0.0** — No active CVD divergence (0.0 pts)
  * Liquidation Magnet Gate (1.5 max): **1.5** — Long Liq Below dominates (69.9:1 (LB)) — Target magnet aligned -> 1.5 pts
  * Options GEX Context (1.0 max): **0.0** — n/a (Non-BTC/ETH perpetual -> 0.0 pts)
  * Broker Spread Drag (1.0 max): **1.0** — Spread 0.0309% < 0.05% -> 1.0 pt

### ICP · Smart Contract L1 (SHORT)

- **Live Spot / Perp Price**: $2.2830
- **Regime / Model**: `TREND_DOWN` | Active Model: `M1:TRIGGERED` (Conf: 92%)
- **Delta Perpetual Contract**: `NOT LISTED` | Contract Value: `None` | Tick Size: `None` | Mark: `$2.2830` | Spread: `0.0000%`
- **Table 7 Confluence Score**: **2.5 / 11.5 pts** → **Grade VETO**
  * Directional Trend (2.0 max): **0.0** — Counter-trend / No alignment (0.0 pts)
  * Auction / VWAP Regime (1.5 max): **0.0** — Discount Short / Premium Long violation (z = -1.77σ -> 0.0 pts)
  * Footprint Signal (2.0 max): **0.0** — No qualifying footprint signal at zone (0.0 pts)
  * Whale Wall Backstop (1.5 max): **0.0** — No confirmed wall backstop (0.0 pts)
  * CVD Divergence (1.0 max): **1.0** — Active BEAR CVD divergence () -> 1.0 pt
  * Liquidation Magnet Gate (1.5 max): **1.5** — Long Liq Below dominates (11.6:1 (LB)) — Target magnet aligned -> 1.5 pts
  * Options GEX Context (1.0 max): **0.0** — n/a (Non-BTC/ETH perpetual -> 0.0 pts)
  * Broker Spread Drag (1.0 max): **0.0** — NOT LISTED ON DELTA (0.0 pts)

### HBAR · Enterprise L1 (SHORT)

- **Live Spot / Perp Price**: $0.0581
- **Regime / Model**: `TREND_DOWN` | Active Model: `M1:TRIGGERED` (Conf: 92%)
- **Delta Perpetual Contract**: `HBARUSD` | Contract Value: `1.0` | Tick Size: `1e-05` | Mark: `$0.0583` | Spread: `0.0515%`
- **Table 7 Confluence Score**: **1.5 / 11.5 pts** → **Grade VETO**
  * Directional Trend (2.0 max): **0.0** — Counter-trend / No alignment (0.0 pts)
  * Auction / VWAP Regime (1.5 max): **0.0** — Discount Short / Premium Long violation (z = -1.39σ -> 0.0 pts)
  * Footprint Signal (2.0 max): **0.0** — No qualifying footprint signal at zone (0.0 pts)
  * Whale Wall Backstop (1.5 max): **0.0** — No confirmed wall backstop (0.0 pts)
  * CVD Divergence (1.0 max): **1.0** — Active BEAR CVD divergence () -> 1.0 pt
  * Liquidation Magnet Gate (1.5 max): **0.0** — Sub-threshold or unaligned skew (0.0 pts)
  * Options GEX Context (1.0 max): **0.0** — n/a (Non-BTC/ETH perpetual -> 0.0 pts)
  * Broker Spread Drag (1.0 max): **0.5** — Spread 0.0515% [0.05%-0.10%] -> 0.5 pts

### APT · Smart Contract L1 (SHORT)

- **Live Spot / Perp Price**: $0.4745
- **Regime / Model**: `TREND_DOWN` | Active Model: `M1:TRIGGERED` (Conf: 92%)
- **Delta Perpetual Contract**: `APTUSD` | Contract Value: `1.0` | Tick Size: `0.0001` | Mark: `$0.4758` | Spread: `0.0420%`
- **Table 7 Confluence Score**: **3.5 / 11.5 pts** → **Grade VETO**
  * Directional Trend (2.0 max): **0.0** — Counter-trend / No alignment (0.0 pts)
  * Auction / VWAP Regime (1.5 max): **0.0** — Discount Short / Premium Long violation (z = -1.40σ -> 0.0 pts)
  * Footprint Signal (2.0 max): **0.0** — No qualifying footprint signal at zone (0.0 pts)
  * Whale Wall Backstop (1.5 max): **0.0** — No confirmed wall backstop (0.0 pts)
  * CVD Divergence (1.0 max): **1.0** — Active BEAR CVD divergence () -> 1.0 pt
  * Liquidation Magnet Gate (1.5 max): **1.5** — Long Liq Below dominates (24.7:1 (LB)) — Target magnet aligned -> 1.5 pts
  * Options GEX Context (1.0 max): **0.0** — n/a (Non-BTC/ETH perpetual -> 0.0 pts)
  * Broker Spread Drag (1.0 max): **1.0** — Spread 0.0420% < 0.05% -> 1.0 pt

### ARB · Ethereum L2 (SHORT)

- **Live Spot / Perp Price**: $0.1345
- **Regime / Model**: `TREND_DOWN` | Active Model: `M1:TRIGGERED` (Conf: 92%)
- **Delta Perpetual Contract**: `ARBUSD` | Contract Value: `1.0` | Tick Size: `1e-05` | Mark: `$0.1350` | Spread: `0.0148%`
- **Table 7 Confluence Score**: **3.5 / 11.5 pts** → **Grade VETO**
  * Directional Trend (2.0 max): **0.0** — Counter-trend / No alignment (0.0 pts)
  * Auction / VWAP Regime (1.5 max): **0.0** — Discount Short / Premium Long violation (z = -1.59σ -> 0.0 pts)
  * Footprint Signal (2.0 max): **0.0** — No qualifying footprint signal at zone (0.0 pts)
  * Whale Wall Backstop (1.5 max): **0.0** — No confirmed wall backstop (0.0 pts)
  * CVD Divergence (1.0 max): **1.0** — Active BEAR CVD divergence () -> 1.0 pt
  * Liquidation Magnet Gate (1.5 max): **1.5** — Long Liq Below dominates (214.6:1 (LB)) — Target magnet aligned -> 1.5 pts
  * Options GEX Context (1.0 max): **0.0** — n/a (Non-BTC/ETH perpetual -> 0.0 pts)
  * Broker Spread Drag (1.0 max): **1.0** — Spread 0.0148% < 0.05% -> 1.0 pt

### OP · Ethereum L2 (SHORT)

- **Live Spot / Perp Price**: $0.0840
- **Regime / Model**: `TREND_DOWN` | Active Model: `M1:TRIGGERED` (Conf: 92%)
- **Delta Perpetual Contract**: `OPUSD` | Contract Value: `0.1` | Tick Size: `0.0001` | Mark: `$0.0842` | Spread: `0.3562%`
- **Table 7 Confluence Score**: **1.0 / 11.5 pts** → **Grade VETO**
  * Directional Trend (2.0 max): **0.0** — Counter-trend / No alignment (0.0 pts)
  * Auction / VWAP Regime (1.5 max): **0.0** — Discount Short / Premium Long violation (z = -1.35σ -> 0.0 pts)
  * Footprint Signal (2.0 max): **0.0** — No qualifying footprint signal at zone (0.0 pts)
  * Whale Wall Backstop (1.5 max): **0.0** — No confirmed wall backstop (0.0 pts)
  * CVD Divergence (1.0 max): **1.0** — Active BEAR CVD divergence () -> 1.0 pt
  * Liquidation Magnet Gate (1.5 max): **0.0** — Sub-threshold or unaligned skew (0.0 pts)
  * Options GEX Context (1.0 max): **0.0** — n/a (Non-BTC/ETH perpetual -> 0.0 pts)
  * Broker Spread Drag (1.0 max): **0.0** — Spread 0.3562% > 0.10% -> 0.0 pts

### SUI · Smart Contract L1 (SHORT)

- **Live Spot / Perp Price**: $0.7284
- **Regime / Model**: `TREND_DOWN` | Active Model: `M1:TRIGGERED` (Conf: 92%)
- **Delta Perpetual Contract**: `SUIUSD` | Contract Value: `1.0` | Tick Size: `0.0001` | Mark: `$0.7308` | Spread: `0.0411%`
- **Table 7 Confluence Score**: **4.0 / 11.5 pts** → **Grade VETO**
  * Directional Trend (2.0 max): **0.0** — Counter-trend / No alignment (0.0 pts)
  * Auction / VWAP Regime (1.5 max): **0.0** — Discount Short / Premium Long violation (z = -1.54σ -> 0.0 pts)
  * Footprint Signal (2.0 max): **0.0** — No qualifying footprint signal at zone (0.0 pts)
  * Whale Wall Backstop (1.5 max): **1.0** — Delta L2 SELL Wall $50.7k @ 0.7312 -> 1.0 pt
  * CVD Divergence (1.0 max): **1.0** — Active BEAR CVD divergence () -> 1.0 pt
  * Liquidation Magnet Gate (1.5 max): **1.0** — Moderate directional skew (2.1:1 (LB)) -> 1.0 pt
  * Options GEX Context (1.0 max): **0.0** — n/a (Non-BTC/ETH perpetual -> 0.0 pts)
  * Broker Spread Drag (1.0 max): **1.0** — Spread 0.0411% < 0.05% -> 1.0 pt

### SEI · Smart Contract L1 (SHORT)

- **Live Spot / Perp Price**: $0.0394
- **Regime / Model**: `TREND_DOWN` | Active Model: `M1:TRIGGERED` (Conf: 92%)
- **Delta Perpetual Contract**: `SEIUSD` | Contract Value: `10.0` | Tick Size: `1e-05` | Mark: `$0.0395` | Spread: `0.0506%`
- **Table 7 Confluence Score**: **1.5 / 11.5 pts** → **Grade VETO**
  * Directional Trend (2.0 max): **0.0** — Counter-trend / No alignment (0.0 pts)
  * Auction / VWAP Regime (1.5 max): **0.0** — Discount Short / Premium Long violation (z = -1.23σ -> 0.0 pts)
  * Footprint Signal (2.0 max): **0.0** — No qualifying footprint signal at zone (0.0 pts)
  * Whale Wall Backstop (1.5 max): **0.0** — No confirmed wall backstop (0.0 pts)
  * CVD Divergence (1.0 max): **1.0** — Active BEAR CVD divergence () -> 1.0 pt
  * Liquidation Magnet Gate (1.5 max): **0.0** — Sub-threshold or unaligned skew (0.0 pts)
  * Options GEX Context (1.0 max): **0.0** — n/a (Non-BTC/ETH perpetual -> 0.0 pts)
  * Broker Spread Drag (1.0 max): **0.5** — Spread 0.0506% [0.05%-0.10%] -> 0.5 pts

### TIA · Modular DA (SHORT)

- **Live Spot / Perp Price**: $0.3516
- **Regime / Model**: `TREND_DOWN` | Active Model: `M1:TRIGGERED` (Conf: 92%)
- **Delta Perpetual Contract**: `TIAUSD` | Contract Value: `1.0` | Tick Size: `0.0001` | Mark: `$0.3522` | Spread: `0.0568%`
- **Table 7 Confluence Score**: **3.0 / 11.5 pts** → **Grade VETO**
  * Directional Trend (2.0 max): **0.0** — Counter-trend / No alignment (0.0 pts)
  * Auction / VWAP Regime (1.5 max): **0.0** — Discount Short / Premium Long violation (z = -1.99σ -> 0.0 pts)
  * Footprint Signal (2.0 max): **0.0** — No qualifying footprint signal at zone (0.0 pts)
  * Whale Wall Backstop (1.5 max): **0.0** — No confirmed wall backstop (0.0 pts)
  * CVD Divergence (1.0 max): **1.0** — Active BEAR CVD divergence () -> 1.0 pt
  * Liquidation Magnet Gate (1.5 max): **1.5** — Long Liq Below dominates (9.2:1 (LB)) — Target magnet aligned -> 1.5 pts
  * Options GEX Context (1.0 max): **0.0** — n/a (Non-BTC/ETH perpetual -> 0.0 pts)
  * Broker Spread Drag (1.0 max): **0.5** — Spread 0.0568% [0.05%-0.10%] -> 0.5 pts

### VET · Supply Chain (SHORT)

- **Live Spot / Perp Price**: $0.0047
- **Regime / Model**: `TREND_DOWN` | Active Model: `M1:TRIGGERED` (Conf: 92%)
- **Delta Perpetual Contract**: `NOT LISTED` | Contract Value: `None` | Tick Size: `None` | Mark: `$0.0047` | Spread: `0.0000%`
- **Table 7 Confluence Score**: **2.5 / 11.5 pts** → **Grade VETO**
  * Directional Trend (2.0 max): **0.0** — Counter-trend / No alignment (0.0 pts)
  * Auction / VWAP Regime (1.5 max): **0.0** — Discount Short / Premium Long violation (z = -1.38σ -> 0.0 pts)
  * Footprint Signal (2.0 max): **0.0** — No qualifying footprint signal at zone (0.0 pts)
  * Whale Wall Backstop (1.5 max): **0.0** — No confirmed wall backstop (0.0 pts)
  * CVD Divergence (1.0 max): **1.0** — Active BEAR CVD divergence () -> 1.0 pt
  * Liquidation Magnet Gate (1.5 max): **1.5** — Long Liq Below dominates (2.8:1 (LB)) — Target magnet aligned -> 1.5 pts
  * Options GEX Context (1.0 max): **0.0** — n/a (Non-BTC/ETH perpetual -> 0.0 pts)
  * Broker Spread Drag (1.0 max): **0.0** — NOT LISTED ON DELTA (0.0 pts)

### 1000PEPE · Meme (LONG)

- **Live Spot / Perp Price**: $0.0040
- **Regime / Model**: `RANGE_BALANCE` | Active Model: `M2:TRIGGERED` (Conf: 66%)
- **Delta Perpetual Contract**: `1000PEPEUSD` | Contract Value: `1000.0` | Tick Size: `1e-07` | Mark: `$0.0040` | Spread: `0.0101%`
- **Table 7 Confluence Score**: **5.0 / 11.5 pts** → **Grade B**
  * Directional Trend (2.0 max): **0.0** — Counter-trend / No alignment (0.0 pts)
  * Auction / VWAP Regime (1.5 max): **1.5** — Discount Zone (price 0.0040 <= VWAP 0.0042)
  * Footprint Signal (2.0 max): **0.0** — No qualifying footprint signal at zone (0.0 pts)
  * Whale Wall Backstop (1.5 max): **0.0** — No confirmed wall backstop (0.0 pts)
  * CVD Divergence (1.0 max): **1.0** — Active BULL CVD divergence () -> 1.0 pt
  * Liquidation Magnet Gate (1.5 max): **1.5** — Short Liq Above dominates (99.0:1 (SA)) — Target magnet aligned -> 1.5 pts
  * Options GEX Context (1.0 max): **0.0** — n/a (Non-BTC/ETH perpetual -> 0.0 pts)
  * Broker Spread Drag (1.0 max): **1.0** — Spread 0.0101% < 0.05% -> 1.0 pt

### 1000SHIB · Meme (SHORT)

- **Live Spot / Perp Price**: $0.0040
- **Regime / Model**: `TREND_DOWN` | Active Model: `M1:TRIGGERED` (Conf: 92%)
- **Delta Perpetual Contract**: `1000SHIBUSD` | Contract Value: `1000.0` | Tick Size: `1e-06` | Mark: `$0.0040` | Spread: `0.0756%`
- **Table 7 Confluence Score**: **3.0 / 11.5 pts** → **Grade VETO**
  * Directional Trend (2.0 max): **0.0** — Counter-trend / No alignment (0.0 pts)
  * Auction / VWAP Regime (1.5 max): **0.0** — Discount Short / Premium Long violation (z = -1.57σ -> 0.0 pts)
  * Footprint Signal (2.0 max): **0.0** — No qualifying footprint signal at zone (0.0 pts)
  * Whale Wall Backstop (1.5 max): **0.0** — No confirmed wall backstop (0.0 pts)
  * CVD Divergence (1.0 max): **1.0** — Active BEAR CVD divergence () -> 1.0 pt
  * Liquidation Magnet Gate (1.5 max): **1.5** — Long Liq Below dominates (4.9:1 (LB)) — Target magnet aligned -> 1.5 pts
  * Options GEX Context (1.0 max): **0.0** — n/a (Non-BTC/ETH perpetual -> 0.0 pts)
  * Broker Spread Drag (1.0 max): **0.5** — Spread 0.0756% [0.05%-0.10%] -> 0.5 pts

## 5. Playbook DECIDE Formulation Cards

## FORMULATION · BTC · 2026-11-14 17:58:40 UTC · S7 (High-Volume Absorption Continuation)
Regime: TREND_DOWN — H4/D1 Trend + Microstructure Order Flow
Direction: SHORT · Grade: VETO · Confidence: 92%
D1  basisPct: n/a | deltaSpread: 0.0008% (BTCUSD)
D2  profile: session POC 65,519.3275 · day VAL/POC/VAH 65,687.8958/67,183.1992/67,700.8042 · month POC 75,849.2458
D3  VWAP 66,564.9120 · z -0.97σ · bands ±1σ/2σ
D4  EMA stacks: H4 13x89 · D1 13x89 (Counter-trend / No alignment (0.0 pts))
D5  RSI: M15 44.08 · H1 28.89 · H4 19.88
D6  delta: taker pressure / volume absorption
D7  signals: 0 Bull / 0 Bear · active: No qualifying footprint signal at zone (0.0 pts)
D8  CVD: both-selling · taker buy 49.1% · Active BEAR CVD divergence () -> 1.0 pt
D9  walls: Delta L2 SELL Wall $297.0k @ 65877.0 -> 1.0 pt (±5% Imbalance: 0.1%)
D10 LTO: institutional limit orders present
D11 clusters: sweep magnets identified
D12 LSR: 1.7:1 (SA) → GATE: PASS
D13 GEX: n/a (Non-BTC/ETH perpetual -> 0.0 pts)
D14 OI: Quadrant both-selling
D15 spread: 0.0008% on Delta Exchange (PASS)
D16 invariants: max heat 1.0% · slots <= 2 crypto · +1.0R BE · 8-bar time stop
Entry: $65,763.1000–$67,700.8042 (Limit Ladder L1 40% / L2 40% / L3 20%) · Stop: $68,716.3162 (Structural Invalidation)
T1: $65,687.8958 (0.07R · Day Value Area) · T2: $63,790.2070 (0.11R · Volume Node) · T3: $62,474.9450 (0.19R · Liquidity Sweep)
Composite R: 0.13R · Active Vetoes: Table 7 score 3.0 < 5.0 — HARD VETO (NO TRADE); Model R 0.70 < 1.5 — reward does not pay risk

## FORMULATION · ETH · 2026-11-14 17:58:40 UTC · S7 (High-Volume Absorption Continuation)
Regime: TREND_DOWN — H4/D1 Trend + Microstructure Order Flow
Direction: SHORT · Grade: VETO · Confidence: 88%
D1  basisPct: n/a | deltaSpread: 0.0027% (ETHUSD)
D2  profile: session POC 1,845.0430 · day VAL/POC/VAH 1,842.5104/1,904.7396/1,915.4688 · month POC 2,233.7137
D3  VWAP 1,872.7175 · z -1.06σ · bands ±1σ/2σ
D4  EMA stacks: H4 13x89 · D1 13x89 (Counter-trend / No alignment (0.0 pts))
D5  RSI: M15 40.72 · H1 29.43 · H4 24.85
D6  delta: taker pressure / volume absorption
D7  signals: 0 Bull / 0 Bear · active: No qualifying footprint signal at zone (0.0 pts)
D8  CVD: both-selling · taker buy 49.3% · Active BEAR CVD divergence () -> 1.0 pt
D9  walls: Delta L2 SELL Wall $257.1k @ 1841.50 -> 1.0 pt (±5% Imbalance: 0.0%)
D10 LTO: institutional limit orders present
D11 clusters: sweep magnets identified
D12 LSR: 1.8:1 (SA) → GATE: PASS
D13 GEX: n/a (Non-BTC/ETH perpetual -> 0.0 pts)
D14 OI: Quadrant both-selling
D15 spread: 0.0027% on Delta Exchange (PASS)
D16 invariants: max heat 1.0% · slots <= 2 crypto · +1.0R BE · 8-bar time stop
Entry: $1,839.1700–$1,915.4688 (Limit Ladder L1 40% / L2 40% / L3 20%) · Stop: $1,944.2008 (Structural Invalidation)
T1: $1,811.5825 (0.96R · Day Value Area) · T2: $1,783.9949 (1.44R · Volume Node) · T3: $1,747.2115 (2.40R · Liquidity Sweep)
Composite R: 1.73R · Active Vetoes: Table 7 score 3.0 < 5.0 — HARD VETO (NO TRADE); Model R 0.47 < 1.5 — reward does not pay risk

## FORMULATION · BNB · 2026-11-14 17:58:40 UTC · S7 (High-Volume Absorption Continuation)
Regime: TREND_DOWN — H4/D1 Trend + Microstructure Order Flow
Direction: SHORT · Grade: VETO · Confidence: 92%
D1  basisPct: n/a | deltaSpread: 0.0034% (BNBUSD)
D2  profile: session POC 599.3530 · day VAL/POC/VAH 595.1946/616.6662/625.7504 · month POC 695.2495
D3  VWAP 607.2465 · z -1.27σ · bands ±1σ/2σ
D4  EMA stacks: H4 13x89 · D1 13x89 (Counter-trend / No alignment (0.0 pts))
D5  RSI: M15 33.79 · H1 23.25 · H4 18.16
D6  delta: taker pressure / volume absorption
D7  signals: 0 Bull / 0 Bear · active: No qualifying footprint signal at zone (0.0 pts)
D8  CVD: both-selling · taker buy 47.8% · Active BEAR CVD divergence () -> 1.0 pt
D9  walls: Delta L2 SELL Wall $50.2k @ 590.420 -> 1.0 pt (±5% Imbalance: 0.0%)
D10 LTO: institutional limit orders present
D11 clusters: sweep magnets identified
D12 LSR: 1.6:1 (LB) → GATE: PASS
D13 GEX: n/a (Non-BTC/ETH perpetual -> 0.0 pts)
D14 OI: Quadrant both-selling
D15 spread: 0.0034% on Delta Exchange (PASS)
D16 invariants: max heat 1.0% · slots <= 2 crypto · +1.0R BE · 8-bar time stop
Entry: $590.5200–$625.7504 (Limit Ladder L1 40% / L2 40% / L3 20%) · Stop: $635.1367 (Structural Invalidation)
T1: $581.6622 (0.94R · Day Value Area) · T2: $572.8044 (1.42R · Volume Node) · T3: $560.9940 (2.36R · Liquidity Sweep)
Composite R: 1.70R · Active Vetoes: Table 7 score 4.0 < 5.0 — HARD VETO (NO TRADE); Model R 0.73 < 1.5 — reward does not pay risk

## FORMULATION · SOL · 2026-11-14 17:58:40 UTC · S7 (High-Volume Absorption Continuation)
Regime: TREND_DOWN — H4/D1 Trend + Microstructure Order Flow
Direction: SHORT · Grade: VETO · Confidence: 92%
D1  basisPct: n/a | deltaSpread: 0.0151% (SOLUSD)
D2  profile: session POC 73.8208 · day VAL/POC/VAH 73.3295/75.5362/76.3085 · month POC 89.7157
D3  VWAP 74.8578 · z -1.49σ · bands ±1σ/2σ
D4  EMA stacks: H4 13x89 · D1 13x89 (Counter-trend / No alignment (0.0 pts))
D5  RSI: M15 33.89 · H1 25.40 · H4 22.37
D6  delta: taker pressure / volume absorption
D7  signals: 0 Bull / 0 Bear · active: No qualifying footprint signal at zone (0.0 pts)
D8  CVD: spot-bid · taker buy 49% · Active BEAR CVD divergence () -> 1.0 pt
D9  walls: Delta L2 SELL Wall $50.7k @ 72.8200 -> 1.0 pt (±5% Imbalance: -0.0%)
D10 LTO: institutional limit orders present
D11 clusters: sweep magnets identified
D12 LSR: 1.9:1 (LB) → GATE: PASS
D13 GEX: n/a (Non-BTC/ETH perpetual -> 0.0 pts)
D14 OI: Quadrant spot-bid
D15 spread: 0.0151% on Delta Exchange (PASS)
D16 invariants: max heat 1.0% · slots <= 2 crypto · +1.0R BE · 8-bar time stop
Entry: $72.7500–$76.3085 (Limit Ladder L1 40% / L2 40% / L3 20%) · Stop: $77.4531 (Structural Invalidation)
T1: $71.6587 (0.95R · Day Value Area) · T2: $70.5675 (1.43R · Volume Node) · T3: $69.1125 (2.38R · Liquidity Sweep)
Composite R: 1.72R · Active Vetoes: Table 7 score 4.0 < 5.0 — HARD VETO (NO TRADE); Model R 0.62 < 1.5 — reward does not pay risk

## FORMULATION · XRP · 2026-11-14 17:58:40 UTC · S7 (High-Volume Absorption Continuation)
Regime: TREND_DOWN — H4/D1 Trend + Microstructure Order Flow
Direction: SHORT · Grade: VETO · Confidence: 92%
D1  basisPct: n/a | deltaSpread: 0.0208% (XRPUSD)
D2  profile: session POC 0.9922 · day VAL/POC/VAH 0.9730/0.9912/1.0037 · month POC 1.2514
D3  VWAP 0.9829 · z -1.56σ · bands ±1σ/2σ
D4  EMA stacks: H4 13x89 · D1 13x89 (Counter-trend / No alignment (0.0 pts))
D5  RSI: M15 36.35 · H1 28.01 · H4 27.10
D6  delta: taker pressure / volume absorption
D7  signals: 0 Bull / 0 Bear · active: No qualifying footprint signal at zone (0.0 pts)
D8  CVD: both-selling · taker buy 48.3% · Active BEAR CVD divergence () -> 1.0 pt
D9  walls: Delta L2 SELL Wall $57.7k @ 0.9608 -> 1.0 pt (±5% Imbalance: -0.0%)
D10 LTO: institutional limit orders present
D11 clusters: sweep magnets identified
D12 LSR: 1.1:1 (SA) → GATE: PASS
D13 GEX: n/a (Non-BTC/ETH perpetual -> 0.0 pts)
D14 OI: Quadrant both-selling
D15 spread: 0.0208% on Delta Exchange (PASS)
D16 invariants: max heat 1.0% · slots <= 2 crypto · +1.0R BE · 8-bar time stop
Entry: $0.9598–$1.0037 (Limit Ladder L1 40% / L2 40% / L3 20%) · Stop: $1.0187 (Structural Invalidation)
T1: $0.9454 (0.96R · Day Value Area) · T2: $0.9310 (1.43R · Volume Node) · T3: $0.9118 (2.39R · Liquidity Sweep)
Composite R: 1.72R · Active Vetoes: Table 7 score 3.0 < 5.0 — HARD VETO (NO TRADE); Model R 0.37 < 1.5 — reward does not pay risk

## FORMULATION · ADA · 2026-11-14 17:58:40 UTC · S7 (High-Volume Absorption Continuation)
Regime: TREND_DOWN — H4/D1 Trend + Microstructure Order Flow
Direction: SHORT · Grade: VETO · Confidence: 92%
D1  basisPct: n/a | deltaSpread: 0.1670% (ADAUSD)
D2  profile: session POC 0.1572 · day VAL/POC/VAH 0.1570/0.1634/0.1657 · month POC 0.1730
D3  VWAP 0.1609 · z -1.40σ · bands ±1σ/2σ
D4  EMA stacks: H4 13x89 · D1 13x89 (Counter-trend / No alignment (0.0 pts))
D5  RSI: M15 34.46 · H1 24.06 · H4 24.58
D6  delta: taker pressure / volume absorption
D7  signals: 0 Bull / 0 Bear · active: No qualifying footprint signal at zone (0.0 pts)
D8  CVD: both-selling · taker buy 48.4% · Active BEAR CVD divergence () -> 1.0 pt
D9  walls: No confirmed wall backstop (0.0 pts) (±5% Imbalance: -0.4%)
D10 LTO: institutional limit orders present
D11 clusters: sweep magnets identified
D12 LSR: 1.1:1 (LB) → GATE: PASS
D13 GEX: n/a (Non-BTC/ETH perpetual -> 0.0 pts)
D14 OI: Quadrant both-selling
D15 spread: 0.1670% on Delta Exchange (VETO)
D16 invariants: max heat 1.0% · slots <= 2 crypto · +1.0R BE · 8-bar time stop
Entry: $0.1555–$0.1657 (Limit Ladder L1 40% / L2 40% / L3 20%) · Stop: $0.1682 (Structural Invalidation)
T1: $0.1532 (0.94R · Day Value Area) · T2: $0.1508 (1.41R · Volume Node) · T3: $0.1477 (2.35R · Liquidity Sweep)
Composite R: 1.69R · Active Vetoes: Delta spread 0.1670% > 0.15% — execution drag veto; Table 7 score 1.0 < 5.0 — HARD VETO (NO TRADE); Model R 0.76 < 1.5 — reward does not pay risk

## FORMULATION · DOGE · 2026-11-14 17:58:40 UTC · S7 (High-Volume Absorption Continuation)
Regime: TREND_DOWN — H4/D1 Trend + Microstructure Order Flow
Direction: SHORT · Grade: VETO · Confidence: 92%
D1  basisPct: n/a | deltaSpread: 0.0331% (DOGEUSD)
D2  profile: session POC 0.0611 · day VAL/POC/VAH 0.0608/0.0629/0.0634 · month POC 0.0753
D3  VWAP 0.0619 · z -1.30σ · bands ±1σ/2σ
D4  EMA stacks: H4 13x89 · D1 13x89 (Counter-trend / No alignment (0.0 pts))
D5  RSI: M15 37.12 · H1 26.98 · H4 25.56
D6  delta: taker pressure / volume absorption
D7  signals: 0 Bull / 0 Bear · active: No qualifying footprint signal at zone (0.0 pts)
D8  CVD: both-selling · taker buy 48.2% · Active BEAR CVD divergence () -> 1.0 pt
D9  walls: No confirmed wall backstop (0.0 pts) (±5% Imbalance: -0.0%)
D10 LTO: institutional limit orders present
D11 clusters: sweep magnets identified
D12 LSR: 1.7:1 (LB) → GATE: PASS
D13 GEX: n/a (Non-BTC/ETH perpetual -> 0.0 pts)
D14 OI: Quadrant both-selling
D15 spread: 0.0331% on Delta Exchange (PASS)
D16 invariants: max heat 1.0% · slots <= 2 crypto · +1.0R BE · 8-bar time stop
Entry: $0.0603–$0.0634 (Limit Ladder L1 40% / L2 40% / L3 20%) · Stop: $0.0643 (Structural Invalidation)
T1: $0.0594 (0.95R · Day Value Area) · T2: $0.0585 (1.43R · Volume Node) · T3: $0.0573 (2.38R · Liquidity Sweep)
Composite R: 1.71R · Active Vetoes: Table 7 score 3.0 < 5.0 — HARD VETO (NO TRADE); Model R 0.32 < 1.5 — reward does not pay risk

## FORMULATION · TRX · 2026-11-14 17:58:40 UTC · S1 (Liquidation Sweep Reversal — Magnet Exhaustion)
Regime: TREND_DOWN — H4/D1 Trend + Microstructure Order Flow
Direction: SHORT · Grade: VETO · Confidence: 45%
D1  basisPct: n/a | deltaSpread: 0.0065% (TRXUSD)
D2  profile: session POC 0.3097 · day VAL/POC/VAH 0.3098/0.3128/0.3138 · month POC 0.3178
D3  VWAP 0.3109 · z -2.13σ · bands ±1σ/2σ
D4  EMA stacks: H4 13x89 · D1 13x89 (Counter-trend / No alignment (0.0 pts))
D5  RSI: M15 17.81 · H1 19.49 · H4 25.86
D6  delta: taker pressure / volume absorption
D7  signals: 0 Bull / 0 Bear · active: No qualifying footprint signal at zone (0.0 pts)
D8  CVD: spot-bid · taker buy 48.9% · Active BEAR CVD divergence () -> 1.0 pt
D9  walls: No confirmed wall backstop (0.0 pts) (±5% Imbalance: 0.1%)
D10 LTO: institutional limit orders present
D11 clusters: sweep magnets identified
D12 LSR: 10.3:1 (LB) → GATE: BANNED (Wait for Sweep S1)
D13 GEX: n/a (Non-BTC/ETH perpetual -> 0.0 pts)
D14 OI: Quadrant spot-bid
D15 spread: 0.0065% on Delta Exchange (PASS)
D16 invariants: max heat 1.0% · slots <= 2 crypto · +1.0R BE · 8-bar time stop
Entry: $0.3070–$0.3138 (Limit Ladder L1 40% / L2 40% / L3 20%) · Stop: $0.3185 (Structural Invalidation)
T1: $0.3024 (0.98R · Day Value Area) · T2: $0.2978 (1.47R · Volume Node) · T3: $0.2917 (2.45R · Liquidity Sweep)
Composite R: 1.76R · Active Vetoes: LSR 10.3:1 (LB) >= 2.5:1 — passive limit front-running (S3) banned; WAIT FOR THE SWEEP (S1); Table 7 score 3.5 < 5.0 — HARD VETO (NO TRADE)

## FORMULATION · LINK · 2026-11-14 17:58:40 UTC · S7 (High-Volume Absorption Continuation)
Regime: TREND_DOWN — H4/D1 Trend + Microstructure Order Flow
Direction: SHORT · Grade: VETO · Confidence: 92%
D1  basisPct: n/a | deltaSpread: 0.0218% (LINKUSD)
D2  profile: session POC 9.2621 · day VAL/POC/VAH 9.2558/9.5943/9.7268 · month POC 10.8543
D3  VWAP 9.4473 · z -1.27σ · bands ±1σ/2σ
D4  EMA stacks: H4 13x89 · D1 13x89 (Counter-trend / No alignment (0.0 pts))
D5  RSI: M15 36.88 · H1 28.34 · H4 27.01
D6  delta: taker pressure / volume absorption
D7  signals: 0 Bull / 0 Bear · active: No qualifying footprint signal at zone (0.0 pts)
D8  CVD: both-selling · taker buy 48.6% · Active BEAR CVD divergence () -> 1.0 pt
D9  walls: Delta L2 SELL Wall $80.8k @ 9.154 -> 1.0 pt (±5% Imbalance: -0.0%)
D10 LTO: institutional limit orders present
D11 clusters: sweep magnets identified
D12 LSR: 2.1:1 (SA) → GATE: PASS
D13 GEX: n/a (Non-BTC/ETH perpetual -> 0.0 pts)
D14 OI: Quadrant both-selling
D15 spread: 0.0218% on Delta Exchange (PASS)
D16 invariants: max heat 1.0% · slots <= 2 crypto · +1.0R BE · 8-bar time stop
Entry: $9.1680–$9.7268 (Limit Ladder L1 40% / L2 40% / L3 20%) · Stop: $9.8727 (Structural Invalidation)
T1: $9.0305 (0.94R · Day Value Area) · T2: $8.8930 (1.41R · Volume Node) · T3: $8.7096 (2.36R · Liquidity Sweep)
Composite R: 1.70R · Active Vetoes: Table 7 score 3.0 < 5.0 — HARD VETO (NO TRADE); Model R 0.42 < 1.5 — reward does not pay risk

## FORMULATION · LTC · 2026-11-14 17:58:40 UTC · S7 (High-Volume Absorption Continuation)
Regime: TREND_DOWN — H4/D1 Trend + Microstructure Order Flow
Direction: SHORT · Grade: VETO · Confidence: 92%
D1  basisPct: n/a | deltaSpread: 0.0437% (LTCUSD)
D2  profile: session POC 46.1442 · day VAL/POC/VAH 46.1690/48.3150/49.0550 · month POC 51.4618
D3  VWAP 47.3257 · z -1.35σ · bands ±1σ/2σ
D4  EMA stacks: H4 13x89 · D1 13x89 (Counter-trend / No alignment (0.0 pts))
D5  RSI: M15 33.18 · H1 25.48 · H4 27.73
D6  delta: taker pressure / volume absorption
D7  signals: 0 Bull / 0 Bear · active: No qualifying footprint signal at zone (0.0 pts)
D8  CVD: both-selling · taker buy 48.4% · Active BEAR CVD divergence () -> 1.0 pt
D9  walls: Delta L2 SELL Wall $55.3k @ 45.83 -> 1.0 pt (±5% Imbalance: -0.0%)
D10 LTO: institutional limit orders present
D11 clusters: sweep magnets identified
D12 LSR: 1.3:1 (SA) → GATE: PASS
D13 GEX: n/a (Non-BTC/ETH perpetual -> 0.0 pts)
D14 OI: Quadrant both-selling
D15 spread: 0.0437% on Delta Exchange (PASS)
D16 invariants: max heat 1.0% · slots <= 2 crypto · +1.0R BE · 8-bar time stop
Entry: $45.6800–$49.0550 (Limit Ladder L1 40% / L2 40% / L3 20%) · Stop: $49.7908 (Structural Invalidation)
T1: $44.9948 (0.93R · Day Value Area) · T2: $44.3096 (1.40R · Volume Node) · T3: $43.3960 (2.33R · Liquidity Sweep)
Composite R: 1.68R · Active Vetoes: Table 7 score 3.0 < 5.0 — HARD VETO (NO TRADE); Model R 0.85 < 1.5 — reward does not pay risk

## FORMULATION · AVAX · 2026-11-14 17:58:40 UTC · S1 (Liquidation Sweep Reversal — Magnet Exhaustion)
Regime: TREND_DOWN — H4/D1 Trend + Microstructure Order Flow
Direction: SHORT · Grade: VETO · Confidence: 92%
D1  basisPct: n/a | deltaSpread: 0.0803% (AVAXUSD)
D2  profile: session POC 7.6740 · day VAL/POC/VAH 7.6582/8.0348/8.1743 · month POC 8.5689
D3  VWAP 7.8704 · z -1.70σ · bands ±1σ/2σ
D4  EMA stacks: H4 13x89 · D1 13x89 (Counter-trend / No alignment (0.0 pts))
D5  RSI: M15 26.04 · H1 20.31 · H4 28.48
D6  delta: taker pressure / volume absorption
D7  signals: 0 Bull / 0 Bear · active: No qualifying footprint signal at zone (0.0 pts)
D8  CVD: both-selling · taker buy 48.9% · Active BEAR CVD divergence () -> 1.0 pt
D9  walls: No confirmed wall backstop (0.0 pts) (±5% Imbalance: 0.1%)
D10 LTO: institutional limit orders present
D11 clusters: sweep magnets identified
D12 LSR: 5.6:1 (LB) → GATE: BANNED (Wait for Sweep S1)
D13 GEX: n/a (Non-BTC/ETH perpetual -> 0.0 pts)
D14 OI: Quadrant both-selling
D15 spread: 0.0803% on Delta Exchange (PASS)
D16 invariants: max heat 1.0% · slots <= 2 crypto · +1.0R BE · 8-bar time stop
Entry: $7.4780–$8.1743 (Limit Ladder L1 40% / L2 40% / L3 20%) · Stop: $8.2969 (Structural Invalidation)
T1: $7.3658 (0.91R · Day Value Area) · T2: $7.2537 (1.37R · Volume Node) · T3: $7.1041 (2.29R · Liquidity Sweep)
Composite R: 1.65R · Active Vetoes: LSR 5.6:1 (LB) >= 2.5:1 — passive limit front-running (S3) banned; WAIT FOR THE SWEEP (S1); Table 7 score 3.0 < 5.0 — HARD VETO (NO TRADE); Model R 0.93 < 1.5 — reward does not pay risk

## FORMULATION · DOT · 2026-11-14 17:58:40 UTC · S7 (High-Volume Absorption Continuation)
Regime: TREND_DOWN — H4/D1 Trend + Microstructure Order Flow
Direction: SHORT · Grade: VETO · Confidence: 92%
D1  basisPct: n/a | deltaSpread: 0.1328% (DOTUSD)
D2  profile: session POC 0.7662 · day VAL/POC/VAH 0.7620/0.7863/0.8004 · month POC 0.9488
D3  VWAP 0.7778 · z -1.44σ · bands ±1σ/2σ
D4  EMA stacks: H4 13x89 · D1 13x89 (Counter-trend / No alignment (0.0 pts))
D5  RSI: M15 35.70 · H1 25.43 · H4 26.32
D6  delta: taker pressure / volume absorption
D7  signals: 0 Bull / 0 Bear · active: No qualifying footprint signal at zone (0.0 pts)
D8  CVD: both-selling · taker buy 47% · Active BEAR CVD divergence () -> 1.0 pt
D9  walls: No confirmed wall backstop (0.0 pts) (±5% Imbalance: 0.0%)
D10 LTO: institutional limit orders present
D11 clusters: sweep magnets identified
D12 LSR: 1.7:1 (LB) → GATE: PASS
D13 GEX: n/a (Non-BTC/ETH perpetual -> 0.0 pts)
D14 OI: Quadrant both-selling
D15 spread: 0.1328% on Delta Exchange (PASS)
D16 invariants: max heat 1.0% · slots <= 2 crypto · +1.0R BE · 8-bar time stop
Entry: $0.7526–$0.8004 (Limit Ladder L1 40% / L2 40% / L3 20%) · Stop: $0.8124 (Structural Invalidation)
T1: $0.7413 (0.94R · Day Value Area) · T2: $0.7300 (1.41R · Volume Node) · T3: $0.7150 (2.35R · Liquidity Sweep)
Composite R: 1.69R · Active Vetoes: Table 7 score 2.0 < 5.0 — HARD VETO (NO TRADE); Model R 0.34 < 1.5 — reward does not pay risk

## FORMULATION · NEAR · 2026-11-14 17:58:40 UTC · S1 (Liquidation Sweep Reversal — Magnet Exhaustion)
Regime: TREND_DOWN — H4/D1 Trend + Microstructure Order Flow
Direction: SHORT · Grade: VETO · Confidence: 92%
D1  basisPct: n/a | deltaSpread: 0.0960% (NEARUSD)
D2  profile: session POC 3.2126 · day VAL/POC/VAH 3.2114/3.3338/3.4698 · month POC 3.7060
D3  VWAP 3.2738 · z -1.46σ · bands ±1σ/2σ
D4  EMA stacks: H4 13x89 · D1 13x89 (Counter-trend / No alignment (0.0 pts))
D5  RSI: M15 34.05 · H1 23.85 · H4 29.40
D6  delta: taker pressure / volume absorption
D7  signals: 0 Bull / 0 Bear · active: No qualifying footprint signal at zone (0.0 pts)
D8  CVD: both-selling · taker buy 48.8% · Active BEAR CVD divergence () -> 1.0 pt
D9  walls: No confirmed wall backstop (0.0 pts) (±5% Imbalance: 0.0%)
D10 LTO: institutional limit orders present
D11 clusters: sweep magnets identified
D12 LSR: 83.8:1 (LB) → GATE: BANNED (Wait for Sweep S1)
D13 GEX: n/a (Non-BTC/ETH perpetual -> 0.0 pts)
D14 OI: Quadrant both-selling
D15 spread: 0.0960% on Delta Exchange (PASS)
D16 invariants: max heat 1.0% · slots <= 2 crypto · +1.0R BE · 8-bar time stop
Entry: $3.1210–$3.4698 (Limit Ladder L1 40% / L2 40% / L3 20%) · Stop: $3.5218 (Structural Invalidation)
T1: $3.0742 (0.90R · Day Value Area) · T2: $3.0274 (1.35R · Volume Node) · T3: $2.9649 (2.25R · Liquidity Sweep)
Composite R: 1.62R · Active Vetoes: LSR 83.8:1 (LB) >= 2.5:1 — passive limit front-running (S3) banned; WAIT FOR THE SWEEP (S1); Table 7 score 3.0 < 5.0 — HARD VETO (NO TRADE); Model R 0.67 < 1.5 — reward does not pay risk

## FORMULATION · UNI · 2026-11-14 17:58:40 UTC · S7 (High-Volume Absorption Continuation)
Regime: TREND_DOWN — H4/D1 Trend + Microstructure Order Flow
Direction: SHORT · Grade: VETO · Confidence: 88%
D1  basisPct: n/a | deltaSpread: 0.0597% (UNIUSD)
D2  profile: session POC 5.1491 · day VAL/POC/VAH 5.1348/5.5153/5.6762 · month POC 7.0085
D3  VWAP 5.3382 · z -1.33σ · bands ±1σ/2σ
D4  EMA stacks: H4 13x89 · D1 13x89 (Counter-trend / No alignment (0.0 pts))
D5  RSI: M15 30.16 · H1 22.87 · H4 14.67
D6  delta: taker pressure / volume absorption
D7  signals: 0 Bull / 0 Bear · active: No qualifying footprint signal at zone (0.0 pts)
D8  CVD: spot-bid · taker buy 48.3% · Active BEAR CVD divergence () -> 1.0 pt
D9  walls: No confirmed wall backstop (0.0 pts) (±5% Imbalance: -0.0%)
D10 LTO: institutional limit orders present
D11 clusters: sweep magnets identified
D12 LSR: 1.4:1 (SA) → GATE: PASS
D13 GEX: n/a (Non-BTC/ETH perpetual -> 0.0 pts)
D14 OI: Quadrant spot-bid
D15 spread: 0.0597% on Delta Exchange (PASS)
D16 invariants: max heat 1.0% · slots <= 2 crypto · +1.0R BE · 8-bar time stop
Entry: $5.0200–$5.6762 (Limit Ladder L1 40% / L2 40% / L3 20%) · Stop: $5.7614 (Structural Invalidation)
T1: $4.9447 (0.88R · Day Value Area) · T2: $4.8694 (1.33R · Volume Node) · T3: $4.7690 (2.21R · Liquidity Sweep)
Composite R: 1.59R · Active Vetoes: Table 7 score 1.5 < 5.0 — HARD VETO (NO TRADE); Model R 0.71 < 1.5 — reward does not pay risk

## FORMULATION · ATOM · 2026-11-14 17:58:40 UTC · S1 (Liquidation Sweep Reversal — Magnet Exhaustion)
Regime: TREND_DOWN — H4/D1 Trend + Microstructure Order Flow
Direction: SHORT · Grade: VETO · Confidence: 92%
D1  basisPct: n/a | deltaSpread: 0.0000% (NOT LISTED)
D2  profile: session POC 1.3018 · day VAL/POC/VAH 1.3088/1.3425/1.3486 · month POC 1.3901
D3  VWAP 1.3253 · z -1.79σ · bands ±1σ/2σ
D4  EMA stacks: H4 13x89 · D1 13x89 (Counter-trend / No alignment (0.0 pts))
D5  RSI: M15 30.89 · H1 26.04 · H4 32.75
D6  delta: taker pressure / volume absorption
D7  signals: 0 Bull / 0 Bear · active: No qualifying footprint signal at zone (0.0 pts)
D8  CVD: spot-bid · taker buy 44% · Active BEAR CVD divergence () -> 1.0 pt
D9  walls: No confirmed wall backstop (0.0 pts) (±5% Imbalance: -0.2%)
D10 LTO: institutional limit orders present
D11 clusters: sweep magnets identified
D12 LSR: 17.0:1 (LB) → GATE: BANNED (Wait for Sweep S1)
D13 GEX: n/a (Non-BTC/ETH perpetual -> 0.0 pts)
D14 OI: Quadrant spot-bid
D15 spread: 0.0000% on Delta Exchange (PASS)
D16 invariants: max heat 1.0% · slots <= 2 crypto · +1.0R BE · 8-bar time stop
Entry: $1.2910–$1.3486 (Limit Ladder L1 40% / L2 40% / L3 20%) · Stop: $1.3689 (Structural Invalidation)
T1: $1.2716 (0.96R · Day Value Area) · T2: $1.2523 (1.44R · Volume Node) · T3: $1.2264 (2.39R · Liquidity Sweep)
Composite R: 1.72R · Active Vetoes: LSR 17.0:1 (LB) >= 2.5:1 — passive limit front-running (S3) banned; WAIT FOR THE SWEEP (S1); Not listed on Delta Exchange; Table 7 score 2.5 < 5.0 — HARD VETO (NO TRADE); Model R 0.77 < 1.5 — reward does not pay risk

## FORMULATION · XLM · 2026-11-14 17:58:40 UTC · S1 (Liquidation Sweep Reversal — Magnet Exhaustion)
Regime: TREND_DOWN — H4/D1 Trend + Microstructure Order Flow
Direction: SHORT · Grade: VETO · Confidence: 92%
D1  basisPct: n/a | deltaSpread: 0.0220% (XLMUSD)
D2  profile: session POC 0.1401 · day VAL/POC/VAH 0.1391/0.1434/0.1446 · month POC 0.1477
D3  VWAP 0.1411 · z -1.73σ · bands ±1σ/2σ
D4  EMA stacks: H4 13x89 · D1 13x89 (Counter-trend / No alignment (0.0 pts))
D5  RSI: M15 30.90 · H1 24.85 · H4 33.64
D6  delta: taker pressure / volume absorption
D7  signals: 0 Bull / 0 Bear · active: No qualifying footprint signal at zone (0.0 pts)
D8  CVD: spot-bid · taker buy 49% · Active BEAR CVD divergence () -> 1.0 pt
D9  walls: No confirmed wall backstop (0.0 pts) (±5% Imbalance: 0.0%)
D10 LTO: institutional limit orders present
D11 clusters: sweep magnets identified
D12 LSR: 4.3:1 (LB) → GATE: BANNED (Wait for Sweep S1)
D13 GEX: n/a (Non-BTC/ETH perpetual -> 0.0 pts)
D14 OI: Quadrant spot-bid
D15 spread: 0.0220% on Delta Exchange (PASS)
D16 invariants: max heat 1.0% · slots <= 2 crypto · +1.0R BE · 8-bar time stop
Entry: $0.1363–$0.1446 (Limit Ladder L1 40% / L2 40% / L3 20%) · Stop: $0.1468 (Structural Invalidation)
T1: $0.1342 (0.94R · Day Value Area) · T2: $0.1322 (1.41R · Volume Node) · T3: $0.1295 (2.36R · Liquidity Sweep)
Composite R: 1.70R · Active Vetoes: LSR 4.3:1 (LB) >= 2.5:1 — passive limit front-running (S3) banned; WAIT FOR THE SWEEP (S1); Table 7 score 3.5 < 5.0 — HARD VETO (NO TRADE); Model R 0.92 < 1.5 — reward does not pay risk

## FORMULATION · ETC · 2026-11-14 17:58:40 UTC · S7 (High-Volume Absorption Continuation)
Regime: TREND_DOWN — H4/D1 Trend + Microstructure Order Flow
Direction: SHORT · Grade: VETO · Confidence: 92%
D1  basisPct: n/a | deltaSpread: 0.0492% (ETCUSD)
D2  profile: session POC 6.1419 · day VAL/POC/VAH 6.0994/6.3036/6.3526 · month POC 6.9668
D3  VWAP 6.2049 · z -1.02σ · bands ±1σ/2σ
D4  EMA stacks: H4 13x89 · D1 13x89 (Counter-trend / No alignment (0.0 pts))
D5  RSI: M15 38.95 · H1 29.36 · H4 25.96
D6  delta: taker pressure / volume absorption
D7  signals: 0 Bull / 0 Bear · active: No qualifying footprint signal at zone (0.0 pts)
D8  CVD: both-selling · taker buy 48.7% · Active BEAR CVD divergence () -> 1.0 pt
D9  walls: No confirmed wall backstop (0.0 pts) (±5% Imbalance: 0.1%)
D10 LTO: institutional limit orders present
D11 clusters: sweep magnets identified
D12 LSR: 2.2:1 (SA) → GATE: PASS
D13 GEX: n/a (Non-BTC/ETH perpetual -> 0.0 pts)
D14 OI: Quadrant both-selling
D15 spread: 0.0492% on Delta Exchange (PASS)
D16 invariants: max heat 1.0% · slots <= 2 crypto · +1.0R BE · 8-bar time stop
Entry: $6.0830–$6.3526 (Limit Ladder L1 40% / L2 40% / L3 20%) · Stop: $6.4479 (Structural Invalidation)
T1: $5.9918 (0.96R · Day Value Area) · T2: $5.9005 (1.44R · Volume Node) · T3: $5.7789 (2.39R · Liquidity Sweep)
Composite R: 1.72R · Active Vetoes: Table 7 score 2.0 < 5.0 — HARD VETO (NO TRADE); Model R 0.44 < 1.5 — reward does not pay risk

## FORMULATION · FIL · 2026-11-14 17:58:40 UTC · S1 (Liquidation Sweep Reversal — Magnet Exhaustion)
Regime: TREND_DOWN — H4/D1 Trend + Microstructure Order Flow
Direction: SHORT · Grade: VETO · Confidence: 45%
D1  basisPct: n/a | deltaSpread: 0.0309% (FILUSD)
D2  profile: session POC 0.6536 · day VAL/POC/VAH 0.6610/0.6829/0.6939 · month POC 0.8637
D3  VWAP 0.6762 · z -2.04σ · bands ±1σ/2σ
D4  EMA stacks: H4 13x89 · D1 13x89 (Counter-trend / No alignment (0.0 pts))
D5  RSI: M15 26.37 · H1 18.34 · H4 21.85
D6  delta: taker pressure / volume absorption
D7  signals: 0 Bull / 0 Bear · active: No qualifying footprint signal at zone (0.0 pts)
D8  CVD: n/a · taker buy n/a% · No active CVD divergence (0.0 pts)
D9  walls: No confirmed wall backstop (0.0 pts) (±5% Imbalance: 0.1%)
D10 LTO: institutional limit orders present
D11 clusters: sweep magnets identified
D12 LSR: 69.9:1 (LB) → GATE: BANNED (Wait for Sweep S1)
D13 GEX: n/a (Non-BTC/ETH perpetual -> 0.0 pts)
D14 OI: Quadrant n/a
D15 spread: 0.0309% on Delta Exchange (PASS)
D16 invariants: max heat 1.0% · slots <= 2 crypto · +1.0R BE · 8-bar time stop
Entry: $0.6462–$0.6939 (Limit Ladder L1 40% / L2 40% / L3 20%) · Stop: $0.7044 (Structural Invalidation)
T1: $0.6365 (0.93R · Day Value Area) · T2: $0.6268 (1.40R · Volume Node) · T3: $0.6139 (2.33R · Liquidity Sweep)
Composite R: 1.68R · Active Vetoes: LSR 69.9:1 (LB) >= 2.5:1 — passive limit front-running (S3) banned; WAIT FOR THE SWEEP (S1); Table 7 score 2.5 < 5.0 — HARD VETO (NO TRADE)

## FORMULATION · ICP · 2026-11-14 17:58:40 UTC · S1 (Liquidation Sweep Reversal — Magnet Exhaustion)
Regime: TREND_DOWN — H4/D1 Trend + Microstructure Order Flow
Direction: SHORT · Grade: VETO · Confidence: 92%
D1  basisPct: n/a | deltaSpread: 0.0000% (NOT LISTED)
D2  profile: session POC 2.3192 · day VAL/POC/VAH 2.3268/2.3997/2.4402 · month POC 2.5394
D3  VWAP 2.3755 · z -1.77σ · bands ±1σ/2σ
D4  EMA stacks: H4 13x89 · D1 13x89 (Counter-trend / No alignment (0.0 pts))
D5  RSI: M15 32.64 · H1 24.89 · H4 31.93
D6  delta: taker pressure / volume absorption
D7  signals: 0 Bull / 0 Bear · active: No qualifying footprint signal at zone (0.0 pts)
D8  CVD: both-selling · taker buy 44.8% · Active BEAR CVD divergence () -> 1.0 pt
D9  walls: No confirmed wall backstop (0.0 pts) (±5% Imbalance: 0.0%)
D10 LTO: institutional limit orders present
D11 clusters: sweep magnets identified
D12 LSR: 11.6:1 (LB) → GATE: BANNED (Wait for Sweep S1)
D13 GEX: n/a (Non-BTC/ETH perpetual -> 0.0 pts)
D14 OI: Quadrant both-selling
D15 spread: 0.0000% on Delta Exchange (PASS)
D16 invariants: max heat 1.0% · slots <= 2 crypto · +1.0R BE · 8-bar time stop
Entry: $2.2830–$2.4402 (Limit Ladder L1 40% / L2 40% / L3 20%) · Stop: $2.4768 (Structural Invalidation)
T1: $2.2488 (0.94R · Day Value Area) · T2: $2.2145 (1.40R · Volume Node) · T3: $2.1688 (2.34R · Liquidity Sweep)
Composite R: 1.68R · Active Vetoes: LSR 11.6:1 (LB) >= 2.5:1 — passive limit front-running (S3) banned; WAIT FOR THE SWEEP (S1); Not listed on Delta Exchange; Table 7 score 2.5 < 5.0 — HARD VETO (NO TRADE); Model R 0.66 < 1.5 — reward does not pay risk

## FORMULATION · HBAR · 2026-11-14 17:58:40 UTC · S7 (High-Volume Absorption Continuation)
Regime: TREND_DOWN — H4/D1 Trend + Microstructure Order Flow
Direction: SHORT · Grade: VETO · Confidence: 92%
D1  basisPct: n/a | deltaSpread: 0.0515% (HBARUSD)
D2  profile: session POC 0.0602 · day VAL/POC/VAH 0.0584/0.0599/0.0604 · month POC 0.0670
D3  VWAP 0.0594 · z -1.39σ · bands ±1σ/2σ
D4  EMA stacks: H4 13x89 · D1 13x89 (Counter-trend / No alignment (0.0 pts))
D5  RSI: M15 38.97 · H1 28.97 · H4 25.85
D6  delta: taker pressure / volume absorption
D7  signals: 0 Bull / 0 Bear · active: No qualifying footprint signal at zone (0.0 pts)
D8  CVD: spot-bid · taker buy 49.1% · Active BEAR CVD divergence () -> 1.0 pt
D9  walls: No confirmed wall backstop (0.0 pts) (±5% Imbalance: -0.0%)
D10 LTO: institutional limit orders present
D11 clusters: sweep magnets identified
D12 LSR: 1.0:1 (LB) → GATE: PASS
D13 GEX: n/a (Non-BTC/ETH perpetual -> 0.0 pts)
D14 OI: Quadrant spot-bid
D15 spread: 0.0515% on Delta Exchange (PASS)
D16 invariants: max heat 1.0% · slots <= 2 crypto · +1.0R BE · 8-bar time stop
Entry: $0.0581–$0.0604 (Limit Ladder L1 40% / L2 40% / L3 20%) · Stop: $0.0613 (Structural Invalidation)
T1: $0.0573 (0.96R · Day Value Area) · T2: $0.0564 (1.44R · Volume Node) · T3: $0.0552 (2.41R · Liquidity Sweep)
Composite R: 1.73R · Active Vetoes: Table 7 score 1.5 < 5.0 — HARD VETO (NO TRADE)

## FORMULATION · APT · 2026-11-14 17:58:40 UTC · S1 (Liquidation Sweep Reversal — Magnet Exhaustion)
Regime: TREND_DOWN — H4/D1 Trend + Microstructure Order Flow
Direction: SHORT · Grade: VETO · Confidence: 92%
D1  basisPct: n/a | deltaSpread: 0.0420% (APTUSD)
D2  profile: session POC 0.4881 · day VAL/POC/VAH 0.4688/0.4873/0.5116 · month POC 0.6005
D3  VWAP 0.4990 · z -1.40σ · bands ±1σ/2σ
D4  EMA stacks: H4 13x89 · D1 13x89 (Counter-trend / No alignment (0.0 pts))
D5  RSI: M15 30.21 · H1 18.91 · H4 21.43
D6  delta: taker pressure / volume absorption
D7  signals: 0 Bull / 0 Bear · active: No qualifying footprint signal at zone (0.0 pts)
D8  CVD: both-selling · taker buy 46.6% · Active BEAR CVD divergence () -> 1.0 pt
D9  walls: No confirmed wall backstop (0.0 pts) (±5% Imbalance: -0.0%)
D10 LTO: institutional limit orders present
D11 clusters: sweep magnets identified
D12 LSR: 24.7:1 (LB) → GATE: BANNED (Wait for Sweep S1)
D13 GEX: n/a (Non-BTC/ETH perpetual -> 0.0 pts)
D14 OI: Quadrant both-selling
D15 spread: 0.0420% on Delta Exchange (PASS)
D16 invariants: max heat 1.0% · slots <= 2 crypto · +1.0R BE · 8-bar time stop
Entry: $0.4745–$0.5116 (Limit Ladder L1 40% / L2 40% / L3 20%) · Stop: $0.5192 (Structural Invalidation)
T1: $0.4688 (0.75R · Day Value Area) · T2: $0.4603 (1.12R · Volume Node) · T3: $0.4508 (1.86R · Liquidity Sweep)
Composite R: 1.34R · Active Vetoes: LSR 24.7:1 (LB) >= 2.5:1 — passive limit front-running (S3) banned; WAIT FOR THE SWEEP (S1); Table 7 score 3.5 < 5.0 — HARD VETO (NO TRADE); Model R 0.49 < 1.5 — reward does not pay risk

## FORMULATION · ARB · 2026-11-14 17:58:40 UTC · S1 (Liquidation Sweep Reversal — Magnet Exhaustion)
Regime: TREND_DOWN — H4/D1 Trend + Microstructure Order Flow
Direction: SHORT · Grade: VETO · Confidence: 92%
D1  basisPct: n/a | deltaSpread: 0.0148% (ARBUSD)
D2  profile: session POC 0.1400 · day VAL/POC/VAH 0.1364/0.1403/0.1416 · month POC 0.1643
D3  VWAP 0.1387 · z -1.59σ · bands ±1σ/2σ
D4  EMA stacks: H4 13x89 · D1 13x89 (Counter-trend / No alignment (0.0 pts))
D5  RSI: M15 37.57 · H1 30.84 · H4 27.26
D6  delta: taker pressure / volume absorption
D7  signals: 0 Bull / 0 Bear · active: No qualifying footprint signal at zone (0.0 pts)
D8  CVD: both-selling · taker buy 47.8% · Active BEAR CVD divergence () -> 1.0 pt
D9  walls: No confirmed wall backstop (0.0 pts) (±5% Imbalance: 0.0%)
D10 LTO: institutional limit orders present
D11 clusters: sweep magnets identified
D12 LSR: 214.6:1 (LB) → GATE: BANNED (Wait for Sweep S1)
D13 GEX: n/a (Non-BTC/ETH perpetual -> 0.0 pts)
D14 OI: Quadrant both-selling
D15 spread: 0.0148% on Delta Exchange (PASS)
D16 invariants: max heat 1.0% · slots <= 2 crypto · +1.0R BE · 8-bar time stop
Entry: $0.1345–$0.1416 (Limit Ladder L1 40% / L2 40% / L3 20%) · Stop: $0.1438 (Structural Invalidation)
T1: $0.1325 (0.95R · Day Value Area) · T2: $0.1304 (1.42R · Volume Node) · T3: $0.1277 (2.37R · Liquidity Sweep)
Composite R: 1.71R · Active Vetoes: LSR 214.6:1 (LB) >= 2.5:1 — passive limit front-running (S3) banned; WAIT FOR THE SWEEP (S1); Table 7 score 3.5 < 5.0 — HARD VETO (NO TRADE); Model R 0.74 < 1.5 — reward does not pay risk

## FORMULATION · OP · 2026-11-14 17:58:40 UTC · S7 (High-Volume Absorption Continuation)
Regime: TREND_DOWN — H4/D1 Trend + Microstructure Order Flow
Direction: SHORT · Grade: VETO · Confidence: 92%
D1  basisPct: n/a | deltaSpread: 0.3562% (OPUSD)
D2  profile: session POC 0.0851 · day VAL/POC/VAH 0.0851/0.0888/0.0909 · month POC 0.1003
D3  VWAP 0.0874 · z -1.35σ · bands ±1σ/2σ
D4  EMA stacks: H4 13x89 · D1 13x89 (Counter-trend / No alignment (0.0 pts))
D5  RSI: M15 37.33 · H1 24.41 · H4 24.50
D6  delta: taker pressure / volume absorption
D7  signals: 0 Bull / 0 Bear · active: No qualifying footprint signal at zone (0.0 pts)
D8  CVD: both-selling · taker buy 46.4% · Active BEAR CVD divergence () -> 1.0 pt
D9  walls: No confirmed wall backstop (0.0 pts) (±5% Imbalance: -0.2%)
D10 LTO: institutional limit orders present
D11 clusters: sweep magnets identified
D12 LSR: 1.1:1 (LB) → GATE: PASS
D13 GEX: n/a (Non-BTC/ETH perpetual -> 0.0 pts)
D14 OI: Quadrant both-selling
D15 spread: 0.3562% on Delta Exchange (VETO)
D16 invariants: max heat 1.0% · slots <= 2 crypto · +1.0R BE · 8-bar time stop
Entry: $0.0840–$0.0909 (Limit Ladder L1 40% / L2 40% / L3 20%) · Stop: $0.0923 (Structural Invalidation)
T1: $0.0827 (0.92R · Day Value Area) · T2: $0.0815 (1.39R · Volume Node) · T3: $0.0798 (2.31R · Liquidity Sweep)
Composite R: 1.66R · Active Vetoes: Delta spread 0.3562% > 0.15% — execution drag veto; Table 7 score 1.0 < 5.0 — HARD VETO (NO TRADE); Model R 0.53 < 1.5 — reward does not pay risk

## FORMULATION · SUI · 2026-11-14 17:58:40 UTC · S7 (High-Volume Absorption Continuation)
Regime: TREND_DOWN — H4/D1 Trend + Microstructure Order Flow
Direction: SHORT · Grade: VETO · Confidence: 92%
D1  basisPct: n/a | deltaSpread: 0.0411% (SUIUSD)
D2  profile: session POC 0.7441 · day VAL/POC/VAH 0.7426/0.7718/0.7851 · month POC 0.8668
D3  VWAP 0.7588 · z -1.54σ · bands ±1σ/2σ
D4  EMA stacks: H4 13x89 · D1 13x89 (Counter-trend / No alignment (0.0 pts))
D5  RSI: M15 32.71 · H1 24.78 · H4 27.45
D6  delta: taker pressure / volume absorption
D7  signals: 0 Bull / 0 Bear · active: No qualifying footprint signal at zone (0.0 pts)
D8  CVD: both-selling · taker buy 48.3% · Active BEAR CVD divergence () -> 1.0 pt
D9  walls: Delta L2 SELL Wall $50.7k @ 0.7312 -> 1.0 pt (±5% Imbalance: 0.1%)
D10 LTO: institutional limit orders present
D11 clusters: sweep magnets identified
D12 LSR: 2.1:1 (LB) → GATE: PASS
D13 GEX: n/a (Non-BTC/ETH perpetual -> 0.0 pts)
D14 OI: Quadrant both-selling
D15 spread: 0.0411% on Delta Exchange (PASS)
D16 invariants: max heat 1.0% · slots <= 2 crypto · +1.0R BE · 8-bar time stop
Entry: $0.7284–$0.7851 (Limit Ladder L1 40% / L2 40% / L3 20%) · Stop: $0.7968 (Structural Invalidation)
T1: $0.7175 (0.93R · Day Value Area) · T2: $0.7065 (1.39R · Volume Node) · T3: $0.6920 (2.32R · Liquidity Sweep)
Composite R: 1.67R · Active Vetoes: Table 7 score 4.0 < 5.0 — HARD VETO (NO TRADE); Model R 0.50 < 1.5 — reward does not pay risk

## FORMULATION · SEI · 2026-11-14 17:58:40 UTC · S7 (High-Volume Absorption Continuation)
Regime: TREND_DOWN — H4/D1 Trend + Microstructure Order Flow
Direction: SHORT · Grade: VETO · Confidence: 92%
D1  basisPct: n/a | deltaSpread: 0.0506% (SEIUSD)
D2  profile: session POC 0.0398 · day VAL/POC/VAH 0.0398/0.0409/0.0422 · month POC 0.0480
D3  VWAP 0.0406 · z -1.23σ · bands ±1σ/2σ
D4  EMA stacks: H4 13x89 · D1 13x89 (Counter-trend / No alignment (0.0 pts))
D5  RSI: M15 39.75 · H1 28.60 · H4 28.81
D6  delta: taker pressure / volume absorption
D7  signals: 0 Bull / 0 Bear · active: No qualifying footprint signal at zone (0.0 pts)
D8  CVD: both-selling · taker buy 42.9% · Active BEAR CVD divergence () -> 1.0 pt
D9  walls: No confirmed wall backstop (0.0 pts) (±5% Imbalance: -0.0%)
D10 LTO: institutional limit orders present
D11 clusters: sweep magnets identified
D12 LSR: 1.1:1 (SA) → GATE: PASS
D13 GEX: n/a (Non-BTC/ETH perpetual -> 0.0 pts)
D14 OI: Quadrant both-selling
D15 spread: 0.0506% on Delta Exchange (PASS)
D16 invariants: max heat 1.0% · slots <= 2 crypto · +1.0R BE · 8-bar time stop
Entry: $0.0394–$0.0422 (Limit Ladder L1 40% / L2 40% / L3 20%) · Stop: $0.0428 (Structural Invalidation)
T1: $0.0388 (0.93R · Day Value Area) · T2: $0.0382 (1.40R · Volume Node) · T3: $0.0374 (2.33R · Liquidity Sweep)
Composite R: 1.68R · Active Vetoes: Table 7 score 1.5 < 5.0 — HARD VETO (NO TRADE); Model R 0.33 < 1.5 — reward does not pay risk

## FORMULATION · TIA · 2026-11-14 17:58:40 UTC · S1 (Liquidation Sweep Reversal — Magnet Exhaustion)
Regime: TREND_DOWN — H4/D1 Trend + Microstructure Order Flow
Direction: SHORT · Grade: VETO · Confidence: 92%
D1  basisPct: n/a | deltaSpread: 0.0568% (TIAUSD)
D2  profile: session POC 0.3658 · day VAL/POC/VAH 0.3597/0.3680/0.3744 · month POC 0.4380
D3  VWAP 0.3665 · z -1.99σ · bands ±1σ/2σ
D4  EMA stacks: H4 13x89 · D1 13x89 (Counter-trend / No alignment (0.0 pts))
D5  RSI: M15 36.47 · H1 20.63 · H4 25.24
D6  delta: taker pressure / volume absorption
D7  signals: 0 Bull / 0 Bear · active: No qualifying footprint signal at zone (0.0 pts)
D8  CVD: both-selling · taker buy 46.9% · Active BEAR CVD divergence () -> 1.0 pt
D9  walls: No confirmed wall backstop (0.0 pts) (±5% Imbalance: 0.0%)
D10 LTO: institutional limit orders present
D11 clusters: sweep magnets identified
D12 LSR: 9.2:1 (LB) → GATE: BANNED (Wait for Sweep S1)
D13 GEX: n/a (Non-BTC/ETH perpetual -> 0.0 pts)
D14 OI: Quadrant both-selling
D15 spread: 0.0568% on Delta Exchange (PASS)
D16 invariants: max heat 1.0% · slots <= 2 crypto · +1.0R BE · 8-bar time stop
Entry: $0.3516–$0.3744 (Limit Ladder L1 40% / L2 40% / L3 20%) · Stop: $0.3800 (Structural Invalidation)
T1: $0.3463 (0.94R · Day Value Area) · T2: $0.3411 (1.41R · Volume Node) · T3: $0.3340 (2.35R · Liquidity Sweep)
Composite R: 1.69R · Active Vetoes: LSR 9.2:1 (LB) >= 2.5:1 — passive limit front-running (S3) banned; WAIT FOR THE SWEEP (S1); Table 7 score 3.0 < 5.0 — HARD VETO (NO TRADE); Model R 0.44 < 1.5 — reward does not pay risk

## FORMULATION · VET · 2026-11-14 17:58:40 UTC · S1 (Liquidation Sweep Reversal — Magnet Exhaustion)
Regime: TREND_DOWN — H4/D1 Trend + Microstructure Order Flow
Direction: SHORT · Grade: VETO · Confidence: 92%
D1  basisPct: n/a | deltaSpread: 0.0000% (NOT LISTED)
D2  profile: session POC 0.0049 · day VAL/POC/VAH 0.0048/0.0049/0.0051 · month POC 0.0052
D3  VWAP 0.0049 · z -1.38σ · bands ±1σ/2σ
D4  EMA stacks: H4 13x89 · D1 13x89 (Counter-trend / No alignment (0.0 pts))
D5  RSI: M15 38.79 · H1 27.27 · H4 27.15
D6  delta: taker pressure / volume absorption
D7  signals: 0 Bull / 0 Bear · active: No qualifying footprint signal at zone (0.0 pts)
D8  CVD: spot-bid · taker buy 49.7% · Active BEAR CVD divergence () -> 1.0 pt
D9  walls: No confirmed wall backstop (0.0 pts) (±5% Imbalance: 0.1%)
D10 LTO: institutional limit orders present
D11 clusters: sweep magnets identified
D12 LSR: 2.8:1 (LB) → GATE: BANNED (Wait for Sweep S1)
D13 GEX: n/a (Non-BTC/ETH perpetual -> 0.0 pts)
D14 OI: Quadrant spot-bid
D15 spread: 0.0000% on Delta Exchange (PASS)
D16 invariants: max heat 1.0% · slots <= 2 crypto · +1.0R BE · 8-bar time stop
Entry: $0.0047–$0.0051 (Limit Ladder L1 40% / L2 40% / L3 20%) · Stop: $0.0052 (Structural Invalidation)
T1: $0.0047 (0.93R · Day Value Area) · T2: $0.0046 (1.40R · Volume Node) · T3: $0.0045 (2.33R · Liquidity Sweep)
Composite R: 1.68R · Active Vetoes: LSR 2.8:1 (LB) >= 2.5:1 — passive limit front-running (S3) banned; WAIT FOR THE SWEEP (S1); Not listed on Delta Exchange; Table 7 score 2.5 < 5.0 — HARD VETO (NO TRADE); Model R 0.75 < 1.5 — reward does not pay risk

## FORMULATION · 1000PEPE · 2026-11-14 17:58:40 UTC · S1 (Liquidation Sweep Reversal — Magnet Exhaustion)
Regime: RANGE_BALANCE — H4/D1 Trend + Microstructure Order Flow
Direction: LONG · Grade: B · Confidence: 66%
D1  basisPct: n/a | deltaSpread: 0.0101% (1000PEPEUSD)
D2  profile: session POC 0.0039 · day VAL/POC/VAH 0.0040/0.0043/0.0043 · month POC 0.0049
D3  VWAP 0.0042 · z -1.19σ · bands ±1σ/2σ
D4  EMA stacks: H4 13x89 · D1 13x89 (Counter-trend / No alignment (0.0 pts))
D5  RSI: M15 37.35 · H1 26.28 · H4 24.31
D6  delta: taker pressure / volume absorption
D7  signals: 0 Bull / 0 Bear · active: No qualifying footprint signal at zone (0.0 pts)
D8  CVD: spot-bid · taker buy 48.8% · Active BULL CVD divergence () -> 1.0 pt
D9  walls: No confirmed wall backstop (0.0 pts) (±5% Imbalance: 0.1%)
D10 LTO: institutional limit orders present
D11 clusters: sweep magnets identified
D12 LSR: 99.0:1 (SA) → GATE: BANNED (Wait for Sweep S1)
D13 GEX: n/a (Non-BTC/ETH perpetual -> 0.0 pts)
D14 OI: Quadrant spot-bid
D15 spread: 0.0101% on Delta Exchange (PASS)
D16 invariants: max heat 1.0% · slots <= 2 crypto · +1.0R BE · 8-bar time stop
Entry: $0.0039–$0.0040 (Limit Ladder L1 40% / L2 40% / L3 20%) · Stop: $0.0039 (Structural Invalidation)
T1: $0.0043 (6.08R · Day Value Area) · T2: $0.0043 (9.12R · Volume Node) · T3: $0.0042 (15.20R · Liquidity Sweep)
Composite R: 10.94R · Active Vetoes: LSR 99.0:1 (SA) >= 2.5:1 — passive limit front-running (S3) banned; WAIT FOR THE SWEEP (S1); Model R 0.66 < 1.5 — reward does not pay risk

## FORMULATION · 1000SHIB · 2026-11-14 17:58:40 UTC · S1 (Liquidation Sweep Reversal — Magnet Exhaustion)
Regime: TREND_DOWN — H4/D1 Trend + Microstructure Order Flow
Direction: SHORT · Grade: VETO · Confidence: 92%
D1  basisPct: n/a | deltaSpread: 0.0756% (1000SHIBUSD)
D2  profile: session POC 0.0040 · day VAL/POC/VAH 0.0040/0.0041/0.0042 · month POC 0.0045
D3  VWAP 0.0041 · z -1.57σ · bands ±1σ/2σ
D4  EMA stacks: H4 13x89 · D1 13x89 (Counter-trend / No alignment (0.0 pts))
D5  RSI: M15 31.85 · H1 22.92 · H4 26.09
D6  delta: taker pressure / volume absorption
D7  signals: 0 Bull / 0 Bear · active: No qualifying footprint signal at zone (0.0 pts)
D8  CVD: spot-bid · taker buy 47.6% · Active BEAR CVD divergence () -> 1.0 pt
D9  walls: No confirmed wall backstop (0.0 pts) (±5% Imbalance: 0.1%)
D10 LTO: institutional limit orders present
D11 clusters: sweep magnets identified
D12 LSR: 4.9:1 (LB) → GATE: BANNED (Wait for Sweep S1)
D13 GEX: n/a (Non-BTC/ETH perpetual -> 0.0 pts)
D14 OI: Quadrant spot-bid
D15 spread: 0.0756% on Delta Exchange (PASS)
D16 invariants: max heat 1.0% · slots <= 2 crypto · +1.0R BE · 8-bar time stop
Entry: $0.0040–$0.0042 (Limit Ladder L1 40% / L2 40% / L3 20%) · Stop: $0.0043 (Structural Invalidation)
T1: $0.0039 (0.94R · Day Value Area) · T2: $0.0038 (1.41R · Volume Node) · T3: $0.0038 (2.35R · Liquidity Sweep)
Composite R: 1.69R · Active Vetoes: LSR 4.9:1 (LB) >= 2.5:1 — passive limit front-running (S3) banned; WAIT FOR THE SWEEP (S1); Table 7 score 3.0 < 5.0 — HARD VETO (NO TRADE); Model R 0.99 < 1.5 — reward does not pay risk
