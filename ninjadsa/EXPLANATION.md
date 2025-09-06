
# Project Explanation — NinjaDSA

## Problem
Authoring DSA problems at scale requires precise statements, adversarial tests, verified solutions, and pedagogy (hints/editorial). Manual work is slow and inconsistent.

## Why multi‑agent
Specialized agents collaborate and verify each other: Author/Testcase/Solver/Verifier for technical correctness; Explainer for pedagogy; Exporter for packaging; Orchestrator to coordinate and enable retries.

## Offline
Everything runs locally without APIs. Optional LLM integration hook is provided for future enrichment.

## Evaluate
1) `python main.py --topic arrays --difficulty easy` → see `./artifacts`  
2) `streamlit run app.py` → paste a solution → run tests → reveal hints → read editorial.

## Extend
Add new patterns & tests, more agents (difficulty calibration, tagging, plagiarism checks), or a real LLM client.
