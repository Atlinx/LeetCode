import sys
from typing import List

# region Ideas
# No merging two sorted arrays (m + n > log(m + n))
#
# Total length = len (nums1) + len (nums2)
# Median location = Total length / 2
# Min  O(1)
# Max  O(1)
#
# How do find ith index of two sorted arrays without merging in log n?
#
# Median has to have same # of elements on left and right
# 
# Idea:
# Start in middle of both arrays, keep track of curr pos with mid_one, mid_two
# If mid_one > mid_two, then go to lowerhalf of mid_one, & update mid_(ne) 
# If mid_two < mid_two, then go to 
# Binary searach between two lists until you hit the median
# How do you know you've hit median?
#   Use counter to track number of 

#
# [Min 1, 2, 3, 4, 5, 6, 7]     len: 7
# [    3, 8  9 Max]             len: 3
# total len = 7 + 3 = 10
# median = 5
#
# [1, 2, 3, 4, 5, 6, 7]     len: 7
# [3, 8  9 ]             len: 3
# [1, 2, 3, 4, 5, 6, 7 -- 3, 8  9]
#  '-------------------------'
# 
#
# [Min 1, 2, 3, 4, 5, 6    ]
# [    3, 4, 5, 7, 8  Max 9]
#
# [3, 4, 5, 7, 8  9]
# [1, 2, 3, 4, 5, 6]
# endregion

MAX_INT = sys.maxsize
MIN_INT = -sys.maxsize - 1

class Solution:
    def findMedianSortedArraysO1(self, nums1: List[int], nums2: List[int]) -> float:  
        if (len(nums1) == 1 and len(nums2) == 0):
            return nums1[0]
        if (len(nums1) == 0 and len(nums2) == 1):
            return nums2[0]
        
        nums1_idx = 0
        nums2_idx = 0
        total_len = len(nums1) + len(nums2)
        median_idx = total_len // 2     # accounts for even length totals
        median = 0
        prev_median = 0
        while nums1_idx < len(nums1) or nums2_idx < len(nums2):
            total_idx = nums1_idx + nums2_idx
            if nums1_idx < len(nums1) and nums2_idx < len(nums2):
                if nums1[nums1_idx] < nums2[nums2_idx]:
                    prev_median = median
                    median = nums1[nums1_idx]
                    nums1_idx += 1
                else:
                    prev_median = median
                    median = nums2[nums2_idx]
                    nums2_idx += 1
            else:
                if nums1_idx < len(nums1):
                    prev_median = median
                    median = nums1[nums1_idx]
                    nums1_idx += 1
                else:
                    prev_median = median
                    median = nums2[nums2_idx]
                    nums2_idx += 1
            if total_idx == median_idx:
                break
        if total_len % 2 == 0:
            return (prev_median + median) / 2
        else:
            return median
    
    def is_in_range(self, nums: List[int], value: int):
        return value >= 0 and value < len(nums)

    def get_left_max(self, nums1: List[int], mid1: int, nums2: List[int], mid2: int):
        if len(nums1) % 2 == 1 and self.is_in_range(nums1, mid1):
            nums1_left_max = nums1[mid1]
        elif self.is_in_range(nums1, mid1 - 1):
            nums1_left_max = nums1[mid1 - 1]
        else:
            nums1_left_max = MIN_INT
        
        if len(nums2) % 2 == 1 and self.is_in_range(nums2, mid2):
            nums2_left_max = nums2[mid2]
        elif self.is_in_range(nums2, mid2 - 1):
            nums2_left_max = nums2[mid2 - 1] if len(nums2) % 2 == 0 else nums2[mid2]
        else:
            nums2_left_max = MIN_INT
            
        # If any of the mids are out of bounds, then we set the value of that mid's 
        # max to MIN_INT to prevent it from competing with the other mid's max
        if (nums1_left_max > nums2_left_max):
            return (nums1[mid1 - 1], True)
        else:
            return (nums2[mid2 - 1], False)

    def get_right_min(self, nums1: List[int], mid1: int, nums2: List[int], mid2: int):
        if mid1 >= 0 and mid1 < len(nums1):
            nums1_right_min = nums1[mid1]
        else:
            nums1_right_min = MAX_INT
        
        if mid2 >= 0 and mid2 < len(nums2):
            nums2_right_min = nums2[mid2]
        else:
            nums2_right_min = MAX_INT
        
        if (nums1_right_min < nums2_right_min):
            return (nums1[mid1], True)
        else:
            return (nums2[mid2], False)

    def find_med_of_array(self, nums: List[int]):
        return nums[len(nums) // 2]

    def findMedianSortedArraysOlogNM(self, nums1: List[int], nums2: List[int]) -> float:  
        # region Idea
        # nums1 and nums2 are sorted.
        # Median -> number which len(left half) = len(right half)
        # Given a sorted array, min = O(1), max = O(1)
        # When merging two arrays, they each contribute a portion to left half, and a portion to right half
        # 
        # We want to find the portion that goes to left and right for nums1 and nums2
        # We'd have to ensure len(left_portion_nums1 + left_portion_nums2) = len(right_portion_nums1 + right_portion_nums2)
        # Also, len(any_portion) < total_length / 2, as anything over would be greater than half of the total array size
        #
        # Ex 1.
        # [6 8 9 10 23 35 36]
        # [6 7 8 9]
        # We start by dividng both arrays in half and contributing those halfs to the portions
        #
        # [6 8 9 | 23 35 36]
        # [6 7 | 8 9]
        # left_portion:  max: 9
        # right_portion: min: 8 
        #
        # min(right_portion) < max(left_portion):
        #   We must do something because the two portions are intersecting!
        #
        # [6 8 | 9 23 35 36]
        # [6 7 8 | 9]
        # Go to the middle of the upper half of the smaller array
        # left_portion:  max: 8
        # right_portion: min: 9
        # They don't intersect! We're good to go!
        # med = (max(left) + min(right)) / 2
        #     = (8 + 9) / 2 = 8.5
        #
        # [6 6 7 8 [8 9] 9 23 35 36]
        # med = 8.5
        #
        #
        #
        # Ex 2.
        # [6 8 9 10 23 35 36 39 56 78 80 81 82 84]
        # [6 7 8 9  20 37 49 90 96 98]
        # We start by dividng both arrays in half and contributing those halfs to the portions
        #
        # [6 8 9 10 23 35 36 | 39 56 78 80 81 82 84]
        # [6 7 8 9  20 | 37 49 90 96 98]
        # left_portion:  max: 36
        # right_portion: min: 37
        # max(left) < min(right)
        # We're good to go!
        # med = (36 + 37) / 2 = 36.5
        #
        #
        #
        # Ex 3.
        # '|' = divides or "cuts" the array into left and right halfs
        # '.' = represents a previous cut line
        #
        # [6  8  9  10 23 35 36 39 56 78 80 81 82 84]
        # [6  22 30 55 85 86 94 98 99 100]
        # We start by dividng both arrays in half and contributing those halfs to the portions
        #
        # [6 8 9 10 23 35 36 | 39 56 78 80 81 82 84]
        # [6 22 30 55 85 | 86 94 98 99 100]
        # left_portion:  max: 85 (2)
        # right_portion: min: 39 (1)
        # Intersect!
        # Because max(left_half_two) > min(right_half_one)
        # We want to move max(left_half_two) and min(right_half_one) apart 
        #                    .----->
        # [6 8 9 10 23 35 36 | 39 56 78 80 81 82 84]
        # [6 22 30 55 85 | 86 94 98 99 100]
        #           <----'
        #
        # [6 8 9 10  23 35 36 . 39 56 | 78 80 81 82 84]
        # [6 22 30 | 55 85 . 86 94 98 99 100]
        # left_portion:  max: 56 (1)
        # right_portion: min: 55 (2)
        # Still intersecting, but this time we have to move in opposite direction
        #                          <--.
        # [6 8 9 10  23 35 36 . 39 56 | 78 80 81 82 84]
        # [6 22 30 | 55 85 . 86 94 98 99 100]
        #          '-->
        #
        # [6 8 9 10 23 35 36 . 39 | 56 . 78 80 81 82 84]
        # [6 22 30 . 55 | 85 . 86 94 98 99 100]
        # left_portion: max: 55
        # right_portion: min: 56
        # The portions don't intersect! max(left) < max(right)
        # We're good to go
        # med = (max(left) + min(right)) / 2 = (55 + 56) / 2 = 55.5
        #
        # NOTE: You must do binary search on the SMALLEST array. This avoids index out of bounds exceptions when both array cuts are moved
        #       If did you the binary search with the largest array, it's possible the movement would go out of bounds of the smaller array.
        #       Also we know the cut has to be within both arrays, so there's no point in prefering the large array
        #
        #
        #
        # Ex.
        # [1 3 |[5] 8]   4 / 2 = 2
        # [1 |[2] 5]     3 / 2 = 1
        # left max: 3 (1)
        # right_min: 2 (2)
        #    <-.
        # [1 3 |[5] 8]
        # [1 |[2] 5]
        #     '->
        #
        # [1 |[3] 5 8]
        # [1 2 |[5]]
        # left max: 2
        # right_min: 3
        # We're a go!
        # med = (2 + 3) / 2 = 2.5
        # endregion

        # DEFINE: cut
        #   left = [0, cut)
        #   right = [cut, last_index]
        if (len(nums1) < len(nums2)):
            largest: List[int] = nums2
            smallest: List[int] = nums1
        else:
            largest = nums1
            smallest = nums2
        
        if (len(smallest) == 0):
            # We're given that there is at least one array with size >= 1
            assert(len(largest) > 0)
            return self.find_med_of_array(largest)

        small_hi = len(smallest)
        small_low = 0
        small_mid = small_hi // 2

        large_mid = len(largest) // 2

        while True:
            (left_max, is_left_max_from_smallest) = self.get_left_max(smallest, small_mid, largest, large_mid)
            (right_min, _) = self.get_right_min(smallest, small_mid, largest, large_mid)

            if left_max > right_min:
                # Uh oh, there's an intersection that we have to resolve!
                if is_left_max_from_smallest:
                    # Move to left half on smallest
                    original_small_mid = small_mid
                    small_hi = small_mid
                    small_mid = (small_low + small_hi) // 2

                    small_movement_amount = original_small_mid - small_mid
                    assert(small_movement_amount > 0)
                    # Move largest by the same amount in the opposite direction (towards right half)
                    large_mid += small_movement_amount
                else:
                    # Move to upper half on smallest
                    original_small_mid = small_mid
                    small_low = small_mid + 1
                    small_mid = (small_low + small_hi) // 2

                    small_movement_amount = small_mid - original_small_mid
                    assert(small_movement_amount > 0)
                    # Move largest by the same amount in the opposite direction (towards right half)
                    large_mid -= small_movement_amount

            else:
                # We did it!
                break
        
        (left_max, _) = self.get_left_max(smallest, small_mid, largest, large_mid)
        (right_min, _) = self.get_right_min(smallest, small_mid, largest, large_mid)
        return (left_max + right_min) / 2

    def findMedianSortedArrays(self, nums1: List[int], nums2: List[int]) -> float:        
        return self.findMedianSortedArraysOlogNM(nums1, nums2)

def test(arr1, arr2, exp):
    res = s.findMedianSortedArrays(arr1, arr2)
    print(f"{'🟩' if res == exp else '🟥' } Value: {res} Expected: {exp}")

if __name__ == "__main__":
    s = Solution()
    # test([1, 3], [2], 2.0)
    # test([1, 2], [3, 4], 2.5)
    # test([0, 0], [0, 0], 0.0)
    # test([], [1], 1.0)
    # test([2], [], 2.0)
    test([1, 2], [3, 4, 5], 3.0)
    # test([1, 2, 3, 7, 29], [4, 5, 6, 83], 5.0)
    # test([1, 2, 3, 4], [5, 6, 7, 8], 4.5)
    # test([1, 2, 3, 4, 5], [6, 7, 8, 9, 10], 5.5)