import subprocess
import sys
import json
import re

round_id = 'R789'
cwd = 'CG-Terminal'

for step in range(1, 12):
    while True:
        cmd = [sys.executable, 'scripts/agent_wake_verification.py', '--round', round_id, '--step', str(step)]
        p = subprocess.run(cmd, cwd=cwd, capture_output=True, text=True)
        if p.returncode != 0:
            err = p.stderr.strip() or p.stdout.strip()
            print(f'Step {step} stopped: {err[:200]}')
            break
        # Look for WAKE_RECEIPT JSON
        match = re.search(r'WAKE_RECEIPT\s+(\{.*\})', p.stdout)
        if match:
            try:
                receipt = json.loads(match.group(1))
                rem = receipt.get('remaining_anchors', [])
                cov = receipt.get('sop_coverage', {})
                print(f"Step {step} anchor read. Remaining in step: {len(rem)}, Total unread: {len(cov.get('unread_anchors', []))}")
                if len(rem) == 0:
                    print(f"Step {step} completely read!")
                    break
            except Exception as e:
                print("JSON parse error:", e)
                break
        else:
            print("No receipt found in output")
            break

cmd_check = [sys.executable, 'scripts/agent_wake_verification.py', '--round', round_id, '--require-formulation-reads']
p_check = subprocess.run(cmd_check, cwd=cwd, capture_output=True, text=True)
print('Formulation reads check code:', p_check.returncode)
print(p_check.stdout[:300])
if p_check.stderr:
    print('Error:', p_check.stderr[:300])
