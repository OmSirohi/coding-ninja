
# NinjaDSA — Multi‑Agent Problem Author & Tutor (Offline‑ready)

What it does: Generates a complete DSA problem bundle (problem statement, signature, constraints, examples, tests, reference solution, hints, editorial) and provides a Streamlit lesson page.

Agents: Curriculum → Author → Testcase → Solver → Verifier → Explainer → Exporter (coordinated by Orchestrator).

## Quick start
```bash
python -m venv .venv && source .venv/bin/activate   # Windows: .venv\Scripts\activate
pip install -r requirements.txt

# Generate a problem bundle
python main.py --topic arrays --difficulty easy

# Launch the lesson UI
streamlit run app.py
```

Artifacts: `./artifacts` (problem.md, problem.json, tests.py, solution.py, hints.md, editorial.md).

## Requirements
- Python 3.10+
- streamlit (UI) — see requirements.txt

## LLM (optional)
Runs offline by default. If you set `LLM_MODEL` and provider keys, implement calls in `agents/llm_client.py`.
