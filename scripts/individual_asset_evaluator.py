import urllib.request
import json
import concurrent.futures
import time
import sys
import os
import re

def load_universe():
    curated_path = os.path.join(os.path.dirname(__file__), '..', 'src', 'lib', 'universe', 'curated.ts')
    if os.path.exists(curated_path):
        with open(curated_path, 'r', encoding='utf-8') as f:
            text = f.read()
        syms = re.findall(r'sym:\s*"([^"]+)"', text)
        seen = set()
        universe = []
        for s in syms:
            if s not in seen:
                seen.add(s)
                universe.append(s)
        if universe:
            return universe
    return [
        "BTC", "ETH", "BNB", "SOL", "XRP", "ADA", "DOGE", "TRX", "LINK", "LTC",
        "AVAX", "DOT", "NEAR", "UNI", "ATOM", "XLM", "ETC", "FIL", "ICP", "HBAR",
        "APT", "ARB", "OP", "SUI", "SEI", "INJ", "TIA", "VET", "1000PEPE", "1000SHIB",
        "XAU", "NVDA", "SNDK", "SOXL", "SPCX", "GOOGL", "MU", "SKHY", "XAG", "CL",
        "INTC", "CRCL", "MSTR", "QQQ", "ANTHROPIC", "AAPL", "TSLA", "DRAM", "KORU", "META",
        "NBIS", "MSFT", "AMZN", "AMD", "COIN", "NFLX", "AVGO", "TSM",
        "SPX500", "UKO", "NDX100"
    ]

EXPANDED_UNIVERSE = load_universe()

def fetch_json(url, timeout=8.0):
    try:
        req = urllib.request.Request(url, headers={'User-Agent': 'Mozilla/5.0'})
        with urllib.request.urlopen(req, timeout=timeout) as response:
            return json.loads(response.read().decode('utf-8'))
    except Exception:
        return None

def audit_single_asset(sym):
    base = "http://127.0.0.1:3000/api/cg"
    
    # 1. Direct individual narrative call (consolidated microstructure intelligence)
    narrative = fetch_json(f"{base}/narrative?sym={sym}", timeout=4.0)
    regime = narrative.get('regime') if narrative else "UNKNOWN"
    model = narrative.get('activeModel') if narrative else "NONE"
    direction = narrative.get('direction') if narrative else "NEUTRAL"
    grade = narrative.get('grade') if narrative else "SKIP"
    confidence = narrative.get('confidence') if narrative else 0
    
    plan = narrative.get('plan') if narrative else {}
    ladder = plan.get('ladder') if plan else None
    entry_zone = plan.get('entryZone') if plan else None
    stop = plan.get('stop') if plan else None
    targets = plan.get('targets', []) if plan else []
    best_r = plan.get('bestR') if plan else None
    
    prob = narrative.get('probability') if narrative else {}
    p_win = prob.get('pWin') if prob else None
    ev_r = prob.get('evR') if prob else None
    
    ctx = narrative.get('context') if narrative else {}
    price = ctx.get('price') if ctx else None
    vwap = None
    
    # Candidate eligibility: Must have defined entry ladder, Grade A or A+, and composite Best R >= 2.00R (User Directive: Target > 2R)
    has_trade = (ladder is not None) and (best_r is not None and best_r >= 2.00) and (grade in ['A', 'A+'])
    
    top_sig = "NONE"
    if narrative and narrative.get('checklist'):
        for item in narrative['checklist']:
            if item.get('key') == 'footprint' and item.get('pass'):
                top_sig = item.get('value', 'PASS')[:18]
                break

    # If candidate setup, enrich with market VWAP and signals
    if has_trade:
        market = fetch_json(f"{base}/market?sym={sym}", timeout=4.0)
        if market:
            price = market.get('price', {}).get('last', price)
            vwap = market.get('vwap', {}).get('vwap')
        signals = fetch_json(f"{base}/signals?sym={sym}", timeout=3.0)
        sig_list = signals.get('signals', []) if signals else []
        if sig_list:
            top_sig = f"{sig_list[0].get('type')} ({sig_list[0].get('side')})"
    
    return {
        "sym": sym,
        "price": price,
        "vwap": vwap,
        "regime": regime,
        "model": model,
        "direction": direction,
        "grade": grade,
        "confidence": confidence,
        "best_r": best_r,
        "ev_r": ev_r,
        "p_win": p_win,
        "signal": top_sig,
        "has_trade": has_trade,
        "ladder": ladder,
        "entry_zone": entry_zone,
        "stop": stop,
        "targets": targets
    }

def main():
    t0 = time.time()
    print(f"Beginning fresh, individual, endpoint-by-endpoint audit of all {len(EXPANDED_UNIVERSE)} Expanded Universe Assets...", flush=True)
    results = {}
    with concurrent.futures.ThreadPoolExecutor(max_workers=8) as executor:
        future_to_sym = {executor.submit(audit_single_asset, sym): sym for sym in EXPANDED_UNIVERSE}
        for future in concurrent.futures.as_completed(future_to_sym):
            res = future.result()
            results[res['sym']] = res
            
    print(f"Audit completed in {time.time()-t0:.2f}s.\n", flush=True)
    print(f"{'SYM':<9} | {'PRICE':<9} | {'REGIME':<14} | {'MODEL':<18} | {'DIR':<5} | {'GR':<3} | {'R-MULT':<6} | {'WIN%':<5} | {'ORACLE':<6} | {'SIGNAL':<16} | {'STATUS'}", flush=True)
    print("-" * 120, flush=True)
    
    candidates = []
    for sym in EXPANDED_UNIVERSE:
        r = results.get(sym, {})
        status = "CANDIDATE SETUP" if r.get('has_trade') else "NO_TRADE (VETO)"
        if r.get('has_trade'):
            candidates.append(r)
        p_str = f"{r.get('price'):,.2f}" if r.get('price') else "-"
        r_str = f"{r.get('best_r'):.2f}R" if r.get('best_r') is not None else "-"
        win_str = f"{int(r.get('p_win')*100)}%" if r.get('p_win') is not None else "-"
        ora_str = f"{r.get('oracle_score')}/100" if r.get('oracle_score') is not None else "-"
        print(f"{sym:<9} | {p_str:<9} | {r.get('regime'):<14} | {r.get('model'):<18} | {r.get('direction'):<5} | {r.get('grade'):<3} | {r_str:<6} | {win_str:<5} | {ora_str:<6} | {r.get('signal'):<16} | {status}", flush=True)
        
    print("\n" + "=" * 80, flush=True)
    print(f"VERDICT: Found {len(candidates)} valid candidate setups meeting Table 7 (BestR >= 2.0R, Grade A/A+, ladder defined).", flush=True)
    if not candidates:
        print("ACTION: 100% CASH DEFENSE ENFORCED. No high-confluence setups exist across any individual asset.", flush=True)
    else:
        base = "http://127.0.0.1:3000/api/cg"
        print(f"\nExtracting Deep Forensic Telemetry (Oracle + Liq Levels) for {len(candidates)} candidate setups...", flush=True)
        for c in candidates:
            sym = c['sym']
            oracle = fetch_json(f"{base}/oracle?sym={sym}", timeout=15.0)
            if oracle and oracle.get('ok'):
                c['oracle_score'] = oracle.get('score')
                c['oracle_verdict'] = oracle.get('verdict', 'n/a')
                c['oracle_factors'] = oracle.get('factors', [])
            liq = fetch_json(f"{base}/liqlevels?sym={sym}", timeout=10.0)
            if liq and liq.get('ok'):
                c['lsr'] = liq.get('lsr')

            print(f"\n-> CANDIDATE: {c['sym']} ({c['direction']} {c['grade']}) | Oracle: {c.get('oracle_score')}/100 ({c.get('oracle_verdict')})")
            print(f"   Entry Zone: {c['entry_zone']} | Stop: {c['stop']} | Best R: {c['best_r']:.2f}R | Win%: {c['p_win']}")
            print(f"   Targets: {c['targets']}")
            if c.get('oracle_factors'):
                print("   ATHENA ORACLE TELEMETRY (6 GODS CONFLUENCE):")
                for f in c['oracle_factors']:
                    print(f"     * {f.get('name')} ({f.get('id')}): {f.get('score')}/100 (wt {f.get('weight')}) -> {f.get('detail')}")

if __name__ == '__main__':
    main()
