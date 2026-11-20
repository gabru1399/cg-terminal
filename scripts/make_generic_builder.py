import re

with open("scripts/build_r649_contract_bundle.py", "r", encoding="utf-8") as f:
    text = f.read()

target = 'ROUND_ID = "R649"'
replacement = '''import argparse
parser = argparse.ArgumentParser()
parser.add_argument("--round", required=True)
args, _ = parser.parse_known_args()
ROUND_ID = args.round'''

if target in text:
    new_text = text.replace(target, replacement, 1)
    with open("scripts/build_round_contract_bundle.py", "w", encoding="utf-8") as f:
        f.write(new_text)
    print("build_round_contract_bundle.py created successfully!")
else:
    print("Target string not found!")
