#!/bin/bash
# Fetch real Binance USDT-M futures 15m klines from data.binance.vision (historical dump)
# BTC/ETH/SOL: monthly 2026-05..2026-10 + daily 2026-11-01..2026-11-17
set -u
BASE="https://data.binance.vision/data/futures/um"
OUT="/home/z/my-project/data/backtest/raw"
mkdir -p "$OUT"
SYMS="BTCUSDT ETHUSDT SOLUSDT"
ok=0; fail=0

fetch() { # $1=url $2=dest
  if [ -s "$2" ]; then ok=$((ok+1)); return 0; fi
  code=$(curl -s -m 60 -o "$2" -w "%{http_code}" "$1")
  if [ "$code" = "200" ] && [ -s "$2" ]; then ok=$((ok+1)); else rm -f "$2"; fail=$((fail+1)); echo "FAIL $1 ($code)"; fi
}

for S in $SYMS; do
  for M in 2026-05 2026-06 2026-07 2026-08 2026-09 2026-10; do
    fetch "$BASE/monthly/klines/$S/15m/$S-15m-$M.zip" "$OUT/$S-15m-$M.zip"
  done
  for D in 01 02 03 04 05 06 07 08 09 10 11 12 13 14 15 16 17; do
    fetch "$BASE/daily/klines/$S/15m/$S-15m-2026-11-$D.zip" "$OUT/$S-15m-2026-11-$D.zip"
  done
done
echo "fetched ok=$ok fail=$fail"
ls "$OUT" | wc -l
