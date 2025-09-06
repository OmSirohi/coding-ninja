def two_sum(nums: list[int], target: int) -> list[int]:
    m = {}
    for i, v in enumerate(nums):
        need = target - v
        if need in m:
            a, b = m[need], i
            return [a, b] if a < b else [b, a]
        m[v] = i
    return []