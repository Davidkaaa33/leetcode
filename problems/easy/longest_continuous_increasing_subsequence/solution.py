class Solution:
    def findLengthOfLCIS(self, nums: list[int]) -> int:
        n = len(nums)
        maxi = 1
        curr = 1
        for i in range(1, n):
            if nums[i - 1] < nums[i]:
                curr += 1
            else:
                maxi = max(maxi, curr)
                curr = 1
        maxi = max(maxi, curr)
        return maxi