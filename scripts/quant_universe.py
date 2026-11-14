"""quant_universe.py: The Curated Top 50 High-Edge MT5 Trading Universe.
Derived from empirical multi-year optimization (Jan 2021 - Nov 2026).
"""

# Map string ribbon names to (fast, mid, slow) tuples
RIBBON_DEFINITIONS = {
    "Fib_21_55_144": (21, 55, 144),
    "Fib_34_89_233": (34, 89, 233),
    "Fib_55_89_233": (55, 89, 233),
    "Classic_50_100_200": (50, 100, 200),
}

QUANT_UNIVERSE = {
    # --- Cryptocurrencies ---
    "DOGUSD": {"category": "Crypto", "tf": "H4", "ribbon": "Fib_55_89_233", "exit_mode": "trail_89", "max_spread_pct": 0.50},
    "XLMUSD": {"category": "Crypto", "tf": "H1", "ribbon": "Fib_21_55_144", "exit_mode": "trail_89", "max_spread_pct": 0.50},
    "ETHUSD": {"category": "Crypto", "tf": "H4", "ribbon": "Fib_21_55_144", "exit_mode": "trail_89", "max_spread_pct": 0.35},
    "BTCUSD": {"category": "Crypto", "tf": "H1", "ribbon": "Fib_55_89_233", "exit_mode": "trail_89", "max_spread_pct": 0.25},
    "ADAUSD": {"category": "Crypto", "tf": "H1", "ribbon": "Fib_21_55_144", "exit_mode": "fixed_3.0", "max_spread_pct": 0.50},
    "LTCUSD": {"category": "Crypto", "tf": "H4", "ribbon": "Fib_34_89_233", "exit_mode": "fixed_3.0", "max_spread_pct": 0.40},
    "LNKUSD": {"category": "Crypto", "tf": "H1", "ribbon": "Fib_55_89_233", "exit_mode": "step_trail", "max_spread_pct": 0.50},

    # --- Commodities & Metals ---
    "XAUUSD": {"category": "Commodities", "tf": "H1", "ribbon": "Fib_21_55_144", "exit_mode": "trail_55", "max_spread_pct": 0.15},
    "USOUSD": {"category": "Commodities", "tf": "H1", "ribbon": "Fib_55_89_233", "exit_mode": "fixed_2.0", "max_spread_pct": 0.20},
    "XAGUSD": {"category": "Commodities", "tf": "H1", "ribbon": "Fib_21_55_144", "exit_mode": "trail_89", "max_spread_pct": 0.25},
    "XPTUSD": {"category": "Commodities", "tf": "H1", "ribbon": "Fib_34_89_233", "exit_mode": "step_trail", "max_spread_pct": 0.30},
    "UKOUSD": {"category": "Commodities", "tf": "H1", "ribbon": "Classic_50_100_200", "exit_mode": "fixed_2.0", "max_spread_pct": 0.20},

    # --- Global Indices ---
    "SPX500": {"category": "Indices", "tf": "H1", "ribbon": "Fib_34_89_233", "exit_mode": "fixed_3.0", "max_spread_pct": 0.10},
    "US30":   {"category": "Indices", "tf": "H1", "ribbon": "Classic_50_100_200", "exit_mode": "fixed_2.5", "max_spread_pct": 0.10},
    "GER30":  {"category": "Indices", "tf": "H1", "ribbon": "Fib_55_89_233", "exit_mode": "trail_55", "max_spread_pct": 0.12},
    "FRA40":  {"category": "Indices", "tf": "H1", "ribbon": "Fib_55_89_233", "exit_mode": "fixed_3.0", "max_spread_pct": 0.15},
    "US2000": {"category": "Indices", "tf": "H4", "ribbon": "Fib_34_89_233", "exit_mode": "fixed_3.0", "max_spread_pct": 0.15},
    "JP225":  {"category": "Indices", "tf": "H1", "ribbon": "Fib_34_89_233", "exit_mode": "step_trail", "max_spread_pct": 0.15},
    "NTH25":  {"category": "Indices", "tf": "H1", "ribbon": "Fib_34_89_233", "exit_mode": "fixed_3.0", "max_spread_pct": 0.15},
    "VIX":    {"category": "Indices", "tf": "H1", "ribbon": "Fib_21_55_144", "exit_mode": "fixed_2.5", "max_spread_pct": 0.30},
    "AUS200": {"category": "Indices", "tf": "H4", "ribbon": "Fib_55_89_233", "exit_mode": "fixed_3.0", "max_spread_pct": 0.15},

    # --- Tech & High-Beta Stock CFDs ---
    "META":   {"category": "Stock CFD", "tf": "H1", "ribbon": "Fib_21_55_144", "exit_mode": "step_trail", "max_spread_pct": 0.20},
    "AMD":    {"category": "Stock CFD", "tf": "H1", "ribbon": "Fib_21_55_144", "exit_mode": "trail_89", "max_spread_pct": 0.20},
    "NFLX":   {"category": "Stock CFD", "tf": "H1", "ribbon": "Classic_50_100_200", "exit_mode": "fixed_3.0", "max_spread_pct": 0.20},
    "MSFT":   {"category": "Stock CFD", "tf": "H1", "ribbon": "Fib_21_55_144", "exit_mode": "trail_55", "max_spread_pct": 0.20},
    "ADS":    {"category": "Stock CFD", "tf": "H1", "ribbon": "Fib_55_89_233", "exit_mode": "fixed_3.0", "max_spread_pct": 0.25},
    "MBG":    {"category": "Stock CFD", "tf": "H1", "ribbon": "Fib_21_55_144", "exit_mode": "fixed_3.0", "max_spread_pct": 0.25},
    "BABA":   {"category": "Stock CFD", "tf": "H1", "ribbon": "Fib_21_55_144", "exit_mode": "step_trail", "max_spread_pct": 0.25},
    "AAPL":   {"category": "Stock CFD", "tf": "H1", "ribbon": "Fib_21_55_144", "exit_mode": "fixed_2.5", "max_spread_pct": 0.20},
    "GOOG":   {"category": "Stock CFD", "tf": "H1", "ribbon": "Fib_21_55_144", "exit_mode": "trail_55", "max_spread_pct": 0.20},
    "INTC":   {"category": "Stock CFD", "tf": "H1", "ribbon": "Fib_21_55_144", "exit_mode": "fixed_2.5", "max_spread_pct": 0.25},
    "MC":     {"category": "Stock CFD", "tf": "H1", "ribbon": "Classic_50_100_200", "exit_mode": "fixed_3.0", "max_spread_pct": 0.25},
    "KO":     {"category": "Stock CFD", "tf": "H1", "ribbon": "Classic_50_100_200", "exit_mode": "fixed_2.5", "max_spread_pct": 0.20},

    # --- Forex Majors & Crosses ---
    "AUDJPY": {"category": "Forex", "tf": "H1", "ribbon": "Fib_21_55_144", "exit_mode": "step_trail", "max_spread_pct": 0.10},
    "USDCNH": {"category": "Forex", "tf": "H4", "ribbon": "Classic_50_100_200", "exit_mode": "trail_89", "max_spread_pct": 0.15},
    "USDCAD": {"category": "Forex", "tf": "H1", "ribbon": "Classic_50_100_200", "exit_mode": "fixed_2.0", "max_spread_pct": 0.08},
    "USDJPY": {"category": "Forex", "tf": "H4", "ribbon": "Fib_55_89_233", "exit_mode": "fixed_3.0", "max_spread_pct": 0.08},
    "EURHUF": {"category": "Forex", "tf": "H1", "ribbon": "Fib_21_55_144", "exit_mode": "trail_55", "max_spread_pct": 0.25},
    "GBPNZD": {"category": "Forex", "tf": "H1", "ribbon": "Fib_34_89_233", "exit_mode": "fixed_2.5", "max_spread_pct": 0.12},
    "EURJPY": {"category": "Forex", "tf": "H4", "ribbon": "Fib_21_55_144", "exit_mode": "fixed_3.0", "max_spread_pct": 0.10},
    "EURNZD": {"category": "Forex", "tf": "H1", "ribbon": "Classic_50_100_200", "exit_mode": "fixed_2.5", "max_spread_pct": 0.12},
    "CHFJPY": {"category": "Forex", "tf": "H1", "ribbon": "Fib_34_89_233", "exit_mode": "step_trail", "max_spread_pct": 0.10},
    "EURUSD": {"category": "Forex", "tf": "H1", "ribbon": "Fib_21_55_144", "exit_mode": "trail_89", "max_spread_pct": 0.05},
    "NZDSGD": {"category": "Forex", "tf": "H1", "ribbon": "Classic_50_100_200", "exit_mode": "fixed_2.0", "max_spread_pct": 0.15},
    "GBPUSD": {"category": "Forex", "tf": "H4", "ribbon": "Fib_34_89_233", "exit_mode": "fixed_3.0", "max_spread_pct": 0.08},
    "USDMXN": {"category": "Forex", "tf": "H4", "ribbon": "Fib_34_89_233", "exit_mode": "fixed_2.5", "max_spread_pct": 0.25},
    "USDDKK": {"category": "Forex", "tf": "H1", "ribbon": "Fib_21_55_144", "exit_mode": "trail_89", "max_spread_pct": 0.20},
    "USDCHF": {"category": "Forex", "tf": "H1", "ribbon": "Fib_55_89_233", "exit_mode": "step_trail", "max_spread_pct": 0.10},
    "MXNJPY": {"category": "Forex", "tf": "H1", "ribbon": "Fib_34_89_233", "exit_mode": "fixed_2.0", "max_spread_pct": 0.25},
    "EURCHF": {"category": "Forex", "tf": "H4", "ribbon": "Fib_21_55_144", "exit_mode": "fixed_2.5", "max_spread_pct": 0.10},
}

def get_universe():
    return QUANT_UNIVERSE

def get_asset_config(symbol):
    cfg = QUANT_UNIVERSE.get(symbol)
    if cfg is None:
        return None
    ribbon_tuple = RIBBON_DEFINITIONS.get(cfg["ribbon"], (34, 89, 233))
    return {
        "symbol": symbol,
        "category": cfg["category"],
        "tf": cfg["tf"],
        "ribbon_name": cfg["ribbon"],
        "fast_p": ribbon_tuple[0],
        "mid_p": ribbon_tuple[1],
        "slow_p": ribbon_tuple[2],
        "exit_mode": cfg["exit_mode"],
        "max_spread_pct": cfg["max_spread_pct"]
    }
