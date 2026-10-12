---
type: concept
status: captured
created: 2026-10-12
updated: 2026-10-12
domain: learning
tags: [dsa, backtracking, recursion, pruning, neetcode, interview, medium]
---

# Combination Sum

| | |
|---|---|
| Topic | [[Backtracking (Neetcode)]] |
| Difficulty | Medium |
| LeetCode | https://leetcode.com/problems/combination-sum/ |
| Status in video | Not yet covered |

## Problem

You get an array `candidates` of distinct integers and an integer `target`. Return every unique combination of candidates that adds up to `target`, in any order. Any number may get picked again and again; two combinations differ only when some number appears a different count of times. The tests promise fewer than 150 combinations.

**Example 1:**

```
Input: candidates = [2,3,6,7], target = 7
Output: [[2,2,3],[7]]
Explanation: 2 + 2 + 3 = 7 (2 used twice), and 7 = 7.
```

**Example 2:**

```
Input: candidates = [2,3,5], target = 8
Output: [[2,2,2,2],[2,3,3],[3,5]]
```

**Example 3:**

```
Input: candidates = [2], target = 1
Output: []
```

**Constraints:**

- `1 <= candidates.length <= 30`
- `2 <= candidates[i] <= 40`
- All values in `candidates` differ.
- `1 <= target <= 40`

## Greg Tang Explains

Making 7 from coins 2, 3, 6, 7? Line the coins up small to big and only ever look right.

1. Grab a 2 → still need 5. Another 2 → need 3. Another 2 → need 1. Nothing fits — hand the coin back.
2. Swap that last 2 for a 3 → need 0. Bingo: 2 + 2 + 3.
3. Never reach left for a smaller coin — that would rebuild 3 + 2 + 2, the same handful in a new order.
4. Coin bigger than what you still need? Every coin to its right weighs more. Stop looking.

Same coin again — yes. Smaller coin later — never. That one rule kills every duplicate.

## Visual

<svg width="600" height="300" viewBox="0 0 600 300" xmlns="http://www.w3.org/2000/svg" style="background:#fafafa">
  <g font-family="monospace" fill="#111">
    <text x="300" y="24" font-size="14" text-anchor="middle">candidates = [2,3,6,7], target = 7 · node = what remains</text>
    <line x1="300" y1="69" x2="150" y2="107" stroke="#111" stroke-width="1.5"/>
    <line x1="300" y1="69" x2="300" y2="107" stroke="#111" stroke-width="1.5"/>
    <line x1="300" y1="69" x2="420" y2="107" stroke="#111" stroke-width="1.5"/>
    <line x1="300" y1="69" x2="530" y2="107" stroke="#111" stroke-width="1.5"/>
    <line x1="150" y1="133" x2="90" y2="171" stroke="#111" stroke-width="1.5"/>
    <line x1="150" y1="133" x2="210" y2="171" stroke="#111" stroke-width="1.5"/>
    <line x1="300" y1="133" x2="320" y2="171" stroke="#111" stroke-width="1.5"/>
    <line x1="90" y1="197" x2="50" y2="235" stroke="#111" stroke-width="1.5"/>
    <line x1="90" y1="197" x2="140" y2="235" stroke="#111" stroke-width="1.5"/>
    <rect x="268" y="43" width="64" height="26" fill="none" stroke="#111" stroke-width="2"/><text x="300" y="61" font-size="13" text-anchor="middle">rem 7</text>
    <rect x="112" y="107" width="76" height="26" fill="none" stroke="#111" stroke-width="2"/><text x="150" y="125" font-size="13" text-anchor="middle">+2 → 5</text>
    <rect x="262" y="107" width="76" height="26" fill="none" stroke="#111" stroke-width="2"/><text x="300" y="125" font-size="13" text-anchor="middle">+3 → 4</text>
    <rect x="382" y="107" width="76" height="26" fill="none" stroke="#111" stroke-width="1.5" stroke-dasharray="4 3"/><text x="420" y="125" font-size="13" text-anchor="middle">+6 → 1</text>
    <rect x="492" y="107" width="76" height="26" fill="#111"/><text x="530" y="125" font-size="13" text-anchor="middle" fill="#fafafa">+7 → 0</text>
    <rect x="52" y="171" width="76" height="26" fill="none" stroke="#111" stroke-width="2"/><text x="90" y="189" font-size="13" text-anchor="middle">+2 → 3</text>
    <rect x="172" y="171" width="76" height="26" fill="none" stroke="#111" stroke-width="1.5" stroke-dasharray="4 3"/><text x="210" y="189" font-size="13" text-anchor="middle">+3 → 2</text>
    <rect x="282" y="171" width="76" height="26" fill="none" stroke="#111" stroke-width="1.5" stroke-dasharray="4 3"/><text x="320" y="189" font-size="13" text-anchor="middle">+3 → 1</text>
    <rect x="12" y="235" width="76" height="26" fill="none" stroke="#111" stroke-width="1.5" stroke-dasharray="4 3"/><text x="50" y="253" font-size="13" text-anchor="middle">+2 → 1</text>
    <rect x="102" y="235" width="76" height="26" fill="#111"/><text x="140" y="253" font-size="13" text-anchor="middle" fill="#fafafa">+3 → 0</text>
    <text x="530" y="152" font-size="12" text-anchor="middle" fill="#111">[7]</text>
    <text x="140" y="280" font-size="12" text-anchor="middle" fill="#111">[2,2,3]</text>
    <rect x="389" y="207" width="22" height="26" fill="#111"/><text x="400" y="225" font-size="13" text-anchor="middle" fill="#fafafa"></text>
    <text x="418" y="225" font-size="12" text-anchor="start" fill="#111">remain 0 → record</text>
    <rect x="389" y="239" width="22" height="26" fill="none" stroke="#111" stroke-width="1.5" stroke-dasharray="4 3"/><text x="400" y="257" font-size="13" text-anchor="middle"></text>
    <text x="418" y="257" font-size="12" text-anchor="start" fill="#111">nothing fits → break</text>
    <text x="330" y="287" font-size="12" text-anchor="start" fill="#111">child loop starts at i: 2 repeats</text>
  </g>
</svg>

## E-Prime Pseudocode

```
SORT candidates ascending.
DEFINE dfs(start, remain):
  IF remain equals 0: RECORD a copy of path. RETURN.
  FOR i FROM start TO the end:
    IF candidates[i] exceeds remain: STOP the loop.  — sorted, so every later one exceeds it too
    PUSH candidates[i].
    CALL dfs(i, remain − candidates[i]).             — i again: reuse allowed
    POP.
CALL dfs(0, target). RETURN result.
```

## Solutions

> [!example]- Java
> ```java
> public List<List<Integer>> combinationSum(int[] candidates, int target) {
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
>         if (c[i] > remain) break;            // sorted: every later one overshoots too
>         path.add(c[i]);
>         dfs(c, i, remain - c[i], path, res); // i, not i + 1: reuse allowed
>         path.remove(path.size() - 1);
>     }
> }
> ```
>
> **What breaks at large input**
>
> - **Input mutation:** `Arrays.sort(candidates)` reorders the caller's array — fine on LeetCode, a surprise in shared code.
> - **Deep chains:** depth = target / smallest candidate. Here 40 / 2 = 20 frames. A target of 10^5 with a candidate of 1 would need 10^5 frames → `StackOverflowError`.
> - **Dead ends outnumber answers:** fewer than 150 answers, yet many more failed branches; the `break` ends each failed level after one comparison.
> - **Boxing:** candidates ≤ 40 sit inside the `Integer` cache — no allocation per push.
>
> **How to improve it**
>
> - Clone before sorting if the caller still needs the original order: `int[] c = candidates.clone();`.
> - Reachability prune: precompute `canReach[r]` (can any mix of candidates sum to r?) with a quick DP; skip a branch whose `remain` can't reach 0.
> - Need only the number of combinations? DP over `remain`: `ways[r] += ways[r − c]`, O(n · target), no enumeration ([[Coin Change II]]).
> - Inputs with deep chains: an explicit stack replaces recursion.

> [!example]- Python
> ```python
> def combinationSum(self, candidates: List[int], target: int) -> List[List[int]]:
>     candidates.sort()
>     res, path = [], []
>
>     def dfs(start, remain):
>         if remain == 0:
>             res.append(path.copy())
>             return
>         for i in range(start, len(candidates)):
>             if candidates[i] > remain:
>                 break                       # sorted: every later one overshoots too
>             path.append(candidates[i])
>             dfs(i, remain - candidates[i])  # i, not i + 1: reuse allowed
>             path.pop()
>
>     dfs(0, target)
>     return res
> ```
>
> **What breaks at large input**
>
> - **Input mutation:** `candidates.sort()` sorts the caller's list in place.
> - **Recursion limit:** default 1,000 frames; depth = target / smallest candidate. Target 5,000 with candidate 2 → 2,500 frames → `RecursionError`.
> - **Interpreter cost:** each call and loop step costs far more than in Java or C#; with < 150 answers and target ≤ 40 it stays instant.
>
> **How to improve it**
>
> - `candidates = sorted(candidates)` — a sorted copy, caller's list untouched.
> - Reachability prune with a `can_reach` DP table, as in Java.
> - Count only → `ways[r] += ways[r - c]` DP.
> - Deep inputs: raise `sys.setrecursionlimit` cautiously, or switch to an explicit stack.

> [!example]- C#
> ```csharp
> public IList<IList<int>> CombinationSum(int[] candidates, int target) {
>     Array.Sort(candidates);
>     var res = new List<IList<int>>();
>     var path = new List<int>();
>     void Dfs(int start, int remain) {
>         if (remain == 0) {
>             res.Add(new List<int>(path));
>             return;
>         }
>         for (int i = start; i < candidates.Length; i++) {
>             if (candidates[i] > remain) break; // sorted: every later one overshoots too
>             path.Add(candidates[i]);
>             Dfs(i, remain - candidates[i]);    // i, not i + 1: reuse allowed
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
> - **Deep chains:** depth 20 costs nothing on the 1 MB default stack; tens of thousands of frames risk a `StackOverflowException`, which .NET cannot catch — the process dies.
> - **Boxing:** none — `List<int>` stores ints unboxed.
>
> **How to improve it**
>
> - `var c = (int[])candidates.Clone(); Array.Sort(c);` keeps the input intact.
> - Reachability prune via a `bool[] canReach` DP.
> - Count only → `ways[r] += ways[r - c]` DP.
> - Deep inputs: explicit `Stack<T>` instead of recursion.

## Why This Data Structure

- **Sorted array:** the first candidate that overshoots ends the loop (`break`). Unsorted, the loop would need `continue` and would test every remaining candidate.
- **Start index:** each path stays non-decreasing, so [2,2,3] appears once and never as [3,2,2] or [2,3,2].
- **`i`, not `i + 1`:** the same candidate may repeat; never moving left keeps the order fixed.
- **`remain` as an integer:** subtract once per step instead of re-summing the path at every node → O(1) check.

## Complexity

| Time | Space |
|---|---|
| O(n^(T/M)) loose bound | O(T/M) |

- T = target, M = smallest candidate: depth ≤ T/M, branching ≤ n.
- **Another loose bound, O(2^T):** every node holds a distinct ordered way of writing some number ≤ T as a sum of positive parts, and at most 2^T such sums exist. Neetcode quotes this one.
- **Brute force:** try every multiset of candidates up to size T/M, check each sum, then dedupe — far more work than a pruned tree.
- **In practice:** < 150 answers and the sort + break prune keep the tree small.
- **Space:** path and call stack ≤ T/M deep.

## Pattern Takeaway

- **Core trick — start index:** loop from `start`, never from 0 → each combination appears once, in sorted order.
- **Reuse knob:** recurse with `i` to allow repeats, `i + 1` to forbid them — that one character separates this problem from [[Combination Sum II]].
- **Sorted prune:** `break` at the first too-big candidate.
- **Count instead of list?** DP, not backtracking ([[Coin Change II]]).

## Related

- [[Backtracking (Neetcode)]]
- [[Backtracking Template]]
- [[Combination Sum II]] — `i + 1` plus a dedupe line for repeated input values
- [[Coin Change II]] — counts these same combinations with DP instead of listing them
- [[Subsets]] — same push/pop; stops at the array end instead of a target
