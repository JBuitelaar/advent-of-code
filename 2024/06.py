import time
from collections import defaultdict
from aocd.models import Puzzle
from copy import deepcopy

puzzle = Puzzle(2024,6)
data = puzzle.input_data
# data = puzzle.examples[0].input_data

start_time = time.time()

lines = data.strip().split('\n')

grid = {r+1j*c: v for r,row in enumerate(lines) for c,v in enumerate(row)}
guard = next(loc for loc,v in grid.items() if v=='^')
dir = -1

def turn_right(direction):  # 90 degrees
    return direction*-1j

def solve1(grid,guard,dir):
    visited = {guard}
    while True:
        new = guard + dir
        if new not in grid:
            return len(visited)
        if grid[new] == '#':
            dir = turn_right(dir)
        else:
            guard=new
            visited.add(guard)

    

ans1=solve1(grid,guard,dir)
timer = time.time() - start_time
print(f"{ans1=}, {timer=:.2f}s")


# visited states, stored as location mapped to set of directions
visited = defaultdict(set)
visited[guard].add(dir)

def is_loop(grid,guard,dir,visited):
    extra_block = guard+dir
    grid[extra_block] = '#'
    while True:
        new = guard + dir
        if new not in grid:
            return False
        if new in visited and dir in visited[new]:
            return True
        if grid[new] == '#':
            dir = turn_right(dir)
        else:
            guard = new
            visited[guard].add(dir)


extra_locs=set()
while True:
    new = guard + dir
    if new not in grid:
        break
    if grid[new] == '#':
        dir = turn_right(dir)
    else:
        guard = new
        visited[guard].add(dir)
    # if we can place a new block in front, see if that results in a loop:
    nxt = guard+dir
    if  nxt in grid and grid[nxt]!="#" and nxt not in extra_locs and nxt not in visited and is_loop(grid.copy(),guard,dir,deepcopy(visited)):
        extra_locs.add(nxt)

ans2=len(extra_locs)

timer = time.time() - start_time
print(f"{ans2=}, {timer=:.2f}s")


