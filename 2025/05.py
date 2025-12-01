import time
from aocd.models import Puzzle

puzzle = Puzzle(2025, 5)

# data = puzzle.examples[0].input_data
data = puzzle.input_data
# print(data[:300],"...")

start_time = time.time()

p1, p2 = data.split("\n\n")
ranges = [tuple(map(int, rang.split("-"))) for rang in p1.split("\n")]
ingrs = [int(line) for line in p2.split("\n")]

### PART 1 ###


def is_in_range(n):
    return any(r[0] <= n <= r[1] for r in ranges)


ans1 = sum(is_in_range(ingr) for ingr in ingrs)
timer = time.time() - start_time
print(f"{ans1=}, {timer=:.2f}s")

### PART 2 ###
ans2 = 0
ranges = sorted(ranges)

start, end = ranges[0]
for nstart, nend in ranges[1:]:
    if nstart <= end + 1:
        end = max(end, nend)
    else:
        ans2 += end - start + 1
        start, end = nstart, nend

ans2 += end - start + 1
timer = time.time() - start_time
print(f"{ans2=}, {timer=:.2f}s")
