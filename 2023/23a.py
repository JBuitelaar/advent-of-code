# Brute force path finding

import time
from aocd.models import Puzzle

puzzle = Puzzle(2023,23)
data = puzzle.input_data
# data = puzzle.examples[0].input_data
# print(data)

start_time = time.time()

rows = data.split('\n')

grid = {r+1j*c: v  for r,row in enumerate(rows) for c,v in enumerate(row) if v != '#'}
R = len(rows)
start_loc = 1j*rows[0].find(".")
end_loc = R-1+1j*rows[R-1].find(".")
to_explore = [(start_loc, {start_loc})]

N,E,S,W = -1,1j,1,-1j

next_tile = {
    ">": E,
    "<": W,
    "^": N,
    "v": S
}


ans1=0

iteration = 0
while to_explore:
    loc, path = to_explore.pop(0)
    iteration += 1
    tile = grid[loc]
    if tile in next_tile:
        dirs = [next_tile[tile]]
    else:
        dirs = [W,N,S,E]

    for d in dirs:
        new_loc = loc + d
        if new_loc in path or new_loc not in grid:
            continue
        if new_loc == end_loc:
            length = len(path)
            if length>ans1:
                ans1 = length
                longest_path = path
                # print(f"interation {iteration}: longest={ans1}")
            continue
        
        to_explore.append((new_loc, path | {new_loc}))

timer = time.time() - start_time
print(f"{ans1=}, {timer=:.2f}")

def getchar(loc):
    if loc in longest_path:
        return "*"
    elif loc in grid:
        return grid[loc]
    else:
        return "█"

for r in range(R):
    print("".join(getchar(r+1j*c) for c in range(len(rows[r]))))
