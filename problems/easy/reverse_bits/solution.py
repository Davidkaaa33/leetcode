class Solution:
    def reverseBits(self, n: int) -> int:
        res = 0
        for i in range(32):
            last = n & 1
            res = (res << 1) | last
            n = n >> 1
        return res
        