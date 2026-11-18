import MetaTrader5 as mt5
import datetime

if not mt5.initialize():
    print('MT5 Init Error:', mt5.last_error())
else:
    t_info = mt5.terminal_info()._asdict()
    a_info = mt5.account_info()._asdict()
    print('Terminal Connected:', t_info.get('connected'))
    print('Trade Allowed:', a_info.get('trade_allowed'))
    print('Server:', a_info.get('server'))
    print('Balance:', a_info.get('balance'), '| Equity:', a_info.get('equity'))
    
    positions = mt5.positions_get() or ()
    print(f'Open Positions ({len(positions)}):')
    for p in positions:
        info = mt5.symbol_info(p.symbol)
        tick = mt5.symbol_info_tick(p.symbol)
        last_time = datetime.datetime.fromtimestamp(tick.time) if tick else 'No tick'
        print(f"  {p.symbol} (Ticket #{p.ticket}):")
        print(f"    Type: {'BUY' if p.type == 0 else 'SELL'} | Lots: {p.volume} | Open: {p.price_open} | Current: {p.price_current}")
        print(f"    Profit: ${p.profit:.2f} USD | Swap (Overnight Fee): ${p.swap:.2f} USD")
        print(f"    Last Tick Time: {last_time} (Bid: {tick.bid}, Ask: {tick.ask}, Spread: {info.spread})")
        print(f"    Swap Short: {info.swap_short} | Swap Long: {info.swap_long} | Swap Mode: {info.swap_mode}")

    print("\nPending Orders:")
    orders = mt5.orders_get() or ()
    for o in orders:
        tick = mt5.symbol_info_tick(o.symbol)
        last_time = datetime.datetime.fromtimestamp(tick.time) if tick else 'No tick'
        vol = getattr(o, 'volume_current', getattr(o, 'volume_initial', 'n/a'))
    print(f"  {o.symbol} (Ticket #{o.ticket}) | Type: {o.type} | Lots: {vol} | Price: {o.price_open} | Last Tick: {last_time}")

    mt5.shutdown()
