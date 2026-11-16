import urllib.request
import json
import math

sym = 'NEAR'
entry = 3.1850
sl = 3.2180
tp = 3.1150
risk = sl - entry
reward = entry - tp
r_mult = reward / risk

def fetch_json(endpoint):
    url = f'http://127.0.0.1:3000{endpoint}'
    try:
        req = urllib.request.Request(url, headers={'User-Agent': 'AdversarialAuditor/3.4'})
        with urllib.request.urlopen(req, timeout=10) as resp:
            return json.loads(resp.read().decode('utf-8'))
    except Exception as e:
        print(f'Error fetching {endpoint}: {e}')
        return None

print('=================== INGESTING TELEMETRY FOR NEAR ===================')
mkt = fetch_json(f'/api/cg/market?sym={sym}')
fp = fetch_json(f'/api/cg/fp?sym={sym}')
liq = fetch_json(f'/api/cg/liqlevels?sym={sym}')
sig = fetch_json(f'/api/cg/signals?sym={sym}')
cvd = fetch_json(f'/api/cg/cvd?sym={sym}')
bw = fetch_json(f'/api/cg/bookwalls?sym={sym}')

# 1. Market Telemetry
price_info = mkt.get('price', {}) if mkt else {}
last_price = float(price_info.get('last') or 0)

auction = mkt.get('auction', {}) if mkt else {}
sess_auc = auction.get('session', {})
sess_poc = float(sess_auc.get('poc') or 0)
sess_vah = float(sess_auc.get('vah') or 0)
sess_val = float(sess_auc.get('val') or 0)

day_auc = auction.get('day', {})
day_poc = float(day_auc.get('poc') or 0)
day_vah = float(day_auc.get('vah') or 0)
day_val = float(day_auc.get('val') or 0)

month_auc = auction.get('month', {})
month_poc = float(month_auc.get('poc') or 0)

vwap_info = mkt.get('vwap', {}) if mkt else {}
vwap_val = float(vwap_info.get('vwap') or 0)
bands = vwap_info.get('bands', {})
sd1 = float(bands.get('sd1') or 0)
z_score = (last_price - vwap_val) / sd1 if sd1 > 0 else 0

emas = mkt.get('ema', {}) if mkt else {}
h4_ema = emas.get('h4', {})
d1_ema = emas.get('d1', {})
h4_trend = 'DOWN' if h4_ema.get('e13', 0) < h4_ema.get('e89', 0) else 'UP'
d1_trend = 'DOWN' if d1_ema.get('e13', 0) < d1_ema.get('e89', 0) else 'UP'

rsis = mkt.get('rsi', {}) if mkt else {}

print(f'Live Price: {last_price}')
print(f'Session (8h) POC: {sess_poc:.4f} | VAH: {sess_vah:.4f} | VAL: {sess_val:.4f}')
print(f'Day POC: {day_poc:.4f} | VAH: {day_vah:.4f} | VAL: {day_val:.4f}')
print(f'Month POC: {month_poc:.4f}')
print(f'Session VWAP: {vwap_val:.4f} (z: {z_score:.2f}σ)')
print(f'Trend: H4={h4_trend} (13:{h4_ema.get("e13", 0):.2f}/89:{h4_ema.get("e89", 0):.2f}), D1={d1_trend} (13:{d1_ema.get("e13", 0):.2f}/89:{d1_ema.get("e89", 0):.2f})')
print(f'RSI: M15={rsis.get("m15"):.1f}, H1={rsis.get("h1"):.1f}, H4={rsis.get("h4"):.1f}')

# 2. Gate 1: Profile & Footprint HVN Clearance
print(f'\n--- GATE 1 CLEARANCE FOR SL={sl} ---')
dist_sess_poc = abs(sl - sess_poc) / sess_poc * 100
dist_day_poc = abs(sl - day_poc) / day_poc * 100
dist_month_poc = abs(sl - month_poc) / month_poc * 100
dist_vwap = abs(sl - vwap_val) / vwap_val * 100

print(f'  Dist to Session (8h) POC ({sess_poc:.4f}): {dist_sess_poc:.3f}% (Clearance >0.8%: {dist_sess_poc > 0.8})')
print(f'  Dist to Day POC ({day_poc:.4f}): {dist_day_poc:.3f}% (Clearance >0.8%: {dist_day_poc > 0.8})')
print(f'  Dist to Month POC ({month_poc:.4f}): {dist_month_poc:.3f}% (Clearance >0.8%: {dist_month_poc > 0.8})')
print(f'  Dist to Session VWAP ({vwap_val:.4f}): {dist_vwap:.3f}% (Clearance >0.8%: {dist_vwap > 0.8})')

bars = fp.get('bars', []) if fp else []
fp_hvn_matches = []
all_pocs = []
for idx, b in enumerate(bars):
    b_fp = b.get('fp', {})
    tick_fp = float(b_fp.get('tick') or 0)
    lo = float(b_fp.get('lo') or 0)
    bc = b_fp.get('bc', [])
    sc = b_fp.get('sc', [])
    b_vol = b_fp.get('b', [])
    s_vol = b_fp.get('s', [])
    if not bc or not sc or tick_fp == 0: continue
    
    n_bins = min(len(bc), len(sc))
    max_c = -1
    max_i = -1
    max_v = -1
    for i in range(n_bins):
        c_tot = bc[i] + sc[i]
        v_tot = (b_vol[i] if i < len(b_vol) else 0) + (s_vol[i] if i < len(s_vol) else 0)
        if c_tot > max_c:
            max_c = c_tot
            max_i = i
            max_v = v_tot
    if max_i >= 0:
        p_poc = lo + max_i * tick_fp
        all_pocs.append({'price': p_poc, 'contracts': max_c, 'vol': max_v, 'ts': b.get('ts')})
        if max_c > 10000:
            d_pct = abs(sl - p_poc) / p_poc * 100
            if d_pct <= 0.8:
                fp_hvn_matches.append({
                    'price': p_poc,
                    'contracts': max_c,
                    'vol': max_v,
                    'dist_pct': d_pct,
                    'ts': b.get('ts')
                })

print(f'  Footprint Bar POCs (>10k contracts) within ±0.8%: {len(fp_hvn_matches)}')
for m in fp_hvn_matches:
    print(f"    MATCH: Bar POC {m['price']} | Contracts: {m['contracts']} | Vol: {m['vol']:.1f} | Dist: {m['dist_pct']:.3f}%")

top_pocs = sorted(all_pocs, key=lambda x: x['contracts'], reverse=True)[:5]
print('  Top 5 Footprint Bar POCs by contracts:')
for p in top_pocs:
    d = abs(sl - p['price']) / p['price'] * 100
    print(f"    POC {p['price']} | Contracts: {p['contracts']} | Vol: {p['vol']:.1f} | Dist to SL: {d:.3f}%")

gate1_pass = (dist_sess_poc > 0.8) and (dist_day_poc > 0.8) and (dist_month_poc > 0.8) and (dist_vwap > 0.8) and (len(fp_hvn_matches) == 0)
print(f'GATE 1 VERDICT: {"PASS" if gate1_pass else "FAIL"}')

# 3. Gate 2: Geometrical Liquidation Risk
print(f'\n--- GATE 2 LIQUIDATION GEOMETRY ---')
liq_stats = liq.get('stats', {}) if liq else {}
bands_liq = liq_stats.get('bands', [])
key_levels = liq_stats.get('keyLevels', {})

below_clusters = key_levels.get('below', [])
vector_a_clusters = [c for c in below_clusters if float(c.get('price', 0)) <= entry]
vector_a_target_path = [c for c in below_clusters if tp <= float(c.get('price', 0)) <= entry]
vector_a_usd = sum(float(c.get('usd', 0)) for c in vector_a_clusters)
print(f'Vector A Downside Traversal Fuel (below Entry {entry}):')
print(f'  Total downside clusters below entry: {len(vector_a_clusters)} (Total: ${vector_a_usd:,.2f})')
for c in vector_a_clusters:
    print(f"    Cluster @ {c.get('price')} | Str: {c.get('strength')} | USD: ${float(c.get('usd', 0)):,.2f} | Dist from last: {c.get('distPct')}%")

above_clusters = key_levels.get('above', [])
vector_b_clusters = [c for c in above_clusters if entry <= float(c.get('price', 0)) <= sl]
vector_b_usd = sum(float(c.get('usd', 0)) for c in vector_b_clusters)

all_overhead_near = [c for c in above_clusters if float(c.get('price', 0)) <= sl + 0.05]
print(f'\nVector B Risk Zone Hazard (between Entry {entry} and SL {sl}):')
print(f'  Clusters directly in Risk Zone [{entry} - {sl}]: {len(vector_b_clusters)} (Total: ${vector_b_usd:,.2f})')
for c in vector_b_clusters:
    print(f"    HAZARD Cluster @ {c.get('price')} | Str: {c.get('strength')} | USD: ${float(c.get('usd', 0)):,.2f} | Venues: {len(c.get('venues', []))}")

print(f'  All overhead clusters near/above SL:')
for c in all_overhead_near:
    print(f"    Overhead Cluster @ {c.get('price')} | Str: {c.get('strength')} | USD: ${float(c.get('usd', 0)):,.2f} | Dist from last: {c.get('distPct')}%")

shorts_2pct = 0
longs_2pct = 0
if len(bands_liq) >= 2:
    shorts_2pct = float(bands_liq[0].get('up', 0)) + float(bands_liq[1].get('up', 0))
    longs_2pct = float(bands_liq[0].get('down', 0)) + float(bands_liq[1].get('down', 0))
dom_2pct = "SA" if shorts_2pct >= longs_2pct else "LB"
skew_2pct_ratio = max(shorts_2pct, longs_2pct) / min(shorts_2pct, longs_2pct) if min(shorts_2pct, longs_2pct) > 0 else 999
print(f'\n±2% Liquidation Skew: {skew_2pct_ratio:.2f}:1 ({dom_2pct}) | Shorts Above: ${shorts_2pct:,.2f} | Longs Below: ${longs_2pct:,.2f}')

# Check dominant squeeze hazard >= $2.0M or LSR >= 2.5:1
lsr_breached = (skew_2pct_ratio >= 2.5 and dom_2pct == "SA")
hazard_exceeds_2m = (vector_b_usd >= 2000000)
# Also check if any single cluster in vector B is catastrophic
single_large_hazard = any(float(c.get('usd', 0)) >= 1000000 and float(c.get('strength', 0)) >= 70 for c in vector_b_clusters)

print(f'  LSR Breached (>=2.5:1 SA): {lsr_breached}')
print(f'  Hazard in Risk Zone >= $2.0M: {hazard_exceeds_2m} (Actual: ${vector_b_usd:,.2f})')
print(f'  Single Large Hazard Cluster in Risk Zone >= $1.0M: {single_large_hazard}')

gate2_pass = (not lsr_breached) and (not hazard_exceeds_2m)
print(f'GATE 2 VERDICT: {"PASS" if gate2_pass else "FAIL"}')

# 4. Table 7 Scoring
print(f'\n--- TABLE 7 CONFLUENCE SCORING ---')
t7_trend = 2.0 if (h4_trend == 'DOWN' and d1_trend == 'DOWN') else (1.0 if (h4_trend == 'DOWN' or d1_trend == 'DOWN') else 0.0)
t7_vwap = 1.5 if entry >= vwap_val else (0.5 if z_score > -0.5 else 0.0)

signals_list = sig.get('signals', []) if sig else []
t7_signal = 0.0
sig_details = []
for s in signals_list[:20]:
    st = s.get('type', '').lower()
    sd = s.get('dir', '').upper()
    sp = float(s.get('price') or 0)
    if ('abs' in st or 'div' in st or 'trap' in st or 'exh' in st) and sd in ['SELL', 'SHORT', 'BEAR']:
        sig_details.append(s)
        if abs(sp - entry) / entry <= 0.02:
            t7_signal = 2.0
            break
        elif t7_signal == 0:
            t7_signal = 1.0

print(f'  Qualifying Footprint Signals found: {len(sig_details)}')
for s in sig_details[:3]:
    print(f"    Signal: {s.get('type')} ({s.get('dir')}) @ {s.get('price')} (ts: {s.get('ts')})")

min_wall = 500000 # alt wall
walls = bw.get('model', {}).get('confirmedWalls', []) if bw else []
t7_wall = 0.0
for w in walls:
    w_usd = float(w.get('usd') or 0)
    w_side = w.get('side', '').lower()
    wp = float(w.get('price') or 0)
    if w_usd >= min_wall and w_side == 'ask':
        if wp >= entry and (wp - entry) / entry <= 0.02:
            t7_wall = 1.5
            break
        elif t7_wall == 0:
            t7_wall = 0.5

divs = cvd.get('divergences', []) if cvd else []
t7_cvd = 1.0 if any('bear' in d.get('type', '').lower() or 'sell' in d.get('type', '').lower() for d in divs) else 0.0

t7_magnet = 0.0
if dom_2pct == "LB":
    if skew_2pct_ratio >= 2.5: t7_magnet = 1.5
    elif skew_2pct_ratio >= 1.5: t7_magnet = 1.0
    else: t7_magnet = 0.5
else:
    # SA dominant
    t7_magnet = 0.0

t7_gex = 0.0 # NEAR is alt perp

# Delta Spread on NEARUSD
# Delta maker rate 0.02%, tick 0.0001
# Check market spread
t7_spread = 1.0 # default assuming <0.05%

t7_total = t7_trend + t7_vwap + t7_signal + t7_wall + t7_cvd + t7_magnet + t7_gex + t7_spread

print(f'Table 7 Factor Breakdown (11.5 max):')
print(f'  Trend (2.0): {t7_trend:.2f} (H4={h4_trend}, D1={d1_trend})')
print(f'  Regime (1.5): {t7_vwap:.2f} (Entry {entry} vs VWAP {vwap_val:.4f})')
print(f'  Signal (2.0): {t7_signal:.2f}')
print(f'  Wall (1.5): {t7_wall:.2f}')
print(f'  CVD (1.0): {t7_cvd:.2f}')
print(f'  Magnet (1.5): {t7_magnet:.2f} (LSR: {skew_2pct_ratio:.2f}:1 {dom_2pct})')
print(f'  GEX (1.0): {t7_gex:.2f}')
print(f'  Spread (1.0): {t7_spread:.2f}')
print(f'TOTAL AUDITED TABLE 7 SCORE: {t7_total:.2f} / 11.5 pts')

# Normalized 8.0 score
f_trend = 1.0 if t7_trend >= 1.5 else (0.5 if t7_trend > 0 else 0.0)
f_regime = 1.0 if t7_vwap >= 1.0 else (0.5 if t7_vwap > 0 else 0.0)
f_signal = 1.0 if t7_signal >= 1.5 else (0.5 if t7_signal > 0 else 0.0)
f_wall = 1.0 if t7_wall >= 1.0 else (0.5 if t7_wall > 0 else 0.0)
f_cvd = 1.0 if t7_cvd >= 1.0 else 0.0
f_magnet = 1.0 if t7_magnet >= 1.0 else (0.5 if t7_magnet > 0 else 0.0)
f_gex = 1.0 if t7_gex >= 1.0 else 0.0
f_spread = 1.0 if t7_spread >= 1.0 else 0.0
score_8_0 = f_trend + f_regime + f_signal + f_wall + f_cvd + f_magnet + f_gex + f_spread
print(f'TOTAL AUDITED NORMALIZED SCORE: {score_8_0:.2f} / 8.0 pts')

print(f'\nRisk: {risk:.4f} | Reward: {reward:.4f} | R-Multiple: {r_mult:.2f}R')

overall_pass = gate1_pass and gate2_pass and (t7_total >= 5.0) and (r_mult >= 2.0)
print(f'\n>>> FINAL AUDIT VERDICT: {"PASS" if overall_pass else "VETO"} <<<')
