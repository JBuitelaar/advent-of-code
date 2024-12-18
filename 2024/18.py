import time
from aocd.models import Puzzle
from dotenv import load_dotenv

# sys.setrecursionlimit(10**6)
from heapq import heappop, heappush
from bisect import bisect

load_dotenv()

puzzle = Puzzle(2024, 18)

# data = puzzle.examples[0].input_data
# max_coord=6
# byte_count=12

data = puzzle.input_data
max_coord = 70
byte_count = 1024

walls = tuple(map(eval, data.split("\n")))
start = 0, 0
end = max_coord, max_coord


def print_grid(visited_locs):
    rows = [["."] * (max_coord + 1) for _ in range(max_coord + 1)]

    for x, y in walls:
        rows[y][x] = "#"
    for x, y in visited_locs:
        rows[y][x] = "O"

    print("\n".join("".join(r) for r in rows))


start_time = time.time()

### PART 1 ###


# This is what I did first. Very simply Dijkstra's algorithm.
def path_length_dijkstra(walls):
    inf = 10**10
    queue = [(0, start)]

    visited = {}

    while len(queue):
        steps, loc = heappop(queue)
        prev_score = visited.get(loc, inf)
        if steps >= prev_score:
            continue

        visited[loc] = steps

        if loc == end:
            # print_grid(visited)
            return steps

        x, y = loc
        for x1, y1 in ((x + 1, y), (x - 1, y), (x, y + 1), (x, y - 1)):
            if (x1, y1) not in walls and 0 <= x1 <= max_coord and 0 <= y1 <= max_coord:
                heappush(queue, (steps + 1, (x1, y1)))
    raise ValueError("no path found")


# But this is much easier (and faster).
# Since every iteration adds 1 step, we have a sorted queue automatically with BFS


def path_length_bfs(walls):
    queue = [(0, start)]
    # we can't go to a wall, and also don't need to revisit a location, so we combine:
    skip = set(walls)
    for steps, loc in queue:
        if loc == end:
            return steps
        x, y = loc
        for x1, y1 in ((x + 1, y), (x - 1, y), (x, y + 1), (x, y - 1)):
            if (x1, y1) not in skip and 0 <= x1 <= max_coord and 0 <= y1 <= max_coord:
                queue.append((steps + 1, (x1, y1)))
                skip.add((x1, y1))
    raise ValueError("no path found")


ans1 = path_length_bfs(walls[:byte_count])

timer = time.time() - start_time
print(f"{ans1=}, {timer=:.2f}s")

### PART 2 ###

max_val = (max_coord + 1) ** 2


def path_length_or_max(ix):
    try:
        return path_length_bfs(walls[:ix])
    except ValueError:
        return max_val


ans2_ix = bisect(range(len(walls)), max_val - 1, byte_count, key=path_length_or_max)
print(ans2_ix)
ans2 = walls[ans2_ix - 1]

timer = time.time() - start_time
print(f"{ans2=}, {timer=:.2f}s")
