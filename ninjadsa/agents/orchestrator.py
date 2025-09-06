# agents/orchestrator.py
from typing import Dict, Any
from .curriculum_agent import CurriculumAgent
from .author_agent import AuthorAgent
from .solver_agent import SolverAgent
from .testcase_agent import TestcaseAgent
from .verifier_agent import VerifierAgent
from .explainer_agent import ExplainerAgent
from .exporter_agent import ExporterAgent

class Orchestrator:
    def __init__(self, artifacts_dir: str = "artifacts"):
        self.artifacts_dir = artifacts_dir
        self.curriculum = CurriculumAgent()
        self.author = AuthorAgent()
        self.solver = SolverAgent()
        self.testcase = TestcaseAgent()
        self.verifier = VerifierAgent()
        self.explainer = ExplainerAgent()
        self.exporter = ExporterAgent()

    def run(
        self,
        topic: str,
        difficulty: str,
        seed: int = 42,
        pattern: str | None = None,   # <— accept optional pattern override
    ) -> Dict[str, Any]:
        state: Dict[str, Any] = {
            "topic": topic,
            "difficulty": difficulty,
            "seed": seed,
            "pattern": pattern,               # make pattern available to CurriculumAgent
            "artifacts_dir": self.artifacts_dir,
        }

        state.update(self.curriculum.act(state))
        state.update(self.author.act(state))
        state.update(self.solver.act(state))
        state.update(self.testcase.act(state))

        v = self.verifier.act(state)
        state.update(v)

        state.update(self.explainer.act(state))
        state.update(self.exporter.act(state))
        return state
