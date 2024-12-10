import time
from functools import reduce, cache
from aocd.models import Puzzle
from dotenv import load_dotenv

load_dotenv()

puzzle = Puzzle(2024, 10)

data = """89010123
78121874
87430965
96549874
45678903
32019012
01329801
10456732"""
# print(f"Example: \n{data}\n{"="*80}")

data = puzzle.input_data

start_time = time.time()

lines = data.strip().split("\n")

grid = {r + 1j * c: int(v) for r, row in enumerate(lines) for c, v in enumerate(row)}
dirs = [-1, 1, -1j, 1j]
start_locs = [loc for loc, v in grid.items() if v == 0]

### PART 1 ###


@cache
def tops(start, val):
    if val == 9:
        return {start}

    next_locs = (start + dir for dir in dirs)
    sets = (
        tops(loc, val + 1) for loc in next_locs if loc in grid and grid[loc] == val + 1
    )
    return reduce(set.union, sets, set())


ans1 = sum(len(tops(loc, 0)) for loc in start_locs)


timer = time.time() - start_time
print(f"{ans1=}, {timer=:.2f}s")


### PART 2 ###


@cache
def count_paths(start, val):
    if val == 9:
        return 1

    next_locs = [start + dir for dir in dirs]
    return sum(
        count_paths(loc, val + 1)
        for loc in next_locs
        if loc in grid and grid[loc] == val + 1
    )


ans2 = sum(count_paths(loc, 0) for loc in start_locs)

timer = time.time() - start_time
print(f"{ans2=}, {timer=:.2f}s")
