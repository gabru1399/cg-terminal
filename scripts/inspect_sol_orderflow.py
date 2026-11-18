import urllib.request, json

def inspect_sol():
    req = urllib.request.Request('http://127.0.0.1:3000/api/cg/liqlevels?sym=SOL', headers={'User-Agent': 'Mozilla/5.0'})
    with urllib.request.urlopen(req) as resp:
        d = json.loads(resp.read().decode('utf-8'))
        last_price = d.get('stats', {}).get('last')
        print(f"=== SOL LIQUIDATION LEVELS (Last Price: ${last_price}) ===")
        print("\n--- Short Liquidation Pools (Stops of Short Sellers / Magnet for Upward Sweeps) ---")
        for l in d.get('stats', {}).get('keyLevels', {}).get('above', []):
            p = l.get('price')
            u = l.get('usd', 0)
            s = l.get('strength', 0)
            venues = ", ".join(l.get('venues', []))
            print(f"  Price: ${p:.2f} | Pool: ${u:,.0f} USD | Strength: {s:.1f}% | Venues: {venues}")
            
        print("\n--- Long Liquidation Pools (Stops of Long Buyers / Downside Cascade Targets) ---")
        for l in d.get('stats', {}).get('keyLevels', {}).get('below', []):
            p = l.get('price')
            u = l.get('usd', 0)
            s = l.get('strength', 0)
            venues = ", ".join(l.get('venues', []))
            print(f"  Price: ${p:.2f} | Pool: ${u:,.0f} USD | Strength: {s:.1f}% | Venues: {venues}")

    # Check totals & skew
    totals = d.get('stats', {}).get('totals', {})
    print(f"\nTotal Short Liq Above: ${totals.get('shortUsd', 0):,.0f} vs Total Long Liq Below: ${totals.get('longUsd', 0):,.0f}")
    if totals.get('longUsd', 0) > 0:
        ratio = totals.get('shortUsd', 0) / totals.get('longUsd', 0)
        print(f"Liquidation Skew Ratio (Short:Long): {ratio:.2f}")

    # Book walls
    req_bw = urllib.request.Request('http://127.0.0.1:3000/api/cg/bookwalls?sym=SOL', headers={'User-Agent': 'Mozilla/5.0'})
    with urllib.request.urlopen(req_bw) as resp:
        bw = json.loads(resp.read().decode('utf-8'))
        print("\n=== SOL ORDER BOOK DEPTH & WALLS ===")
        model = bw.get('model', {})
        print("Model keys:", list(model.keys()))
        last_snap = model.get('last', {})
        print(f"Snapshot Price: {last_snap.get('price')}")
        bids = sorted(last_snap.get('bids', []), key=lambda x: x.get('usd', 0), reverse=True)[:5]
        asks = sorted(last_snap.get('asks', []), key=lambda x: x.get('usd', 0), reverse=True)[:5]
        print("Top Resting Bid Walls (Support):")
        for b in bids:
            print(f"  Price: ${b.get('p')} | Size: ${b.get('usd', 0):,.0f}")
        print("Top Resting Ask Walls (Resistance):")
        for a in asks:
            print(f"  Price: ${a.get('p')} | Size: ${a.get('usd', 0):,.0f}")

if __name__ == '__main__':
    inspect_sol()

def print_all_clusters():
    req = urllib.request.Request('http://127.0.0.1:3000/api/cg/liqlevels?sym=SOL', headers={'User-Agent': 'Mozilla/5.0'})
    with urllib.request.urlopen(req) as resp:
        d = json.loads(resp.read().decode('utf-8'))
        clusters = d.get('stats', {}).get('keyLevels', {}).get('above', [])
        print('\n--- ALL SHORT CLUSTERS ABOVE (sorted by price) ---')
        for c in sorted(clusters, key=lambda x: x['price']):
            print("  Price: " + str(c['price']) + " | Strength: " + str(c.get('strength')) + "% | USD: " + str(c.get('usd')))

if __name__ == '__main__':
    print_all_clusters()
