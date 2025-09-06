# Two Sum (Unique Indices)

## Problem
Given an array nums of integers and an integer target, return indices of the two numbers such that they add up to target. Assume exactly one solution and the same element cannot be used twice. Return the indices in increasing order.

## Function Signature
```python
def two_sum(nums: list[int], target: int) -> list[int]:
```

## Constraints
- 2 <= len(nums) <= 1e5
- -1e9 <= nums[i], target <= 1e9
- There is exactly one valid pair

## Examples
```python
Input: {'nums': [2, 7, 11, 15], 'target': 9}
Output: [0, 1]
```

```python
Input: {'nums': [3, 2, 4], 'target': 6}
Output: [1, 2]
```
