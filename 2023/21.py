# For part 2 I basically did the same as here:
# https://www.reddit.com/r/adventofcode/comments/18nevo3/comment/kealztx/
# also here: https://www.reddit.com/r/adventofcode/comments/18o4y0m/2023_day_21_part_2_algebraic_solution_using_only/
# apparently you can also just fit a quadratic function to the data and get the answer

import time
from collections import defaultdict, Counter
from aocd.models import Puzzle

puzzle = Puzzle(2023,21)
data = puzzle.input_data
# data = puzzle.examples[0].input_data
# print("example answers: ",example.answer_a, example.answer_b)
# print(data)
# print(data[:1000])
start_time = time.time()

rows = data.strip().split('\n')
R = len(rows)
assert R == len(rows[0])
grid = {}

for r,row in enumerate(rows):
    for c,v in enumerate(row):
        loc = (r,c)
        if v == "S":
            start = loc
            v = "."
        grid[loc]=v

def print_grid(locations):
    print("grid:")
    for r in range(R):
        print("".join("O" if (r,c) in locations else grid[r+1j*c] for c in range(R)))

part1_steps = 64


part2_steps = 26501365
# S sits at the center of the block:
S = (R-1)/2
assert S.is_integer()
S = int(S)
assert start == (S,S)

# The row and column through the center don't contain any rock
assert all(grid[(r,S)]=="." for r in range(R))
assert all(grid[(S,c)]=="." for c in range(R))
# That means that after S steps, we reach the boundary of the block on each axis
# After that, we'll reach the end of the next block every R steps
# That means we reach the end of block (0,B), (B,0), (-B,0), (0,-B) with
B = (part2_steps - S) / R
assert B.is_integer()
B = int(B)

# also the boundaries are empty:
assert all (grid[(r,c)]=="." for r in range(R) for c in (0,R-1))
assert all (grid[(r,c)]=="." for c in range(R) for r in (0,R-1))
# That means we reach the corners after 2*S==R-1 steps. 2 steps later we enter the blocks on the diagonals
# That also repeats for all the off-axis blocks

# So we get a figure like this after 3 "block steps" (so S+3*R steps):
#   234
#  22344
# 2223444
# 1110555
# 8887666
#  88766
#   876
# Here we have a center block (0), 4 axes with blocks (1,3,5,7) and 4 off-axss regions with blocks (2,4,6,8)
# this extends outward in every direction with every R steps
# So after B block steps, we will have:
# * 1 center block
# * 4 x B axis blocks
# * 4 x B*(B+1)/2 off-axis blocks
# Each of these 9 types can have different counts at the end of each block step, until they converge

# Now we count the number of cells in each block after 3 block steps:

dirs = ((1,0),(-1,0),(0,1),(0,-1))
locations = {start}
# we'll count the number of elements in these blocks (and ignore the rest)
relevant_blocks = set((r,c) for r in range(-1,2) for c in range(-1,2))
block_count_ts = {k:[] for k in relevant_blocks}

for step in range(1,S+3*R+1):
    locations = set((r1,c1) for (r1,c1) in ((r+dr,c+dc) for r,c in locations for dr,dc in dirs) if grid[(r1%R,c1%R)] == ".")
            
    if step == part1_steps:
        ans1 = len(locations)
        timer = time.time() - start_time
        print(f"{ans1=}, {timer=}")
             
    if not (step - S) % R:
        block_counts = Counter(b_loc for b_loc in ((r//R,c//R) for (r,c) in locations) if b_loc in relevant_blocks)
        for block,v in block_counts.items():
            block_count_ts[block].append(v)
        print(f"{step=}")

for block, vals in sorted(block_count_ts.items()):
    print(block,vals)


"""
step=458
(-1, -1) [946, 6342, 7334]
(-1, 0) [5456, 7334, 7250]
(-1, 1) [921, 6364, 7334]
(0, -1) [5480, 7334, 7250]
(0, 0) [3703, 7334, 7250, 7334]
(0, 1) [5473, 7334, 7250]
(1, -1) [924, 6388, 7334]
(1, 0) [5497, 7334, 7250]
(1, 1) [926, 6359, 7334]
"""

# From this we can get the values the block count oscilates betweeen (N1,N2)
# Since B is even, we can find the final configuration of the center block: N1
assert B%2==0
center_counts = block_count_ts[(0,0)]
start_cycle = [0]*8

for i,v in enumerate(center_counts):
    if v == center_counts[i+2]:
        if i%2:
            # note that the first element corresponds to cycle 0 (the first S steps)
            i+=1 
        [N1,N2] = center_counts[i:i+2]
        cycle = [N1,N2]
        break


# The rest of the oscilating blocks show a chessboard pattern.
# So now we can start adding up all the elements:
ans2=0
for (r,c),block_counts in block_count_ts.items():
    if (r,c) == (0,0):
        # Center block
        v = N1
    elif r==0 or c==0:
        # Axis blocks
        # from the center: N2,N1,N2,N1,...N2,special
        assert block_counts[1]==N2
        regular = (B-1)//2
        v=regular*sum(cycle) + sum(block_counts[:B-regular*2])
    else:
        # Off-axis blocks
        assert block_counts[2]==N2
        # At the very end we have B blocks on the diagonal in "stage 1":
        v = B*block_counts[0]
        # Then we have B-1 blocks on the next diagonal in "stage 2":
        v += (B-1)*block_counts[1]
        # We have odd blocks (same count as the center block):
        # 1+3+...+B-3
        v += ((B-2)*(B-2)/4)*N1
        # and even blocks (the inverse of the center block):
        # 2+4+...+B-2
        v += (B/2-1)*(B)/2*N2
    ans2+=int(v)

timer = time.time() - start_time
print(f"{ans2=}, {timer=}")
