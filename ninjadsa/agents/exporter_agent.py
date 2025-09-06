
from typing import Dict, Any
import os, json, time

class ExporterAgent:
    name = "ExporterAgent"

    def act(self, state: Dict[str, Any]) -> Dict[str, Any]:
        artifacts_dir = state.get("artifacts_dir", "artifacts")
        os.makedirs(artifacts_dir, exist_ok=True)
        problem = state["problem"]
        tests = state["tests"]
        solution_code = state["reference_solution_code"]
        hints = state["hints"]
        editorial = state["editorial"]

        problem_md = [
            f"# {problem['title']}",
            "",
            "## Problem",
            problem["statement"],
            "",
            "## Function Signature",
            f"```python\n{problem['signature']}\n```",
            "",
            "## Constraints",
        ]
        problem_md += [f"- {c}" for c in problem["constraints"]]
        problem_md += ["", "## Examples"]
        for ex in problem["examples"]:
            problem_md += [
                "```python",
                f"Input: {ex['in']}",
                f"Output: {ex['out']}",
                "```",
                ""
            ]

        with open(os.path.join(artifacts_dir, "problem.md"), "w", encoding="utf-8") as f:
            f.write("\n".join(problem_md))

        with open(os.path.join(artifacts_dir, "solution.py"), "w", encoding="utf-8") as f:
            f.write(solution_code)

        with open(os.path.join(artifacts_dir, "tests.py"), "w", encoding="utf-8") as f:
            f.write("### Generated tests as data, consumed by harness\n")
            f.write("TESTS = ")
            f.write(json.dumps(tests, indent=2))

        bundle = {
            "problem": problem,
            "tests": tests,
            "hints": hints,
            "editorial": editorial,
            "generated_at": time.time(),
        }
        with open(os.path.join(artifacts_dir, "problem.json"), "w", encoding="utf-8") as f:
            json.dump(bundle, f, indent=2)

        with open(os.path.join(artifacts_dir, "editorial.md"), "w", encoding="utf-8") as f:
            f.write(editorial)

        with open(os.path.join(artifacts_dir, "hints.md"), "w", encoding="utf-8") as f:
            f.write("\n".join(f"- {h}" for h in hints))

        return {"exported": True, "artifact_paths": [
            "problem.md", "solution.py", "tests.py", "problem.json", "editorial.md", "hints.md"
        ]}
