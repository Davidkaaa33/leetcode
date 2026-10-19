class Solution:
    def merge(self, nums1: list[int], m: int, nums2: list[int], n: int) -> None:
        pointer_fill = len(nums1) - 1
        pointer_nums1 = m - 1
        pointer_nums2 = n - 1
        while pointer_nums2 >= 0:
            if nums1[pointer_nums1] >= nums2[pointer_nums2] and pointer_nums1 >= 0:
                nums1[pointer_fill] = nums1[pointer_nums1]
                pointer_fill -= 1
                pointer_nums1 -= 1
            else:
                nums1[pointer_fill] = nums2[pointer_nums2]
                pointer_fill -= 1
                pointer_nums2 -= 1