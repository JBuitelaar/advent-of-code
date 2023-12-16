# try with complex numbers
import time
from aocd.models import Puzzle

puzzle = Puzzle(2023,16)
data = puzzle.input_data
# example = puzzle.examples[0]
# data = example.input_data

lines = data.strip().split('\n')
R = len(lines)
C = len(lines[0])

grid = {r+1j*c: v for r,row in enumerate(lines) for c,v in enumerate(row)}

N,S,W,E = -1,1,-1j,1j
next_dirs = {
    "\\": {N:W,S:E,W:N,E:S},
    "/": {N:E,S:W,W:S,E:N}
}

def print_map(seen):
    print("map:")
    visited = set([loc for (loc,_) in seen])
    for r in range(R):
        print("".join("#" if (r,c) in visited else "." for c in range(C)))


def calc(start_beam):
    to_do = [start_beam]
    seen = set()
    while to_do:
        beam = to_do.pop()
        loc,dir=beam

        while True:
            loc+=dir
            
            if loc not in grid:
                break
            beam = (loc,dir)
            if beam in seen:  # cycle: done
                break
            seen.add(beam)

            tile = grid[loc]

            if next_dir := next_dirs.get(tile):
                dir = next_dir[dir]
            elif tile == "|" and dir in (W,E):
                to_do.append((loc,S))
                dir = N
            elif tile == "-" and dir in (N,S):
                to_do.append((loc,E))
                dir = W
    return len(set(loc for (loc,_dir) in seen))

ans1=calc((-1j,E))
print(f"{ans1=}")

start = time.time()
start_beams = [((r+1j*c),dir) for r in range(R) for c,dir in ((-1,E),(C,W))] \
    +[((r+1j*c),dir) for c in range(C) for r,dir in ((-1,S),(R,N))]

ans2=max(calc(start_beam) for start_beam in start_beams)
print(f"{ans2=}")
timer = time.time()-start
print(f"{timer=:.2f}")
