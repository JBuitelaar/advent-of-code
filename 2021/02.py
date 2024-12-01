import time
from aocd.models import Puzzle

puzzle = Puzzle(2021, 2)
data = puzzle.input_data

start_time = time.time()

lines = data.strip().split("\n")

hor = 0
depth = 0
for line in lines:
    action, count_str = line.split()
    count = int(count_str)
    match action:
        case "forward":
            hor += count
        case "down":
            depth += count
        case "up":
            depth -= count
        case other:
            print(action)

ans1 = hor * depth
timer = time.time() - start_time
print(f"{ans1=}, {timer=:.2f}s")

hor = 0
aim = 0
depth = 0
for line in lines:
    action, count_str = line.split()
    count = int(count_str)
    match action:
        case "forward":
            hor += count
            depth += aim * count
        case "down":
            aim += count
        case "up":
            aim -= count
        case other:
            raise ValueError(action)

ans2 = hor * depth

timer = time.time() - start_time
print(f"{ans2=}, {timer=:.2f}s")
