import time
from bisect import bisect
from aocd.models import Puzzle
from collections import Counter
puzzle = Puzzle(2023,14)
data = puzzle.input_data
# example = puzzle.examples[0]
# data = example.input_data
# print(data)

lines = data.strip().split('\n')
R = len(lines)
C = len(lines[0])
assert R == C
cubes = []
balls = []
for r,row in enumerate(lines):
    row_balls = [-1]
    for c, val in enumerate(row):
        if val == "O":
            balls.append((r,c))
        elif val == "#":
            cubes.append((r,c))

balls = tuple(balls)


def roll(balls, cubes):
    """roll the balls. 
    cubes is the location of the fixed rocks. 
    """
    res = []
    count = [Counter() for _ in range(R)]
    for (r,c) in balls:
        j = bisect(cubes[c],r)-1
        count[c][j]+=1
        res.append((cubes[c][j]+count[c][j],c))
    return tuple(sorted(res))

def score(balls):
    return sum(R-r for r,c in balls)

def rotate(locations):
    # rotate the grid 90 degrees clockwise
    return tuple((c,R-1-r) for (r,c) in locations)

def bisectlist(values):
    res = []
    vals = sorted([-1]+values)
    for ix,val in enumerate(vals):
        # skip the rocks that are next to each other, because they don't matter
        if ix==len(vals)-1 or val+1<vals[ix+1] and val<R-1:
            res.append(val)
    return tuple(res)

def transform(locations):
    # creates the relevant rock locations, so we can easily find where the balls will roll
    res = [[] for _ in range(R)]
    for (r,c) in locations:
        res[c].append(r)
    return tuple(bisectlist(r) for r in res)

# location of the fixed rocks for NWSE (every step rotated 90 degrees clockwise)
cube_by_dir = []
for _ in range(4):
    cube_by_dir.append(transform(cubes))
    cubes = rotate(cubes)

def get_char(r,c,balls,cubes_):
    if (r,c) in balls:
        return "O"
    if r in cubes_[c]:
        return "#"
    return "."

def print_grid(balls,cubes=cube_by_dir[0]):
    for r in range(R):
        print("".join(get_char(r,c,balls,cubes) for c in range(C)))

new_balls = roll(balls, cube_by_dir[0])
# print_grid(new_balls)
ans1=score(new_balls)
print(f"{ans1=}")

start = time.time()
cycle_cache = {balls: 0}
balls_by_cycle=[balls]
total_cycles=int(1e9)
j=1
while j<=total_cycles:
    # print(f"cycle {j}: t={time.time()-start:.2f}s")
    for cubes in cube_by_dir:
        balls = roll(balls, cubes)
        balls = rotate(balls)

    if balls in cycle_cache:
        start_cycle = cycle_cache[balls]
        cycle_length = j - start_cycle
        # now we actually have seen the answer already
        skip_cycles = (total_cycles - j ) // cycle_length
        print(f"cycle found: {start_cycle}=>{j} (length {cycle_length})")
    
        solution_ix = int(start_cycle + (total_cycles - j) % cycle_length)
        print(f"That means cycle {total_cycles} is equal to cycle {solution_ix}={total_cycles}-{skip_cycles}*{cycle_length}")
        # We could also just skip skip_cycles*cycle_length steps, then we don't need to cache anything
        balls = balls_by_cycle[solution_ix]
        break
    else:
        cycle_cache[balls]=j
        balls_by_cycle.append(balls)
    j+=1

ans2=score(balls)
print(f"{ans2=}")
timer = time.time()-start
print(f"{timer=:.2f} seconds")
