class Solution:
    def isValid(self, s: str) -> bool:
        opening = ['(', '[', '{']
        closing = [')', ']', '}']

        stack = []
        for char in s:
            if char in opening:
                stack.append(char)

            elif char in closing:
                if not stack:
                    return False
                else:
                    if stack[-1] == opening[closing.index(char)]:
                        stack.pop()
                    else:
                        return False
        return not stack

        