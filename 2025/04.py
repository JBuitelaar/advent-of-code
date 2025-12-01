import time
from aocd.models import Puzzle

puzzle = Puzzle(2025, 4)

# data = puzzle.examples[0].input_data
data = puzzle.input_data
# print(data[:300],"...")

start_time = time.time()

### PART 1 ###
lines = data.strip().split("\n")

grid = {
    r + 1j * c: v for r, row in enumerate(lines) for c, v in enumerate(row) if v == "@"
}

offsets = [-1, 0, 1]
dirs = [r + 1j * c for r in offsets for c in offsets if not (r == 0 and c == 0)]

# Easier, but we need the rest anyway for part 2:
# ans1 = sum(sum(loc + d in grid for d in dirs) < 4 for loc in grid)

delete = []
counts = {}
for loc in grid:
    count = sum(loc + d in grid for d in dirs)
    if count < 4:
        delete.append(loc)
    else:
        counts[loc] = count

ans1 = len(delete)
timer = time.time() - start_time
print(f"{ans1=}, {timer=:.2f}s")

### PART 2 ###

ans2 = ans1

while delete:
    loc = delete.pop()
    for d in dirs:
        nloc = loc + d
        if nloc in counts:
            counts[nloc] -= 1
            if counts[nloc] < 4:
                ans2 += 1
                del counts[nloc]
                delete.append(nloc)

timer = time.time() - start_time
print(f"{ans2=}, {timer=:.2f}s")
