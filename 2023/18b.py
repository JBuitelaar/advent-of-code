# Solving the same problem with the Shoelaces formula
from aocd.models import Puzzle

puzzle = Puzzle(2023,18)
data = puzzle.input_data
# data = puzzle.examples[0].input_data
# print(data)

E, S, W, N = list(range(4))
dir_map = {
    "L": W,
    "R": E,
    "U": N,
    "D": S,
}

def read_ln(ln,part1=True):
    if part1:
        (dir,steps,_) = ln.split()
        return (dir_map[dir],int(steps))
    else:
        return (int(ln[-2]),int(ln[-7:-2],base=16))


def shoelace(corners):
    area = 0
    for i, (x1,y1) in enumerate(corners[:-1]):
        x2, y2 = corners[i + 1]
        area += x1 * y2 - x2 * y1
    return abs(area) // 2

def solve(part1):
    instrs = [read_ln(ln,part1) for ln in data.split('\n')]

    r,c=0,0
    corners = []
    perimeter=0
    for (dir,steps) in instrs:
        perimeter+=steps
        if dir==E:
            c+=steps
        elif dir==W:
            c-=steps
        elif dir==S:
            r+=steps
        else:
            assert dir==N
            r-=steps

        corners.append((r,c))
    assert (r,c) == (0,0)

    area = shoelace(corners)
    interior_area = area - perimeter // 2 + 1
    return interior_area + perimeter

ans1=solve(True)
print(f"{ans1=}")

ans2=solve(False)
print(f"{ans2=}")



