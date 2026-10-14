class Solution:
    def transpose(self, matrix: list[list[int]]) -> list[list[int]]:
        rows, cols = len(matrix), len(matrix[0])
        res = [[0] * rows for _ in range(cols)]
        for r in range(rows):
            for c in range(cols):
                res[c][r] = matrix[r][c]
        return res