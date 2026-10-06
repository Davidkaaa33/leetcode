class Solution:
    def addToArrayForm(self, num: list[int], k: int) -> list[int]:
        num.reverse()
        i = 0
        while k:
            digit  = k % 10
            if i < len(num):
                num[i] += digit
            else:
                num.append(digit)
            carry = num[i] // 10
            num[i] = num[i] % 10

            k = k // 10
            k += carry
            i += 1

        num.reverse()
        return num