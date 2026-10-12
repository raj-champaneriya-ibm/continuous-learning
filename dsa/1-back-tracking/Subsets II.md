---
type: concept
status: captured
created: 2026-10-12
updated: 2026-10-12
domain: learning
tags: [dsa, backtracking, recursion, sorting, dedupe, neetcode, interview, medium]
---

# Subsets II

| | |
|---|---|
| Topic | [[Backtracking (Neetcode)]] |
| Difficulty | Medium |
| LeetCode | https://leetcode.com/problems/subsets-ii/ |
| Status in video | Not yet covered |

## Problem

You get an integer array `nums` that may contain duplicates. Return every possible subset. The answer must not hold the same subset twice; any order works.

**Example 1:**

```
Input: nums = [1,2,2]
Output: [[],[1],[1,2],[1,2,2],[2],[2,2]]
```

**Example 2:**

```
Input: nums = [0]
Output: [[],[0]]
```

**Constraints:**

- `1 <= nums.length <= 10`
- `-10 <= nums[i] <= 10`

## Greg Tang Explains

A fruit bowl: one apple, two identical bananas. How many different snacks?

1. Line the fruit up so the bananas stand together: apple, banana, banana.
2. Apple: in or out — same as [[Subsets]].
3. Bananas: take one, then decide on the next.
4. Say no to a banana? Then say no to every banana left. "Skip banana #1, take banana #2" makes the same snack as "take #1, skip #2" — a twin.

Group the twins, and one "no" covers the whole group. 6 snacks, zero repeats.

## Visual

<svg width="620" height="290" viewBox="0 0 620 290" xmlns="http://www.w3.org/2000/svg" style="background:#fafafa">
  <g font-family="monospace" fill="#111">
    <text x="310" y="24" font-size="14" text-anchor="middle">nums = [1,2,2] (sorted) · skipping one 2 skips every 2</text>
    <line x1="310" y1="69" x2="160" y2="103" stroke="#111" stroke-width="1.5"/>
    <line x1="310" y1="69" x2="460" y2="103" stroke="#111" stroke-width="1.5"/>
    <line x1="160" y1="129" x2="90" y2="163" stroke="#111" stroke-width="1.5"/>
    <line x1="160" y1="129" x2="230" y2="163" stroke="#111" stroke-width="1.5" stroke-dasharray="4 3"/>
    <line x1="460" y1="129" x2="390" y2="163" stroke="#111" stroke-width="1.5"/>
    <line x1="460" y1="129" x2="530" y2="163" stroke="#111" stroke-width="1.5" stroke-dasharray="4 3"/>
    <line x1="90" y1="189" x2="40" y2="223" stroke="#111" stroke-width="1.5"/>
    <line x1="90" y1="189" x2="140" y2="223" stroke="#111" stroke-width="1.5"/>
    <line x1="390" y1="189" x2="340" y2="223" stroke="#111" stroke-width="1.5"/>
    <line x1="390" y1="189" x2="440" y2="223" stroke="#111" stroke-width="1.5"/>
    <rect x="285" y="43" width="50" height="26" fill="none" stroke="#111" stroke-width="2"/><text x="310" y="61" font-size="13" text-anchor="middle">[]</text>
    <rect x="132" y="103" width="56" height="26" fill="none" stroke="#111" stroke-width="2"/><text x="160" y="121" font-size="13" text-anchor="middle">[1]</text>
    <rect x="432" y="103" width="56" height="26" fill="none" stroke="#111" stroke-width="2"/><text x="460" y="121" font-size="13" text-anchor="middle">[]</text>
    <rect x="59" y="163" width="62" height="26" fill="none" stroke="#111" stroke-width="2"/><text x="90" y="181" font-size="13" text-anchor="middle">[1,2]</text>
    <rect x="199" y="163" width="62" height="26" fill="#111"/><text x="230" y="181" font-size="13" text-anchor="middle" fill="#fafafa">[1]</text>
    <rect x="359" y="163" width="62" height="26" fill="none" stroke="#111" stroke-width="2"/><text x="390" y="181" font-size="13" text-anchor="middle">[2]</text>
    <rect x="499" y="163" width="62" height="26" fill="#111"/><text x="530" y="181" font-size="13" text-anchor="middle" fill="#fafafa">[]</text>
    <rect x="5" y="223" width="70" height="26" fill="#111"/><text x="40" y="241" font-size="13" text-anchor="middle" fill="#fafafa">[1,2,2]</text>
    <rect x="109" y="223" width="62" height="26" fill="#111"/><text x="140" y="241" font-size="13" text-anchor="middle" fill="#fafafa">[1,2]</text>
    <rect x="309" y="223" width="62" height="26" fill="#111"/><text x="340" y="241" font-size="13" text-anchor="middle" fill="#fafafa">[2,2]</text>
    <rect x="409" y="223" width="62" height="26" fill="#111"/><text x="440" y="241" font-size="13" text-anchor="middle" fill="#fafafa">[2]</text>
    <text x="310" y="276" font-size="12" text-anchor="middle" fill="#111">6 leaves, no repeats · plain Subsets would print [1,2] and [2] twice</text>
    <text x="235" y="90" font-size="11" text-anchor="middle" stroke="#fafafa" stroke-width="5" paint-order="stroke">take 1</text>
    <text x="385" y="90" font-size="11" text-anchor="middle" stroke="#fafafa" stroke-width="5" paint-order="stroke">skip 1</text>
    <text x="125" y="150" font-size="11" text-anchor="middle" stroke="#fafafa" stroke-width="5" paint-order="stroke">take 2</text>
    <text x="195" y="150" font-size="11" text-anchor="middle" stroke="#fafafa" stroke-width="5" paint-order="stroke">skip all 2s</text>
    <text x="425" y="150" font-size="11" text-anchor="middle" stroke="#fafafa" stroke-width="5" paint-order="stroke">take 2</text>
    <text x="495" y="150" font-size="11" text-anchor="middle" stroke="#fafafa" stroke-width="5" paint-order="stroke">skip all 2s</text>
  </g>
</svg>

## E-Prime Pseudocode

```
SORT nums so equal values sit side by side.
DEFINE dfs(i):
  IF i reaches the end: RECORD a copy of path. RETURN.
  PUSH nums[i]. CALL dfs(i + 1). POP.             — take nums[i]
  WHILE the next value equals nums[i]: ADVANCE i.  — skip the whole run
  CALL dfs(i + 1).                                 — the skip branch
CALL dfs(0). RETURN result.
```

## Solutions

> [!example]- Java
> ```java
> public List<List<Integer>> subsetsWithDup(int[] nums) {
>     Arrays.sort(nums);                  // duplicates now sit side by side
>     List<List<Integer>> res = new ArrayList<>();
>     dfs(nums, 0, new ArrayList<>(), res);
>     return res;
> }
>
> private void dfs(int[] nums, int i, List<Integer> path, List<List<Integer>> res) {
>     if (i == nums.length) {
>         res.add(new ArrayList<>(path));
>         return;
>     }
>     path.add(nums[i]);                  // take nums[i]
>     dfs(nums, i + 1, path, res);
>     path.remove(path.size() - 1);
>     int j = i;
>     while (j + 1 < nums.length && nums[j] == nums[j + 1]) j++; // skip the whole run
>     dfs(nums, j + 1, path, res);
> }
> ```
>
> **What breaks at large input**
>
> - **Input mutation:** `Arrays.sort(nums)` reorders the caller's array.
> - **Output size:** at most 2^n; duplicates shrink it — all-equal input gives only n + 1 subsets.
> - **Naive dedupe trap:** build all 2^n subsets, then drop twins with a `HashSet<List<Integer>>`. It works (Java lists compare by content) but hashes every list in O(n) and still builds every twin first.
> - **Boxing:** −10..10 sits inside the `Integer` cache.
>
> **How to improve it**
>
> - **Count-based tree:** compress into (value, count) pairs and choose 0..count copies of each value — branch factor count + 1, no skip loop.
> - **Iterative:** grow subsets value by value; when a value repeats the previous one, extend only the subsets created in the previous round.
> - Pre-size `res` with `1 << nums.length` as an upper bound.

> [!example]- Python
> ```python
> def subsetsWithDup(self, nums: List[int]) -> List[List[int]]:
>     nums.sort()                      # duplicates now sit side by side
>     res, path = [], []
>
>     def dfs(i):
>         if i == len(nums):
>             res.append(path.copy())
>             return
>         path.append(nums[i])         # take nums[i]
>         dfs(i + 1)
>         path.pop()
>         while i + 1 < len(nums) and nums[i] == nums[i + 1]:
>             i += 1                   # skipping one copy means skipping them all
>         dfs(i + 1)
>
>     dfs(0)
>     return res
> ```
>
> **What breaks at large input**
>
> - **Input mutation:** `nums.sort()` sorts the caller's list in place.
> - **Naive dedupe trap:** lists can't go into a `set`; the usual workaround `set(tuple(sorted(s)) ...)` sorts and hashes every subset — extra O(n log n) each, plus all the wasted twins.
> - **Recursion depth:** n + 1 ≤ 11.
>
> **How to improve it**
>
> - `collections.Counter(nums)` → for each value, choose 0..count copies.
> - `nums = sorted(nums)` to leave the input alone.
> - Generator version when the caller only iterates.

> [!example]- C#
> ```csharp
> public IList<IList<int>> SubsetsWithDup(int[] nums) {
>     Array.Sort(nums);                     // duplicates now sit side by side
>     var res = new List<IList<int>>();
>     var path = new List<int>();
>     void Dfs(int i) {
>         if (i == nums.Length) {
>             res.Add(new List<int>(path));
>             return;
>         }
>         path.Add(nums[i]);                // take nums[i]
>         Dfs(i + 1);
>         path.RemoveAt(path.Count - 1);
>         int j = i;
>         while (j + 1 < nums.Length && nums[j] == nums[j + 1]) j++; // skip the whole run
>         Dfs(j + 1);
>     }
>     Dfs(0);
>     return res;
> }
> ```
>
> **What breaks at large input**
>
> - **Input mutation:** `Array.Sort(nums)` reorders the caller's array.
> - **Naive dedupe trap:** a `HashSet<List<int>>` keeps every twin — `List<int>` compares by reference, not content. It needs a custom `IEqualityComparer`.
> - **Closure:** struct capture, no allocation; depth n + 1.
>
> **How to improve it**
>
> - Count runs after sorting and choose 0..count copies per value.
> - Iterative "extend only last round's subsets" loop.
> - Pre-size `res` with `1 << nums.Length`.

## Why This Data Structure

- **Sorted array:** equal values form runs, so one comparison `nums[j] == nums[j + 1]` walks the whole run — no hash set needed.
- Sorting costs O(n log n), noise beside O(n · 2^n).
- **Why the skip-run rule works:** copies of a value always get taken from the left — 0 copies, the first copy, the first two copies, and so on. Each multiset gets built exactly one way.

## Complexity

| Time | Space |
|---|---|
| O(n · 2^n) | O(n) extra, output excluded |

- **Brute force:** plain Subsets over 2^n index sets, then dedupe through a set → same O(n · 2^n) time plus O(n · 2^n) memory for the set and all the wasted twins.
- **Skip-run:** never creates a twin, so every leaf yields a new answer.
- **Sort:** O(n log n).
- **Space:** path and call stack, O(n).

## Pattern Takeaway

- **Core trick — skip the whole run:** after sorting, "skip this value" means "skip every copy of it". Duplicates die at the source.
- **Same rule, loop form:** `if (i > start && a[i] == a[i − 1]) continue;` — [[Combination Sum II]] and [[3Sum]] use exactly that line.
- **Sort first** whenever duplicate values threaten duplicate answers.

## Related

- [[Backtracking (Neetcode)]]
- [[Backtracking Template]]
- [[Subsets]] — same tree without duplicates
- [[Combination Sum II]] — the same dedupe in loop form
- [[3Sum]] — "skip equal neighbours after sorting", outside recursion
