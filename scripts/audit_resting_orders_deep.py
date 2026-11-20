import json
import urllib.request
import MetaTrader5 as mt5

print("==================== AUDIT OF DELTA RESTING ORDERS ====================")
delta_orders = json.load(open('C:/Users/SIGMA/.gemini/antigravity/brain/566267b2-a02c-4896-b021-b1e756f57654/.system_generated/steps/32313/output.txt')).get('result', [])
for o in delta_orders:
    if o.get('state') == 'open':
        sym = o.get('product_symbol')
        limit = float(o.get('limit_price', 0))
        sl = float(o.get('bracket_stop_loss_price', 0) or 0)
        tp = float(o.get('bracket_take_profit_price', 0) or 0)
        # Fetch current price from terminal
        try:
            base_sym = sym.replace('USD', '').replace('T', '')
            if sym == 'XAUTUSD':
                base_sym = 'XAU'
            m = json.loads(urllib.request.urlopen(f"http://127.0.0.1:3000/api/cg/market?sym={base_sym}").read().decode())
            p_obj = m.get('price', {})
            cur_price = float(p_obj.get('last', 0)) if isinstance(p_obj, dict) else float(p_obj)
            v_obj = m.get('vwap') or (m.get('vwapDay') or {}).get('vwap')
            vwap = float(v_obj.get('vwap', 0)) if isinstance(v_obj, dict) else float(v_obj or 0)
            dist_pct = ((limit - cur_price) / cur_price) * 100 if cur_price else 0
            print(f"Delta #{o.get('id')} | {sym:<8} | Side: {o.get('side'):<4} | Size: {o.get('size')} | Cur: {cur_price:<8.4f} | Limit: {limit:<8.4f} | Dist: {dist_pct:+.2f}% | VWAP: {vwap:<8.4f} | SL: {sl} | TP: {tp}")
        except Exception as e:
            print(f"Delta #{o.get('id')} | {sym:<8} | Limit: {limit} | Error fetching market: {e}")

print("\n==================== AUDIT OF MT5 RESTING ORDERS ====================")
if mt5.initialize():
    orders = mt5.orders_get()
    for o in (orders or []):
        sym = o.symbol
        limit = o.price_open
        sl = o.sl
        tp = o.tp
        t = mt5.symbol_info_tick(sym)
        cur_price = (t.bid + t.ask) / 2 if t else 0
        dist_pct = ((limit - cur_price) / cur_price) * 100 if cur_price else 0
        print(f"MT5 #{o.ticket} | {sym:<10} | Type: {o.type} | Lots: {o.volume_current} | Cur: {cur_price:<8.2f} | Limit: {limit:<8.2f} | Dist: {dist_pct:+.2f}% | SL: {sl} | TP: {tp}")
    mt5.shutdown()
