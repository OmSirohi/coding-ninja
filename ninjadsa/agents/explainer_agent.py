from typing import Dict, Any
from .llm_client import LLMClient

HINTS = {
    "two_sum": [
        "Hint 1: Try storing numbers you have seen along with their indices.",
        "Hint 2: For each value v, what complement do you need to reach target?",
        "Hint 3: A dictionary mapping number → index allows O(1) lookup."
    ],
    "max_subarray_sum": [
        "Hint 1: Consider if extending the current segment helps or hurts.",
        "Hint 2: Track a running best and a running current sum.",
        "Hint 3: Kadane's algorithm solves it in O(n)."
    ],
    "binary_search_insert": [
        "Hint 1: Use binary search boundaries [lo, hi).",
        "Hint 2: Move left/right depending on nums[mid] < target.",
        "Hint 3: The insertion index is where the loop ends."
    ],
}

EDITORIALS = {
    "two_sum": "Use a single pass and a hash map. For each value v, check if target-v was seen; else store v→i.",
    "max_subarray_sum": "Kadane’s algorithm keeps a running sum and a best answer; reset the sum if it ever goes negative.",
    "binary_search_insert": "Classic lower_bound: maintain [lo,hi), mid=(lo+hi)//2, move boundaries until lo==hi."
}

class ExplainerAgent:
    name = "ExplainerAgent"

    def act(self, state: Dict[str, Any]) -> Dict[str, Any]:
        pattern = state["curriculum"]["pattern"]

        # ✨ Gemini polish (safe fallback if key missing)
        llm = LLMClient()
        refined_hints = [llm.refine(h, "Polish as a short, progressive DSA hint.") for h in HINTS[pattern]]
        refined_editorial = llm.refine(EDITORIALS[pattern], "Polish the editorial for clarity and pedagogy.")

        return {"hints": refined_hints, "editorial": refined_editorial}
