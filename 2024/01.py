import time
from collections import Counter
from aocd.models import Puzzle

puzzle = Puzzle(2024, 1)
data = puzzle.input_data
# data = puzzle.examples[0].input_data
# print(data)

start_time = time.time()

lines = data.strip().split("\n")

list1, list2 = [], []

for line in lines:
    v1, v2 = map(int, line.split())
    list1.append(v1)
    list2.append(v2)

ans1 = sum(abs(y - x) for x, y in zip(sorted(list1), sorted(list2)))
timer = time.time() - start_time

print(f"{ans1=}, {timer=:.2f}s")

counts = Counter(list2)
ans2 = sum(v * counts.get(v, 0) for v in list1)
timer = time.time() - start_time
print(f"{ans2=}, {timer=:.2f}s")
