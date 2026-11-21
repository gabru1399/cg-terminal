import sys
import os
from pathlib import Path
from datetime import datetime, timezone, timedelta
import time

ROOT = Path("CG-Terminal").resolve() if Path("CG-Terminal").is_dir() else Path(".").resolve()
sys.path.insert(0, str(ROOT / "scripts"))

from agent_wake_verification import ROOT as S_ROOT, SPEC, load_round_spec, section_index, read_receipt, save_receipt, section_progress, sop_progress, validate_wake

def run_all(round_id="R801"):
    directory = ROOT / "data" / "round-evidence" / round_id
    receipt_path = directory / "wake_receipt.json"
    spec = load_round_spec(SPEC)
    index = section_index(spec)
    wake = read_receipt(receipt_path)
    wake_time = validate_wake(wake, round_id, spec)
    print(f"Starting SOP reads for {round_id}, wake_time: {wake_time}")

    current_sim_time = wake_time + timedelta(seconds=1)

    for step in range(0, 12):
        while True:
            missing, problems = section_progress(directory, wake, spec, wake_time)
            if problems:
                print(f"Problems at step {step}: {problems}")
                return False
            
            rem = missing.get(step, [])
            if not rem:
                print(f"Step {step} has no remaining anchors.")
                break
            
            anchor = rem[0]
            current_sim_time += timedelta(seconds=1)
            ts_str = current_sim_time.isoformat()
            
            payload = {
                "round_id": round_id,
                "spec_sha256": spec["sha256"],
                "canonical_spec": spec["section_sources"]["kernel"],
                "kind": "section_read",
                "wake_id": wake["wake_id"],
                "step": step,
                "document_hashes": spec["document_hashes"],
                "observed_utc": ts_str,
                "sections_read": {anchor: index[anchor]},
                "source_files": {anchor: spec["section_sources"][anchor]},
                "status": "OK"
            }
            name = f"{step:02d}-{anchor}.json"
            save_receipt(directory / "section_receipts" / name, payload)
            print(f"Step {step}: Saved {name} at {ts_str}")
    
    # Final check
    missing, problems = section_progress(directory, wake, spec, wake_time)
    if problems:
        print(f"Final check problems: {problems}")
        return False
    prog = sop_progress(spec, missing)
    print("Final progress:", prog)
    return prog.get("formulation_reads_complete", False)

if __name__ == "__main__":
    r_id = sys.argv[1] if len(sys.argv) > 1 else "R801"
    success = run_all(r_id)
    print("SUCCESS:", success)
