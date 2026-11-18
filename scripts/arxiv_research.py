#!/usr/bin/env python3
"""Deep research pull: arXiv q-fin queries for entry-strategy families mappable
to the desk's order-flow telemetry. Saves titles+abstracts to /tmp for digest."""
import urllib.request, urllib.parse, re, json, time

def q(search, n=12):
    url = ("https://export.arxiv.org/api/query?search_query=" +
           urllib.parse.quote(search) +
           f"&start=0&max_results={n}&sortBy=relevance")
    with urllib.request.urlopen(url, timeout=50) as r:
        x = r.read().decode()
    entries = re.findall(r'<entry>(.*?)</entry>', x, re.S)
    out = []
    for e in entries:
        t = " ".join(re.search(r'<title>(.*?)</title>', e, re.S).group(1).split())
        a = " ".join(re.search(r'<summary>(.*?)</summary>', e, re.S).group(1).split())
        i = re.search(r'<id>https?://arxiv.org/abs/(.*?)</id>', e).group(1)
        y = re.search(r'<published>(\d{4})', e).group(1)
        out.append({"id": i, "year": y, "title": t, "abstract": a[:1200]})
    return out

queries = {
    "OFI": 'all:"order flow imbalance"',
    "OFI_forecast": 'all:"forecasting high frequency order flow imbalance"',
    "liquidation_crypto": 'all:"liquidation" AND all:"perpetual futures"',
    "crypto_micro": 'all:"cryptocurrency" AND all:"limit order book" AND all:"trading strategy"',
    "vwap": 'all:"VWAP" AND all:"execution strategy"',
    "mean_reversion_intraday": 'all:"intraday" AND all:"mean reversion" AND all:"order flow"',
    "orderbook_dynamics": 'all:"limit order book" AND all:"price impact" AND all:"deep learning"',
}

results = {}
for name, query in queries.items():
    try:
        results[name] = q(query)
        print(f"{name}: {len(results[name])} papers")
    except Exception as e:
        print(f"{name}: ERR {str(e)[:60]}")
    time.sleep(3.5)  # arXiv politeness

json.dump(results, open("/tmp/arxiv_research.json", "w"), indent=1)
print("saved /tmp/arxiv_research.json")
