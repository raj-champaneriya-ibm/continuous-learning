---
type: concept
status: captured
created: 2026-10-12
updated: 2026-10-12
domain: learning
tags: [dsa, backtracking, recursion, neetcode, interview, medium]
---

# Subsets

| Topic      | [[Backtracking (Neetcode)]]            |
| ---------- | -------------------------------------- |
| Difficulty | Medium                                 |
| LeetCode   | https://leetcode.com/problems/subsets/ |

## Problem

You get an array `nums` of distinct integers. Return every possible subset of it (the power set). No subset may appear twice in the answer; any order works.

**Example 1:**

```
Input: nums = [1,2,3]
Output: [[],[1],[2],[1,2],[3],[1,3],[2,3],[1,2,3]]
```

**Example 2:**

```
Input: nums = [0]
Output: [[],[0]]
```

**Constraints:**

- `1 <= nums.length <= 10`
- `-10 <= nums[i] <= 10`
- All values in `nums` differ.

## Greg Tang Explains Visually

Packing a lunchbox from three snacks? 
Don't list lunches — walk the snacks and answer yes or no.
## Visual

<svg width="640" height="290" viewBox="0 0 640 290" xmlns="http://www.w3.org/2000/svg" style="background:#fafafa">
  <g font-family="monospace" fill="#111">
    <text x="320" y="24" font-size="14" text-anchor="middle">nums = [1,2,3] · left = take nums[i], right = skip it</text>
    <line x1="320" y1="69" x2="160" y2="103" stroke="#111" stroke-width="1.5"/>
    <line x1="320" y1="69" x2="480" y2="103" stroke="#111" stroke-width="1.5"/>
    <line x1="160" y1="129" x2="80" y2="163" stroke="#111" stroke-width="1.5"/>
    <line x1="160" y1="129" x2="240" y2="163" stroke="#111" stroke-width="1.5"/>
    <line x1="480" y1="129" x2="400" y2="163" stroke="#111" stroke-width="1.5"/>
    <line x1="480" y1="129" x2="560" y2="163" stroke="#111" stroke-width="1.5"/>
    <line x1="80" y1="189" x2="40" y2="223" stroke="#111" stroke-width="1.5"/>
    <line x1="80" y1="189" x2="120" y2="223" stroke="#111" stroke-width="1.5"/>
    <line x1="240" y1="189" x2="200" y2="223" stroke="#111" stroke-width="1.5"/>
    <line x1="240" y1="189" x2="280" y2="223" stroke="#111" stroke-width="1.5"/>
    <line x1="400" y1="189" x2="360" y2="223" stroke="#111" stroke-width="1.5"/>
    <line x1="400" y1="189" x2="440" y2="223" stroke="#111" stroke-width="1.5"/>
    <line x1="560" y1="189" x2="520" y2="223" stroke="#111" stroke-width="1.5"/>
    <line x1="560" y1="189" x2="600" y2="223" stroke="#111" stroke-width="1.5"/>
    <rect x="295" y="43" width="50" height="26" fill="none" stroke="#111" stroke-width="2"/><text x="320" y="61" font-size="13" text-anchor="middle">[]</text>
    <rect x="132" y="103" width="56" height="26" fill="none" stroke="#111" stroke-width="2"/><text x="160" y="121" font-size="13" text-anchor="middle">[1]</text>
    <rect x="452" y="103" width="56" height="26" fill="none" stroke="#111" stroke-width="2"/><text x="480" y="121" font-size="13" text-anchor="middle">[]</text>
    <rect x="50" y="163" width="60" height="26" fill="none" stroke="#111" stroke-width="2"/><text x="80" y="181" font-size="13" text-anchor="middle">[1,2]</text>
    <rect x="210" y="163" width="60" height="26" fill="none" stroke="#111" stroke-width="2"/><text x="240" y="181" font-size="13" text-anchor="middle">[1]</text>
    <rect x="370" y="163" width="60" height="26" fill="none" stroke="#111" stroke-width="2"/><text x="400" y="181" font-size="13" text-anchor="middle">[2]</text>
    <rect x="530" y="163" width="60" height="26" fill="none" stroke="#111" stroke-width="2"/><text x="560" y="181" font-size="13" text-anchor="middle">[]</text>
    <rect x="7" y="223" width="66" height="26" fill="#111"/><text x="40" y="241" font-size="13" text-anchor="middle" fill="#fafafa">[1,2,3]</text>
    <rect x="87" y="223" width="66" height="26" fill="#111"/><text x="120" y="241" font-size="13" text-anchor="middle" fill="#fafafa">[1,2]</text>
    <rect x="167" y="223" width="66" height="26" fill="#111"/><text x="200" y="241" font-size="13" text-anchor="middle" fill="#fafafa">[1,3]</text>
    <rect x="247" y="223" width="66" height="26" fill="#111"/><text x="280" y="241" font-size="13" text-anchor="middle" fill="#fafafa">[1]</text>
    <rect x="327" y="223" width="66" height="26" fill="#111"/><text x="360" y="241" font-size="13" text-anchor="middle" fill="#fafafa">[2,3]</text>
    <rect x="407" y="223" width="66" height="26" fill="#111"/><text x="440" y="241" font-size="13" text-anchor="middle" fill="#fafafa">[2]</text>
    <rect x="487" y="223" width="66" height="26" fill="#111"/><text x="520" y="241" font-size="13" text-anchor="middle" fill="#fafafa">[3]</text>
    <rect x="567" y="223" width="66" height="26" fill="#111"/><text x="600" y="241" font-size="13" text-anchor="middle" fill="#fafafa">[]</text>
    <text x="320" y="276" font-size="12" text-anchor="middle" fill="#111">3 levels × 2 choices → 2³ = 8 leaves · each black leaf = one subset</text>
    <text x="240" y="90" font-size="11" text-anchor="middle" stroke="#fafafa" stroke-width="5" paint-order="stroke">take 1</text>
    <text x="400" y="90" font-size="11" text-anchor="middle" stroke="#fafafa" stroke-width="5" paint-order="stroke">skip 1</text>
    <text x="120" y="150" font-size="11" text-anchor="middle" stroke="#fafafa" stroke-width="5" paint-order="stroke">take 2</text>
    <text x="200" y="150" font-size="11" text-anchor="middle" stroke="#fafafa" stroke-width="5" paint-order="stroke">skip 2</text>
  </g>
</svg>

1. Snack 1 asks: "In or out?" Two answers, two piles.
2. Snack 2 asks every pile the same question. Four piles.
3. Snack 3 asks again. Eight piles.
4. Out of snacks? Each pile now names one lunch. Write it down.

Three yes-or-no questions, 2 × 2 × 2 = 8 lunches. 

## E-Prime Pseudocode

If you think, this is related to tree traversal but we need to build and write leaf node together so we can back track and build result on top of previously calculated result.

If want to use nested for loop approach, input length will dictate how many nested loops will be required or may need frequent code change per input variance.

```
CREATE an empty path and an empty result list.

DEFINE dfs(i):
  IF i reaches the end of nums:
    RECORD a copy of path. RETURN.

  PUSH nums[i] onto path.      — take it
  
  CALL dfs(i + 1).
  
  POP nums[i] off path.        — undo the take

  CALL dfs(i + 1).             — skip it

CALL dfs(0). RETURN result.
```

```
def subsets(nums):
    path = []
    result = []

    def dfs(i):

        if i == len(nums):
            result.append(path.copy())
            return

        # TAKE
        path.append(nums[i])
        dfs(i + 1)

        # UNDO TAKE
        path.pop()

        # SKIP
        dfs(i + 1)

    dfs(0)

    return result
```

Output

```

[
    [1,2,3],
    [1,2],
    [1,3],
    [1],
    [2,3],
    [2],
    [3],
    []
]

```

## Solutions

> [!example]- Java
> ```java
> public List<List<Integer>> subsets(int[] nums) {
>     List<List<Integer>> res = new ArrayList<>();
>     dfs(nums, 0, new ArrayList<>(), res);
>     return res;
> }
>
> private void dfs(int[] nums, int i, List<Integer> path, List<List<Integer>> res) {
>     if (i == nums.length) {
>         res.add(new ArrayList<>(path)); // snapshot, not a reference
>         return;
>     }
>     path.add(nums[i]);                  // choose: take nums[i]
>     dfs(nums, i + 1, path, res);
>     path.remove(path.size() - 1);       // unchoose
>     dfs(nums, i + 1, path, res);        // skip nums[i]
> }
> ```
>
> **What breaks at large input**
>
> - **Output size:** 2^n subsets holding n·2^(n−1) numbers in total. n = 10 gives 1,024 lists; n = 20 gives ~1 million lists and ~10 million slots — on the order of 100 MB of objects before any algorithm cost.
> - **Snapshot copy:** `new ArrayList<>(path)` costs O(n) per leaf — unavoidable, since the output holds those numbers anyway. Drop it and every leaf points at one shared list, empty by the end.
> - **Boxing:** values in −10..10 fall inside Java's `Integer` cache (−128..127), so `path.add(nums[i])` allocates nothing new here; wider values would.
> - **Recursion depth:** n + 1 frames, 11 at most. Stack overflow needs thousands of frames — the output explodes long before.
>
> **How to improve it**
>
> - Pre-size the result: `new ArrayList<>(1 << nums.length)` — no regrowth mid-search.
> - Bitmask loop: `for mask in 0 .. 2^n − 1`, bit j set → include `nums[j]`. No recursion, same O(n·2^n).
> - Doubling loop: start from `[[]]`; for each x, copy every existing subset and append x.
> - Need only a count or a yes/no (does some subset hit sum k)? Skip enumeration — DP over sums ([[Partition Equal Subset Sum]]).

> [!example]- Python
> ```python
> def subsets(self, nums: List[int]) -> List[List[int]]:
>     res, path = [], []
>
>     def dfs(i):
>         if i == len(nums):
>             res.append(path.copy())  # snapshot, not a reference
>             return
>         path.append(nums[i])         # choose: take nums[i]
>         dfs(i + 1)
>         path.pop()                   # unchoose
>         dfs(i + 1)                   # skip nums[i]
>
>     dfs(0)
>     return res
> ```
>
> **What breaks at large input**
>
> - **Output size:** same 2^n wall; each list carries ~56 bytes of header plus 8 bytes per slot. Small ints (−5..256) come pre-built, so the values themselves cost only a pointer.
> - **Interpreter cost:** 2^(n+1) − 1 calls. n = 10 → ~2,000 calls, instant; n = 20 → ~2 million calls, about a second in CPython.
> - **Recursion limit:** default 1,000 frames; depth here stays at n + 1 = 11.
> - **Snapshot:** forget `path.copy()` and every entry aliases one list, empty by the end.
>
> **How to improve it**
>
> - `itertools.combinations(nums, k)` for k in 0..n runs in C — far fewer interpreter steps.
> - Doubling one-liner: `res = [[]]` then `for x in nums: res += [s + [x] for s in res]`.
> - Caller only iterates? Turn `dfs` into a generator and `yield` each subset — memory drops to O(n).
> - Count or yes/no only → DP, no enumeration.

> [!example]- C#
> ```csharp
> public IList<IList<int>> Subsets(int[] nums) {
>     var res = new List<IList<int>>();
>     var path = new List<int>();
>     void Dfs(int i) {
>         if (i == nums.Length) {
>             res.Add(new List<int>(path)); // snapshot, not a reference
>             return;
>         }
>         path.Add(nums[i]);                // choose: take nums[i]
>         Dfs(i + 1);
>         path.RemoveAt(path.Count - 1);    // unchoose
>         Dfs(i + 1);                       // skip nums[i]
>     }
>     Dfs(0);
>     return res;
> }
> ```
>
> **What breaks at large input**
>
> - **Output size:** same 2^n wall. `List<int>` stores ints unboxed, but each subset still costs a list object plus its own backing array.
> - **Closure:** the local function `Dfs` captures `res`, `path` and `nums`; it never becomes a delegate, so the compiler passes those captures through a struct by reference — no heap allocation for the closure.
> - **Recursion depth:** n + 1 frames on a 1 MB default stack — nothing to worry about.
> - **Snapshot:** `new List<int>(path)` copies — required, same reason as Java.
>
> **How to improve it**
>
> - Pre-size: `new List<IList<int>>(1 << nums.Length)`.
> - Keep the path in an `int[] buf` with a length counter and record `buf[..len]` — a range on an array creates an exact-size copy, and arrays implement `IList<int>`, so no `List` wrapper per answer.
> - Bitmask or doubling loop, as in Java.
> - Count or yes/no only → DP.

## Why This Data Structure

- One mutable list serves as the path for the whole search: push on take, pop on undo — O(1) per step.
- The alternative — pass `path + [x]` into each call — copies at every one of the 2^(n+1) nodes instead of only at the 2^n leaves.
- The call stack does the bookkeeping: each frame remembers its own `i`, so the code never stores the tree.
- Distinct values → no dedupe needed. Duplicates change that — see [[Subsets II]].

## Complexity

| Time | Space |
|---|---|
| O(n · 2^n) | O(n) extra, output excluded |

- **Brute force:** nothing beats it — the answer itself holds n·2^(n−1) numbers, so any method pays O(n·2^n) just to write it down.
- **Tree:** 2^(n+1) − 1 calls; each of the 2^n leaves copies a path of up to n → O(n·2^n).
- **Space:** path holds ≤ n items, call stack ≤ n + 1 frames → O(n). The output adds O(n·2^n).
- With n ≤ 10, at most 1,024 subsets.

## Pattern Takeaway

- **Core trick — take or skip:** turn "list every subset" into n yes/no decisions; the recursion tree visits each combination of answers once.
- **Choose → explore → unchoose:** push, recurse, pop. The pop restores the path, so the skip branch starts from the same state the take branch did.
- **Record a copy:** the shared path keeps changing; an answer needs a frozen snapshot.
- **Reused everywhere:** Subsets II adds dedupe, Combination Sum swaps "end of array" for "hit the target", Partition Equal Subset Sum swaps enumeration for DP.

## Related

- [[Backtracking (Neetcode)]]
- [[Backtracking Template]] — the same tree in loop form, plus the four knobs
- [[Subsets II]] — same tree; duplicate values force "skip all copies at once"
- [[Combination Sum]] — same push/pop, stops at a target instead of the array end
