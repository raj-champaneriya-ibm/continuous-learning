---
type: concept
status: captured
created: 2026-10-12
updated: 2026-10-12
domain: learning
tags: [dsa, backtracking, recursion, constraints, neetcode, interview, hard]
---

# N-Queens

| | |
|---|---|
| Topic | [[Backtracking (Neetcode)]] |
| Difficulty | Hard |
| LeetCode | https://leetcode.com/problems/n-queens/ |
| Status in video | Not yet covered |

## Problem

Place `n` chess queens on an n × n board so no two attack each other — no shared row, column, or diagonal. Return every distinct board, each as a list of strings where `'Q'` marks a queen and `'.'` an empty square. Any order works.

**Example 1:**

```
Input: n = 4
Output: [[".Q..","...Q","Q...","..Q."],["..Q.","Q...","...Q",".Q.."]]
```

**Example 2:**

```
Input: n = 1
Output: [["Q"]]
```

**Constraints:**

- `1 <= n <= 9`

## Greg Tang Explains

Seat 4 queens at a 4 × 4 table so no two can see each other along a row, column, or diagonal.

1. One queen per row — rows never fight. Go row by row.
2. Each seated queen casts three shadows: her column, her ↘ diagonal (same r − c), her ↙ diagonal (same r + c).
3. Try each seat in the row. In a shadow? Skip it. Free? Sit, cast shadows, move to the next row.
4. Row with no free seat? The previous queen stands up, her shadows lift, and she tries her next seat.

Three lists of shadows answer "safe?" instantly. Board full? One answer.

## Visual

<svg width="560" height="260" viewBox="0 0 560 260" xmlns="http://www.w3.org/2000/svg" style="background:#fafafa">
  <g font-family="monospace" fill="#111">
    <text x="280" y="24" font-size="14" text-anchor="middle">n = 4, one solution · three sets catch every attack</text>
    <rect x="30" y="50" width="44" height="44" fill="none" stroke="#111" stroke-width="2"/>
    <rect x="74" y="50" width="44" height="44" fill="#111" stroke="#111" stroke-width="2"/>
    <text x="96" y="79" font-size="20" text-anchor="middle" fill="#fafafa" font-weight="bold">Q</text>
    <rect x="118" y="50" width="44" height="44" fill="none" stroke="#111" stroke-width="2"/>
    <rect x="162" y="50" width="44" height="44" fill="none" stroke="#111" stroke-width="2"/>
    <rect x="30" y="94" width="44" height="44" fill="#d9d9d9" stroke="#111" stroke-width="2"/>
    <rect x="74" y="94" width="44" height="44" fill="#d9d9d9" stroke="#111" stroke-width="2"/>
    <rect x="118" y="94" width="44" height="44" fill="#d9d9d9" stroke="#111" stroke-width="2"/>
    <rect x="162" y="94" width="44" height="44" fill="none" stroke="#111" stroke-width="2"/>
    <text x="184" y="123" font-size="20" text-anchor="middle" fill="#111" font-weight="bold">Q</text>
    <rect x="30" y="138" width="44" height="44" fill="none" stroke="#111" stroke-width="2"/>
    <text x="52" y="167" font-size="20" text-anchor="middle" fill="#111" font-weight="bold">Q</text>
    <rect x="74" y="138" width="44" height="44" fill="#d9d9d9" stroke="#111" stroke-width="2"/>
    <rect x="118" y="138" width="44" height="44" fill="none" stroke="#111" stroke-width="2"/>
    <rect x="162" y="138" width="44" height="44" fill="#d9d9d9" stroke="#111" stroke-width="2"/>
    <rect x="30" y="182" width="44" height="44" fill="none" stroke="#111" stroke-width="2"/>
    <rect x="74" y="182" width="44" height="44" fill="#d9d9d9" stroke="#111" stroke-width="2"/>
    <rect x="118" y="182" width="44" height="44" fill="none" stroke="#111" stroke-width="2"/>
    <text x="140" y="211" font-size="20" text-anchor="middle" fill="#111" font-weight="bold">Q</text>
    <rect x="162" y="182" width="44" height="44" fill="none" stroke="#111" stroke-width="2"/>
    <text x="20" y="76" font-size="11" text-anchor="middle" fill="#111">0</text>
    <text x="52" y="44" font-size="11" text-anchor="middle" fill="#111">0</text>
    <text x="20" y="120" font-size="11" text-anchor="middle" fill="#111">1</text>
    <text x="96" y="44" font-size="11" text-anchor="middle" fill="#111">1</text>
    <text x="20" y="164" font-size="11" text-anchor="middle" fill="#111">2</text>
    <text x="140" y="44" font-size="11" text-anchor="middle" fill="#111">2</text>
    <text x="20" y="208" font-size="11" text-anchor="middle" fill="#111">3</text>
    <text x="184" y="44" font-size="11" text-anchor="middle" fill="#111">3</text>
    <text x="20" y="248" font-size="12" text-anchor="start" fill="#111">gray = cells the row-0 queen attacks</text>
    <text x="314" y="70" font-size="14" text-anchor="middle" fill="#111" font-weight="bold">r</text>
    <text x="350" y="70" font-size="14" text-anchor="middle" fill="#111" font-weight="bold">c</text>
    <text x="396" y="70" font-size="14" text-anchor="middle" fill="#111" font-weight="bold">r−c</text>
    <text x="442" y="70" font-size="14" text-anchor="middle" fill="#111" font-weight="bold">r+c</text>
    <text x="314" y="96" font-size="14" text-anchor="middle" fill="#111">0</text>
    <text x="350" y="96" font-size="14" text-anchor="middle" fill="#111">1</text>
    <text x="396" y="96" font-size="14" text-anchor="middle" fill="#111">−1</text>
    <text x="442" y="96" font-size="14" text-anchor="middle" fill="#111">1</text>
    <text x="314" y="120" font-size="14" text-anchor="middle" fill="#111">1</text>
    <text x="350" y="120" font-size="14" text-anchor="middle" fill="#111">3</text>
    <text x="396" y="120" font-size="14" text-anchor="middle" fill="#111">−2</text>
    <text x="442" y="120" font-size="14" text-anchor="middle" fill="#111">4</text>
    <text x="314" y="144" font-size="14" text-anchor="middle" fill="#111">2</text>
    <text x="350" y="144" font-size="14" text-anchor="middle" fill="#111">0</text>
    <text x="396" y="144" font-size="14" text-anchor="middle" fill="#111">2</text>
    <text x="442" y="144" font-size="14" text-anchor="middle" fill="#111">2</text>
    <text x="314" y="168" font-size="14" text-anchor="middle" fill="#111">3</text>
    <text x="350" y="168" font-size="14" text-anchor="middle" fill="#111">2</text>
    <text x="396" y="168" font-size="14" text-anchor="middle" fill="#111">1</text>
    <text x="442" y="168" font-size="14" text-anchor="middle" fill="#111">5</text>
    <line x1="300" y1="78" x2="460" y2="78" stroke="#111" stroke-width="1"/>
    <text x="300" y="208" font-size="12" text-anchor="start" fill="#111">each column holds 4 distinct values</text>
    <text x="300" y="226" font-size="12" text-anchor="start" fill="#111">→ no shared column or diagonal</text>
  </g>
</svg>

## E-Prime Pseudocode

```
CREATE sets cols, diag (r − c), anti (r + c). FILL the board with '.'.
DEFINE dfs(r):
  IF r equals n: RECORD a copy of the board. RETURN.
  FOR c FROM 0 TO n − 1:
    IF c, r − c, or r + c already sits in its set: SKIP to the next c.
    ADD c, r − c, r + c to their sets. PLACE 'Q' at (r, c).
    CALL dfs(r + 1).
    REMOVE them from their sets. PUT '.' back at (r, c).
CALL dfs(0). RETURN result.
```

## Solutions

> [!example]- Java
> ```java
> public List<List<String>> solveNQueens(int n) {
>     char[][] board = new char[n][n];
>     for (char[] row : board) Arrays.fill(row, '.');
>     List<List<String>> res = new ArrayList<>();
>     dfs(0, board, new boolean[n], new boolean[2 * n - 1], new boolean[2 * n - 1], res);
>     return res;
> }
>
> private void dfs(int r, char[][] board, boolean[] cols, boolean[] diag, boolean[] anti,
>                  List<List<String>> res) {
>     int n = board.length;
>     if (r == n) {
>         List<String> snapshot = new ArrayList<>(n);
>         for (char[] row : board) snapshot.add(new String(row));
>         res.add(snapshot);
>         return;
>     }
>     for (int c = 0; c < n; c++) {
>         int d = r - c + n - 1, a = r + c;   // shift r - c into 0..2n-2
>         if (cols[c] || diag[d] || anti[a]) continue;
>         cols[c] = diag[d] = anti[a] = true;
>         board[r][c] = 'Q';
>         dfs(r + 1, board, cols, diag, anti, res);
>         cols[c] = diag[d] = anti[a] = false;
>         board[r][c] = '.';
>     }
> }
> ```
>
> **What breaks at large input**
>
> - **Answer counts climb fast:** n = 8 → 92, n = 9 → 352, n = 12 → 14,200, n = 14 → 365,596 boards.
> - **Snapshots:** each answer builds n strings of length n → O(n²) per board.
> - **Index shift:** r − c ranges over −(n−1)..n−1; `+ n − 1` shifts it into 0..2n−2. Forget it and the array throws `ArrayIndexOutOfBoundsException`.
> - **Recursion depth:** n + 1 frames.
>
> **How to improve it**
>
> - **Bitmasks:** three `int`s for cols / diag / anti. Free squares = `~(cols | diag | anti) & ((1 << n) − 1)`; take the lowest with `p & -p`; shift one diagonal mask left and the other right per row. The standard fast solver.
> - **Mirror symmetry:** place the row-0 queen only in the left half and mirror each board — about 2× less work (odd n needs the middle column handled once).
> - **Count only** (LeetCode 52, N-Queens II): skip board building entirely.

> [!example]- Python
> ```python
> def solveNQueens(self, n: int) -> List[List[str]]:
>     cols, diag, anti = set(), set(), set()  # c, r - c, r + c
>     board = [["."] * n for _ in range(n)]
>     res = []
>
>     def dfs(r):
>         if r == n:
>             res.append(["".join(row) for row in board])
>             return
>         for c in range(n):
>             if c in cols or (r - c) in diag or (r + c) in anti:
>                 continue
>             cols.add(c); diag.add(r - c); anti.add(r + c)
>             board[r][c] = "Q"
>             dfs(r + 1)
>             cols.remove(c); diag.remove(r - c); anti.remove(r + c)
>             board[r][c] = "."
>
>     dfs(0)
>     return res
> ```
>
> **What breaks at large input**
>
> - **Same counts** as Java; each try does several set operations in interpreted code — much slower per node than Java arrays.
> - **Snapshots:** `"".join(row)` for every row of every answer.
> - **Recursion depth:** n + 1, tiny.
>
> **How to improve it**
>
> - Lists of booleans indexed by `c`, `r - c + n - 1`, `r + c` — or plain int bitmasks — instead of sets.
> - Store only `queens[r] = c` during the search; build `"." * c + "Q" + "." * (n - c - 1)` at the end.
> - Symmetry; count-only variant.

> [!example]- C#
> ```csharp
> public IList<IList<string>> SolveNQueens(int n) {
>     var res = new List<IList<string>>();
>     var board = new char[n][];
>     for (int r = 0; r < n; r++) { board[r] = new char[n]; Array.Fill(board[r], '.'); }
>     bool[] cols = new bool[n], diag = new bool[2 * n - 1], anti = new bool[2 * n - 1];
>     void Dfs(int r) {
>         if (r == n) {
>             res.Add(board.Select(row => new string(row)).ToList());
>             return;
>         }
>         for (int c = 0; c < n; c++) {
>             int d = r - c + n - 1, a = r + c; // shift r - c into 0..2n-2
>             if (cols[c] || diag[d] || anti[a]) continue;
>             cols[c] = diag[d] = anti[a] = true;
>             board[r][c] = 'Q';
>             Dfs(r + 1);
>             cols[c] = diag[d] = anti[a] = false;
>             board[r][c] = '.';
>         }
>     }
>     Dfs(0);
>     return res;
> }
> ```
>
> **What breaks at large input**
>
> - **Same counts** as Java.
> - **Snapshot via LINQ:** `Select(...).ToList()` per answer — a little overhead, fine at n ≤ 9.
> - **Index shift** for `r − c`, same trap as Java (`IndexOutOfRangeException`).
>
> **How to improve it**
>
> - Bitmask solver; `BitOperations.TrailingZeroCount` (System.Numerics) turns the lowest free bit into a column index.
> - Store columns only; build each row as `new string('.', c) + 'Q' + new string('.', n - c - 1)`.
> - Symmetry; count-only variant.

## Why This Data Structure

- **Rows:** one queen per row by construction → no row check at all.
- **Columns:** `cols[c]`.
- **Diagonals:** every cell on one ↘ diagonal shares r − c; every cell on one ↙ diagonal shares r + c → two more boolean arrays of size 2n − 1.
- **Result:** an O(1) safety check instead of scanning the board in O(n) per try.
- **Array index fits** because all three ids span fewer than 2n values — the same reasoning as `used[]` in [[Permutations]].

## Complexity

| Time | Space |
|---|---|
| O(n!) | O(n) extra, plus O(n²) per stored board |

- **Brute force:** choose n of n² cells → C(81, 9) ≈ 2.6 × 10^11 at n = 9.
- **One queen per row:** n^n → 9^9 ≈ 3.9 × 10^8.
- **Plus the column check:** n! → 362,880 at n = 9; the diagonal checks prune most of those.
- **Space:** three arrays of O(n), depth n; each stored board O(n²).

## Pattern Takeaway

- **Core trick — constraints as O(1) lookups:** r − c and r + c turn "diagonal attack?" into an array read.
- **One item per level:** placing by row removes the row constraint for free.
- **Same id trick** as [[Valid Sudoku]] (box id = (r / 3) · 3 + c / 3).

## Related

- [[Backtracking (Neetcode)]]
- [[Backtracking Template]]
- [[Permutations]] — N-Queens = permutations of columns, filtered by diagonals
- [[Valid Sudoku]] — row / column / box sets, same O(1) membership idea
- N-Queens II (LeetCode 52) — count the boards instead of listing them
