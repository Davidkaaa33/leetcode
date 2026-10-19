class Solution:
    def canThreePartsEqualSum(self, arr: list[int]) -> bool:
        total = sum(arr)
        if total % 3 != 0:
            return False
        target = total // 3
        cumsum = 0
        n = len(arr)
        nparts = 0
        for i in range(n - 1):
            cumsum += arr[i]
            if cumsum == target:
                cumsum = 0
                nparts += 1
            if nparts == 2:
                return True
        return False
