---
type: concept
status: captured
created: 2026-10-12
updated: 2026-10-12
domain: learning
tags: [dsa, backtracking, recursion, neetcode, interview, medium]
---

# Permutations

| | |
|---|---|
| Topic | [[Backtracking (Neetcode)]] |
| Difficulty | Medium |
| LeetCode | https://leetcode.com/problems/permutations/ |
| Status in video | Not yet covered |

## Problem

You get an array `nums` of distinct integers. Return every possible ordering of it (every permutation), in any order.

**Example 1:**

```
Input: nums = [1,2,3]
Output: [[1,2,3],[1,3,2],[2,1,3],[2,3,1],[3,1,2],[3,2,1]]
```

**Example 2:**

```
Input: nums = [0,1]
Output: [[0,1],[1,0]]
```

**Example 3:**

```
Input: nums = [1]
Output: [[1]]
```

**Constraints:**

- `1 <= nums.length <= 6`
- `-10 <= nums[i] <= 10`
- All values in `nums` differ.

## Greg Tang Explains

Three kids, three chairs. How many ways to seat them?

1. Chair 1: any of the 3 kids sits.
2. Chair 2: any of the 2 still standing.
3. Chair 3: the last kid — no choice left.
4. Before the next kid tries a chair, the current sitter stands back up.

3 × 2 × 1 = 6 seatings. A sticker on each seated kid — the `used[]` array — stops anyone from sitting twice.

## Visual

<svg width="600" height="290" viewBox="0 0 600 290" xmlns="http://www.w3.org/2000/svg" style="background:#fafafa">
  <g font-family="monospace" fill="#111">
    <text x="300" y="24" font-size="14" text-anchor="middle">nums = [1,2,3] · each level picks any number not yet used</text>
    <line x1="300" y1="69" x2="100" y2="103" stroke="#111" stroke-width="1.5"/>
    <line x1="300" y1="69" x2="300" y2="103" stroke="#111" stroke-width="3"/>
    <line x1="300" y1="69" x2="500" y2="103" stroke="#111" stroke-width="1.5"/>
    <line x1="100" y1="129" x2="50" y2="163" stroke="#111" stroke-width="1.5"/>
    <line x1="100" y1="129" x2="150" y2="163" stroke="#111" stroke-width="1.5"/>
    <line x1="300" y1="129" x2="250" y2="163" stroke="#111" stroke-width="1.5"/>
    <line x1="300" y1="129" x2="350" y2="163" stroke="#111" stroke-width="3"/>
    <line x1="500" y1="129" x2="450" y2="163" stroke="#111" stroke-width="1.5"/>
    <line x1="500" y1="129" x2="550" y2="163" stroke="#111" stroke-width="1.5"/>
    <line x1="50" y1="189" x2="50" y2="223" stroke="#111" stroke-width="1.5"/>
    <line x1="150" y1="189" x2="150" y2="223" stroke="#111" stroke-width="1.5"/>
    <line x1="250" y1="189" x2="250" y2="223" stroke="#111" stroke-width="1.5"/>
    <line x1="350" y1="189" x2="350" y2="223" stroke="#111" stroke-width="3"/>
    <line x1="450" y1="189" x2="450" y2="223" stroke="#111" stroke-width="1.5"/>
    <line x1="550" y1="189" x2="550" y2="223" stroke="#111" stroke-width="1.5"/>
    <rect x="275" y="43" width="50" height="26" fill="none" stroke="#111" stroke-width="2"/><text x="300" y="61" font-size="13" text-anchor="middle">[]</text>
    <rect x="72" y="103" width="56" height="26" fill="none" stroke="#111" stroke-width="2"/><text x="100" y="121" font-size="13" text-anchor="middle">[1]</text>
    <rect x="272" y="103" width="56" height="26" fill="none" stroke="#111" stroke-width="3"/><text x="300" y="121" font-size="13" text-anchor="middle">[2]</text>
    <rect x="472" y="103" width="56" height="26" fill="none" stroke="#111" stroke-width="2"/><text x="500" y="121" font-size="13" text-anchor="middle">[3]</text>
    <rect x="19" y="163" width="62" height="26" fill="none" stroke="#111" stroke-width="2"/><text x="50" y="181" font-size="13" text-anchor="middle">[1,2]</text>
    <rect x="15" y="223" width="70" height="26" fill="#111"/><text x="50" y="241" font-size="13" text-anchor="middle" fill="#fafafa">[1,2,3]</text>
    <rect x="119" y="163" width="62" height="26" fill="none" stroke="#111" stroke-width="2"/><text x="150" y="181" font-size="13" text-anchor="middle">[1,3]</text>
    <rect x="115" y="223" width="70" height="26" fill="#111"/><text x="150" y="241" font-size="13" text-anchor="middle" fill="#fafafa">[1,3,2]</text>
    <rect x="219" y="163" width="62" height="26" fill="none" stroke="#111" stroke-width="2"/><text x="250" y="181" font-size="13" text-anchor="middle">[2,1]</text>
    <rect x="215" y="223" width="70" height="26" fill="#111"/><text x="250" y="241" font-size="13" text-anchor="middle" fill="#fafafa">[2,1,3]</text>
    <rect x="319" y="163" width="62" height="26" fill="none" stroke="#111" stroke-width="3"/><text x="350" y="181" font-size="13" text-anchor="middle">[2,3]</text>
    <rect x="315" y="223" width="70" height="26" fill="#111"/><text x="350" y="241" font-size="13" text-anchor="middle" fill="#fafafa">[2,3,1]</text>
    <rect x="419" y="163" width="62" height="26" fill="none" stroke="#111" stroke-width="2"/><text x="450" y="181" font-size="13" text-anchor="middle">[3,1]</text>
    <rect x="415" y="223" width="70" height="26" fill="#111"/><text x="450" y="241" font-size="13" text-anchor="middle" fill="#fafafa">[3,1,2]</text>
    <rect x="519" y="163" width="62" height="26" fill="none" stroke="#111" stroke-width="2"/><text x="550" y="181" font-size="13" text-anchor="middle">[3,2]</text>
    <rect x="515" y="223" width="70" height="26" fill="#111"/><text x="550" y="241" font-size="13" text-anchor="middle" fill="#fafafa">[3,2,1]</text>
    <text x="300" y="276" font-size="12" text-anchor="middle" fill="#111">bold path: at [2,3], used = [F,T,T] → only 1 left · 3 × 2 × 1 = 6 leaves</text>
  </g>
</svg>

## E-Prime Pseudocode

```
CREATE an empty path, an empty result, and used[] filled with false.
DEFINE dfs():
  IF path holds all n numbers: RECORD a copy. RETURN.
  FOR i FROM 0 TO n − 1:
    IF used[i]: SKIP to the next i.
    MARK used[i]. PUSH nums[i].
    CALL dfs().
    POP. UNMARK used[i].
CALL dfs(). RETURN result.
```

## Solutions

> [!example]- Java
> ```java
> public List<List<Integer>> permute(int[] nums) {
>     List<List<Integer>> res = new ArrayList<>();
>     dfs(nums, new boolean[nums.length], new ArrayList<>(), res);
>     return res;
> }
>
> private void dfs(int[] nums, boolean[] used, List<Integer> path, List<List<Integer>> res) {
>     if (path.size() == nums.length) {
>         res.add(new ArrayList<>(path));
>         return;
>     }
>     for (int i = 0; i < nums.length; i++) {
>         if (used[i]) continue;
>         used[i] = true;
>         path.add(nums[i]);
>         dfs(nums, used, path, res);
>         path.remove(path.size() - 1);
>         used[i] = false;
>     }
> }
> ```
>
> **What breaks at large input**
>
> - **Output size:** n! outruns 2^n fast. n = 10 → 3,628,800 lists (~36 million stored numbers); n = 12 → ~479 million lists — heap gone.
> - **Snapshot copy:** O(n) per leaf — the same size as the output itself.
> - **Boxing:** −10..10 stays inside the `Integer` cache.
> - **Recursion depth:** n + 1 ≤ 7 frames.
>
> **How to improve it**
>
> - **Swap in place:** permute `nums` itself — swap `nums[start]` with each `nums[i]`, recurse on `start + 1`, swap back. No `used[]`, no path list; snapshot by copying `nums`.
> - **Next permutation:** build each ordering from the previous one in amortized O(1) — no recursion, lexicographic order for free.
> - Pre-size `res` with n! (720 at most here).
> - Need only the k-th ordering? The factorial number system finds it in O(n²) without listing the rest (LeetCode 60, Permutation Sequence).

> [!example]- Python
> ```python
> def permute(self, nums: List[int]) -> List[List[int]]:
>     res, path = [], []
>     used = [False] * len(nums)
>
>     def dfs():
>         if len(path) == len(nums):
>             res.append(path.copy())
>             return
>         for i in range(len(nums)):
>             if used[i]:
>                 continue
>             used[i] = True
>             path.append(nums[i])
>             dfs()
>             path.pop()
>             used[i] = False
>
>     dfs()
>     return res
> ```
>
> **What breaks at large input**
>
> - **Output size:** n! lists of ~56 + 8n bytes each. n = 9 → 362,880 lists, about a second to build in CPython.
> - **Loop cost:** every node scans all n slots of `used`, so ~e · n! nodes × n checks of interpreted code.
> - **Recursion depth:** 7 frames at most — far below the 1,000 limit.
>
> **How to improve it**
>
> - `itertools.permutations(nums)` runs in C; wrap with `[list(p) for p in ...]` if lists (not tuples) needed.
> - Turn `dfs` into a generator when the caller only iterates — memory drops to O(n).
> - Swap-in-place variant, as in Java.

> [!example]- C#
> ```csharp
> public IList<IList<int>> Permute(int[] nums) {
>     var res = new List<IList<int>>();
>     var path = new List<int>();
>     var used = new bool[nums.Length];
>     void Dfs() {
>         if (path.Count == nums.Length) {
>             res.Add(new List<int>(path));
>             return;
>         }
>         for (int i = 0; i < nums.Length; i++) {
>             if (used[i]) continue;
>             used[i] = true;
>             path.Add(nums[i]);
>             Dfs();
>             path.RemoveAt(path.Count - 1);
>             used[i] = false;
>         }
>     }
>     Dfs();
>     return res;
> }
> ```
>
> **What breaks at large input**
>
> - **Output size:** n! — the only real wall. `List<int>` avoids boxing.
> - **Closure:** `Dfs` captures `res`, `path`, `used`, `nums` through a struct passed by reference — no closure allocation.
> - **Recursion depth:** 7 frames.
>
> **How to improve it**
>
> - Swap in place and record `(int[])nums.Clone()` — arrays implement `IList<int>`, no `List` wrapper per answer.
> - Iterative next-permutation loop.
> - Pre-size `res` with n!.

## Why This Data Structure

- **`bool[] used` indexed by position:** O(1) check, n bytes total. Two Sum had to reject the array-index trick because values spanned ±10^9; here the index runs only 0..n−1, so the array wins.
- A `HashSet` would also answer "already used?" in O(1) but hashes on every check; scanning the path instead costs O(n) per check.
- **Loop from 0, not from `start`:** order matters, so every unused number deserves a turn at every position.

## Complexity

| Time | Space |
|---|---|
| O(n · n!) | O(n) extra, output excluded |

- **Brute force:** generate all n^n sequences with repeats and throw out invalid ones → 6^6 = 46,656 sequences vs 720 permutations at n = 6.
- **Tree:** level k holds n!/(n−k)! nodes, ~e · n! in total; each scans n slots → O(n · n!). Each of the n! leaves copies n numbers — also O(n · n!).
- **Space:** `used[]`, path, and call stack, each O(n).

## Pattern Takeaway

- **Core trick — `used[]` instead of `start`:** order matters → every position may take any unused element.
- **The knob:** start index → combinations (order ignored); `used[]` → permutations (order counts).
- **Undo both:** pop the path *and* clear the flag. Forget the flag and later branches silently lose numbers.
- **Duplicates in input** (LeetCode 47, Permutations II): sort, then skip `nums[i]` when it equals `nums[i − 1]` and `used[i − 1]` reads false.

## Related

- [[Backtracking (Neetcode)]]
- [[Backtracking Template]]
- [[Subsets]] — same push/pop; start index instead of `used[]`
- [[N-Queens]] — a permutation of columns, filtered by diagonal checks
