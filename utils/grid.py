"""
Using complex numbers for a grid helps because:
* it can be a key in a dictionary (this you can also do with a tuple)
* you can move in all 4 (even 8) direction by just adding complex numbers
* you can rotate by multiplying by a complex number

Using a dictionary to keep the location instead of list of lists/strings:
* makes it easy to know whether you're on the grid, also for non-rectangular grids
* on the other hand, it's harder to print

It's important to use a consistent notation though. Here we use the real part for the row (y-axis).
That's different from how you usually draw a complex plane
"""

# see for example 2023/17.py
from aocd.models import Puzzle

puzzle = Puzzle(2023, 17)
data = puzzle.input_data
lines = data.strip().split("\n")
R = len(lines)
C = len(lines[0])

dirs = -1, 1, -1j, 1j
N, S, W, E = dirs
dir_map = dict(zip("^v<>", dirs))


grid = {}
for r, row in enumerate(lines):
    for c, v in enumerate(row):
        loc = r + 1j * c
        if v == "@":
            start_loc = loc
            v = "."
        grid[loc] = v


grid = {r + 1j * c: v for r, row in enumerate(lines) for c, v in enumerate(row)}

start_loc = 0
end_loc = R - 1 + (C - 1) * 1j


def turn_right(direction):  # 90 degrees
    return direction * -1j


def turn_left(direction):
    return direction * 1j


def neighbours(loc):
    return [loc + d for d in dirs]


# simple grid starting at 0,0 on the top left with known number of rows and columns
# locs is a set of wall (#) locations
def set_to_str(locs):
    rows = []
    for r in range(R):
        rows.append(["#" if (r + 1j * c) in locs else "." for c in range(C)])
    return "\n".join(rows)


# simple grid starting at 0,0 on the top left with known number of rows and columns
# grid is a dictionary of locs to values
def dict_to_str(grid):
    rows = []
    for r in range(R):
        rows.append("".join(grid.get(r + 1j * c, ".") for c in range(C)))
    return "\n".join(rows)


# infinite grid where we don't know the boundaries
# Now we assume that positive coordinates (e.g. r==1,c==1) are in the top right quadrant
def print_grid2(locs):
    min_r = int(min(loc.real for loc in locs))
    min_c = int(min(loc.imag for loc in locs))
    max_r = int(max(loc.real for loc in locs))
    max_c = int(max(loc.imag for loc in locs))
    rows = [["."] * (max_c - min_c + 1) for _ in range(max_r - min_r + 1)]
    for loc in locs:
        rows[int(loc.real) - min_r][int(loc.imag) - min_c] = "#"

    for row in reversed(rows):
        print("".join(row))


def groups(locs):
    # put any neighbouring locs in the same group (floodfill)
    res = []
    while locs:
        robot = locs.pop()
        to_do = [robot]
        group = set()
        while to_do:
            loc = to_do.pop()
            neighbours = [loc + d for d in dirs]
            for nb in neighbours:
                if nb in locs:
                    group.add(nb)
                    locs.remove(nb)
                    to_do.append(nb)
        res.append(group)
    return res
