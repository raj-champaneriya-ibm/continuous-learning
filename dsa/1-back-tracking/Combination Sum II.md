---
type: concept
status: captured
created: 2026-10-12
updated: 2026-10-12
domain: learning
tags: [dsa, backtracking, recursion, sorting, dedupe, pruning, neetcode, interview, medium]
---

# Combination Sum II

| | |
|---|---|
| Topic | [[Backtracking (Neetcode)]] |
| Difficulty | Medium |
| LeetCode | https://leetcode.com/problems/combination-sum-ii/ |
| Status in video | Not yet covered |

## Problem

You get an array `candidates` (duplicates allowed) and an integer `target`. Return every unique combination of candidates that sums to `target`, where each array element gets used at most once. No combination may appear twice.

**Example 1:**

```
Input: candidates = [10,1,2,7,6,1,5], target = 8
Output: [[1,1,6],[1,2,5],[1,7],[2,6]]
```

**Example 2:**

```
Input: candidates = [2,5,2,1,2], target = 5
Output: [[1,2,2],[5]]
```

**Constraints:**

- `1 <= candidates.length <= 100`
- `1 <= candidates[i] <= 50`
- `1 <= target <= 30`

## Greg Tang Explains

A bag of number tiles: 10, 1, 2, 7, 6, 1, 5. Make 8, each tile once.

1. Sort the tiles: 1, 1, 2, 5, 6, 7, 10. Twins now sit side by side.
2. At each step, line up the tiles you could add next. Two identical tiles in that line? Try only the first — the second would open the exact same door.
3. Go one step deeper, and the second 1 may join — it stands in a fresh line now, behind the first 1. That gives 1 + 1 + 6.
4. Tile bigger than what you still need? Every tile after it weighs more. Stop.

One rule — same line, same tile, skip — kills every repeat while keeping 1 + 1 + 6 alive.

## Visual

<svg width="640" height="320" viewBox="0 0 640 320" xmlns="http://www.w3.org/2000/svg" style="background:#fafafa">
  <g font-family="monospace" fill="#111">
    <text x="320" y="24" font-size="14" text-anchor="middle">sorted [1,1,2,5,6,7,10], target 8 · 1a, 1b = the two 1s</text>
    <line x1="320" y1="65" x2="55" y2="103" stroke="#111" stroke-width="3"/>
    <line x1="320" y1="65" x2="145" y2="103" stroke="#111" stroke-width="1.5"/>
    <line x1="320" y1="65" x2="230" y2="103" stroke="#111" stroke-width="1.5"/>
    <line x1="320" y1="65" x2="310" y2="103" stroke="#111" stroke-width="1.5"/>
    <line x1="320" y1="65" x2="390" y2="103" stroke="#111" stroke-width="1.5"/>
    <line x1="320" y1="65" x2="470" y2="103" stroke="#111" stroke-width="1.5"/>
    <line x1="320" y1="65" x2="570" y2="103" stroke="#111" stroke-width="1.5"/>
    <line x1="55" y1="129" x2="55" y2="183" stroke="#111" stroke-width="3"/>
    <line x1="55" y1="129" x2="150" y2="183" stroke="#111" stroke-width="1.5"/>
    <line x1="55" y1="129" x2="260" y2="183" stroke="#111" stroke-width="1.5"/>
    <line x1="55" y1="209" x2="55" y2="253" stroke="#111" stroke-width="3"/>
    <rect x="288" y="39" width="64" height="26" fill="none" stroke="#111" stroke-width="2"/><text x="320" y="57" font-size="13" text-anchor="middle">rem 8</text>
    <rect x="14" y="103" width="82" height="26" fill="none" stroke="#111" stroke-width="3"/><text x="55" y="121" font-size="13" text-anchor="middle">+1a → 7</text>
    <rect x="104" y="103" width="82" height="26" fill="none" stroke="#111" stroke-width="1.5" stroke-dasharray="4 3"/><text x="145" y="121" font-size="13" text-anchor="middle">1b: skip</text>
    <rect x="195" y="103" width="70" height="26" fill="none" stroke="#111" stroke-width="2"/><text x="230" y="121" font-size="13" text-anchor="middle">+2 → 6</text>
    <rect x="275" y="103" width="70" height="26" fill="none" stroke="#111" stroke-width="2"/><text x="310" y="121" font-size="13" text-anchor="middle">+5 → 3</text>
    <rect x="355" y="103" width="70" height="26" fill="none" stroke="#111" stroke-width="2"/><text x="390" y="121" font-size="13" text-anchor="middle">+6 → 2</text>
    <rect x="435" y="103" width="70" height="26" fill="none" stroke="#111" stroke-width="2"/><text x="470" y="121" font-size="13" text-anchor="middle">+7 → 1</text>
    <rect x="515" y="103" width="110" height="26" fill="none" stroke="#111" stroke-width="1.5" stroke-dasharray="4 3"/><text x="570" y="121" font-size="13" text-anchor="middle">10 > 8: break</text>
    <rect x="14" y="183" width="82" height="26" fill="none" stroke="#111" stroke-width="3"/><text x="55" y="201" font-size="13" text-anchor="middle">+1b → 6</text>
    <rect x="115" y="183" width="70" height="26" fill="none" stroke="#111" stroke-width="2"/><text x="150" y="201" font-size="13" text-anchor="middle">+2 → 5</text>
    <rect x="225" y="183" width="70" height="26" fill="#111"/><text x="260" y="201" font-size="13" text-anchor="middle" fill="#fafafa">+7 → 0</text>
    <rect x="20" y="253" width="70" height="26" fill="#111"/><text x="55" y="271" font-size="13" text-anchor="middle" fill="#fafafa">+6 → 0</text>
    <text x="205" y="201" font-size="13" text-anchor="middle" fill="#111">…</text>
    <text x="115" y="271" font-size="13" text-anchor="middle" fill="#111">…</text>
    <text x="260" y="228" font-size="12" text-anchor="middle" fill="#111">[1,7]</text>
    <text x="55" y="298" font-size="12" text-anchor="middle" fill="#111">[1,1,6]</text>
    <text x="340" y="252" font-size="12" text-anchor="start" fill="#111">top level: 1b skipped, 1a already</text>
    <text x="340" y="268" font-size="12" text-anchor="start" fill="#111">opened that branch (i > start)</text>
    <text x="340" y="292" font-size="12" text-anchor="start" fill="#111">under 1a: 1b allowed (i == start),</text>
    <text x="340" y="308" font-size="12" text-anchor="start" fill="#111">a new level, so [1,1,6] survives</text>
  </g>
</svg>

## E-Prime Pseudocode

```
SORT candidates ascending.
DEFINE dfs(start, remain):
  IF remain equals 0: RECORD a copy of path. RETURN.
  FOR i FROM start TO the end:
    IF i > start AND candidates[i] equals candidates[i − 1]: SKIP to the next i.
    IF candidates[i] exceeds remain: STOP the loop.
    PUSH candidates[i].
    CALL dfs(i + 1, remain − candidates[i]).   — i + 1: each tile once
    POP.
CALL dfs(0, target). RETURN result.
```

## Solutions

> [!example]- Java
> ```java
> public List<List<Integer>> combinationSum2(int[] candidates, int target) {
>     Arrays.sort(candidates);
>     List<List<Integer>> res = new ArrayList<>();
>     dfs(candidates, 0, target, new ArrayList<>(), res);
>     return res;
> }
>
> private void dfs(int[] c, int start, int remain, List<Integer> path, List<List<Integer>> res) {
>     if (remain == 0) {
>         res.add(new ArrayList<>(path));
>         return;
>     }
>     for (int i = start; i < c.length; i++) {
>         if (i > start && c[i] == c[i - 1]) continue; // same value, same level: already tried
>         if (c[i] > remain) break;                    // sorted: nothing later fits either
>         path.add(c[i]);
>         dfs(c, i + 1, remain - c[i], path, res);     // i + 1: each element once
>         path.remove(path.size() - 1);
>     }
> }
> ```
>
> **What breaks at large input**
>
> - **Input mutation:** `Arrays.sort(candidates)` reorders the caller's array.
> - **The `i > 0` bug:** write `i > 0` instead of `i > start` and the skip also fires on the first slot of a deeper level — [1,1,6] vanishes. Example 1 catches it.
> - **Without the dedupe line:** 100 ones with target 30 hold one answer (thirty 1s), yet a plain search walks C(100, 30) ≈ 2.9 × 10^25 paths to it. With the line: one path, instant.
> - **Boxing:** values ≤ 50 sit inside the `Integer` cache.
>
> **How to improve it**
>
> - **Group duplicates:** compress into (value, count) pairs and choose 0..min(count, remain / value) copies — fewer frames when repeats pile up.
> - **Suffix-sum prune:** if every remaining candidate together can't reach `remain`, return early.
> - Count only → bounded-knapsack DP over the (value, count) groups, O(groups · target · count) — no enumeration.

> [!example]- Python
> ```python
> def combinationSum2(self, candidates: List[int], target: int) -> List[List[int]]:
>     candidates.sort()
>     res, path = [], []
>
>     def dfs(start, remain):
>         if remain == 0:
>             res.append(path.copy())
>             return
>         for i in range(start, len(candidates)):
>             if i > start and candidates[i] == candidates[i - 1]:
>                 continue                        # same value, same level: already tried
>             if candidates[i] > remain:
>                 break                           # sorted: nothing later fits either
>             path.append(candidates[i])
>             dfs(i + 1, remain - candidates[i])  # i + 1: each element once
>             path.pop()
>
>     dfs(0, target)
>     return res
> ```
>
> **What breaks at large input**
>
> - **Input mutation:** `candidates.sort()` sorts in place.
> - **The `i > 0` bug** and the **C(100, 30) blow-up without dedupe** apply exactly as in Java.
> - **Recursion depth:** ≤ target ≤ 30 frames.
>
> **How to improve it**
>
> - `candidates = sorted(candidates)` keeps the caller's list intact.
> - `collections.Counter` grouping → choose 0..count copies per value.
> - Suffix-sum prune; DP for counts.

> [!example]- C#
> ```csharp
> public IList<IList<int>> CombinationSum2(int[] candidates, int target) {
>     Array.Sort(candidates);
>     var res = new List<IList<int>>();
>     var path = new List<int>();
>     void Dfs(int start, int remain) {
>         if (remain == 0) {
>             res.Add(new List<int>(path));
>             return;
>         }
>         for (int i = start; i < candidates.Length; i++) {
>             if (i > start && candidates[i] == candidates[i - 1]) continue; // same level, same value
>             if (candidates[i] > remain) break;   // sorted: nothing later fits either
>             path.Add(candidates[i]);
>             Dfs(i + 1, remain - candidates[i]);  // i + 1: each element once
>             path.RemoveAt(path.Count - 1);
>         }
>     }
>     Dfs(0, target);
>     return res;
> }
> ```
>
> **What breaks at large input**
>
> - **Input mutation:** `Array.Sort(candidates)` reorders the caller's array.
> - **The `i > 0` bug** and the **C(100, 30) blow-up** apply here too.
> - **No boxing; struct closure;** depth ≤ 30.
>
> **How to improve it**
>
> - Clone before sorting; group runs into (value, count).
> - Suffix-sum prune: precompute `suffix[i]` = sum of `candidates[i..]`.
> - Count only → bounded-knapsack DP.

## Why This Data Structure

- **Sorted array does double duty:** equal values sit next to each other (dedupe with one comparison), and the first too-big value ends the loop (`break`).
- **`i > start` compares siblings only** — values tried at the same depth. Parent and child may share a value; siblings may not.
- **`i + 1` on recursion:** each array position gets used at most once — contrast [[Combination Sum]], which recurses with `i`.

## Complexity

| Time | Space |
|---|---|
| O(n · 2^n) | O(n) extra, output excluded |

- **Brute force:** all 2^n subsets, check each sum, dedupe through a set → O(n · 2^n) plus the set's memory.
- **Backtracking:** each element in or out → ≤ 2^n leaves, copy ≤ n each. Sorting adds O(n log n).
- **In practice:** target ≤ 30 caps the depth at 30, and break + dedupe prune most of the tree.
- **Space:** depth ≤ min(n, target) → O(n).

## Pattern Takeaway

- **Core trick — sibling dedupe:** `i > start && a[i] == a[i − 1] → continue`. The same value may stack down a path, never across siblings.
- **Two knobs vs [[Combination Sum]]:** `i + 1` instead of `i` (no reuse) and the dedupe line (repeated input values).
- **The same line returns** in [[3Sum]], [[Subsets II]] (loop form), and Permutations II.

## Related

- [[Backtracking (Neetcode)]]
- [[Backtracking Template]]
- [[Combination Sum]] — reuse allowed, no duplicates in input
- [[Subsets II]] — same dedupe idea, take/skip form
- [[3Sum]] — same "skip equal neighbours after sorting"
