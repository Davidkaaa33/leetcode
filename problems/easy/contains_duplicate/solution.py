class Solution:
    def containsDuplicate(self, nums: list[int]) -> bool:
        seen = set()
        for x in nums:
            if x in seen:
                return True
            else:
                seen.add(x)
        return False