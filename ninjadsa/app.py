
import streamlit as st
import json, os, tempfile, subprocess, sys

ART = "artifacts"
st.set_page_config(page_title="NinjaDSA Tutor", layout="centered")
st.title("🧠 NinjaDSA — Multi‑Agent Tutor")

pj = os.path.join(ART, "problem.json")
if not os.path.exists(pj):
    st.warning("No artifacts found. Run `python main.py --topic arrays --difficulty easy` first.")
    st.stop()

with open(pj, "r", encoding="utf-8") as f:
    bundle = json.load(f)

st.header(bundle["problem"]["title"])
st.markdown("### Problem")
st.write(bundle["problem"]["statement"])
st.markdown("**Function Signature**")
st.code(bundle["problem"]["signature"], language="python")

with st.expander("Constraints & Examples"):
    st.write(bundle["problem"]["constraints"])
    for ex in bundle["problem"]["examples"]:
        st.code(f"Input: {ex['in']}\nOutput: {ex['out']}", language="python")

user_code = st.text_area("Paste your solution code:", height=240, value="")

def infer_call_expr(sig: str):
    if "two_sum(" in sig:
        return "two_sum(case['in']['nums'], case['in']['target'])"
    if "max_subarray(" in sig:
        return "max_subarray(case['in']['nums'])"
    if "search_insert(" in sig:
        return "search_insert(case['in']['nums'], case['in']['target'])"
    return ""

if st.button("Run Tests"):
    if not user_code.strip():
        st.error("Please paste your function code.")
    else:
        call_expr = infer_call_expr(bundle["problem"]["signature"])
        with tempfile.TemporaryDirectory() as td:
            sol = os.path.join(td, "solution.py")
            tst = os.path.join(td, "tests.py")
            with open(sol, "w", encoding="utf-8") as f:
                f.write(user_code)
            with open(tst, "w", encoding="utf-8") as f:
                f.write("from solution import *\n")
                f.write("import json\n")
                f.write("def run():\n")
                f.write("  tests = " + json.dumps(bundle["tests"]) + "\n")
                f.write("  for idx, case in enumerate(tests):\n")
                f.write(f"    got = {call_expr}\n")
                f.write("    if got != case['out']:\n")
                f.write("      print('FAIL {}: expected={} got={}'.format(idx, case['out'], got))\n")

                f.write("      return 1\n")
                f.write("  print('OK')\n  return 0\n")
                f.write("if __name__=='__main__':\n  raise SystemExit(run())\n")
            try:
                p = subprocess.run([sys.executable, tst], capture_output=True, text=True, timeout=5)
                st.code(p.stdout or p.stderr or "(no output)")
            except subprocess.TimeoutExpired:
                st.error("Execution timed out.")

with st.expander("Hints (progressive)"):
    for i, h in enumerate(bundle["hints"], 1):
        st.write(f"{i}. {h}")

with st.expander("Editorial"):
    st.write(bundle["editorial"])
