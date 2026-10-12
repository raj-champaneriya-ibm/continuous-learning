"""Step through the take/skip algorithm from Subsets.md.

Run from the repository root:
    python3 dsa/1-back-tracking/subsets.py

Debug without installing anything:
    python3 -m pdb dsa/1-back-tracking/subsets.py
    (Pdb) b 27
    (Pdb) c

At dfs, use `n` for the next line, `s` to enter a recursive call,
`p i`, `p path`, and `p result` to inspect state, and `w` for the call stack.
Use `s` on BOTH dfs(i + 1) lines: `n` runs that whole branch at once.
In an IDE, put a breakpoint on the first line inside dfs and use Step Into.

Start with [1, 2]; change nums below to [1, 2, 3] when comfortable.
Each call owns its i, but all calls share path and result.
"""


def subsets(nums):
    """Return all subsets of distinct nums, printing the recursion steps."""
    path = []
    result = []

    def dfs(i):
        indent = "    " * i
        print(f"{indent}ENTER dfs({i}): path={path}")

        if i == len(nums):
            result.append(path.copy())  # Save a snapshot; path keeps changing.
            print(f"{indent}SAVE {path}; RETURN to caller")
            return

        print(f"{indent}TAKE nums[{i}]={nums[i]}")
        path.append(nums[i])
        dfs(i + 1)  # Step Into: explore every subset that includes this value.

        # The child finished BOTH its branches. This frame resumes with its own i.
        print(f"{indent}BACK in dfs({i}) after TAKE: path={path}")
        path.pop()
        print(f"{indent}UNDO take of {nums[i]}: path={path}")

        # Skip means move to the next index WITHOUT adding nums[i].
        print(f"{indent}SKIP nums[{i}]={nums[i]}: keep path={path}, visit index {i + 1}")
        dfs(i + 1)  # Step Into: the same next index, but a different path.

        print(f"{indent}RETURN from dfs({i}) after SKIP: path={path}")

    dfs(0)
    return result


if __name__ == "__main__":
    nums = [1, 2]
    print(f"Input: {nums}\nIndentation shows recursion depth.\n")
    result = subsets(nums)
    assert len(result) == 2 ** len(nums)
    assert len({tuple(subset) for subset in result}) == len(result)
    print(f"\nAll {len(result)} subsets: {result}")
