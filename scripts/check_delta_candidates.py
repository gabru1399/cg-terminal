import urllib.request
import json

def check_delta_tickers():
    symbols = ['ADAUSD', 'DOGEUSD', 'ARBUSD', 'AMZNBUSD', 'GOOGLBUSD', 'SPCXBUSD', 'NVDAUSD']
    for sym in symbols:
        try:
            url = f"https://cdn.india.delta.exchange/v2/tickers/{sym}"
            req = urllib.request.Request(url, headers={'User-Agent': 'Mozilla/5.0'})
            with urllib.request.urlopen(req, timeout=5) as r:
                res = json.loads(r.read().decode('utf-8'))
                res_data = res.get('result', {})
                print(f"{sym:<10} Mark: {res_data.get('mark_price'):<10} 24hChg: {res_data.get('mark_change_24h'):<8} "
                      f"ContractVal: {res_data.get('contract_value'):<6} Tick: {res_data.get('tick_size'):<8} Leverage: {res_data.get('leverage')}")
        except Exception as e:
            print(f"{sym:<10} Error: {e}")

if __name__ == '__main__':
    check_delta_tickers()
