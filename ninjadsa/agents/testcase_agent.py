
from typing import Dict, Any
import random

def _tests_for_two_sum():
    t = []
    t.append({"in": {"nums": [2,7,11,15], "target": 9}, "out": [0,1]})
    t.append({"in": {"nums": [3,2,4], "target": 6}, "out": [1,2]})
    rnd = random.Random(123)
    arr = rnd.sample(range(-100, 101), 30)  # unique values
    i, j = rnd.sample(range(30), 2)
    target = arr[i] + arr[j]
    ans = sorted([i, j])
    t.append({"in": {"nums": arr, "target": target}, "out": ans})
    return t

def _tests_for_max_subarray():
    t = []
    t.append({"in": {"nums": [-2,1,-3,4,-1,2,1,-5,4]}, "out": 6})
    t.append({"in": {"nums": [1]}, "out": 1})
    t.append({"in": {"nums": [5,4,-1,7,8]}, "out": 23})
    rnd = random.Random(456)
    for _ in range(3):
        n = 20
        arr = [rnd.randint(-20,20) for _ in range(n)]
        best = -10**18
        for i in range(n):
            cur = 0
            for j in range(i, n):
                cur += arr[j]
                best = max(best, cur)
        t.append({"in": {"nums": arr}, "out": best})
    return t

def _tests_for_bsi():
    return [
        {"in": {"nums": [1,3,5,6], "target": 5}, "out": 2},
        {"in": {"nums": [1,3,5,6], "target": 2}, "out": 1},
        {"in": {"nums": [1,3,5,6], "target": 7}, "out": 4},
        {"in": {"nums": [1,3,5,6], "target": 0}, "out": 0},
    ]

TEST_BUILDERS = {
    "two_sum": _tests_for_two_sum,
    "max_subarray_sum": _tests_for_max_subarray,
    "binary_search_insert": _tests_for_bsi,
}

class TestcaseAgent:
    name = "TestcaseAgent"

    def act(self, state: Dict[str, Any]) -> Dict[str, Any]:
        pattern = state["curriculum"]["pattern"]
        tests = TEST_BUILDERS[pattern]()
        return {"tests": tests}
