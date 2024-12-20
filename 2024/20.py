import time
from aocd.models import Puzzle
from dotenv import load_dotenv

load_dotenv()

puzzle = Puzzle(2024, 20)

# data = puzzle.examples[0].input_data
# print(f"Example: \n{data}\n{"="*80}")

data = puzzle.input_data
min_saving = 100

lines = data.strip().split("\n")

walls = set()
for r, row in enumerate(lines):
    for c, v in enumerate(row):
        loc = r + 1j * c
        if v == "S":
            start_loc = (r, c)
        elif v == "E":
            end_loc = (r, c)
        elif v == "#":
            walls.add((r, c))


def neighbours(x, y):
    return ((x + 1, y), (x - 1, y), (x, y + 1), (x, y - 1))


### PART 1 ###
start_time = time.time()

path = [(start_loc, d := 0)]
loc = prev = start_loc

# We can only go one way, so we just follow the path till the end::
while loc != end_loc:
    for nb in neighbours(*loc):
        if nb not in walls and nb != prev:
            path.append((nb, d := d + 1))
            prev = loc
            loc = nb
            break

path_length = len(path) - 1
print(f"{path_length=}")


def solve(cheat_length):
    res = 0
    for (x1, y1), d1 in path:
        for (x2, y2), d2 in path[d1 + min_saving + 2 :]:
            dist = abs(x1 - x2) + abs(y1 - y2)
            if d2 - d1 - dist >= min_saving and dist <= cheat_length:
                res += 1
    return res


ans1 = solve(2)
timer = time.time() - start_time
print(f"{ans1=}, {timer=:.2f}s")

ans2 = solve(20)
timer = time.time() - start_time
print(f"{ans2=}, {timer=:.2f}s")


"""
I actually solved a more generic case where we have a maze with multiple routes.
Here I do a BFS to get all distances from start until we find the end
Then I do the same from the end to the start
After that, the trick is the same as above
"""


def bfs_distances(start, end):
    """we can stop at end, because we're not interested in any longer paths anway"""
    queue = [(0, start)]
    distances = {}
    for steps, loc in queue:
        distances[loc] = steps
        if loc == end:
            return distances

        for nb in neighbours(*loc):
            if nb not in walls and nb not in distances:
                queue.append((steps + 1, nb))
                distances[nb] = steps + 1

    raise ValueError("no path found")


distance_from_start = bfs_distances(start_loc, end_loc)
distance_to_end = bfs_distances(end_loc, start_loc)

# shortest path without cheating:
path_length = distance_from_start[end_loc]

# Some points we can already discard:
max_length = path_length - min_saving
ds = {k: v for k, v in distance_from_start.items() if v <= max_length}
de = {k: v for k, v in distance_to_end.items() if v <= max_length}


def solve_maze(cheat_length):
    res = 0
    for (x1, y1), d1 in distance_from_start.items():
        for (x2, y2), d2 in distance_to_end.items():
            if d1 + d2 <= max_length:
                dist = abs(x1 - x2) + abs(y1 - y2)
                if dist <= cheat_length and d1 + d2 + dist <= max_length:
                    res += 1
    return res


# assert solve_maze(2)==ans1
# assert solve_maze(20)==ans2
