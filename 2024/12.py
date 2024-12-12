import time
from aocd.models import Puzzle
from dotenv import load_dotenv

load_dotenv()

puzzle = Puzzle(2024, 12)
start_time = time.time()

data = """RRRRIICCFF
RRRRIICCCF
VVRRRCCFFF
VVRCCCJFFF
VVVVCJJCFE
VVIVCCJJEE
VVIIICJJEE
MIIIIIJJEE
MIIISIJEEE
MMMISSJEEE"""

print(f"Example: \n{data}\n{"="*80}")

data = puzzle.input_data

dirs = [-1, 1, -1j, 1j]

lines = data.strip().split("\n")
R = len(lines)
C = len(lines[0])
print(R, C)
grid = {r + 1j * c: v for r, row in enumerate(lines) for c, v in enumerate(row)}

groups = []

while grid:
    loc, plant = grid.popitem()
    # take 1 square and find all connected squares with the same plants
    group = {loc}
    to_do = [loc]
    while to_do:
        loc = to_do.pop()

        neighbours = [loc + d for d in dirs]
        for nb in neighbours:
            if nb in grid and grid[nb] == plant:
                grid.pop(nb)
                group.add(nb)
                to_do.append(nb)
    # no need to keep track of v, just for debugging:
    groups.append((group, plant))

ans1 = ans2 = 0
for group, plant in groups:
    # there's a perimeter whenever the neighbour is not in the same group
    perims = set()
    for loc in group:
        perims |= {(loc, d) for d in dirs if loc + d not in group}
    perim = len(perims)

    # drop all the perims that are next to another one.
    # we could also just take the left/downmost one (checking if there is nothing to the left/down)
    side_count = 0
    while perims:
        loc, side = perims.pop()
        side_count += 1
        fence_dirs = [side * 1j, side * -1j]
        to_do = [loc]
        while to_do:
            loc = to_do.pop()

            neighbours = [loc + d for d in fence_dirs]
            for nb in neighbours:
                if (nb, side) in perims:
                    perims.remove((nb, side))
                    to_do.append(nb)

    # print(f"{plant}: {len(group):-3d}|{perim:-3d}|{side_count:-3d}")
    ans1 += perim * len(group)
    ans2 += side_count * len(group)

timer = time.time() - start_time
print(f"{ans1=}, {ans2=}, {timer=:.2f}s")
