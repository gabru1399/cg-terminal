import MetaTrader5 as mt5
import datetime
import json

def analyze():
    if not mt5.initialize():
        print(f"Failed to initialize MT5: {mt5.last_error()}")
        return

    from_date = datetime.datetime(2025, 1, 1)
    to_date = datetime.datetime(2027, 1, 1)
    deals = mt5.history_deals_get(from_date, to_date)
    orders = mt5.history_orders_get(from_date, to_date)
    
    if not deals:
        print("No deals found")
        mt5.shutdown()
        return

    print(f"Total deals: {len(deals)}")
    closed_deals = [d._asdict() for d in deals if d.entry == mt5.DEAL_ENTRY_OUT]
    entry_deals = {d.position_id: d._asdict() for d in deals if d.entry == mt5.DEAL_ENTRY_IN}
    
    # Map orders for SL/TP info
    order_dict = {o.ticket: o._asdict() for o in orders} if orders else {}

    print(f"\n--- ALL CLOSED POSITIONS ({len(closed_deals)}) ---")
    sl_hits = []
    
    for cd in closed_deals:
        pos_id = cd['position_id']
        ed = entry_deals.get(pos_id, {})
        sym = cd['symbol']
        profit = cd['profit']
        magic = cd.get('magic', 0)
        reason = cd.get('reason', 0)
        # Reason codes: 3 = DEAL_REASON_SL, 4 = DEAL_REASON_TP, 0 = DEAL_REASON_CLIENT, etc.
        is_sl = (reason == 3) or (profit < 0 and "sl" in cd.get('comment', '').lower()) or (profit < 0)
        
        t_close = datetime.datetime.fromtimestamp(cd['time']).strftime('%Y-%m-%d %H:%M:%S')
        t_open = datetime.datetime.fromtimestamp(ed.get('time', 0)).strftime('%Y-%m-%d %H:%M:%S') if ed else 'Unknown'
        
        item = {
            'position_id': pos_id,
            'symbol': sym,
            'magic': magic,
            'entry_type': 'BUY' if ed.get('type') == 0 else ('SELL' if ed.get('type') == 1 else 'UNKNOWN'),
            'volume': cd['volume'],
            'entry_price': ed.get('price', 0),
            'exit_price': cd['price'],
            'profit': profit,
            'reason': reason,
            'is_sl_hit': is_sl,
            'open_time': t_open,
            'close_time': t_close,
            'comment': cd.get('comment', ''),
            'open_comment': ed.get('comment', '')
        }
        
        print(f"Pos {pos_id} | {sym} | Type: {item['entry_type']} | Vol: {item['volume']} | Open: {item['entry_price']} ({t_open}) -> Close: {item['exit_price']} ({t_close}) | PnL: ${profit:.2f} | Reason: {reason} | Comment: '{item['comment']}' | Magic: {magic}")
        
        if is_sl and profit < 0:
            sl_hits.append(item)

    print(f"\n=======================================================")
    print(f"TOTAL LOSS / SL HIT TRADES: {len(sl_hits)}")
    print(f"=======================================================")
    for s in sl_hits:
        print(f"\n[SL HIT] Symbol: {s['symbol']} | Pos ID: {s['position_id']} | Magic: {s['magic']}")
        print(f"  Direction: {s['entry_type']} | Volume: {s['volume']}")
        print(f"  Entry: {s['entry_price']} at {s['open_time']}")
        print(f"  Exit (SL): {s['exit_price']} at {s['close_time']}")
        print(f"  Loss: ${s['profit']:.2f}")
        print(f"  Comments: open='{s['open_comment']}', close='{s['comment']}'")

    mt5.shutdown()

if __name__ == '__main__':
    analyze()
