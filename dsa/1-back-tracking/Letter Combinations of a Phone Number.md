---
type: concept
status: captured
created: 2026-10-12
updated: 2026-10-12
domain: learning
tags: [dsa, backtracking, recursion, strings, neetcode, interview, medium]
---

# Letter Combinations of a Phone Number

| | |
|---|---|
| Topic | [[Backtracking (Neetcode)]] |
| Difficulty | Medium |
| LeetCode | https://leetcode.com/problems/letter-combinations-of-a-phone-number/ |
| Status in video | Not yet covered |

## Problem

You get a string `digits` made of the characters 2–9. Each digit maps to the letters printed on a phone keypad: 2 → abc, 3 → def, 4 → ghi, 5 → jkl, 6 → mno, 7 → pqrs, 8 → tuv, 9 → wxyz. Return every string the digits could spell, in any order.

**Example 1:**

```
Input: digits = "23"
Output: ["ad","ae","af","bd","be","bf","cd","ce","cf"]
```

**Example 2:**

```
Input: digits = "2"
Output: ["a","b","c"]
```

**Constraints:**

- `1 <= digits.length <= 4`
- `digits[i]` lies in `['2', '9']`.
- Older versions of the problem allowed an empty string (answer `[]`); the code below still guards for it.

## Greg Tang Explains

An old phone, a two-digit code "23". Which words could it type?

1. Key 2 offers a, b, c. Pick one.
2. Key 3 offers d, e, f. Pick one.
3. Two keys, two picks → one word. Write it down, erase the last pick, try the next letter.
4. Out of key-3 letters? Erase the key-2 pick and move to its next letter.

Like an odometer: the last wheel spins fastest. 3 × 3 = 9 words.

## Visual

<svg width="620" height="248" viewBox="0 0 620 248" xmlns="http://www.w3.org/2000/svg" style="background:#fafafa">
  <g font-family="monospace" fill="#111">
    <text x="310" y="24" font-size="14" text-anchor="middle">digits = "23" · level i loops over the letters on key digits[i]</text>
    <line x1="310" y1="69" x2="115" y2="103" stroke="#111" stroke-width="1.5"/>
    <line x1="310" y1="69" x2="310" y2="103" stroke="#111" stroke-width="1.5"/>
    <line x1="310" y1="69" x2="505" y2="103" stroke="#111" stroke-width="1.5"/>
    <line x1="115" y1="129" x2="50" y2="163" stroke="#111" stroke-width="1.5"/>
    <line x1="115" y1="129" x2="115" y2="163" stroke="#111" stroke-width="1.5"/>
    <line x1="115" y1="129" x2="180" y2="163" stroke="#111" stroke-width="1.5"/>
    <line x1="310" y1="129" x2="245" y2="163" stroke="#111" stroke-width="1.5"/>
    <line x1="310" y1="129" x2="310" y2="163" stroke="#111" stroke-width="1.5"/>
    <line x1="310" y1="129" x2="375" y2="163" stroke="#111" stroke-width="1.5"/>
    <line x1="505" y1="129" x2="440" y2="163" stroke="#111" stroke-width="1.5"/>
    <line x1="505" y1="129" x2="505" y2="163" stroke="#111" stroke-width="1.5"/>
    <line x1="505" y1="129" x2="570" y2="163" stroke="#111" stroke-width="1.5"/>
    <rect x="288" y="43" width="44" height="26" fill="none" stroke="#111" stroke-width="2"/><text x="310" y="61" font-size="13" text-anchor="middle">""</text>
    <rect x="95" y="103" width="40" height="26" fill="none" stroke="#111" stroke-width="2"/><text x="115" y="121" font-size="13" text-anchor="middle">a</text>
    <rect x="290" y="103" width="40" height="26" fill="none" stroke="#111" stroke-width="2"/><text x="310" y="121" font-size="13" text-anchor="middle">b</text>
    <rect x="485" y="103" width="40" height="26" fill="none" stroke="#111" stroke-width="2"/><text x="505" y="121" font-size="13" text-anchor="middle">c</text>
    <rect x="27" y="163" width="46" height="26" fill="#111"/><text x="50" y="181" font-size="13" text-anchor="middle" fill="#fafafa">ad</text>
    <rect x="92" y="163" width="46" height="26" fill="#111"/><text x="115" y="181" font-size="13" text-anchor="middle" fill="#fafafa">ae</text>
    <rect x="157" y="163" width="46" height="26" fill="#111"/><text x="180" y="181" font-size="13" text-anchor="middle" fill="#fafafa">af</text>
    <rect x="222" y="163" width="46" height="26" fill="#111"/><text x="245" y="181" font-size="13" text-anchor="middle" fill="#fafafa">bd</text>
    <rect x="287" y="163" width="46" height="26" fill="#111"/><text x="310" y="181" font-size="13" text-anchor="middle" fill="#fafafa">be</text>
    <rect x="352" y="163" width="46" height="26" fill="#111"/><text x="375" y="181" font-size="13" text-anchor="middle" fill="#fafafa">bf</text>
    <rect x="417" y="163" width="46" height="26" fill="#111"/><text x="440" y="181" font-size="13" text-anchor="middle" fill="#fafafa">cd</text>
    <rect x="482" y="163" width="46" height="26" fill="#111"/><text x="505" y="181" font-size="13" text-anchor="middle" fill="#fafafa">ce</text>
    <rect x="547" y="163" width="46" height="26" fill="#111"/><text x="570" y="181" font-size="13" text-anchor="middle" fill="#fafafa">cf</text>
    <text x="310" y="214" font-size="12" text-anchor="middle" fill="#111">level 1 loops key 2 (a b c) · level 2 loops key 3 (d e f)</text>
    <text x="310" y="232" font-size="12" text-anchor="middle" fill="#111">3 × 3 = 9 leaves · depth = len(digits), fixed</text>
  </g>
</svg>

## E-Prime Pseudocode

```
IF digits holds nothing: RETURN an empty list.
DEFINE dfs(i):
  IF i equals the length of digits: RECORD path as a string. RETURN.
  FOR each letter ch ON key digits[i]:
    APPEND ch. CALL dfs(i + 1). REMOVE the last letter.
CALL dfs(0). RETURN result.
```

## Solutions

> [!example]- Java
> ```java
> private static final String[] KEYS = {"", "", "abc", "def", "ghi", "jkl", "mno", "pqrs", "tuv", "wxyz"};
>
> public List<String> letterCombinations(String digits) {
>     List<String> res = new ArrayList<>();
>     if (digits.isEmpty()) return res;
>     dfs(digits, 0, new StringBuilder(), res);
>     return res;
> }
>
> private void dfs(String digits, int i, StringBuilder path, List<String> res) {
>     if (i == digits.length()) {
>         res.add(path.toString());
>         return;
>     }
>     String letters = KEYS[digits.charAt(i) - '0'];
>     for (int j = 0; j < letters.length(); j++) {
>         path.append(letters.charAt(j));
>         dfs(digits, i + 1, path, res);
>         path.deleteCharAt(path.length() - 1);
>     }
> }
> ```
>
> **What breaks at large input**
>
> - **Output size:** up to 4^n strings (7 and 9 carry four letters). n = 4 → 256, tiny; n = 15 would mean 4^15 ≈ 1.07 billion strings.
> - **One builder, many answers:** a single `StringBuilder` serves the whole search; `toString()` copies once per leaf — the only allocation per answer.
> - **Concatenation trap:** passing `path + ch` down instead creates a new `String` at every node, not just every leaf.
> - **Recursion depth:** n + 1 ≤ 5.
>
> **How to improve it**
>
> - Pre-size: `new ArrayList<>(product of key sizes)` and `new StringBuilder(n)`.
> - **Iterative (BFS):** start from `[""]`; for each digit, replace the list with every string + every letter. No recursion.
> - **Odometer loop:** n counters ticking like a clock — O(n) extra space besides the output.

> [!example]- Python
> ```python
> def letterCombinations(self, digits: str) -> List[str]:
>     if not digits:
>         return []
>     keys = {"2": "abc", "3": "def", "4": "ghi", "5": "jkl",
>             "6": "mno", "7": "pqrs", "8": "tuv", "9": "wxyz"}
>     res, path = [], []
>
>     def dfs(i):
>         if i == len(digits):
>             res.append("".join(path))
>             return
>         for ch in keys[digits[i]]:
>             path.append(ch)
>             dfs(i + 1)
>             path.pop()
>
>     dfs(0)
>     return res
> ```
>
> **What breaks at large input**
>
> - **Output size:** 4^n strings.
> - **Join per leaf:** `"".join(path)` costs O(n) per answer — the output needs that anyway.
> - **Concatenation alternative:** `dfs(i + 1, prefix + ch)` reads nicely but builds a string at every node.
>
> **How to improve it**
>
> - `["".join(p) for p in itertools.product(*(keys[d] for d in digits))]` — the product runs in C.
> - Iterative build-up: `res = [p + ch for p in res for ch in keys[d]]` per digit.

> [!example]- C#
> ```csharp
> private static readonly string[] Keys = { "", "", "abc", "def", "ghi", "jkl", "mno", "pqrs", "tuv", "wxyz" };
>
> public IList<string> LetterCombinations(string digits) {
>     var res = new List<string>();
>     if (digits.Length == 0) return res;
>     var path = new StringBuilder();
>     void Dfs(int i) {
>         if (i == digits.Length) {
>             res.Add(path.ToString());
>             return;
>         }
>         foreach (char ch in Keys[digits[i] - '0']) {
>             path.Append(ch);
>             Dfs(i + 1);
>             path.Length--;                // unchoose: drop the last letter
>         }
>     }
>     Dfs(0);
>     return res;
> }
> ```
>
> **What breaks at large input**
>
> - **Output size:** 4^n strings.
> - **Cheap undo:** `path.Length--` drops the last char in O(1).
> - **`foreach` over a string** compiles to an index loop — no enumerator allocation.
>
> **How to improve it**
>
> - Pre-size `res` with the product of key sizes.
> - `char[] buf` + `new string(buf)` per leaf — same cost model as the builder, no builder object.
> - Iterative build-up or odometer loop, as in Java.

## Why This Data Structure

- **Lookup array `KEYS[digit]`:** digits 0–9 form a tiny bounded range, so a plain array index beats a hash map — the trick Two Sum couldn't use with ±10^9 values.
- **Mutable builder as the path:** append, recurse, delete last — O(1) per move.
- **No start index, no `used[]`:** each level owns a different key, so choices never collide.

## Complexity

| Time | Space |
|---|---|
| O(n · 4^n) | O(n) extra, output excluded |

- **Brute force:** nothing faster — every answer must get built.
- **Tree:** ≤ 4^n leaves, each building a string of length n.
- **Space:** depth n, builder n.

## Pattern Takeaway

- **Core trick — fixed-depth product:** level i picks from its own option set → the answer equals the Cartesian product of the sets.
- **No pruning, no dedupe** — the purest form of the template; a warm-up for the knobs other problems add.
- **Same build-a-string backtracking** powers [[Generate Parentheses]], where a validity rule prunes the tree.

## Related

- [[Backtracking (Neetcode)]]
- [[Backtracking Template]]
- [[Generate Parentheses]] — build a string char by char, with pruning
- [[Subsets]] — take/skip vs pick-one-of-k per level
