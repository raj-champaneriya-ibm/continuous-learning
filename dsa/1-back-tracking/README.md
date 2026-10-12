# Backtracking

Topic map for the Backtracking section of the Neetcode 150 course. Notes are drafted for all nine problems.

## Covered

| # | Problem | Difficulty | Core trick |
|---|---|---|---|
| 1 | [Subsets](Subsets.md) | Medium | Include or exclude each element to enumerate every subset. |
| 2 | [Combination Sum](Combination%20Sum.md) | Medium | Reuse the current candidate; keep indices nondecreasing to avoid reordered duplicates. |
| 3 | [Permutations](Permutations.md) | Medium | Choose any unused element, then undo the choice before trying the next. |
| 4 | [Subsets II](Subsets%20II.md) | Medium | Sort first; when excluding a value, skip all its remaining duplicates. |
| 5 | [Combination Sum II](Combination%20Sum%20II.md) | Medium | Sort, skip duplicates at the same depth, and advance the index after each pick. |
| 6 | [Word Search](Word%20Search.md) | Medium | Search four neighbours; mark cells on the current path and restore them on return. |
| 7 | [Palindrome Partitioning](Palindrome%20Partitioning.md) | Medium | Try each palindromic prefix, then recursively partition the remaining suffix. |
| 8 | [Letter Combinations of a Phone Number](Letter%20Combinations%20of%20a%20Phone%20Number.md) | Medium | Choose one mapped letter per digit; each recursion level handles the next digit. |
| 9 | [N-Queens](N-Queens.md) | Hard | Place one queen per row; track occupied columns and diagonals (`r - c`, `r + c`). |

## Source

- Video: Neetcode 150 Course — All Coding Interview Questions Solved — https://youtu.be/T0u5nwSA0w0
- https://www.freecodecamp.org/news/leetcode-dsa-concepts-handbook/?utm_source=chatgpt.com#heading-chapter-nine-backtracking
