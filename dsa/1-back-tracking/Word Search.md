---
type: concept
status: captured
created: 2026-10-12
updated: 2026-10-12
domain: learning
tags: [dsa, backtracking, recursion, grid, dfs, neetcode, interview, medium]
---

# Word Search

| | |
|---|---|
| Topic | [[Backtracking (Neetcode)]] |
| Difficulty | Medium |
| LeetCode | https://leetcode.com/problems/word-search/ |
| Status in video | Not yet covered |

## Problem

You get an m × n grid of letters `board` and a string `word`. Return true when some path of horizontally or vertically neighbouring cells spells `word`, with no cell used twice in that path. Otherwise return false.

**Example 1:**

```
Input: board = [["A","B","C","E"],["S","F","C","S"],["A","D","E","E"]], word = "ABCCED"
Output: true
```

**Example 2:**

```
Input: board = (same), word = "SEE"
Output: true
```

**Example 3:**

```
Input: board = (same), word = "ABCB"
Output: false
Explanation: the path would need the B cell twice.
```

**Constraints:**

- `m == board.length`, `n == board[i].length`
- `1 <= m, n <= 6`
- `1 <= word.length <= 15`
- `board` and `word` hold only upper- and lowercase English letters.
- Follow-up: can search pruning speed this up on a larger board?

## Greg Tang Explains

Find "ABCCED" in a letter grid? Treat it as a hike from tile to tile.

1. Stand on every A in turn. Each A starts a hike.
2. From each tile, look up, down, left, right for the next letter. Wrong letter? Don't step.
3. Drop a pebble (#) on each tile you stand on, so you never loop back onto your own trail.
4. Dead end? Step back one tile and pick the pebble up — another hike might need that tile.

Pebbles down on the way in, pebbles up on the way out. One grid, no extra visited map.

## Visual

<svg width="560" height="250" viewBox="0 0 560 250" xmlns="http://www.w3.org/2000/svg" style="background:#fafafa">
  <defs><marker id="ah-ws" viewBox="0 0 8 8" refX="7" refY="4" markerUnits="userSpaceOnUse" markerWidth="9" markerHeight="9" orient="auto"><path d="M0,0 L8,4 L0,8 z" fill="#111"/></marker></defs>
  <g font-family="monospace" fill="#111">
    <text x="280" y="24" font-size="14" text-anchor="middle">word = ABCCED · mark a cell on enter, restore it on exit</text>
    <rect x="30" y="50" width="52" height="52" fill="#d9d9d9" stroke="#111" stroke-width="2"/>
    <text x="56" y="83" font-size="20" text-anchor="middle" fill="#111">A</text>
    <text x="35" y="63" font-size="10" text-anchor="start" fill="#111">1</text>
    <rect x="82" y="50" width="52" height="52" fill="#d9d9d9" stroke="#111" stroke-width="2"/>
    <text x="108" y="83" font-size="20" text-anchor="middle" fill="#111">B</text>
    <text x="87" y="63" font-size="10" text-anchor="start" fill="#111">2</text>
    <rect x="134" y="50" width="52" height="52" fill="#d9d9d9" stroke="#111" stroke-width="2"/>
    <text x="160" y="83" font-size="20" text-anchor="middle" fill="#111">C</text>
    <text x="139" y="63" font-size="10" text-anchor="start" fill="#111">3</text>
    <rect x="186" y="50" width="52" height="52" fill="none" stroke="#111" stroke-width="2"/>
    <text x="212" y="83" font-size="20" text-anchor="middle" fill="#111">E</text>
    <rect x="30" y="102" width="52" height="52" fill="none" stroke="#111" stroke-width="2"/>
    <text x="56" y="135" font-size="20" text-anchor="middle" fill="#111">S</text>
    <rect x="82" y="102" width="52" height="52" fill="none" stroke="#111" stroke-width="2"/>
    <text x="108" y="135" font-size="20" text-anchor="middle" fill="#111">F</text>
    <rect x="134" y="102" width="52" height="52" fill="#d9d9d9" stroke="#111" stroke-width="2"/>
    <text x="160" y="135" font-size="20" text-anchor="middle" fill="#111">C</text>
    <text x="139" y="115" font-size="10" text-anchor="start" fill="#111">4</text>
    <rect x="186" y="102" width="52" height="52" fill="none" stroke="#111" stroke-width="2"/>
    <text x="212" y="135" font-size="20" text-anchor="middle" fill="#111">S</text>
    <rect x="30" y="154" width="52" height="52" fill="none" stroke="#111" stroke-width="2"/>
    <text x="56" y="187" font-size="20" text-anchor="middle" fill="#111">A</text>
    <rect x="82" y="154" width="52" height="52" fill="#d9d9d9" stroke="#111" stroke-width="2"/>
    <text x="108" y="187" font-size="20" text-anchor="middle" fill="#111">D</text>
    <text x="87" y="167" font-size="10" text-anchor="start" fill="#111">6</text>
    <rect x="134" y="154" width="52" height="52" fill="#d9d9d9" stroke="#111" stroke-width="2"/>
    <text x="160" y="187" font-size="20" text-anchor="middle" fill="#111">E</text>
    <text x="139" y="167" font-size="10" text-anchor="start" fill="#111">5</text>
    <rect x="186" y="154" width="52" height="52" fill="none" stroke="#111" stroke-width="2"/>
    <text x="212" y="187" font-size="20" text-anchor="middle" fill="#111">E</text>
    <line x1="70" y1="76" x2="91" y2="76" stroke="#111" stroke-width="2" marker-end="url(#ah-ws)"/>
    <line x1="122" y1="76" x2="143" y2="76" stroke="#111" stroke-width="2" marker-end="url(#ah-ws)"/>
    <line x1="160" y1="91" x2="160" y2="109" stroke="#111" stroke-width="2" marker-end="url(#ah-ws)"/>
    <line x1="160" y1="143" x2="160" y2="161" stroke="#111" stroke-width="2" marker-end="url(#ah-ws)"/>
    <line x1="146" y1="180" x2="125" y2="180" stroke="#111" stroke-width="2" marker-end="url(#ah-ws)"/>
    <text x="134" y="228" font-size="12" text-anchor="middle" fill="#111">path of 6 cells, each used once</text>
    <text x="380" y="52" font-size="12" text-anchor="middle" fill="#111">board inside step 4</text>
    <rect x="320" y="62" width="30" height="30" fill="#111" stroke="#111" stroke-width="1.5"/>
    <text x="335" y="82" font-size="14" text-anchor="middle" fill="#fafafa">#</text>
    <rect x="350" y="62" width="30" height="30" fill="#111" stroke="#111" stroke-width="1.5"/>
    <text x="365" y="82" font-size="14" text-anchor="middle" fill="#fafafa">#</text>
    <rect x="380" y="62" width="30" height="30" fill="#111" stroke="#111" stroke-width="1.5"/>
    <text x="395" y="82" font-size="14" text-anchor="middle" fill="#fafafa">#</text>
    <rect x="410" y="62" width="30" height="30" fill="none" stroke="#111" stroke-width="1.5"/>
    <text x="425" y="82" font-size="14" text-anchor="middle" fill="#111">E</text>
    <rect x="320" y="92" width="30" height="30" fill="none" stroke="#111" stroke-width="1.5"/>
    <text x="335" y="112" font-size="14" text-anchor="middle" fill="#111">S</text>
    <rect x="350" y="92" width="30" height="30" fill="none" stroke="#111" stroke-width="1.5"/>
    <text x="365" y="112" font-size="14" text-anchor="middle" fill="#111">F</text>
    <rect x="380" y="92" width="30" height="30" fill="#111" stroke="#111" stroke-width="1.5"/>
    <text x="395" y="112" font-size="14" text-anchor="middle" fill="#fafafa">#</text>
    <rect x="410" y="92" width="30" height="30" fill="none" stroke="#111" stroke-width="1.5"/>
    <text x="425" y="112" font-size="14" text-anchor="middle" fill="#111">S</text>
    <rect x="320" y="122" width="30" height="30" fill="none" stroke="#111" stroke-width="1.5"/>
    <text x="335" y="142" font-size="14" text-anchor="middle" fill="#111">A</text>
    <rect x="350" y="122" width="30" height="30" fill="none" stroke="#111" stroke-width="1.5"/>
    <text x="365" y="142" font-size="14" text-anchor="middle" fill="#111">D</text>
    <rect x="380" y="122" width="30" height="30" fill="none" stroke="#111" stroke-width="1.5"/>
    <text x="395" y="142" font-size="14" text-anchor="middle" fill="#111">E</text>
    <rect x="410" y="122" width="30" height="30" fill="none" stroke="#111" stroke-width="1.5"/>
    <text x="425" y="142" font-size="14" text-anchor="middle" fill="#111">E</text>
    <text x="300" y="175" font-size="12" text-anchor="start" fill="#111"># = on the current path → no reuse</text>
    <text x="300" y="193" font-size="12" text-anchor="start" fill="#111">dead end → write the letter back</text>
    <text x="300" y="211" font-size="12" text-anchor="start" fill="#111">ABCB fails: B already holds #</text>
  </g>
</svg>

## E-Prime Pseudocode

```
FOR each cell (r, c): IF dfs(r, c, 0) succeeds: RETURN true.
RETURN false.

DEFINE dfs(r, c, k):
  IF k equals the word length: RETURN true.           — every letter matched
  IF (r, c) falls outside the board OR board[r][c] differs from word[k]: RETURN false.
  SAVE board[r][c]. WRITE '#' there.                  — mark
  found ← dfs on the four neighbours with k + 1, stopping at the first success.
  RESTORE board[r][c].                                — unmark
  RETURN found.
```

## Solutions

> [!example]- Java
> ```java
> public boolean exist(char[][] board, String word) {
>     for (int r = 0; r < board.length; r++)
>         for (int c = 0; c < board[0].length; c++)
>             if (dfs(board, word, r, c, 0)) return true;
>     return false;
> }
>
> private boolean dfs(char[][] b, String word, int r, int c, int k) {
>     if (k == word.length()) return true;
>     if (r < 0 || c < 0 || r >= b.length || c >= b[0].length || b[r][c] != word.charAt(k)) return false;
>     char saved = b[r][c];
>     b[r][c] = '#';                      // mark: on the current path
>     boolean found = dfs(b, word, r + 1, c, k + 1) || dfs(b, word, r - 1, c, k + 1)
>                  || dfs(b, word, r, c + 1, k + 1) || dfs(b, word, r, c - 1, k + 1);
>     b[r][c] = saved;                    // unmark on the way back
>     return found;
> }
> ```
>
> **What breaks at large input**
>
> - **Branching:** up to 4 first moves, then 3 (the way back holds `#`) → m · n · 4 · 3^(L−1) calls in the worst case. A 6 × 6 board with L = 15 → 36 × 4 × 3^14 ≈ 6.9 × 10^8. Only adversarial boards (all A's, word AAA…AB) get near it.
> - **Board mutation:** the search writes `#` into the caller's board and restores it. An exception mid-search would leave marks behind; a concurrent reader would see them.
> - **The `#` sentinel:** safe only because the board holds letters — `#` never matches one.
> - **Recursion depth:** ≤ L + 1 = 16 frames.
>
> **How to improve it**
>
> - **Frequency prune:** count letters on the board; if `word` needs more of any letter than the board holds, return false before any DFS. Also return false when L > m · n.
> - **Reverse trick:** if the word's first letter appears more often on the board than its last, search the reversed word — fewer starting points, earlier failures. (The usual answer to the follow-up.)
> - Many words on one board? Build a trie and walk every word at once ([[Word Search II]]).

> [!example]- Python
> ```python
> def exist(self, board: List[List[str]], word: str) -> bool:
>     rows, cols = len(board), len(board[0])
>
>     def dfs(r, c, k):
>         if k == len(word):
>             return True
>         if r < 0 or c < 0 or r >= rows or c >= cols or board[r][c] != word[k]:
>             return False
>         saved = board[r][c]
>         board[r][c] = "#"                   # mark: on the current path
>         found = (dfs(r + 1, c, k + 1) or dfs(r - 1, c, k + 1) or
>                  dfs(r, c + 1, k + 1) or dfs(r, c - 1, k + 1))
>         board[r][c] = saved                 # unmark on the way back
>         return found
>
>     return any(dfs(r, c, 0) for r in range(rows) for c in range(cols))
> ```
>
> **What breaks at large input**
>
> - **Branching:** same 3^L bound; in CPython the adversarial ~10^8–10^9 calls take minutes, not seconds.
> - **Board mutation:** the caller's list of lists changes during the search.
> - **Recursion depth:** 16 frames, well under 1,000.
>
> **How to improve it**
>
> - **Frequency prune:** `Counter(word) - Counter(ch for row in board for ch in row)` non-empty → return False.
> - **Reverse trick:** `if board_count[word[0]] > board_count[word[-1]]: word = word[::-1]`.
> - Many words → trie ([[Word Search II]]).

> [!example]- C#
> ```csharp
> public bool Exist(char[][] board, string word) {
>     int rows = board.Length, cols = board[0].Length;
>     bool Dfs(int r, int c, int k) {
>         if (k == word.Length) return true;
>         if (r < 0 || c < 0 || r >= rows || c >= cols || board[r][c] != word[k]) return false;
>         char saved = board[r][c];
>         board[r][c] = '#';                // mark: on the current path
>         bool found = Dfs(r + 1, c, k + 1) || Dfs(r - 1, c, k + 1)
>                   || Dfs(r, c + 1, k + 1) || Dfs(r, c - 1, k + 1);
>         board[r][c] = saved;              // unmark on the way back
>         return found;
>     }
>     for (int r = 0; r < rows; r++)
>         for (int c = 0; c < cols; c++)
>             if (Dfs(r, c, 0)) return true;
>     return false;
> }
> ```
>
> **What breaks at large input**
>
> - **Branching:** same m · n · 3^L bound.
> - **Board mutation:** marks live in the caller's `char[][]` during the search.
> - **Closure:** `Dfs` captures `board`, `word`, `rows`, `cols` through a struct by reference — no allocation.
>
> **How to improve it**
>
> - **Frequency prune** with an `int[128]` count array — chars form a small bounded range, so a plain array index beats a dictionary.
> - **Reverse trick**, as in Java.
> - Many words → trie ([[Word Search II]]).

## Why This Data Structure

- **The board doubles as the visited set:** writing `#` in place costs O(1) time and zero extra memory.
- A separate `boolean[m][n]` works the same with O(m · n) extra; a `HashSet` of (r, c) pairs adds hashing on every step.
- **Restore on exit matters:** "visited" here means "on the current path", not "ever touched". A cell rejected by one path may sit on the winning path from another start. Permanent marks — fine for flood fill — give wrong answers here.

## Complexity

| Time | Space |
|---|---|
| O(m · n · 3^L) | O(L) |

- **Brute force:** every walk of length L from every cell, letters checked only at the end → m · n · 4^L.
- **Backtracking:** the letter check kills a branch at the first mismatch; `#` removes the way back, so branching drops to ≤ 3 after the first step.
- **Space:** recursion depth L; no visited array.
- **Bounds:** m, n ≤ 6 and L ≤ 15.

## Pattern Takeaway

- **Core trick — mark on enter, unmark on exit:** the grid cell plays the role of push and pop.
- **Path search vs region search:** here visited resets per path; in [[Number of Islands]] it stays marked forever, because islands count regions, not paths.
- **Cheap global checks first** (letter counts, length) before an exponential search.

## Related

- [[Backtracking (Neetcode)]]
- [[Backtracking Template]]
- [[Word Search II]] — many words, one trie, one walk
- [[Number of Islands]] — grid DFS with permanent marks
