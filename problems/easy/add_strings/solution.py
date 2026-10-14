class Solution:
    def addStrings(self, num1: str, num2: str) -> str:
        i = len(num1) - 1
        j = len(num2) - 1

        carry = 0
        res = []
        while i >= 0 or j >= 0:
            d1 = int(num1[i]) if i >= 0 else 0
            d2 = int(num2[j]) if j >= 0 else 0
            k = d1 + d2 + carry
            res_d = k % 10
            carry = k // 10
            i -= 1
            j -= 1
            res.append(str(res_d))
        if carry:
            res.append(str(carry))
        return ''.join(reversed(res))