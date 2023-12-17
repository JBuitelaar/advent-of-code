# Shortest path using Dijkstra's algorithm
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

loss_grid = {r+1j*c: int(v) for r,row in enumerate(lines) for c,v in enumerate(row)}
N,S,W,E = -1,1,-1j,1j
directions = (S,E,N,W)

start_loc = 0
end_loc = R-1+(C-1)*1j

def print_path(path):
    for r,row in enumerate(lines):
        print("".join("█" if r+1j*c in path else val for c,val in enumerate(row)))


def solve(min_steps,max_steps): #loc,prev_dir,dir_steps,heat_lost):
    to_do = [] # priority queue of nodes to evaluate (starting with the lowest value)
    seen = {}
    path = []  # for debugging and printing, keep track of the path
    start_dir = -10  # a non-direction, so we're free to choose every direction
    start_steps = min_steps  # so we don't need to repeat those steps again
    counter=0  # need some way to sort the heap
    heappush(to_do,(0,counter,start_loc,start_dir,start_steps,[start_loc]))
    # print(loc,prev_dir,dir_steps)

    while to_do:
        (heat_lost,_,loc,prev_dir,dir_steps,path) = heappop(to_do)

        if loc == end_loc:
            # DONE!
            print_path(path)
            # print("cache_size by step_count=",{i:sum(1 for (_,_,steps) in seen if steps==i) for i in range(min_steps,max_steps+1)})
            return heat_lost

        for next_dir in directions:
            if next_dir == -prev_dir:  # can't reverse
                continue
            if next_dir==prev_dir:
                if dir_steps == max_steps:  # no more than max_steps in the same direction
                    continue
                next_steps = dir_steps+1
                steps = 1
            else:
                next_steps = min_steps
                steps = min_steps

            next_loc = loc+next_dir*steps

            if next_loc not in loss_grid:   # don't go outside of the grid
                continue
            
            step_locs = [loc+next_dir*(ix+1) for ix in range(steps)]
            step_loss = sum(loss_grid[g] for g in step_locs)
            next_cost = heat_lost + step_loss
            
            key = (next_loc,next_dir,next_steps)
            # if we reach the same point with fewer steps that is strictly better, so we can ignore it
            # this reduces the number of points to visit by quite a lot
            if any(seen.get((next_loc,next_dir,steps),1e9)<=next_cost for steps in range(min_steps,next_steps+1)):
                continue
            seen[key] = next_cost

            counter+=1
            heappush(to_do,(next_cost,counter,next_loc,next_dir,next_steps,path+[g for g in step_locs]))


inputs = [(1,3),(4,10)]

for q,(min_steps,max_steps) in enumerate(inputs,1):
    start_time = time.time()
    ans = solve(min_steps,max_steps)
    timer = time.time()-start_time
    print(f"ans{q}={ans}, {timer=:.2f}")
