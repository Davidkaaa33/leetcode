class Solution:
    def twoSum(self, nums: list[int], target: int) -> list[int]:
        seen = dict()
        for i, n in enumerate(nums):
            diff = target - n
            if diff in seen:
                return [seen[diff], i]
            seen[n] = i
        return -1