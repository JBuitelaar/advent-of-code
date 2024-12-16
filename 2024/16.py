import time
from aocd.models import Puzzle
from dotenv import load_dotenv
from heapq import heappop, heappush

load_dotenv()

puzzle = Puzzle(2024, 16)

# data = puzzle.examples[0].input_data
# print(f"Example: \n{data}\n{"="*80}")

data = puzzle.input_data

lines = data.strip().split("\n")

grid = {r + 1j * c: v for r, row in enumerate(lines) for c, v in enumerate(row)}
walls = {loc for loc, v in grid.items() if v == "#"}
start = next(loc for loc, v in grid.items() if v == "S")
end = next(loc for loc, v in grid.items() if v == "E")
dirs = -1, 1, -1j, 1j
N, S, W, E = dirs


# to print the grid:
R = len(lines)
C = len(lines[0])


def insert(rows, loc, v):
    r, c = int(loc.real), int(loc.imag)
    rows[r][c] = v


def print_grid(visited_locs):
    rows = [["."] * C for _ in range(R)]
    for loc in walls:
        insert(rows, loc, "#")
    for loc in visited_locs:
        insert(rows, loc, "O")
    insert(rows, start, "S")
    insert(rows, end, "E")
    print("\n".join("".join(r) for r in rows))


start_time = time.time()
# ### PART 1 ###

# Dijstra's shortest path algorithm
# For the state we need to keep track of the location and the direction locdir=(loc,dir)
# In the queue we add a unique id (i), because sorting is not defined for complex numbers
# For part 2 we keep track of the previous locdir, so we can travel the path backwards

inf = 10**10
i = 0

locdir = (start, E)
queue = [(0, i := i + 1, locdir, locdir)]

visited = {}
prev_locs = {}

while len(queue):
    score, _, locdir, prev = heappop(queue)

    prev_score = visited.get(locdir, inf)
    if score > prev_score:
        continue

    if score == prev_score:
        prev_locs[locdir].add(prev)
        continue

    prev_locs[locdir] = {prev}
    visited[locdir] = score

    loc, dir = locdir
    if loc == end:
        # since we use Dijkstra, we can stop here, because there is no shorter path
        # maybe there could be another one with the same score?
        ans1 = score
        break

    if loc + dir not in walls:
        heappush(queue, (score + 1, i := i + 1, (loc + dir, dir), locdir))

    for turn in (1j, -1j):
        # turning twice (going back) is never optimal, so we can turn and move in one go:
        next_dir = dir * turn
        next_loc = loc + next_dir
        if next_loc not in walls:
            heappush(queue, (score + 1001, i := i + 1, (next_loc, next_dir), locdir))


timer = time.time() - start_time
print(f"{ans1=}, {timer=:.2f}s")

# ### PART 2 ###

# Go backwards from the end to the start
locdirs = set()
to_check = {(locdir)}
while to_check:
    locdir = to_check.pop()
    locdirs.add(locdir)
    for prev_locdir in prev_locs[locdir]:
        if prev_locdir not in locdirs:
            to_check.add(prev_locdir)

locs = {loc for loc, _ in locdirs}
ans2 = len(locs)

timer = time.time() - start_time
print(f"{ans2=}, {timer=:.2f}s")
