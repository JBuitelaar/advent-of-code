import time
from aocd.models import Puzzle

puzzle = Puzzle(2023,14)
data = puzzle.input_data
# example = puzzle.examples[0]
# data = example.input_data
# print(data)

lines = data.strip().split('\n')
R = len(lines)
C = len(lines[0])
# location of the cubes. Add one at the beginning and end of each row and column
cubes_by_row = [[0,C+1] for _ in range(R)]
cubes_by_col = [[0,R+1] for _ in range(C)]
balls = []
for r,row in enumerate(lines,1):
    row_balls = [0]
    for c, val in enumerate(row,1):
        if val == "O":
            balls.append((r,c))
        elif val == "#":
            cubes_by_col[c-1].append(r)
            row_balls.append(c)
    row_balls.append(R+1)
    cubes_by_row[r-1]=tuple(row_balls)

balls = tuple(balls)
cubes_by_col = [tuple(sorted(cubes)) for cubes in cubes_by_col]

def roll(balls, cubes, reverse):
    """roll the balls. 
    cubes is the location of the fixed rocks. 
    an array of arrays, containing either the rownos for every column, or the columnnos for every row
    reverse: roll up/left (False) or down/right (True) 
    """
    new_balls = []
    # We use col, r, c, but it could also be the other way around (row,c,r), depending on what cubes is
    for col, cube_locs in enumerate(cubes,1):
        for ix,r0 in enumerate(cube_locs[:-1]):
            r1 = cube_locs[ix+1]
            range_balls = sum(1 for (r,c) in balls if c==col and r0<r<r1)
            for r in range(range_balls):
                loc = r1-1-r if reverse else r0+1+r
                new_balls.append((loc,col))
    return tuple(new_balls)

def score(balls):
    return sum(R+1-r for r,c in balls)

def transpose(balls):
    return tuple((c,r) for (r,c) in balls)

def get_char(r,c,balls):
    if (r+1,c+1) in balls:
        return "O"
    if r+1 in cubes_by_col[c]:
        return "#"
    return "."

def print_grid(balls):
    for r in range(R):
        print("".join(get_char(r,c,balls) for c in range(C)))

new_balls = roll(balls, cubes_by_col, False)
# print_grid(new_balls)
ans1=score(new_balls)
print(f"{ans1=}")

start = time.time()
cycle_cache = {balls: 0}
balls_by_cycle=[balls]
total_cycles=int(1e9)
j=1
while j<=total_cycles:
    print(f"cycle {j}: t={time.time()-start:.2f}s")
    for reverse in [False, True]:  # roll up/left (False) or down/right (True)
        for is_row, cubes in enumerate([cubes_by_col, cubes_by_row]):  # up/down or left/right
            if is_row:
                # revert rows and columns, revert back after the calculation
                balls = transpose(balls)
            balls = roll(balls, cubes, reverse)
            if is_row:
                balls = transpose(balls)

    key = tuple(balls)
    if key in cycle_cache:
        start_cycle = cycle_cache[key]
        cycle_length = j - start_cycle
        # now we actually have seen the answer already
        skip_cycles = (total_cycles - j ) // cycle_length
        print(f"cycle found: {start_cycle}=>{j} (length {cycle_length})")
    
        solution_ix = int(start_cycle + (total_cycles - j) % cycle_length)
        print(f"That means cycle {total_cycles} is equal to cycle {solution_ix}={total_cycles}-{skip_cycles}*{cycle_length}")
        balls = balls_by_cycle[solution_ix]
        break
    else:
        cycle_cache[key]=j
        balls_by_cycle.append(balls)
    j+=1

ans2=score(balls)
print(f"{ans2=}")
timer = time.time()-start
print(f"{timer=:.2f} seconds")
