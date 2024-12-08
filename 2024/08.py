import time
import itertools
from collections import defaultdict
from aocd.models import Puzzle

puzzle = Puzzle(2024, 8)
data = puzzle.input_data
# data = puzzle.examples[0].input_data

start_time = time.time()

lines = data.strip().split("\n")
R = len(lines)
C = len(lines[0])

# complex numbers would be easier again
antennas = {
    (r, c): val
    for r, line in enumerate(lines)
    for c, val in enumerate(line)
    if val != "."
}

locs = defaultdict(set)
for loc, val in antennas.items():
    locs[val].add(loc)

antinodes1 = set()
antinodes2 = set()

for char, locs2 in locs.items():
    for loc1, loc2 in itertools.permutations(locs2, 2):
        r1, c1 = loc1
        r2, c2 = loc2
        dr = r2 - r1
        dc = c2 - c1

        # look in both directions until we're off the grid
        counters = [itertools.count(0, 1), itertools.count(-1, -1)]
        for counter in counters:
            for k in counter:
                rc = r1 + dr * k
                cc = c1 + dc * k
                if 0 <= rc < R and 0 <= cc < C:
                    antinodes2.add((rc, cc))
                    if k in (-1, 2):
                        antinodes1.add((rc, cc))
                else:
                    break

ans1 = len(antinodes1)
ans2 = len(antinodes2)

timer = time.time() - start_time

# print the grid
for r in range(R):
    vals = [
        "#" if (r, c) in antinodes2 else antennas.get((r, c), ".") for c in range(C)
    ]
    print("".join(vals))

print(f"{ans1=}, {ans2=},{timer=:.2f}s")
