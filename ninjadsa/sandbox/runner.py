
import os, sys, subprocess, tempfile, json

def run_in_sandbox(solution_code: str, tests_json: str, call_expr: str, timeout_sec: int = 2):
    with tempfile.TemporaryDirectory() as td:
        sol = os.path.join(td, "solution.py")
        tst = os.path.join(td, "tests.py")
        with open(sol, "w", encoding="utf-8") as f:
            f.write(solution_code)
        harness = f"""
import json, sys
from solution import *
def run():
    tests = {tests_json}
    for idx, case in enumerate(tests):
        got = {call_expr}
        exp = case['out']
        if got != exp:
            print(f'FAIL {{idx}}: expected={{exp}} got={{got}}'); return 1
    print('OK'); return 0
if __name__=='__main__':
    raise SystemExit(run())
"""
        with open(tst, "w", encoding="utf-8") as f:
            f.write(harness)
        try:
            p = subprocess.run([sys.executable, tst], capture_output=True, text=True, timeout=timeout_sec+1)
        except subprocess.TimeoutExpired:
            return {"status": "timeout", "stdout": "", "stderr": ""}
        return {"status": "ok" if p.returncode == 0 else "fail", "stdout": p.stdout, "stderr": p.stderr}
