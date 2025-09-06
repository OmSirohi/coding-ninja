
from typing import Dict, Any

SOLUTIONS = {
    "two_sum": '''def two_sum(nums: list[int], target: int) -> list[int]:
    m = {}
    for i, v in enumerate(nums):
        need = target - v
        if need in m:
            a, b = m[need], i
            return [a, b] if a < b else [b, a]
        m[v] = i
    return []''',

    "max_subarray_sum": '''def max_subarray(nums: list[int]) -> int:
    best = cur = nums[0]
    for x in nums[1:]:
        cur = max(x, cur + x)
        best = max(best, cur)
    return best''',

    "binary_search_insert": '''def search_insert(nums: list[int], target: int) -> int:
    lo, hi = 0, len(nums)
    while lo < hi:
        mid = (lo + hi) // 2
        if nums[mid] < target:
            lo = mid + 1
        else:
            hi = mid
    return lo'''
}

class SolverAgent:
    name = "SolverAgent"

    def act(self, state: Dict[str, Any]) -> Dict[str, Any]:
        pattern = state["curriculum"]["pattern"]
        code = SOLUTIONS.get(pattern)
        return {"reference_solution_code": code}
