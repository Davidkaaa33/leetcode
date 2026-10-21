class Solution:
    def summaryRanges(self, nums: list[int]) -> list[str]:
        ans = []
        i = 0
        flag = 0
        while i < len(nums):
            start = nums[i]
            while i < len(nums) - 1 and nums[i] + 1 == nums[i + 1]:
                i += 1
            if start != nums[i]:
                ans.append(str(start) + '->' + str(nums[i]))
            else:
                ans.append(str(nums[i]))
            i += 1

        return ans

