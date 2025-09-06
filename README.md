1) Problem Statement
Creating strong DSA practice content is slow and inconsistent. Instructors must craft precise statements, design adversarial tests, implement and verify reference solutions, and provide teaching materials (hints/editorial). This does not scale; learners get uneven quality.
Goal: Use AI multi-agent collaboration to author, verify, and teach DSA problems end-to-end with consistent quality and minimal manual overhead.
Why AI multi-agent (not single agent)?
Specialization: Writing crisp statements ≠ producing adversarial tests ≠ explaining pedagogy. Separate agents excel at each.
Checks & balances: A Verifier executes the Solver against the Testcase suite; failures force revisions. This reduces silently-wrong outputs.
Scalability & modularity: Add/replace agents (e.g., difficulty calibrator, plagiarism checker) without disrupting the rest.
2) What This App Does
Given a topic & difficulty (e.g., arrays / easy), NinjaDSA:
Authors a problem statement, function signature, constraints, examples.
Generates adversarial tests, including randomized edge cases.
Produces a reference solution (canonical algorithm for the pattern).
Verifies the reference solution in a sandbox with timeouts.
Explains with a 3-step hint ladder and a complete editorial.
Exports a bundle to /artifacts and serves a Streamlit lesson page for learners to paste their own code and run tests.
Artifacts produced: problem.md, problem.json, solution.py, tests.py, hints.md, editorial.md
3) Architecture & Agent Interactions
Agents (roles):
CurriculumAgent — selects a problem pattern by topic/difficulty (e.g., Two-Sum / Kadane / Binary Search Insert).
AuthorAgent — drafts statement, signature, constraints, examples.
TestcaseAgent — builds deterministic + randomized tests; covers edge cases.
SolverAgent — writes a canonical reference solution with time/space complexity.
VerifierAgent — sandbox-executes the solution vs tests; enforces timeouts; returns pass/fail diagnostics.
ExplainerAgent — generates progressive hints and an editorial (intuition → approach → complexity).
ExporterAgent — writes markdown/code/JSON artifacts for the app and for upload.
Orchestrator coordinates message passing across agents via a shared state:
Curriculum → Author → Testcase → Solver → Verifier → Explainer → Exporter
If verification fails, the Orchestrator can loop back to Author/Testcase/Solver for revision (extensible).
4) Tech Stack (Tools, Libraries, Frameworks)
Language: Python 3.10+
UI: Streamlit (lesson page for learning & self-testing)
Orchestration: Lightweight custom orchestrator (framework-agnostic, offline-first)
Sandbox: Python subprocess with timeouts (and resource limits where supported)
Optional orchestration frameworks (not required): LangGraph / CrewAI / AutoGen
Optional LLM client: Gemini (Flash) via google-genai SDK
5) LLM Selection (Optional)
The system runs fully offline by default. LLMs are optional and used only to polish natural language (statement/hints/editorial).
Ideal (best quality): GPT-4/4o, Claude 3.5, Gemini 1.5 Pro
Free/low-cost options (recommended):
Gemini 1.5 Flash (free tier; fast, good for paraphrasing)
Open-source via Ollama (e.g., Mistral 7B, Llama 3 variants) — local, private, zero API spend
Justification: Language polish benefits from LLMs; tests and verification are deterministic and do not require an LLM (keeps cost low and reliability high).
6) Repository Structure
ninjadsa/
  agents/
    base.py
    curriculum_agent.py
    author_agent.py
    testcase_agent.py
    solver_agent.py
    verifier_agent.py
    explainer_agent.py
    exporter_agent.py
    llm_client.py      # optional Gemini client; safe no-op if key missing
    orchestrator.py
  sandbox/
    runner.py          # minimal sandbox harness (timeouts)
  artifacts/           # generated outputs (problem.md/json, tests, solution, hints, editorial)
  app.py               # Streamlit lesson UI (paste code, run tests, reveal hints, read editorial)
  main.py              # CLI to generate a bundle end-to-end
  README.md
  EXPLANATION.md
  requirements.txt
7) Setup & Run (Local)
Works offline. LLM is optional. Use macOS commands below; Windows equivalents are provided.
A) Create venv & install dependencies
python3 -m venv .venv
source .venv/bin/activate           # Windows: .venv\Scripts\activate
pip install -r requirements.txt
B) Generate a problem bundle (offline)
python main.py --topic arrays --difficulty easy
You’ll see the files in ./artifacts:
problem.md, problem.json, solution.py, tests.py, hints.md, editorial.md
C) Run the lesson UI
streamlit run app.py
Open the browser tab:
Read the problem, paste your solution function, click Run Tests
Reveal the Hints and Editorial progressively
8) Enable Gemini Flash (Optional)
Install SDK
pip install -U google-genai
(Add google-genai>=1.0.0 to requirements.txt.)
Set environment variables (macOS)
export GEMINI_API_KEY="PASTE-YOUR-KEY"
export LLM_MODEL="gemini-1.5-flash"
(For project use in VS Code, add a .env with those two lines and set .vscode/settings.json → "python.envFile": "${workspaceFolder}/.env".)
Regenerate & run
python main.py --topic arrays --difficulty easy
streamlit run app.py
If the key is missing, the LLM client safely returns original text—nothing breaks.
9) Deployment
Streamlit Cloud
Push this repo to GitHub.
Create a new Streamlit app → entrypoint app.py.
If using Gemini, add GEMINI_API_KEY and LLM_MODEL as secrets.
Optionally run python main.py on deploy (or commit artifacts).
Hugging Face Spaces (Streamlit)
Create a new Space → choose Streamlit.
Set commands: pip install -r requirements.txt && python main.py && streamlit run app.py.
Add secrets for Gemini only if enabling the LLM.
10) Originality / Plagiarism Strategy
Statements, hints, editorial are original.
Randomized tests reduce overlap/run-to-run similarity.
When LLM is enabled, it’s used for paraphrasing and clarity—not for copying public text.
Everything needed to re-generate outputs locally is included.
11) Troubleshooting
“No artifacts found” in the UI
Run:
python main.py --topic arrays --difficulty easy
streamlit run app.py
Streamlit not found
Activate venv and install deps:
source .venv/bin/activate
pip install -r requirements.txt
Gemini not detected
Verify env vars:
python -c "import os; print('has_key=', bool(os.environ.get('GEMINI_API_KEY')), 'model=', os.environ.get('LLM_MODEL'))"
Expect: has_key= True, model= gemini-1.5-flash.
12) Assignment Mapping (Company’s Requirements)
Problem Statement — See Section 1.
Why AI Agents / Multi-Agent Value — See Sections 1 & 3.
Project Description — See Sections 2 & 3.
Tools, Libraries, Frameworks — See Section 4.
LLM Selection (+ free tier) — See Section 5.
Code & Deployment — See Sections 6, 7, 9.
README includes: problem statement, agent interactions, technologies used, setup & run instructions — yes.
