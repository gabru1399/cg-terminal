import subprocess
import sys

round_id = "R798"
symbols = ["BTC", "ETH", "SOL", "BNB", "XRP", "ADA", "DOGE", "AVAX", "LINK", "LTC", "XAU", "XAG"]
feeds = ["market", "cvd", "fp", "bookwalls", "lto", "oi", "signals"]

for sym in symbols:
    print(f"--- Capturing {sym} feeds ---")
    for feed in feeds:
        cmd = [sys.executable, "scripts/capture_round_evidence.py", "--round", round_id, "--feed", feed, "--symbol", sym]
        res = subprocess.run(cmd, capture_output=True, text=True, cwd=".")
        if res.returncode == 0:
            print(f"  {feed} for {sym}: OK")
        else:
            print(f"  {feed} for {sym}: FAIL: {res.stderr.strip() or res.stdout.strip()}")
            
    # Also capture liqlevels 3d, 7d, 30d for crypto symbols
    if sym not in ("XAU", "XAG"):
        for r in ["3d", "7d", "30d"]:
            cmd = [sys.executable, "scripts/capture_round_evidence.py", "--round", round_id, "--feed", "liqlevels", "--symbol", sym, "--range", r]
            res = subprocess.run(cmd, capture_output=True, text=True, cwd=".")
            if res.returncode == 0:
                print(f"  liqlevels {r} for {sym}: OK")
            else:
                print(f"  liqlevels {r} for {sym}: FAIL: {res.stderr.strip() or res.stdout.strip()}")

# Capture narrative and options
cmd_narrative = [sys.executable, "scripts/capture_round_evidence.py", "--round", round_id, "--feed", "narrative"]
subprocess.run(cmd_narrative, capture_output=True, text=True, cwd=".")
print("Narrative captured.")

for sym in ["BTC", "ETH"]:
    cmd_opt = [sys.executable, "scripts/capture_round_evidence.py", "--round", round_id, "--feed", "options", "--symbol", sym]
    subprocess.run(cmd_opt, capture_output=True, text=True, cwd=".")
    print(f"Options {sym} captured.")

print("All R798 captures completed!")
