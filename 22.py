import time
import itertools
from aocd.models import Puzzle

puzzle = Puzzle(2023,22)
data = puzzle.input_data
# data = puzzle.examples[0].input_data
# print(data)
start_time = time.time()


"""
Each brick contains of a couple of cubes in 1 line
It will stop falling when it reaches support somewhere. That happens when one of locations below is not empty

"""
lines = data.strip().split('\n')


# [(x1,y1,z1),(x2,y2,z2)]
bricks_snap = [[list(map(int,loc.split(","))) for loc in line.split("~")] for line in lines]
bricks_snap.sort(key=lambda x: x[0][2])
size_x,size_y = [max(b[1][j] for b in bricks_snap)+1 for j in (0,1)]
# print(bricks[:10])
bricks_snap = [tuple(itertools.product(*(range(d1,d2+1) for d1,d2 in zip(b1,b2)))) for b1,b2 in bricks_snap]
# print(bricks[:10])

# bricks = [itertools.product(*(range(d1,d2+1) for d1,d2 in zip(map(int,loc.split(",")) for loc in line.split("~")) )) for line in lines]
# bricks
print(size_x,size_y)
floor= tuple((x,y,0) for x in range(size_x) for y in range(size_y))
# bricks_down= [floor]
stack = dict.fromkeys(floor,-1)

bricks = []
supporting_bricks = []  # ix of all bricks supporting this brick

for ix, brick in enumerate(bricks_snap):
    offset = 0
    while all((x,y,z+offset-1) not in stack for x,y,z in brick):
        offset -=1
    if offset:
        brick = tuple((x,y,z+offset) for (x,y,z) in brick)

    # potential support locatoins:
    support_locs = set((x,y,z-1) for (x,y,z) in brick if (x,y,z-1) not in brick)
    # actual support:
    support_bricks = set(stack[loc] for loc in support_locs if loc in stack)
    supporting_bricks.append(support_bricks)

    for cube in brick:
        stack[cube] = ix
    bricks.append(brick)


ans1 = sum(1 for b in range(len(bricks_snap)) if {b} not in supporting_bricks)

timer = time.time() - start_time
print(f"{ans1=}, {timer=:.2f}")

# part2:
other = set(b for b in range(len(bricks_snap)) if {b} in supporting_bricks)

ans2=0
for b_remove in other:
    move = {b_remove}

    while True:
        new_move = set(b for b,supporters in enumerate(supporting_bricks) if not len(supporters-move))|{b_remove}
        if new_move==move:
            break
        move = new_move

    ans2+=len(move)-1  # ignore the original one

timer = time.time() - start_time
print(f"{ans2=}, {timer=:.2f}")
