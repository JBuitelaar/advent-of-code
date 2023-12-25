# Apparently there is the shoelaces formula for this, but I calculated it myself
# I basically did the same as this: https://www.reddit.com/r/adventofcode/comments/18l0qtr/comment/kdvcsza/

import time
import itertools
from collections import defaultdict
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


def solve(part1):
    instrs = [read_ln(ln,part1) for ln in data.split('\n')]

    # Horizontal lines: r: (c1,c2,flip), c1/c2 both inclusive
    # flip means whether we change in/out of the area
    # Vertical lines: (c,r1,r2), both exclusive(!)
    horizontal = defaultdict(list)
    vertical = []

    r,c=0,0
    prev_dir = instrs[-1][0]
    assert prev_dir in (N,S)

    for ix,(dir,steps) in enumerate(instrs):
        if dir in (E,W):
            next_dir = instrs[ix+1][0]
            flip = next_dir == prev_dir
            prev_dir = next_dir
            if dir == E:
                horizontal[r].append((c,c+steps,flip))
                c+=steps
            else:
                assert dir == W
                horizontal[r].append((c-steps,c,flip))
                c-=steps
        elif dir == S:
            vertical.append((c,r+1,r+steps-1))
            r+=steps
        else: 
            assert dir == N
            vertical.append((c,r-steps+1,r-1))
            r-=steps

    count = 0
    horizontal = sorted(horizontal.items())

    for ix, (r,bars) in enumerate(horizontal):
        # count tnis row
        row_count=0
        vert = [(c,) for c,r1,r2 in vertical if r1<=r<=r2]
        elements = sorted(vert+bars)
        
        c0 = -1
        in_area = False
        for el in elements:
            match el:
                case (c1,):
                    if in_area:
                        row_count+=c1-c0+1
                    in_area = not in_area
                    c0=c1
                case (c1,c2,flip):
                    row_count+=c2-c1+1  # add the horizontal bar itself
                    if in_area:
                        row_count+=c1-c0  # and the area in between (don't double count the end)
                    if flip:
                        in_area = not in_area
                    c0=c2+1 # 1 extra, to avoid double counting the end
                case _:
                    raise(ValueError("unreachable"))
        count+=row_count
        # print(f"{r}: {row_count}")

        if ix == len(horizontal)-1:
            continue

        next_row = horizontal[ix+1][0]
        # area in between (exclusive)
        rows = next_row-r-1
        if rows:
            vert = sorted([c for c,r1,r2 in vertical if r1<=r+1<=r2])
            cols = sum(c2-c1+1 for c1,c2 in itertools.batched(vert,2))
            # print(f"{r+1}: {rows}x{cols}")
            count+=rows*cols
    return count

ans1=solve(True)
print(f"{ans1=}")
start_time = time.time()

ans2=solve(False)
timer = time.time()-start_time
print(f"{ans2=}, {timer=}s")



