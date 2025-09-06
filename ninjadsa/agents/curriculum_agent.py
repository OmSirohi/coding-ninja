
from typing import Dict, Any
import random

TOPIC_LIBRARY = {
    "arrays": {
        "easy": [
            {"pattern": "two_sum", "objectives": ["hash map lookup", "linear scan"], "tags": ["hashing", "array"]},
        ],
        "medium": [
            {"pattern": "max_subarray_sum", "objectives": ["Kadane's algorithm"], "tags": ["dp", "array"]},
            {"pattern": "binary_search_insert", "objectives": ["binary search"], "tags": ["search", "array"]},
        ],
    }
}

class CurriculumAgent:
    name = "CurriculumAgent"

    def act(self, state: Dict[str, Any]) -> Dict[str, Any]:
        topic = state.get("topic", "arrays")
        difficulty = state.get("difficulty", "easy")
        choices = TOPIC_LIBRARY.get(topic, TOPIC_LIBRARY["arrays"]).get(difficulty, TOPIC_LIBRARY["arrays"]["easy"])
        rand = random.Random(state.get("seed", 42))
        pick = rand.choice(choices)
        return {"curriculum": {"topic": topic, "difficulty": difficulty, **pick}}
