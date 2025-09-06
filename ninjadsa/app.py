# app.py
import streamlit as st
import json, os, tempfile, subprocess, sys

# --- Auto-generate artifacts on first run (works on Streamlit Cloud) ---
from agents.orchestrator import Orchestrator

ART = "artifacts"

def ensure_artifacts(topic: str = "arrays", difficulty: str = "easy", seed: int = 42):
    """Generate a bundle if artifacts/problem.json is missing."""
    pj = os.path.join(ART, "problem.json")
    if not os.path.exists(pj):
        os.makedirs(ART, exist_ok=True)
        orch = Orchestrator(artifacts_dir=ART)
        state = orch.run(topic=topic, difficulty=difficulty, seed=seed)
        # If exporter didn't create problem.json for any reason, write a minimal one:
        if not os.path.exists(pj):
            with open(pj, "w", encoding="utf-8") as f:
                json.dump({
                    "problem": state.get("problem"),
                    "tests": state.get("tests"),
                    "hints": state.get("hints"),
                    "editorial": state.get("editorial"),
                }, f, indent=2)

# Generate once on startup
ensure_artifacts()

# --- Streamlit UI ---
st.set_page_config(page_title="NinjaDSA Tutor", layout="centered")
st.title("🧠 NinjaDSA — Multi-Agent Tutor")

# Sidebar controls for regeneration
with st.sidebar:
    st.caption("Bundle controls")
    topic = st.selectbox("Topic", ["arrays", "strings", "graphs"], index=0)
    difficulty = st.selectbox("Difficulty", ["easy", "medium"], index=0)
    seed = st.number_input("Seed", min_value=0, value=42, step=1)
    if st.button("Regenerate bundle"):
        ensure_artifacts(topic=topic, difficulty=difficulty, seed=int(seed))
        st.success("Bundle regenerated.")
        st.experimental_rerun()

pj = os.path.join(ART, "problem.json")
if not os.path.exists(pj):
    st.error("Failed to generate artifacts. Please try the 'Regenerate bundle' button.")
    st.stop()

with open(pj, "r", encoding="utf-8") as f:
    bundle = json.load(f)

problem = bundle.get("problem", {})
tests = bundle.get("tests", [])
hints = bundle.get("hints", [])
editorial = bundle.get("editorial", "")

st.header(problem.get("title", "Problem"))
st.markdown("### Problem")
st.write(problem.get("statement", ""))
st.markdown("**Function Signature**")
st.code(problem.get("signature", ""), language="python")

with st.expander("Constraints & Examples", expanded=False):
    constraints = problem.get("constraints", [])
    if constraints:
        st.write(constraints)
    for ex in problem.get("examples", []):
        st.code(f"Input: {ex.get('in')}\nOutput: {ex.get('out')}", language="python")

user_code = st.text_area(
    "Paste your solution code (define the function with the exact signature):",
    height=240,
    value=""
)

def infer_call_expr(sig: str) -> str:
    """Return the Python expression to call the user's function for each test case."""
    if "two_sum(" in sig:
        return "two_sum(case['in']['nums'], case['in']['target'])"
    if "max_subarray(" in sig:
        return "max_subarray(case['in']['nums'])"
    if "search_insert(" in sig:
        return "search_insert(case['in']['nums'], case['in']['target'])"
    # Fallback: try to infer by name tokens (very basic)
    name = sig.strip().split("(")[0].split()[-1]
    args = "case['in']"
    return f"{name}({args})"

if st.button("Run Tests"):
    if not user_code.strip():
        st.error("Please paste your function code.")
    else:
        call_expr = infer_call_expr(problem.get("signature", ""))
        with tempfile.TemporaryDirectory() as td:
            sol = os.path.join(td, "solution.py")
            tst = os.path.join(td, "tests.py")
            with open(sol, "w", encoding="utf-8") as f:
                f.write(user_code)
            with open(tst, "w", encoding="utf-8") as f:
                f.write("from solution import *\n")
                f.write("import json\n")
                f.write("def run():\n")
                f.write("  tests = " + json.dumps(tests) + "\n")
                f.write("  for idx, case in enumerate(tests):\n")
                # IMPORTANT: no f-string here; use .format to avoid quoting issues
                f.write(f"    got = {call_expr}\n")
                f.write("    if got != case['out']:\n")
                f.write("      print('FAIL {}: expected={} got={}'.format(idx, case['out'], got))\n")
                f.write("      return 1\n")
                f.write("  print('OK')\n  return 0\n")
                f.write("if __name__=='__main__':\n  raise SystemExit(run())\n")
            try:
                p = subprocess.run([sys.executable, tst], capture_output=True, text=True, timeout=8)
                st.code((p.stdout or "") + (p.stderr or ""), language="text")
            except subprocess.TimeoutExpired:
                st.error("Execution timed out.")

with st.expander("Hints (progressive)"):
    for i, h in enumerate(hints, 1):
        st.write(f"{i}. {h}")

with st.expander("Editorial"):
    st.write(editorial if editorial else "_No editorial available._")
