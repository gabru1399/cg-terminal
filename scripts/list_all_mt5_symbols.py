import MetaTrader5 as mt5
import json

def get_mt5_symbols():
    if not mt5.initialize():
        print("Failed to initialize MT5:", mt5.last_error())
        return

    symbols = mt5.symbols_get()
    print(f"Total symbols found in MT5: {len(symbols)}")
    
    categories = {}
    tradable = []
    
    for s in symbols:
        path = s.path
        top_group = path.split('\\')[0] if '\\' in path else 'Other'
        if top_group not in categories:
            categories[top_group] = []
        categories[top_group].append({
            'name': s.name,
            'path': s.path,
            'spread': s.spread,
            'digits': s.digits,
            'trade_mode': s.trade_mode,
            'visible': s.visible,
            'point': s.point,
            'trade_contract_size': s.trade_contract_size,
            'volume_min': s.volume_min,
            'volume_max': s.volume_max,
            'volume_step': s.volume_step,
        })
        if s.trade_mode == mt5.SYMBOL_TRADE_MODE_FULL:
            tradable.append(s.name)

    print(f"Tradable symbols count: {len(tradable)}")
    for grp, syms in categories.items():
        print(f"Group: {grp} ({len(syms)} symbols)")
        sample = [x['name'] for x in syms[:8]]
        print(f"  Samples: {', '.join(sample)}")

    # Save to a json reference file
    with open('desk/mt5_symbols_universe.json', 'w') as f:
        json.dump(categories, f, indent=2)
    print("Saved MT5 symbols universe to desk/mt5_symbols_universe.json")

    mt5.shutdown()

if __name__ == '__main__':
    get_mt5_symbols()
