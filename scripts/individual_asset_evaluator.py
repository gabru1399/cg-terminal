import urllib.request
import json
import concurrent.futures
import time
import sys

CURATED_61 = [
    # 30 Crypto USDT-M
    "BTC", "ETH", "BNB", "SOL", "XRP", "ADA", "DOGE", "TRX", "LINK", "LTC",
    "AVAX", "DOT", "NEAR", "UNI", "ATOM", "XLM", "ETC", "FIL", "ICP", "HBAR",
    "APT", "ARB", "OP", "SUI", "SEI", "INJ", "TIA", "VET", "1000PEPE", "1000SHIB",
    # 28 TradFi USDT-M
    "XAU", "NVDA", "SNDK", "SOXL", "SPCX", "GOOGL", "MU", "SKHY", "XAG", "CL",
    "INTC", "CRCL", "MSTR", "QQQ", "ANTHROPIC", "AAPL", "TSLA", "DRAM", "KORU", "META",
    "NBIS", "MSFT", "AMZN", "AMD", "COIN", "NFLX", "AVGO", "TSM",
    # 3 Classic
    "SPX500", "UKO", "NDX100"
]

def fetch_json(url, timeout=1.8):
    try:
        req = urllib.request.Request(url, headers={'User-Agent': 'Mozilla/5.0'})
        with urllib.request.urlopen(req, timeout=timeout) as response:
            return json.loads(response.read().decode('utf-8'))
    except Exception:
        return None

def audit_single_asset(sym):
    base = "http://127.0.0.1:3000/api/cg"
    
    # Direct individual narrative call
    narrative = fetch_json(f"{base}/narrative?sym={sym}")
    regime = narrative.get('regime') if narrative else "UNKNOWN"
    model = narrative.get('activeModel') if narrative else "NONE"
    direction = narrative.get('direction') if narrative else "NEUTRAL"
    grade = narrative.get('grade') if narrative else "SKIP"
    ladder = narrative.get('ladder') if narrative else None
    ev = narrative.get('evR') if narrative else None
    
    # Direct individual market call
    market = fetch_json(f"{base}/market?sym={sym}")
    price = market.get('price', {}).get('last') if market else None
    
    top_sig = "NONE"
    lsr = None
    if ladder is not None or grade in ['A', 'A+', 'B']:
        signals = fetch_json(f"{base}/signals?sym={sym}", timeout=1.0)
        sig_list = signals.get('signals', []) if signals else []
        if sig_list:
            top_sig = f"{sig_list[0].get('type')} ({sig_list[0].get('side')})"
        liq = fetch_json(f"{base}/liqlevels?sym={sym}", timeout=1.0)
        lsr = liq.get('lsr') if liq else None

    has_trade = (ladder is not None) and (ev is not None and ev >= 1.50) and (grade in ['A', 'A+'])
    
    return {
        "sym": sym,
        "price": price,
        "regime": regime,
        "model": model,
        "direction": direction,
        "grade": grade,
        "ev": ev,
        "signal": top_sig,
        "lsr": lsr,
        "has_trade": has_trade,
        "ladder": ladder
    }

def main():
    t0 = time.time()
    print("Beginning fresh, individual, endpoint-by-endpoint audit of all 61 Curated Assets...", flush=True)
    results = {}
    with concurrent.futures.ThreadPoolExecutor(max_workers=15) as executor:
        future_to_sym = {executor.submit(audit_single_asset, sym): sym for sym in CURATED_61}
        for future in concurrent.futures.as_completed(future_to_sym):
            res = future.result()
            results[res['sym']] = res
            
    print(f"Audit completed in {time.time()-t0:.2f}s.\n", flush=True)
    print(f"{'SYM':<9} | {'PRICE':<9} | {'REGIME':<14} | {'MODEL':<20} | {'DIR':<6} | {'GR':<3} | {'EV':<6} | {'SIGNAL':<18} | {'STATUS'}", flush=True)
    print("-" * 105, flush=True)
    
    candidates = []
    for sym in CURATED_61:
        r = results.get(sym, {})
        status = "CANDIDATE SETUP" if r.get('has_trade') else "NO_TRADE (VETO)"
        if r.get('has_trade'):
            candidates.append(r)
        p_str = f"{r.get('price'):,.2f}" if r.get('price') else "-"
        ev_str = f"+{r.get('ev')}R" if r.get('ev') is not None else "-"
        print(f"{sym:<9} | {p_str:<9} | {r.get('regime'):<14} | {r.get('model'):<20} | {r.get('direction'):<6} | {r.get('grade'):<3} | {ev_str:<6} | {r.get('signal'):<18} | {status}", flush=True)
        
    print("\n" + "=" * 80, flush=True)
    print(f"VERDICT: Found {len(candidates)} valid candidate setups meeting Table 7 (EV >= 1.5R, Grade A/A+, ladder defined).", flush=True)
    if not candidates:
        print("ACTION: 100% CASH DEFENSE ENFORCED. No high-confluence setups exist across any individual asset.", flush=True)
    else:
        for c in candidates:
            print(f"-> CANDIDATE: {c['sym']} | Direction: {c['direction']} | Ladder: {c['ladder']}", flush=True)
    print("=" * 80, flush=True)

if __name__ == '__main__':
    main()
