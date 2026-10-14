class Solution:
    def diagonalSum(self, mat: list[list[int]]) -> int:
        n = len(mat)
        res = 0
        for i in range(n):
            res += mat[i][i]
            res += mat[i][n - 1 - i]
        
        return res - (mat[n//2][n//2] if n % 2 else 0)
