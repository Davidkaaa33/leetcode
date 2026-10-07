# LeetCode — Algorithms & Data Structures

A continuously maintained collection of algorithm and data-structure practice from [LeetCode](https://leetcode.com). Every solution in this repository was written by hand.

**25** solved · 15 easy · 10 medium · 0 hard

![Coverage](./coverage.svg)

_Synced nightly at 00:00 MSK via GitHub Actions. Accepted submissions, dates, the problem index and coverage visualization are regenerated automatically._

## Why this repository exists

The purpose of this repository is to strengthen the software-engineering and algorithmic foundations that support production ML work: choosing suitable data structures, reasoning about complexity, recognizing standard patterns and writing small correct implementations under clear constraints.

It is intentionally kept separate from my ML case studies. The ML repositories demonstrate modeling, validation, APIs and deployment; this repository demonstrates ongoing **DS&A problem-solving discipline**.

## Workflow

~~~text
accepted LeetCode submission
        ↓
nightly authenticated sync
        ↓
problem stored by difficulty
        ↓
first-solved date recovered from Git history
        ↓
README + coverage.svg regenerated
        ↓
changes committed automatically
~~~

The automation is implemented in .github/workflows/leetcode-sync.yml and scripts/generate_readme.py. If LeetCode's live problem totals cannot be refreshed, the generator falls back to conservative local totals so README generation remains deterministic.

## Repository structure

~~~text
problems/
├── easy/
├── medium/
└── hard/

scripts/generate_readme.py       progress / index generator
.github/workflows/leetcode-sync.yml
coverage.svg                    generated coverage visualization
README.md                       generated problem index
~~~

## What I focus on while solving

- selecting the appropriate data structure before coding;
- reducing unnecessary time or space complexity;
- handling boundary cases explicitly;
- recognizing reusable patterns rather than memorizing isolated answers;
- keeping implementations readable enough to revisit later.

## Problems

| Problem | Difficulty | Solved | Solution |
| --- | --- | --- | --- |
| [Add Strings](https://leetcode.com/problems/add-strings/) | easy | 2026-10-06 | [solution](problems/easy/add_strings) |
| [Add To Array Form Of Integer](https://leetcode.com/problems/add-to-array-form-of-integer/) | easy | 2026-10-06 | [solution](problems/easy/add_to_array_form_of_integer) |
| [Best Time To Buy And Sell Stock](https://leetcode.com/problems/best-time-to-buy-and-sell-stock/) | easy | 2026-10-06 | [solution](problems/easy/best_time_to_buy_and_sell_stock) |
| [Climbing Stairs](https://leetcode.com/problems/climbing-stairs/) | easy | 2026-10-06 | [solution](problems/easy/climbing_stairs) |
| [Contains Duplicate](https://leetcode.com/problems/contains-duplicate/) | easy | 2026-10-06 | [solution](problems/easy/contains_duplicate) |
| [Linked List Cycle](https://leetcode.com/problems/linked-list-cycle/) | easy | 2026-10-06 | [solution](problems/easy/linked_list_cycle) |
| [Maximum Depth Of Binary Tree](https://leetcode.com/problems/maximum-depth-of-binary-tree/) | easy | 2026-10-06 | [solution](problems/easy/maximum_depth_of_binary_tree) |
| [Merge Sorted Array](https://leetcode.com/problems/merge-sorted-array/) | easy | 2026-10-06 | [solution](problems/easy/merge_sorted_array) |
| [Merge Two Sorted Lists](https://leetcode.com/problems/merge-two-sorted-lists/) | easy | 2026-10-06 | [solution](problems/easy/merge_two_sorted_lists) |
| [Number Of 1 Bits](https://leetcode.com/problems/number-of-1-bits/) | easy | 2026-10-06 | [solution](problems/easy/number_of_1_bits) |
| [Reverse Bits](https://leetcode.com/problems/reverse-bits/) | easy | 2026-10-06 | [solution](problems/easy/reverse_bits) |
| [Same Tree](https://leetcode.com/problems/same-tree/) | easy | 2026-10-06 | [solution](problems/easy/same_tree) |
| [Two Sum](https://leetcode.com/problems/two-sum/) | easy | 2026-10-06 | [solution](problems/easy/two_sum) |
| [Valid Palindrome](https://leetcode.com/problems/valid-palindrome/) | easy | 2026-10-06 | [solution](problems/easy/valid_palindrome) |
| [Valid Parentheses](https://leetcode.com/problems/valid-parentheses/) | easy | 2026-10-06 | [solution](problems/easy/valid_parentheses) |
| [Add Two Numbers](https://leetcode.com/problems/add-two-numbers/) | medium | 2026-10-06 | [solution](problems/medium/add_two_numbers) |
| [Combination Sum II](https://leetcode.com/problems/combination-sum-ii/) | medium | 2026-10-06 | [solution](problems/medium/combination_sum_ii) |
| [Generate Parentheses](https://leetcode.com/problems/generate-parentheses/) | medium | 2026-10-06 | [solution](problems/medium/generate_parentheses) |
| [Group Anagrams](https://leetcode.com/problems/group-anagrams/) | medium | 2026-10-06 | [solution](problems/medium/group_anagrams) |
| [Kth Largest Element In An Array](https://leetcode.com/problems/kth-largest-element-in-an-array/) | medium | 2026-10-06 | [solution](problems/medium/kth_largest_element_in_an_array) |
| [Number Of Islands](https://leetcode.com/problems/number-of-islands/) | medium | 2026-10-06 | [solution](problems/medium/number_of_islands) |
| [Product Of Array Except Self](https://leetcode.com/problems/product-of-array-except-self/) | medium | 2026-10-06 | [solution](problems/medium/product_of_array_except_self) |
| [Remove Nth Node From End Of List](https://leetcode.com/problems/remove-nth-node-from-end-of-list/) | medium | 2026-10-06 | [solution](problems/medium/remove_nth_node_from_end_of_list) |
| [Sum Of Subarray Minimums](https://leetcode.com/problems/sum-of-subarray-minimums/) | medium | 2026-10-06 | [solution](problems/medium/sum_of_subarray_minimums) |
| [Top K Frequent Elements](https://leetcode.com/problems/top-k-frequent-elements/) | medium | 2026-10-06 | [solution](problems/medium/top_k_frequent_elements) |

---

_This README and the coverage grid are regenerated automatically after every sync._
