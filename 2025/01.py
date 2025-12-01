import time
from aocd.models import Puzzle

puzzle = Puzzle(2025, 1)

data = puzzle.input_data

start_time = time.time()

ans1 = ans2 = 0
lines = data.strip().split("\n")
loc = 50

for line in lines:
    steps = int(line[1:])
    ans2 += steps // 100
    steps %= 100

    move = 1 if line[0] == "L" else -1

    for j in range(steps):
        loc = (loc + move) % 100
        if loc == 0:
            ans2 += 1
    if loc == 0:
        ans1 += 1

timer = time.time() - start_time
print(f"{ans1=}, {ans2=}, {timer=:.2f}s")
