import MetaTrader5 as mt5

if not mt5.initialize():
    print('Failed to init MT5:', mt5.last_error())
    exit(1)

acc = mt5.account_info()
print(f'Account: {acc.login} | Balance: {acc.balance:.2f} | Equity: {acc.equity:.2f} | Margin: {acc.margin:.2f} | Free Margin: {acc.margin_free:.2f}')

positions = mt5.positions_get()
print(f'Total open positions: {len(positions)}')
total_profit = sum(p.profit for p in positions)
print(f'Total floating PnL: {total_profit:+.2f} USD')

print('=' * 120)
print(f"{'Ticket':<10} {'Symbol':<12} {'Type':<6} {'Volume':<8} {'Open Price':<12} {'Current':<12} {'SL':<12} {'TP':<12} {'Profit':<10} {'Magic':<10} {'Comment'}")
print('-' * 120)
for p in sorted(positions, key=lambda x: x.profit):
    side = 'BUY' if p.type == 0 else 'SELL'
    print(f"{p.ticket:<10} {p.symbol:<12} {side:<6} {p.volume:<8} {p.price_open:<12.5f} {p.price_current:<12.5f} {p.sl:<12.5f} {p.tp:<12.5f} {p.profit:<+10.2f} {p.magic:<10} {p.comment}")

mt5.shutdown()
