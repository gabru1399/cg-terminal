#!/usr/bin/env python3
"""Capture read-only source payloads and receipts for a pinned audit round."""

import argparse
from datetime import datetime, timezone
import hashlib
import json
import os
from pathlib import Path
import re
import sys
from urllib.parse import urlencode
from urllib.request import urlopen

from agent_wake_verification import ROOT, ROUND_ID, SPEC, load_round_spec, read_receipt, save_receipt, validate_wake


TERMINAL = "http://127.0.0.1:3000/api/cg"
DELTA_PRODUCTS = "https://api.india.delta.exchange/v2/products"
FEEDS = {"market", "narrative", "fp", "signals", "cvd", "bookwalls", "lto",
         "liqlevels", "stopmap", "options", "oi", "liq-live"}


def utc_now():
    return datetime.now(timezone.utc).isoformat()


def fetch(url):
    with urlopen(url, timeout=5) as response:
        if response.geturl() != url:
            raise ValueError("Source redirected away from the requested endpoint")
        return response.read()


def delta_inventory():
    pages = []
    seen = set()
    params = {"contract_types": "perpetual_futures", "states": "live", "page_size": 100}
    while len(pages) < 100:
        page = json.loads(fetch(f"{DELTA_PRODUCTS}?{urlencode(params)}"))
        if page.get("success") is not True or not isinstance(page.get("result"), list):
            raise ValueError("Delta product inventory failed")
        pages.append(page)
        after = page.get("meta", {}).get("after")
        if not after:
            return {"pages": pages}
        if after in seen:
            raise ValueError("Delta repeated an inventory cursor")
        seen.add(after)
        params["after"] = after
    raise ValueError("Delta product inventory did not finish paginating")


def mt5_inventory():
    import MetaTrader5 as mt5

    if not mt5.initialize(timeout=15_000):
        raise ValueError(f"MT5 initialization failed: {mt5.last_error()}")
    try:
        account = mt5.account_info()
        if account is None:
            raise ValueError("MT5 account unavailable")
        symbols = mt5.symbols_get()
        if symbols is None:
            raise ValueError(f"MT5 symbol inventory failed: {mt5.last_error()}")
        return {"login": account.login, "symbols": [
            {"name": symbol.name, "trade_mode": symbol.trade_mode} for symbol in symbols
        ]}
    finally:
        mt5.shutdown()


def capture(directory, wake, args):
    query = {}
    if args.feed in FEEDS:
        query["sym"] = args.symbol
    if args.range:
        query["range"] = args.range
    if args.feed == "liq-live":
        query["limit"] = 400
    started = utc_now()
    if args.feed == "delta-inventory":
        data = json.dumps(delta_inventory(), ensure_ascii=False).encode("utf-8")
    elif args.feed == "mt5-inventory":
        data = json.dumps(mt5_inventory(), ensure_ascii=False).encode("utf-8")
    else:
        data = fetch(f"{TERMINAL}/{args.feed}?{urlencode(query)}")
    received = utc_now()
    json.loads(data)
    digest = hashlib.sha256(data).hexdigest()
    raw = directory / "raw"
    raw.mkdir(parents=True, exist_ok=True)
    name = f"{args.feed}-{query.get('sym', 'all')}-{query.get('range', 'all')}-{digest[:16]}.json"
    path = raw / name
    # Publish the captured bytes before the receipt. An interrupted capture
    # cannot make a partial payload valid.
    if not path.exists():
        temp = raw / f".{name}.{os.getpid()}.tmp"
        try:
            with temp.open("xb") as handle:
                handle.write(data)
            try:
                os.link(temp, path)
            except FileExistsError:
                pass
        finally:
            temp.unlink(missing_ok=True)
    if hashlib.sha256(path.read_bytes()).hexdigest() != digest:
        raise ValueError("Existing source bytes do not match capture")
    result = {"path": f"raw/{name}", "sha256": digest}
    save_receipt(directory / "captures" / name, {
        **result, "round_id": wake["round_id"], "wake_id": wake["wake_id"],
        "spec_sha256": wake["spec_sha256"], "feed": args.feed, "query": query,
        "requested_utc": started, "received_utc": received,
    })
    return result


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--round", required=True)
    parser.add_argument("--feed", required=True, choices=sorted(FEEDS | {"delta-inventory", "mt5-inventory"}))
    parser.add_argument("--symbol")
    parser.add_argument("--range", choices=["3d", "7d", "30d"])
    args = parser.parse_args()
    if not ROUND_ID.fullmatch(args.round):
        parser.error("--round must be R followed by digits")
    if args.feed in FEEDS and not re.fullmatch(r"[A-Za-z0-9._-]{1,40}", args.symbol or ""):
        parser.error("terminal feeds require an exact --symbol")
    if bool(args.range) != (args.feed == "liqlevels"):
        parser.error("--range is required for, and limited to, liqlevels")
    directory = ROOT / "data" / "round-evidence" / args.round
    try:
        wake = read_receipt(directory / "wake_receipt.json")
        validate_wake(wake, args.round, load_round_spec(SPEC))
        print(json.dumps(capture(directory, wake, args)))
        return 0
    except (ImportError, OSError, ValueError, TypeError, KeyError) as exc:
        print(json.dumps({"status": "UNRESOLVED", "error": str(exc)}))
        return 1


if __name__ == "__main__":
    sys.exit(main())
