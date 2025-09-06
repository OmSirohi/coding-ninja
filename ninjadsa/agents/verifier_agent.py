
from typing import Dict, Any
import os, subprocess, tempfile, sys, json

class VerifierAgent:
    name = "VerifierAgent"

    def _write_file(self, path: str, content: str):
        with open(path, "w", encoding="utf-8") as f:
            f.write(content)

    def act(self, state: Dict[str, Any]) -> Dict[str, Any]:
        solution_code = state["reference_solution_code"]
        tests = state["tests"]
        pattern = state["curriculum"]["pattern"]
        if pattern == "two_sum":
            call = "two_sum(case['in']['nums'], case['in']['target'])"
        elif pattern == "max_subarray_sum":
            call = "max_subarray(case['in']['nums'])"
        else:
            call = "search_insert(case['in']['nums'], case['in']['target'])"

        test_py = [
            "import json, sys",
            "from solution import *",
            "def run():",
            "  tests = " + json.dumps(tests),
            "  for idx, case in enumerate(tests):",
            f"    got = {call}",
            "    exp = case['out']",
            "    if got != exp:",
            "      print(f'FAIL {idx}: expected={exp} got={got}') ; return 1",
            "  print('OK'); return 0",
            "if __name__=='__main__':",
            "  raise SystemExit(run())",
        ]
        test_py = "\n".join(test_py)

        with tempfile.TemporaryDirectory() as td:
            sol = os.path.join(td, "solution.py")
            tst = os.path.join(td, "tests.py")
            self._write_file(sol, solution_code)
            self._write_file(tst, test_py)
            try:
                proc = subprocess.run([sys.executable, tst], capture_output=True, text=True, timeout=5)
            except subprocess.TimeoutExpired:
                return {"verification": {"status": "timeout", "stdout": "", "stderr": ""}}
            return {"verification": {"status": "ok" if proc.returncode == 0 else "fail",
                                     "stdout": proc.stdout.strip(),
                                     "stderr": proc.stderr.strip()}}
