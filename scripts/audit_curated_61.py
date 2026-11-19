import urllib.request
import json
import concurrent.futures
import time

CURATED_61 = [
    # 30 Crypto USDT-M Perps
    "BTC", "ETH", "BNB", "SOL", "XRP", "ADA", "DOGE", "TRX", "LINK", "LTC",
    "AVAX", "DOT", "NEAR", "UNI", "ATOM", "XLM", "ETC", "FIL", "ICP", "HBAR",
    "APT", "ARB", "OP", "SUI", "SEI", "INJ", "TIA", "VET", "1000PEPE", "1000SHIB",
    # 28 TradFi USDT-M Perps
    "XAU", "NVDA", "SNDK", "SOXL", "SPCX", "GOOGL", "MU", "SKHY", "XAG", "CL",
    "INTC", "CRCL", "MSTR", "QQQ", "ANTHROPIC", "AAPL", "TSLA", "DRAM", "KORU", "META",
    "NBIS", "MSFT", "AMZN", "AMD", "COIN", "NFLX", "AVGO", "TSM",
    # 3 Classic Indices/Commodities
    "SPX500", "UKO", "NDX100"
]

def fetch_json(url, timeout=2.0):
    try:
        req = urllib.request.Request(url, headers={'User-Agent': 'Mozilla/5.0'})
        with urllib.request.urlopen(req, timeout=timeout) as response:
            return json.loads(response.read().decode('utf-8'))
    except Exception:
        return None

def audit_symbol(sym):
    base = "http://127.0.0.1:3000/api/cg"
    narrative = fetch_json(f"{base}/narrative?sym={sym}")
    
    price = None
    regime = "CHOP/RANGE"
    model = "NONE"
    direction = "NEUTRAL"
    grade = "SKIP"
    best_r = 0.0
    ev_r = 0.0
    p_win = 0.0
    top_sig = "NONE"
    lsr = 1.0
    
    if narrative:
        regime = narrative.get('regime', 'RANGE_BALANCE')
        model = narrative.get('activeModel', 'NONE')
        direction = narrative.get('direction', 'NEUTRAL')
        grade = narrative.get('grade', 'SKIP')
        plan = narrative.get('plan') or {}
        best_r = plan.get('bestR') or 0.0
        prob = narrative.get('probability') or {}
        p_win = prob.get('pWin') or 0.0
        ev_r = prob.get('evR') or 0.0
        ctx = narrative.get('context') or {}
        price = ctx.get('price')
        
        # Check signals
        checklist = narrative.get('checklist') or []
        for chk in checklist:
            if chk.get('key') == 'footprint' and chk.get('pass'):
                top_sig = str(chk.get('value', 'PASS'))[:16]
                break

    # If Grade A or B or high R, fetch liqlevels and signals directly
    if grade in ['A', 'A+', 'B'] or best_r >= 1.5:
        liq = fetch_json(f"{base}/liqlevels?sym={sym}")
        if liq and liq.get('ok'):
            lsr = liq.get('lsr', 1.0)
            
        sigs = fetch_json(f"{base}/signals?sym={sym}")
        if sigs and sigs.get('sets'):
            for s_set in sigs['sets']:
                for s in s_set.get('sigs', []):
                    st = s.get('t', '')
                    side = s.get('side', '')
                    sig_map = {"abs": "Absorption", "trap": "Trap", "sdiv": "StrongDiv", "div": "Divergence", "exh": "Exhaustion"}
                    top_sig = f"{sig_map.get(st, st)} ({side})"
                    break
                if top_sig != "NONE":
                    break

    # Compute Table 7 Confluence Score
    score = 0.0
    # F1: Trend
    if regime in ['TREND_UP', 'TREND_DOWN']:
        score += 1.5
    # F2: Auction / VWAP
    if model in ['S1', 'S2', 'S5', 'S7', 'S9']:
        score += 1.5
    # F3: Footprint
    if "Absorption" in top_sig or "StrongDiv" in top_sig:
        score += 2.0
    elif "Trap" in top_sig or "Divergence" in top_sig or "Exhaustion" in top_sig:
        score += 1.0
    # F4: Playbook alignment
    if best_r >= 2.0:
        score += 1.5
    # F5: Liquidity / LSR
    if lsr >= 2.5:
        if model == 'S1':
            score += 1.5 # S1 sweep valid
        else:
            score -= 1.0 # Passive front run penalty
    elif lsr < 2.0:
        score += 1.0
        
    score = min(max(score, 0.0), 10.0)

    # Determine status
    if score >= 7.0 and best_r >= 2.0 and grade in ['A', 'A+']:
        status = "A+ QUALIFIED"
    elif score >= 5.0 and best_r >= 1.5 and grade in ['A', 'B']:
        status = "GRADE B WATCH"
    else:
        status = "NO TRADE (VETO)"

    return {
        "sym": sym,
        "price": price,
        "regime": regime,
        "model": model,
        "direction": direction,
        "grade": grade,
        "best_r": best_r,
        "p_win": p_win,
        "ev_r": ev_r,
        "signal": top_sig,
        "lsr": lsr,
        "score": score,
        "status": status
    }

def main():
    t0 = time.time()
    results = []
    with concurrent.futures.ThreadPoolExecutor(max_workers=16) as executor:
        futs = {executor.submit(audit_symbol, sym): sym for sym in CURATED_61}
        for f in concurrent.futures.as_completed(futs):
            try:
                results.append(f.result())
            except Exception as e:
                pass

    results.sort(key=lambda x: CURATED_61.index(x['sym']) if x['sym'] in CURATED_61 else 999)
    print(f"=== FULL MARKET AUDIT: CURATED 61 ASSETS ({time.time()-t0:.2f}s) ===")
    print(f"{'SYM':<9} | {'PRICE':<10} | {'REGIME':<14} | {'ARCHETYPE':<10} | {'BIAS':<5} | {'GR':<3} | {'R-MULT':<6} | {'LSR':<5} | {'SCORE':<5} | {'TOP SIGNAL':<18} | {'STATUS'}")
    print("-" * 120)
    for r in results:
        p_str = f"{r['price']:,.2f}" if r['price'] is not None else "-"
        r_str = f"{r['best_r']:.2f}R" if r['best_r'] > 0 else "-"
        lsr_str = f"{r['lsr']:.2f}" if r['lsr'] else "1.0"
        print(f"{r['sym']:<9} | {p_str:<10} | {r['regime'][:14]:<14} | {r['model'][:10]:<10} | {r['direction'][:5]:<5} | {r['grade']:<3} | {r_str:<6} | {lsr_str:<5} | {r['score']:<5.1f} | {r['signal'][:18]:<18} | {r['status']}")

    candidates = [r for r in results if r['status'] == "A+ QUALIFIED"]
    watchlist = [r for r in results if r['status'] == "GRADE B WATCH"]
    print("\n" + "=" * 80)
    print(f"AUDIT SUMMARY: {len(candidates)} A+ QUALIFIED | {len(watchlist)} GRADE B WATCH | {len(results)-len(candidates)-len(watchlist)} NO TRADE VETOES")
    if candidates:
        print("\n--> QUALIFIED A+ CANDIDATES:")
        for c in candidates:
            print(f"  * {c['sym']} {c['direction']} ({c['model']}) — Score: {c['score']}/10, BestR: {c['best_r']:.2f}R, Signal: {c['signal']}")
    if watchlist:
        print("\n--> GRADE B WATCHLIST (Near Misses):")
        for w in watchlist:
            print(f"  * {w['sym']} {w['direction']} ({w['model']}) — Score: {w['score']}/10, BestR: {w['best_r']:.2f}R, Signal: {w['signal']}")

if __name__ == '__main__':
    main()
