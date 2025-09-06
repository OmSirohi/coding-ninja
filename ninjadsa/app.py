# app.py
import streamlit as st
import json, os, tempfile, subprocess, sys
from agents.orchestrator import Orchestrator

ART = "artifacts"

# Pattern selector with an "Auto" option that defers to Topic/Difficulty
PATTERN_CHOICES = [
    ("Auto (use Topic/Difficulty)", None),
    ("two_sum", "two_sum"),
    ("max_subarray_sum", "max_subarray_sum"),
    ("binary_search_insert", "binary_search_insert"),
    ("is_valid_parentheses", "is_valid_parentheses"),
    ("is_anagram", "is_anagram"),
    ("longest_substring_no_repeat", "longest_substring_no_repeat"),
    ("num_islands", "num_islands"),
]

def ensure_artifacts(topic="arrays", difficulty="easy", seed=42, pattern=None):
    """Always (re)generate a bundle so UI reflects the user's selection."""
    os.makedirs(ART, exist_ok=True)
    orch = Orchestrator(artifacts_dir=ART)
    orch.run(topic=topic, difficulty=difficulty, seed=seed, pattern=pattern)

def load_bundle():
    pj = os.path.join(ART, "problem.json")
    if not os.path.exists(pj):
        return {}
    with open(pj, "r", encoding="utf-8") as f:
        return json.load(f)

# ---------------- UI ----------------
st.set_page_config(page_title="NinjaDSA — Multi-Agent Tutor", layout="centered")
st.title("🧠 NinjaDSA — Multi-Agent Tutor")

with st.sidebar:
    st.caption("Bundle controls")

    topic = st.selectbox("Topic", ["arrays", "strings", "graphs"], index=0)
    difficulty = st.selectbox("Difficulty", ["easy", "medium"], index=0)
    pattern_label = st.selectbox("Pattern",
                                 [label for label, _ in PATTERN_CHOICES],
                                 index=0)
    pattern_value = {label: val for label, val in PATTERN_CHOICES}[pattern_label]
    seed = st.number_input("Seed", min_value=0, value=42, step=1)

    if st.button("Generate / Regenerate bundle", use_container_width=True):
        ensure_artifacts(topic=topic, difficulty=difficulty, seed=int(seed), pattern=pattern_value)
        st.success(f"Generated bundle "
                   f"(Topic={topic}, Difficulty={difficulty}, "
                   f"Pattern={'auto' if pattern_value is None else pattern_value}).")
        try:
            st.rerun()
        except Exception:
            st.experimental_rerun()

# First run: if nothing exists yet, generate a default AUTO bundle
if not os.path.exists(os.path.join(ART, "problem.json")):
    ensure_artifacts(topic="arrays", difficulty="easy", seed=42, pattern=None)

bundle = load_bundle()
if not bundle:
    st.error("Failed to generate or load the bundle. Try regenerating from the sidebar.")
    st.stop()

problem = bundle.get("problem", {})
tests = bundle.get("tests", [])
hints = bundle.get("hints", [])
editorial = bundle.get("editorial", "")

# Helpful header showing what is currently active
st.markdown(
    f"**Active Bundle:** "
    f"Topic=`{problem.get('tags', ['?'])[0] if problem.get('tags') else 'n/a'}`, "
    f"Difficulty=`{problem.get('difficulty','n/a') if 'difficulty' in problem else 'n/a'}`, "
    f"Pattern=`{problem.get('pattern','n/a')}`"
)

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
    height=240, value=""
)

CALLS = {
    "two_sum": "two_sum(case['in']['nums'], case['in']['target'])",
    "max_subarray_sum": "max_subarray(case['in']['nums'])",
    "binary_search_insert": "search_insert(case['in']['nums'], case['in']['target'])",
    "is_valid_parentheses": "is_valid_parentheses(case['in']['s'])",
    "is_anagram": "is_anagram(case['in']['s'], case['in']['t'])",
    "longest_substring_no_repeat": "length_of_longest_substring(case['in']['s'])",
    "num_islands": "num_islands(case['in']['grid'])",
}

def infer_call_expr(sig: str, problem: dict) -> str:
    pat = problem.get("pattern")
    if pat in CALLS:
        return CALLS[pat]
    # signature fallback
    if "two_sum(" in sig: return CALLS["two_sum"]
    if "max_subarray(" in sig: return CALLS["max_subarray_sum"]
    if "search_insert(" in sig: return CALLS["binary_search_insert"]
    if "is_valid_parentheses(" in sig: return CALLS["is_valid_parentheses"]
    if "is_anagram(" in sig: return CALLS["is_anagram"]
    if "length_of_longest_substring(" in sig: return CALLS["longest_substring_no_repeat"]
    if "num_islands(" in sig: return CALLS["num_islands"]
    # generic last resort
    name = sig.strip().split("(")[0].split()[-1]
    return f"{name}(**case['in'])"

if st.button("Run Tests"):
    if not user_code.strip():
        st.error("Please paste your function code.")
    else:
        call_expr = infer_call_expr(problem.get("signature", ""), problem)
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
