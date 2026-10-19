class Solution:
    def productExceptSelf(self, nums: list[int]) -> list[int]:
        n = len(nums)
        prods = [1] * n
        for i in range(1, n):
            prods[i] = prods[i - 1] * nums[i - 1]
        right = 1
        for i in range(n - 1, -1, -1):
            prods[i] *= right
            right *= nums[i]
        return prods