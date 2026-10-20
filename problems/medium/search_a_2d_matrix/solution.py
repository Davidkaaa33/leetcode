class Solution:
    def searchMatrix(self, matrix: list[list[int]], target: int) -> bool:
        rows, cols = len(matrix), len(matrix[0])
        bot, top = 0, rows - 1
        while bot <= top:
            mid_row = (top - bot) // 2 + bot
            if target > matrix[mid_row][-1]:
                bot = mid_row + 1
            elif target < matrix[mid_row][0]:
                top = mid_row - 1
            else:
                l, r = 0, cols - 1
                while l <= r:
                    m = (r - l) // 2 + l
                    if target < matrix[mid_row][m]:
                        r = m - 1
                    elif target > matrix[mid_row][m]:
                        l = m + 1
                    else:
                        return True
                return False
        return False
        