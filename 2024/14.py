import re
import time
import itertools
from collections import defaultdict
from functools import reduce
from aocd.models import Puzzle
from dotenv import load_dotenv

load_dotenv()

puzzle = Puzzle(2024, 14)

# data = puzzle.examples[0].input_data
# width = 11
# height = 7
# print(f"Example: \n{data}\n{"="*80}")

data = puzzle.input_data
width = 101
height = 103

lines = data.strip().split("\n")
vals = [list(map(int, re.findall("-?\d+", line))) for line in lines]
robots = [(px + py * 1j, vx + vy * 1j) for px, py, vx, vy in vals]


### PART 1 ###
start_time = time.time()

seconds = 100
divx = width // 2
divy = height // 2


def print_grid(locs):
    for r in range(height):
        row = "".join(str(locs.get(c + 1j * r, ".")) for c in range(width))
        print(row)


def get_locs(robots, steps):
    locs = defaultdict(int)
    for loc, vel in robots:
        loc += steps * vel
        loc = (loc.real % width) + (loc.imag % height) * 1j
        locs[loc] += 1
    return locs


locs = get_locs(robots, seconds)

quadrants = [0] * 4

for loc in locs:
    if loc.imag == (height - 1) / 2 or loc.real == (width - 1) / 2:
        continue
    quadrant = (loc.real > divx) + (loc.imag > divy) * 2
    quadrants[quadrant] += 1

ans1 = reduce(lambda a, b: a * b, quadrants)

timer = time.time() - start_time
print(f"{ans1=}, {timer=:.2f}s")


### PART 2 ###

dirs = -1, 1, -1j, 1j

for seconds in itertools.count():
    robot_locations = get_locs(robots, seconds)

    locs = set(robot_locations.keys())
    if not seconds % 1000:
        print(f"{seconds} seconds...")

    # To make a picture, you would expect many robots to be connected.
    # So let's find the largest connected group and print:
    max_size = 0
    while locs:
        size = 0
        robot = locs.pop()
        to_do = [robot]
        while to_do:
            loc = to_do.pop()
            neighbours = [loc + d for d in dirs]
            for nb in neighbours:
                if nb in locs:
                    locs.remove(nb)
                    to_do.append(nb)
                    size += 1

        if size > max_size:
            max_size = size

    if max_size > 20:
        ans2 = seconds
        break

timer = time.time() - start_time
print(f"{ans2=}, {timer=:.2f}s")

print_grid(robot_locations)
