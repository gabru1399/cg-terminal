import urllib.request
import json

base = "http://127.0.0.1:3000"

req = urllib.request.Request(f"{base}/api/cg/screener", headers={'User-Agent': 'Mozilla/5.0'})
with urllib.request.urlopen(req, timeout=5.0) as r:
    data = json.loads(r.read().decode('utf-8'))

rows = data.get("rows", [])
print(f"Total Rows: {len(rows)}")

# Filter and format
print("\n" + "="*110)
print(f"{'SYM':<8} | {'PRICE':<9} | {'24H%':<6} | {'EV(R)':<6} | {'VWAP z':<7} | {'RVOL':<5} | {'M1/M2 MODEL':<18} | {'CONFLUENCE':<10} | {'FOOTPRINT':<18} | {'LIQ MAGNET':<16}")
print("="*110)

for r in rows:
    sym = r.get("sym", "")
    price = r.get("price")
    price_str = f"{price:.4f}" if price and price < 1 else (f"{price:.2f}" if price else "-")
    chg = r.get("chg24hPct")
    chg_str = f"{chg:+.1f}%" if chg is not None else "-"
    
    m1m2 = r.get("m1m2") or {}
    ev = m1m2.get("evR")
    ev_str = f"{ev:+.2f}R" if ev is not None else "-"
    model = m1m2.get("activeModel", "-")
    dir_m = m1m2.get("direction", "")
    grade_m = m1m2.get("grade", "")
    m_str = f"{model} ({grade_m})" if model != "-" else "-"
    
    vwap_z = r.get("vwapZ")
    z_str = f"{vwap_z:+.2f}σ" if vwap_z is not None else "-"
    rvol = r.get("rvol")
    rvol_str = f"{rvol:.2f}x" if rvol is not None else "-"
    
    conf = r.get("confluence") or {}
    readiness = conf.get("readiness", "-")
    bias = conf.get("bias", "")
    conf_str = f"{readiness} {bias}".strip()
    
    sig = r.get("signal") or {}
    sig_title = sig.get("title", "")
    sig_side = sig.get("side", "")
    sig_bt = sig.get("bt", "")
    sig_str = f"{sig_side.upper()} {sig_title}" if sig_title else "-"
    
    liq = r.get("liqMagnet") or {}
    liq_usd = liq.get("usd")
    liq_dist = liq.get("distPct")
    if liq_usd and liq_dist:
        u_str = f"${liq_usd/1e6:.1f}M" if liq_usd >= 1e6 else f"${liq_usd/1e3:.0f}k"
        magnet_str = f"{liq_dist:+.1f}% {u_str}"
    else:
        magnet_str = "-"
        
    print(f"{sym:<8} | {price_str:<9} | {chg_str:<6} | {ev_str:<6} | {z_str:<7} | {rvol_str:<5} | {m_str:<18} | {conf_str:<10} | {sig_str:<18} | {magnet_str:<16}")
