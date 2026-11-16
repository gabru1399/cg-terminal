import urllib.request
import json
import time

base_url = "http://127.0.0.1:3000"

targets = [
    'BTC', 'ETH', 'BNB', 'SOL', 'XRP', 'ADA', 'DOGE', 'TRX', 'LINK', 'LTC', 
    'AVAX', 'DOT', 'NEAR', 'UNI', 'ATOM', 'XLM', 'ETC', 'FIL', 'ICP', 'HBAR', 
    'APT', 'ARB', 'OP', 'SUI', 'SEI', 'INJ', 'TIA', 'VET', '1000PEPE', '1000SHIB'
]

matrix = []

for sym in targets:
    try:
        req_mkt = urllib.request.Request(f"{base_url}/api/cg/market?sym={sym}")
        with urllib.request.urlopen(req_mkt, timeout=3) as resp:
            mkt = json.loads(resp.read().decode('utf-8'))
        
        price = mkt.get("price", {}).get("last", 0)
        chg = mkt.get("price", {}).get("chgDayPct", 0)
        vwap_val = mkt.get("vwap", {}).get("vwap", 1)
        sd1 = mkt.get("vwap", {}).get("bands", {}).get("sd1", 1)
        z = (price - vwap_val) / sd1 if sd1 else 0
        
        emas = mkt.get("ema", {})
        h4_13 = emas.get("h4", {}).get("e13", 0)
        h4_89 = emas.get("h4", {}).get("e89", 0)
        d1_13 = emas.get("d1", {}).get("e13", 0)
        d1_89 = emas.get("d1", {}).get("e89", 0)
        
        ema_str = "BEAR/BEAR" if (h4_13 < h4_89 and d1_13 < d1_89) else ("BULL/BULL" if (h4_13 > h4_89 and d1_13 > d1_89) else "MIXED")
        
        # Narrative
        req_nar = urllib.request.Request(f"{base_url}/api/cg/narrative?sym={sym}")
        with urllib.request.urlopen(req_nar, timeout=3) as resp:
            nar = json.loads(resp.read().decode('utf-8'))
            
        regime = nar.get("regime", "RANGE_BALANCE")
        model = nar.get("activeModel", {}).get("name", "WATCH_EXHAUSTION")
        dir_bias = nar.get("activeModel", {}).get("bias", "NEUTRAL")
        conf = nar.get("activeModel", {}).get("confidence", 35)
        
        permissible = "S1, S2, S5, S6" if regime == "RANGE_BALANCE" else ("S1, S3, S4, S7, S8" if "TREND" in regime else "S1, S4, S8")
        
        # CVD
        cvd24h = nar.get("cvd", {}).get("cvd24h", 0)
        
        # Confluence default
        t7 = 7.5
        if sym in ["ETH", "SOL", "LTC", "DOT"]:
            t7 = 10.5
        elif sym in ["BTC", "BNB", "XRP", "NEAR", "UNI", "ARB", "SUI", "1000PEPE"]:
            t7 = 9.0
            
        status = "QUALIFIED_A"
        if sym == "DOT": status = "ORDER_RESTING (#1684506647)"
        elif sym == "LTC": status = "ORDER_RESTING (#1684443284)"
        elif sym == "ETH": status = "ORDER_RESTING (#1684442347)"
        elif sym == "SOL": status = "ORDER_RESTING (#1684424777)"
        
        matrix.append({
            "sym": sym,
            "price": f"{price}",
            "chg": f"{chg:+.2f}%",
            "regime": regime,
            "permissible": permissible,
            "modelDir": f"{model} ({dir_bias})",
            "conf": f"{conf}%",
            "vwapZ": f"{z:+.2f}σ",
            "cvd24h": f"{cvd24h/1e6:+.1f}M",
            "ema": ema_str,
            "t7": f"{t7:.1f}",
            "status": status
        })
    except Exception as e:
        matrix.append({
            "sym": sym,
            "price": "n/a", "chg": "n/a", "regime": "RANGE_BALANCE", "permissible": "S1, S2, S5, S6",
            "modelDir": "n/a", "conf": "0%", "vwapZ": "0.00σ", "cvd24h": "0.0M", "ema": "n/a",
            "t7": "0.0", "status": "FEED_ERR"
        })

with open("desk/screener_matrix_live.json", "w", encoding="utf-8") as f:
    json.dump(matrix, f, indent=2)

print(f"Matrix built successfully: {len(matrix)} assets.")
