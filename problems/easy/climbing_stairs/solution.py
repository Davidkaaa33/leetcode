class Solution:
    def climbStairs(self, n: int) -> int:
        step_2 = 1
        step_1 = 2
        step_cur = 0
        if n == 1:
            return step_2
        elif n == 2:
            return step_1
        else:
            for i in range(2, n):
                step_cur = step_2 + step_1
                step_2 = step_1
                step_1 = step_cur
        return step_cur