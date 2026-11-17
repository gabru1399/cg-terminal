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
        sig_list = []
        if signals and signals.get('sets'):
            for s_set in signals['sets']:
                for s in s_set.get('sigs', []):
                    sig_list.append(s)
        sig_list.sort(key=lambda x: x.get('ts', 0), reverse=True)
        if sig_list:
            top = sig_list[0]
            sig_name = {"abs": "Absorption", "trap": "Trap", "sdiv": "Strong Div", "div": "Divergence", "exh": "Exhaustion"}.get(top.get('t'), top.get('t', 'Signal'))
            top_sig = f"{sig_name} ({top.get('side')})"
    
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

def enrich_candidate(c):
    base = "http://127.0.0.1:3000/api/cg"
    sym = c['sym']
    oracle = fetch_json(f"{base}/oracle?sym={sym}", timeout=4.0)
    if oracle and oracle.get('ok'):
        c['oracle_score'] = oracle.get('score')
        c['oracle_verdict'] = oracle.get('verdict', 'n/a')
        c['oracle_factors'] = oracle.get('factors', [])
    liq = fetch_json(f"{base}/liqlevels?sym={sym}", timeout=4.0)
    if liq and liq.get('ok'):
        c['lsr'] = liq.get('lsr')
        c['liq_stats'] = liq.get('stats', {})

    market = fetch_json(f"{base}/market?sym={sym}", timeout=4.0)
    ema_data = market.get('ema', {}) if market else {}
    
    # Dual-Spine EMA 89 ⟷ EMA 233 Narrative Extraction
    m15_89 = ema_data.get('m15', {}).get('e89')
    m15_233 = ema_data.get('m15', {}).get('e233')
    h1_89 = ema_data.get('h1', {}).get('e89')
    h1_233 = ema_data.get('h1', {}).get('e233')
    
    narrative_state = "STANDARD"
    if h1_89 and h1_233 and c.get('price'):
        p = c['price']
        if h1_89 < h1_233: # Bear Regime
            if p > h1_89 and p < h1_233:
                narrative_state = "TRAP_ZONE (Between 89 & 233) — Bear Trap Ambush"
            elif abs(p - h1_89) / h1_89 <= 0.003:
                narrative_state = "BASELINE_DEFENSE (Testing declining 1H EMA 89)"
            elif abs(p - h1_233) / h1_233 <= 0.003:
                narrative_state = "MACRO_SPINE_COLLISION (Testing declining 1H EMA 233)"
        else: # Bull Regime
            if p < h1_89 and p > h1_233:
                narrative_state = "DISCOUNT_ZONE (Between 89 & 233) — Bull Shakeout"
            elif abs(p - h1_89) / h1_89 <= 0.003:
                narrative_state = "DYNAMIC_SUPPORT (Testing rising 1H EMA 89)"
            elif abs(p - h1_233) / h1_233 <= 0.003:
                narrative_state = "MACRO_SPINE_BOUNCE (Testing rising 1H EMA 233)"

    c['narrative_state'] = narrative_state
    c['m15_89'] = m15_89
    c['m15_233'] = m15_233
    c['h1_89'] = h1_89
    c['h1_233'] = h1_233

    # Cold Zone Stop-Loss Audit (PIT-16)
    sl_audit = "PASSED_COLD_ZONE"
    hazard_detected = False
    cold_zone_sl = None
    if c.get('stop') and c.get('price') and c.get('liq_stats'):
        entry = c.get('entry_zone', {}).get('mid', c['price']) if isinstance(c.get('entry_zone'), dict) else c['price']
        planned_sl = c['stop']
        side = c.get('direction', '').lower()
        
        key_levels = c['liq_stats'].get('keyLevels', {})
        check_levels = key_levels.get('below', []) if side == 'long' else key_levels.get('above', [])
        
        hazards = []
        for kl in check_levels:
            kl_price = kl.get('price')
            kl_strength = kl.get('strength', 0)
            if kl_price and kl_strength >= 40.0:
                if side == 'long' and planned_sl <= kl_price <= entry:
                    hazards.append(kl)
                elif side == 'short' and entry <= kl_price <= planned_sl:
                    hazards.append(kl)
        
        if hazards:
            hazard_detected = True
            max_haz = max(hazards, key=lambda x: x.get('strength', 0))
            sl_audit = f"HAZARD: SL collides with {max_haz.get('strength')}% Liq Cluster at {max_haz.get('price')}!"
            if side == 'long' and check_levels:
                lowest_cluster = min([x.get('price') for x in check_levels if x.get('price')])
                cold_zone_sl = lowest_cluster * 0.9985
            elif side == 'short' and check_levels:
                highest_cluster = max([x.get('price') for x in check_levels if x.get('price')])
                cold_zone_sl = highest_cluster * 1.0015

    c['sl_audit'] = sl_audit
    c['hazard_detected'] = hazard_detected
    c['cold_zone_sl'] = cold_zone_sl
    return c

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
        print(f"\nExtracting Deep Forensic Telemetry (Oracle + Liq Levels + Dual-Spine EMA 89/233) for {len(candidates)} candidate setups in parallel...", flush=True)
        t_en = time.time()
        with concurrent.futures.ThreadPoolExecutor(max_workers=8) as executor:
            enriched = list(executor.map(enrich_candidate, candidates))
        print(f"Deep forensic enrichment completed in {time.time()-t_en:.2f}s.\n", flush=True)

        for c in enriched:
            print(f"\n-> CANDIDATE: {c['sym']} ({c['direction']} {c['grade']}) | Oracle: {c.get('oracle_score')}/100 ({c.get('oracle_verdict')})", flush=True)
            print(f"   Entry Zone: {c['entry_zone']} | Stop: {c['stop']} | Best R: {c['best_r']:.2f}R | Win%: {c['p_win']}", flush=True)
            print(f"   Targets: {c['targets']}", flush=True)
            print(f"   DUAL-SPINE NARRATIVE (EMA 89 ⟷ 233): {c.get('narrative_state')}", flush=True)
            if c.get('m15_89') and c.get('m15_233'):
                print(f"     * 15m EMAs: 89={c['m15_89']:,.1f} | 233={c['m15_233']:,.1f}", flush=True)
            if c.get('h1_89') and c.get('h1_233'):
                print(f"     * 1H  EMAs: 89={c['h1_89']:,.1f} | 233={c['h1_233']:,.1f}", flush=True)
            print(f"   COLD ZONE SL AUDIT (PIT-16): {c.get('sl_audit')}", flush=True)
            if c.get('hazard_detected') and c.get('cold_zone_sl'):
                print(f"     * RECOMMENDED SAFE COLD ZONE SL: {c['cold_zone_sl']:,.2f} (Beyond entire cluster shelf)", flush=True)
            if c.get('oracle_factors'):
                print("   ATHENA ORACLE TELEMETRY (6 GODS CONFLUENCE):", flush=True)
                for f in c['oracle_factors']:
                    print(f"     * {f.get('name')} ({f.get('id')}): {f.get('score')}/100 (wt {f.get('weight')}) -> {f.get('detail')}", flush=True)

if __name__ == '__main__':
    main()
