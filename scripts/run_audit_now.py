import os
import sys

engine_dir = r"C:\Users\SIGMA\Documents\cg-terminal\Delta_Fibonacci_Institutional_Business\engine"
sys.path.append(engine_dir)
import run_full_business_audit

print("Executing audit...")
run_full_business_audit.main()
print("Audit script finished.")
