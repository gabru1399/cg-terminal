import urllib.request
import json

base_url = "http://127.0.0.1:3000"

targets = [
    'BTC', 'ETH', 'BNB', 'SOL', 'XRP', 'ADA', 'DOGE', 'TRX', 'LINK', 'LTC', 
    'AVAX', 'DOT', 'NEAR', 'UNI', 'ATOM', 'XLM', 'ETC', 'FIL', 'ICP', 'HBAR', 
    'APT', 'ARB', 'OP', 'SUI', 'SEI', 'INJ', 'TIA', 'VET', '1000PEPE', '1000SHIB'
]

skew_results = []

for sym in targets:
    try:
        req = urllib.request.Request(f"{base_url}/api/cg/liqlevels?sym={sym}")
        with urllib.request.urlopen(req, timeout=3) as resp:
            data = json.loads(resp.read().decode('utf-8'))
        
        stats = data.get("stats", {})
        totals = stats.get("totals", {})
        shorts = totals.get("shorts", 0) # above
        longs = totals.get("longs", 0)   # below
        last = stats.get("last", 0)
        
        if shorts > 0 and longs > 0:
            long_to_short = longs / shorts # skew towards longs below
            short_to_long = shorts / longs # skew towards shorts above
        else:
            long_to_short = 0
            short_to_long = 0
            
        skew_results.append({
            "sym": sym,
            "last": last,
            "longs_below_m": longs / 1e6,
            "shorts_above_m": shorts / 1e6,
            "long_to_short_skew": round(long_to_short, 2),
            "short_to_long_skew": round(short_to_long, 2)
        })
    except Exception as e:
        pass

# Sort by highest Longs Below Skew (perfect fuel for SHORTS)
skew_results.sort(key=lambda x: x["long_to_short_skew"], reverse=True)

print("Top 10 Assets with Longs Below Magnet (Fuel for SHORTS):")
for r in skew_results[:10]:
    print(f"{r['sym']:<10} | Price: {r['last']:<10} | Longs Below: ${r['longs_below_m']:.2f}M | Shorts Above: ${r['shorts_above_m']:.2f}M | Long Skew: {r['long_to_short_skew']}:1")

print("\nTop 5 Assets with Shorts Above Magnet:")
skew_results.sort(key=lambda x: x["short_to_long_skew"], reverse=True)
for r in skew_results[:5]:
    print(f"{r['sym']:<10} | Price: {r['last']:<10} | Shorts Above: ${r['shorts_above_m']:.2f}M | Longs Below: ${r['longs_below_m']:.2f}M | Short Skew: {r['short_to_long_skew']}:1")
