import MetaTrader5 as mt5
import datetime

def audit_external():
    if not mt5.initialize():
        print(f"Failed to init MT5: {mt5.last_error()}")
        return

    # 1. Current Open Positions
    positions = mt5.positions_get()
    print("=== CURRENT OPEN POSITIONS ===")
    if positions:
        for p in positions:
            d = p._asdict()
            side = "BUY" if d['type'] == 0 else "SELL"
            print(f"Ticket: {d['ticket']} | Sym: {d['symbol']} | Side: {side} | Vol: {d['volume']} | Open: {d['price_open']} | Current: {d['price_current']} | SL: {d['sl']} | TP: {d['tp']} | Profit: ${d['profit']:.2f} | Magic: {d['magic']} | Comment: '{d['comment']}'")
    else:
        print("None")

    # 2. Deals for fib_orders (magic 202611) and fvg_strategy (magic 7771399)
    from_date = datetime.datetime(2025, 1, 1)
    to_date = datetime.datetime(2027, 1, 1)
    deals = mt5.history_deals_get(from_date, to_date)
    orders = mt5.history_orders_get(from_date, to_date)
    order_map = {o.ticket: o._asdict() for o in orders} if orders else {}

    closed_deals = [d._asdict() for d in deals if d.entry == mt5.DEAL_ENTRY_OUT and d.magic in (202611, 7771399)]
    entry_deals = {d.position_id: d._asdict() for d in deals if d.entry == mt5.DEAL_ENTRY_IN}

    print("\n=== CLOSED TRADES OF FIB_ORDERS & FVG_STRATEGY ===")
    for cd in closed_deals:
        pos_id = cd['position_id']
        ed = entry_deals.get(pos_id, {})
        sym = cd['symbol']
        profit = cd['profit']
        magic = cd['magic']
        strategy = "fib_orders" if magic == 202611 else "fvg_strategy"
        side = "BUY" if ed.get('type') == 0 else "SELL"
        t_open = datetime.datetime.fromtimestamp(ed.get('time', 0)).strftime('%Y-%m-%d %H:%M:%S') if ed else 'Unknown'
        t_close = datetime.datetime.fromtimestamp(cd['time']).strftime('%Y-%m-%d %H:%M:%S')
        
        # Original order to get TP
        orig_order = order_map.get(pos_id, {})
        orig_tp = orig_order.get('tp', 0.0)
        orig_sl = orig_order.get('sl', 0.0)

        # Check subsequent rates
        dt_close = datetime.datetime.fromtimestamp(cd['time'])
        rates = mt5.copy_rates_range(sym, mt5.TIMEFRAME_M15, dt_close, dt_close + datetime.timedelta(hours=24))
        max_h = max([r['high'] for r in rates]) if rates is not None and len(rates) > 0 else 0
        min_l = min([r['low'] for r in rates]) if rates is not None and len(rates) > 0 else 0
        
        print(f"\n[{strategy.upper()}] Pos {pos_id} | {sym} {side} {cd['volume']} lots")
        print(f"  Open: {ed.get('price', 0)} ({t_open}) -> Close: {cd['price']} ({t_close})")
        print(f"  PnL: ${profit:.2f} | Reason: {cd['reason']} | Comment: '{cd['comment']}'")
        print(f"  Recorded SL: {orig_sl} | Recorded TP: {orig_tp}")
        if rates is not None and len(rates) > 0:
            print(f"  Next 24h: High = {max_h} | Low = {min_l}")
            if side == "SELL":
                adverse = max_h - cd['price']
                favorable = ed.get('price', 0) - min_l
                print(f"  Post-Exit Move: Adverse excursion higher = +{adverse:.5f} | Drop lower = {favorable:.5f}")
                if orig_tp > 0:
                    tp_hit_possible = min_l <= orig_tp
                    print(f"  Would price have reached TP ({orig_tp})? {'YES! Reached ' + str(min_l) if tp_hit_possible else 'NO! Min low was ' + str(min_l)}")
            else:
                adverse = cd['price'] - min_l
                favorable = max_h - ed.get('price', 0)
                print(f"  Post-Exit Move: Adverse excursion lower = -{adverse:.5f} | Rally higher = {favorable:.5f}")
                if orig_tp > 0:
                    tp_hit_possible = max_h >= orig_tp
                    print(f"  Would price have reached TP ({orig_tp})? {'YES! Reached ' + str(max_h) if tp_hit_possible else 'NO! Max high was ' + str(max_h)}")

    mt5.shutdown()

if __name__ == '__main__':
    audit_external()
