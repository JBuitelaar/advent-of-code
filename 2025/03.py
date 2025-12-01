import time
from aocd.models import Puzzle

puzzle = Puzzle(2025, 3)

# data = puzzle.examples[0].input_data
data = puzzle.input_data
# print(data[:300],"...")

start_time = time.time()

banks = data.strip().split("\n")


# bank=banks[0]
def solve(bank, digits):
    vals = tuple(map(int, bank))
    length = len(vals)
    joltage = 0
    index_max = -1
    for offset in range(digits - 1, -1, -1):
        joltage *= 10
        index_max = max(range(index_max + 1, length - offset), key=vals.__getitem__)
        joltage += vals[index_max]
    return joltage


### PART 1 ###
ans1 = sum(solve(bank, 2) for bank in banks)
timer = time.time() - start_time
print(f"{ans1=}, {timer=:.2f}s")

### PART 2 ###
ans2 = sum(solve(bank, 12) for bank in banks)
timer = time.time() - start_time
print(f"{ans2=}, {timer=:.2f}s")
