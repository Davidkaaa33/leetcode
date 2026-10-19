class Solution:
    def canConstruct(self, ransomNote: str, magazine: str) -> bool:
        dictn, dictm = {}, {}
        for c in ransomNote:
            dictn[c] = 1 + dictn.get(c, 0)
        for c in magazine:
            dictm[c] = 1 + dictm.get(c, 0)
        for c in dictn:
            if dictn[c] > dictm.get(c, 0):
                return False
        return True