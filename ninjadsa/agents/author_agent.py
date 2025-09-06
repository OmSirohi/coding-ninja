from typing import Dict, Any
from .llm_client import LLMClient

TEMPLATES = {
    "two_sum": {
        "title": "Two Sum (Unique Indices)",
        "signature": "def two_sum(nums: list[int], target: int) -> list[int]:",
        "statement": (
            "Given an array nums of integers and an integer target, return indices of the two numbers such that they add up to target. "
            "Assume exactly one solution and the same element cannot be used twice. Return the indices in increasing order."
        ),
        "constraints": [
            "2 <= len(nums) <= 1e5",
            "-1e9 <= nums[i], target <= 1e9",
            "There is exactly one valid pair"
        ],
        "examples": [
            {"in": {"nums": [2,7,11,15], "target": 9}, "out": [0,1]},
            {"in": {"nums": [3,2,4], "target": 6}, "out": [1,2]}
        ]
    },
    "max_subarray_sum": {
        "title": "Maximum Subarray Sum (Kadane)",
        "signature": "def max_subarray(nums: list[int]) -> int:",
        "statement": "Given an integer array nums, find the contiguous subarray with the largest sum and return its sum.",
        "constraints": ["1 <= len(nums) <= 1e5", "-1e9 <= nums[i] <= 1e9"],
        "examples": [
            {"in": {"nums": [-2,1,-3,4,-1,2,1,-5,4]}, "out": 6},
            {"in": {"nums": [1]}, "out": 1}
        ]
    },
    "binary_search_insert": {
        "title": "Binary Search Insert Position",
        "signature": "def search_insert(nums: list[int], target: int) -> int:",
        "statement": "Given a sorted array of distinct integers and a target value, return the index if the target is found, otherwise the insertion index.",
        "constraints": ["1 <= len(nums) <= 1e5", "-1e9 <= nums[i], target <= 1e9"],
        "examples": [
            {"in": {"nums": [1,3,5,6], "target": 5}, "out": 2},
            {"in": {"nums": [1,3,5,6], "target": 2}, "out": 1}
        ]
    }
}

class AuthorAgent:
    name = "AuthorAgent"

    def act(self, state: Dict[str, Any]) -> Dict[str, Any]:
        curriculum = state["curriculum"]
        pattern = curriculum["pattern"]
        spec = TEMPLATES.get(pattern, TEMPLATES["two_sum"])

        problem = {
            "title": spec["title"],
            "statement": spec["statement"],
            "signature": spec["signature"],
            "constraints": spec["constraints"],
            "examples": spec["examples"],
            "tags": curriculum.get("tags", []),
            "objectives": curriculum.get("objectives", []),
            "pattern": pattern,
        }

        # ✨ Gemini polish (safe fallback if key missing)
        llm = LLMClient()
        problem["statement"] = llm.refine(
            problem["statement"],
            system_hint="Polish the DSA problem statement for clarity and concision without changing meaning."
        )
        # Optional: also polish constraints/examples if you want:
        # problem["constraints"] = [llm.refine(c, "Polish this constraint.") for c in problem["constraints"]]

        return {"problem": problem}
