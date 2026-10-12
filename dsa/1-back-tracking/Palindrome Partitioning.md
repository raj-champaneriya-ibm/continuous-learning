---
type: concept
status: captured
created: 2026-10-12
updated: 2026-10-12
domain: learning
tags: [dsa, backtracking, recursion, strings, palindrome, neetcode, interview, medium]
---

# Palindrome Partitioning

| | |
|---|---|
| Topic | [[Backtracking (Neetcode)]] |
| Difficulty | Medium |
| LeetCode | https://leetcode.com/problems/palindrome-partitioning/ |
| Status in video | Not yet covered |

## Problem

You get a string `s`. Split it into pieces so every piece reads the same forwards and backwards (a palindrome). Return every such split, in any order.

**Example 1:**

```
Input: s = "aab"
Output: [["a","a","b"],["aa","b"]]
```

**Example 2:**

```
Input: s = "a"
Output: [["a"]]
```

**Constraints:**

- `1 <= s.length <= 16`
- `s` holds only lowercase English letters.

## Greg Tang Explains

Cut a ribbon reading "aab" into pieces, each piece a mirror of itself.

1. First cut: try "a", "aa", or "aab" off the front.
2. "aab" doesn't mirror — toss that cut; nothing after it matters.
3. Kept "a"? Now cut the rest, "ab", the same way. Kept "aa"? Cut "b".
4. Ribbon gone? The pieces in your hand form one answer.

Every answer = a sequence of front cuts. Check each piece the moment you cut it, and bad ribbons never get far.

## Visual

<svg width="600" height="290" viewBox="0 0 600 290" xmlns="http://www.w3.org/2000/svg" style="background:#fafafa">
  <g font-family="monospace" fill="#111">
    <text x="300" y="24" font-size="14" text-anchor="middle">s = "aab" · each branch cuts one palindrome off the front</text>
    <line x1="300" y1="69" x2="130" y2="111" stroke="#111" stroke-width="1.5"/>
    <line x1="300" y1="69" x2="330" y2="111" stroke="#111" stroke-width="1.5"/>
    <line x1="300" y1="69" x2="510" y2="111" stroke="#111" stroke-width="1.5"/>
    <line x1="130" y1="137" x2="70" y2="181" stroke="#111" stroke-width="1.5"/>
    <line x1="130" y1="137" x2="200" y2="181" stroke="#111" stroke-width="1.5"/>
    <line x1="330" y1="137" x2="330" y2="181" stroke="#111" stroke-width="1.5"/>
    <line x1="70" y1="207" x2="70" y2="247" stroke="#111" stroke-width="1.5"/>
    <rect x="250" y="43" width="100" height="26" fill="none" stroke="#111" stroke-width="2"/><text x="300" y="61" font-size="13" text-anchor="middle">rest "aab"</text>
    <rect x="84" y="111" width="92" height="26" fill="none" stroke="#111" stroke-width="2"/><text x="130" y="129" font-size="13" text-anchor="middle">rest "ab"</text>
    <rect x="284" y="111" width="92" height="26" fill="none" stroke="#111" stroke-width="2"/><text x="330" y="129" font-size="13" text-anchor="middle">rest "b"</text>
    <rect x="464" y="111" width="92" height="26" fill="none" stroke="#111" stroke-width="1.5" stroke-dasharray="4 3"/><text x="510" y="129" font-size="13" text-anchor="middle">"aab" ✗</text>
    <rect x="24" y="181" width="92" height="26" fill="none" stroke="#111" stroke-width="2"/><text x="70" y="199" font-size="13" text-anchor="middle">rest "b"</text>
    <rect x="160" y="181" width="80" height="26" fill="none" stroke="#111" stroke-width="1.5" stroke-dasharray="4 3"/><text x="200" y="199" font-size="13" text-anchor="middle">"ab" ✗</text>
    <rect x="290" y="181" width="80" height="26" fill="#111"/><text x="330" y="199" font-size="13" text-anchor="middle" fill="#fafafa">[aa,b]</text>
    <rect x="28" y="247" width="84" height="26" fill="#111"/><text x="70" y="265" font-size="13" text-anchor="middle" fill="#fafafa">[a,a,b]</text>
    <rect x="419" y="193" width="22" height="26" fill="none" stroke="#111" stroke-width="1.5" stroke-dasharray="4 3"/><text x="430" y="211" font-size="13" text-anchor="middle"></text>
    <text x="448" y="211" font-size="12" text-anchor="start" fill="#111">prefix not a</text>
    <text x="448" y="225" font-size="12" text-anchor="start" fill="#111">palindrome → prune</text>
    <rect x="419" y="243" width="22" height="26" fill="#111"/><text x="430" y="261" font-size="13" text-anchor="middle" fill="#fafafa"></text>
    <text x="448" y="261" font-size="12" text-anchor="start" fill="#111">rest empty → record</text>
    <text x="215" y="94" font-size="11" text-anchor="middle" stroke="#fafafa" stroke-width="5" paint-order="stroke">cut "a"</text>
    <text x="315" y="94" font-size="11" text-anchor="middle" stroke="#fafafa" stroke-width="5" paint-order="stroke">cut "aa"</text>
    <text x="435" y="100" font-size="11" text-anchor="middle" stroke="#fafafa" stroke-width="5" paint-order="stroke">try "aab"</text>
    <text x="100" y="163" font-size="11" text-anchor="middle" stroke="#fafafa" stroke-width="5" paint-order="stroke">cut "a"</text>
    <text x="165" y="163" font-size="11" text-anchor="middle" stroke="#fafafa" stroke-width="5" paint-order="stroke">try "ab"</text>
    <text x="330" y="163" font-size="11" text-anchor="middle" stroke="#fafafa" stroke-width="5" paint-order="stroke">cut "b"</text>
    <text x="70" y="231" font-size="11" text-anchor="middle" stroke="#fafafa" stroke-width="5" paint-order="stroke">cut "b"</text>
  </g>
</svg>

## E-Prime Pseudocode

```
DEFINE dfs(start):
  IF start reaches the end of s: RECORD a copy of path. RETURN.
  FOR end FROM start TO the last index:
    IF s[start..end] reads the same both ways:   — prune everything else
      PUSH s[start..end].
      CALL dfs(end + 1).
      POP.
CALL dfs(0). RETURN result.
```

## Solutions

> [!example]- Java
> ```java
> public List<List<String>> partition(String s) {
>     List<List<String>> res = new ArrayList<>();
>     dfs(s, 0, new ArrayList<>(), res);
>     return res;
> }
>
> private void dfs(String s, int start, List<String> path, List<List<String>> res) {
>     if (start == s.length()) {
>         res.add(new ArrayList<>(path));
>         return;
>     }
>     for (int end = start; end < s.length(); end++) {
>         if (!isPal(s, start, end)) continue; // prune: cut only at palindromes
>         path.add(s.substring(start, end + 1));
>         dfs(s, end + 1, path, res);
>         path.remove(path.size() - 1);
>     }
> }
>
> private boolean isPal(String s, int l, int r) {
>     while (l < r) if (s.charAt(l++) != s.charAt(r--)) return false;
>     return true;
> }
> ```
>
> **What breaks at large input**
>
> - **Worst input:** one repeated letter ("aaaa…"). Every cut works → 2^(n−1) partitions; n = 16 → 32,768 answers of up to 16 strings each.
> - **Repeated checks:** `isPal(start, end)` reruns from scratch at every node, so the same substring gets checked again and again across branches.
> - **Substring copies:** `s.substring` allocates a new `String` (no shared backing array since Java 7u6).
> - **Recursion depth:** ≤ n + 1 = 17 frames.
>
> **How to improve it**
>
> - **Palindrome table:** precompute `pal[i][j] = s[i] == s[j] && (j − i < 2 || pal[i + 1][j − 1])` in O(n²); every check becomes O(1).
> - **Memoize suffixes:** cache the list of partitions for each `start`; branches that reach the same `start` reuse it.
> - Need only the fewest cuts? DP in O(n²), no enumeration (LeetCode 132, Palindrome Partitioning II).

> [!example]- Python
> ```python
> def partition(self, s: str) -> List[List[str]]:
>     res, path = [], []
>
>     def is_pal(l, r):
>         while l < r:
>             if s[l] != s[r]:
>                 return False
>             l, r = l + 1, r - 1
>         return True
>
>     def dfs(start):
>         if start == len(s):
>             res.append(path.copy())
>             return
>         for end in range(start, len(s)):
>             if is_pal(start, end):          # prune: cut only at palindromes
>                 path.append(s[start:end + 1])
>                 dfs(end + 1)
>                 path.pop()
>
>     dfs(0)
>     return res
> ```
>
> **What breaks at large input**
>
> - **Worst input:** "aaaa…" → 2^(n−1) partitions, same as Java.
> - **Interpreted check:** the `is_pal` loop runs one Python step per character. `piece == piece[::-1]` runs in C and often wins despite allocating a reversed copy.
> - **Slicing:** `s[start:end + 1]` allocates a new string — needed for the output anyway.
>
> **How to improve it**
>
> - Palindrome table as a list of lists, filled bottom-up in O(n²).
> - `@functools.cache` on a `dfs(start)` that returns all partitions of `s[start:]` — shared suffixes get computed once.
> - Fewest cuts only → DP.

> [!example]- C#
> ```csharp
> public IList<IList<string>> Partition(string s) {
>     var res = new List<IList<string>>();
>     var path = new List<string>();
>     bool IsPal(int l, int r) {
>         while (l < r) if (s[l++] != s[r--]) return false;
>         return true;
>     }
>     void Dfs(int start) {
>         if (start == s.Length) {
>             res.Add(new List<string>(path));
>             return;
>         }
>         for (int end = start; end < s.Length; end++) {
>             if (!IsPal(start, end)) continue; // prune: cut only at palindromes
>             path.Add(s.Substring(start, end - start + 1));
>             Dfs(end + 1);
>             path.RemoveAt(path.Count - 1);
>         }
>     }
>     Dfs(0);
>     return res;
> }
> ```
>
> **What breaks at large input**
>
> - **Worst input:** "aaaa…" → 2^(n−1) partitions.
> - **Repeated checks:** `IsPal` reruns at every node.
> - **Allocation:** `Substring` allocates — but only after the check passes, so rejected pieces cost nothing.
>
> **How to improve it**
>
> - `bool[,] pal` table filled in O(n²).
> - Memoize partitions per `start`.
> - Fewest cuts only → DP.

## Why This Data Structure

- **Branch = where the next piece ends:** a loop over `end`, starting at `start`.
- **Path as a stack of strings:** push a piece, recurse on the rest, pop.
- **Two-pointer palindrome check:** O(length) time, O(1) space. Upgrade to an O(n²) boolean table once the same checks repeat.
- **Pass `start`, don't slice the rest:** no copy of the remaining string at every level.

## Complexity

| Time | Space |
|---|---|
| O(n · 2^n) | O(n) extra (O(n²) with the table) |

- **Brute force:** try all 2^(n−1) cut patterns and test every piece → also O(n · 2^n), but backtracking abandons a pattern at its first bad piece.
- **Per node:** up to n checks of O(n) each; the precomputed table drops each check to O(1).
- **Space:** depth ≤ n, path ≤ n strings; the table adds n².

## Pattern Takeaway

- **Core trick — cut a prefix, recurse on the rest:** branch over where the first piece ends; the validity check prunes at once.
- **Same skeleton, other rules:** [[Word Break]] cuts prefixes that sit in a dictionary — and since it needs only yes/no, DP replaces enumeration.
- **Precompute expensive checks** when the tree keeps asking them.

## Related

- [[Backtracking (Neetcode)]]
- [[Backtracking Template]]
- [[Palindromic Substrings]] — the same palindrome table, counted instead of cut
- [[Longest Palindromic Substring]]
- [[Word Break]] — prefix cuts, decided by DP
