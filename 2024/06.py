import time
from aocd.models import Puzzle

puzzle = Puzzle(2024, 6)
data = puzzle.input_data
# data = puzzle.examples[0].input_data

start_time = time.time()

lines = data.strip().split("\n")

grid = {r + 1j * c: v for r, row in enumerate(lines) for c, v in enumerate(row)}
guard = next(loc for loc, v in grid.items() if v == "^")
dir = -1


def turn_right(direction):  # 90 degrees
    return direction * -1j


def solve1(grid, guard, dir):
    visited = {guard}
    while True:
        new = guard + dir
        if new not in grid:
            return len(visited)
        if grid[new] == "#":
            dir = turn_right(dir)
        else:
            guard = new
            visited.add(guard)


ans1 = solve1(grid, guard, dir)
timer = time.time() - start_time
print(f"{ans1=}, {timer=:.2f}s")

# PART 2


def is_loop(grid, guard, dir, visited, extra_block):
    while True:
        new = guard + dir
        if new not in grid:
            return False
        if (new, dir) in visited:
            return True
        if grid[new] == "#" or new == extra_block:
            dir = turn_right(dir)
        else:
            guard = new
        visited.add((guard, dir))


# storing it as a set of (loc,dir) is *much* faster than using a defaultdict(set)
visited = {(guard, dir)}
# need to keep track of a separate list of visited nodes,
# because we can't place a block on the travelled path as it means the path would have been different
visited_locs = {guard}

extra_locs = set()
while True:
    new = guard + dir
    if new not in grid:
        break
    if grid[new] == "#":
        dir = turn_right(dir)
    else:
        guard = new
        visited.add((guard, dir))
        visited_locs.add(guard)
    # if we can place a new block in front, see if that results in a loop:
    nxt = guard + dir
    if (
        nxt in grid
        and grid[nxt] != "#"
        and nxt not in extra_locs
        and nxt not in visited_locs
        and is_loop(grid, guard, dir, visited.copy(), nxt)
    ):
        extra_locs.add(nxt)

ans2 = len(extra_locs)

timer = time.time() - start_time
print(f"{ans2=}, {timer=:.2f}s")
