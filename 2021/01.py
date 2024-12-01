import time
from aocd.models import Puzzle

puzzle = Puzzle(2021, 1)
data = puzzle.input_data
# data = puzzle.examples[0].input_data

start_time = time.time()

lines = data.strip().split("\n")
depths = [int(line) for line in lines]
ans1 = sum(b > a for a, b in zip(depths[:-1], depths[1:]))

timer = time.time() - start_time
print(f"{ans1=}, {timer=:.2f}s")

ans2 = sum(b > a for a, b in zip(depths[:-3], depths[3:]))
print(f"{ans2=}, {timer=:.2f}s")
