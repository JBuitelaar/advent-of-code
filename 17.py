import time
from heapq import heappush, heappop
from aocd.models import Puzzle

puzzle = Puzzle(2023,17)
data = puzzle.input_data
# example = puzzle.examples[0]
# data = example.input_data

lines = data.strip().split('\n')
R = len(lines)
C = len(lines[0])
loss_grid = {(r,c):int(val) for r,row in enumerate(lines) for c,val in enumerate(row)}
N,S,W,E = (-1,0),(1,0),(0,-1),(0,1)
directions = (S,E,N,W)

start_loc = (0,0)
end_loc = (R-1,C-1)

def move(loc,dir):
    return (loc[0]+dir[0],loc[1]+dir[1])


def print_path(path):
    for r,row in enumerate(lines):
        print("".join("█" if (r,c) in path else val for c,val in enumerate(row)))


def solve(min_steps,max_steps): #loc,prev_dir,dir_steps,heat_lost):
    to_do = [] # priority queue of nodes to evaluate (starting with the lowest value)
    seen = {}
    path = []  # for debugging and printing, keep track of the path
    start_dir = (0,0)  # a non-direction, so we're free to choose every direction
    start_steps = min_steps  # so we don't need to repeat those steps again
    heappush(to_do,(0,start_loc,start_dir,start_steps,[start_loc]))
    # print(loc,prev_dir,dir_steps)

    while to_do:
        (heat_lost,loc,prev_dir,dir_steps,path) = heappop(to_do)

        for next_dir in directions:
            if next_dir!=prev_dir and dir_steps < min_steps:  # need to move in the same direction for min_steps
                continue
            if next_dir == (-prev_dir[0],-prev_dir[1]):  # can't reverse
                continue
            next_loc = move(loc,next_dir)
            if next_loc not in loss_grid:   # don't go outside of the grid
                continue
            if next_dir==prev_dir:
                if dir_steps == max_steps:  # no more than max_steps in the same direction
                    continue
                next_steps = dir_steps+1
            else:
                next_steps = 1

            next_cost = heat_lost + loss_grid[next_loc]

            if next_loc == end_loc and next_steps>=min_steps:
                # print_path(path + [next_loc])
                # print(len(seen))
                # print([sum(1 for (_,_,steps) in seen.keys() if steps==i) for i in range(1,max_steps+1)])
                return next_cost

            key = (next_loc,next_dir,next_steps)
            if key in seen and next_cost >= seen[key]:
                continue
            seen[key] = next_cost

            heappush(to_do,(next_cost,next_loc,next_dir,next_steps,path+[next_loc]))

start_time = time.time()
ans1 = solve(1,3)
timer = time.time()-start_time
print(f"{ans1=},{timer=:.2f}")

start_time = time.time()
ans2 = solve(4,10)
timer = time.time()-start_time
print(f"{ans1=},{timer=:.2f}")
