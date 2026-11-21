import MetaTrader5 as mt5

if mt5.initialize():
    print("=== LIVE MT5 DESK ORDERS ===")
    ords = mt5.orders_get()
    for o in (ords or []):
        if o.magic == 42001 or "cg_terminal" in o.comment:
            print(f"  Desk Order #{o.ticket} {o.symbol}: type={o.type}, vol={o.volume_current}, open={o.price_open}, curr={o.price_current}, SL={o.sl}, TP={o.tp}")
    
    print("\n=== LIVE MT5 DESK POSITIONS ===")
    pos = mt5.positions_get()
    for p in (pos or []):
        if p.magic == 42001 or "cg_terminal" in p.comment:
            print(f"  Desk Position #{p.ticket} {p.symbol}: type={p.type}, vol={p.volume}, open={p.price_open}, curr={p.price_current}, SL={p.sl}, TP={p.tp}, PnL=${p.profit:.2f}")
    
    mt5.shutdown()
else:
    print("MT5 init failed")
