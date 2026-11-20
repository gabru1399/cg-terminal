import json

with open('desk/deepscan/LATEST_16D_TELEMETRY.json') as f:
    d = json.load(f)

for sym in ['BTC', 'ETH', 'SOL', 'ADA', 'BNB', 'GOOGL', 'SEI']:
    item = d.get('assets', {}).get(sym)
    if not item:
        print(f"=== {sym} NOT FOUND ===")
        continue
    dims = item.get('dimensions', {})
    d16 = dims.get('D16', {})
    print(f"=== {sym} ===")
    print(f"  Price: {item.get('price')}")
    print(f"  Score: {d16.get('confluence_score_11_5')}, Archetype: {d16.get('best_archetype')}, R: {d16.get('best_r_multiple')}, Status: {d16.get('qualification_status')}")
    print(f"  Day POC: {dims.get('D02', {}).get('day_utc', {}).get('poc')}, VAL: {dims.get('D02', {}).get('day_utc', {}).get('val')}, VAH: {dims.get('D02', {}).get('day_utc', {}).get('vah')}")
    print(f"  VWAP: {dims.get('D03', {}).get('vwap')}, Z: {dims.get('D03', {}).get('z_score')}")
    print(f"  H4 Trend: {dims.get('D04', {}).get('h4_trend')}, D1 Trend: {dims.get('D04', {}).get('d1_trend')}")
    print(f"  Top Signal: {dims.get('D07', {}).get('top_signal')}")
    print(f"  LSR: {dims.get('D12', {}).get('lsr')}, Dominant: {dims.get('D12', {}).get('dominant_side')}, Gate: {dims.get('D12', {}).get('magnet_gate_status')}")
    print(f"  Short Liq: {dims.get('D11', {}).get('nearest_short_cluster_above')}")
    print(f"  Long Liq: {dims.get('D11', {}).get('nearest_long_cluster_below')}")
