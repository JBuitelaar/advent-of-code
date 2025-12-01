import time
from operator import add, mul
from functools import reduce
from aocd.models import Puzzle

puzzle = Puzzle(2025, 6)

# data = puzzle.examples[0].input_data
data = puzzle.input_data
# print(data[:300],"...")

start_time = time.time()

lines = data.strip().split("\n")
*num_lines, op_line = lines
operators = [add if op == "+" else mul for op in op_line.split()]

### PART 1 ###
numbers = [list(map(int, line.split())) for line in num_lines]
ans1 = sum(reduce(op, vals) for op, vals in zip(operators, zip(*numbers)))

timer = time.time() - start_time
print(f"{ans1=}, {timer=:.2f}s")

### PART 2 ###

groups = [[]]

for chars in zip(*num_lines):
    row = "".join(chars).strip()
    if row == "":
        groups.append([])
    else:
        groups[-1].append(int(row))

ans2 = sum(reduce(op, vals) for op, vals in zip(operators, groups))

timer = time.time() - start_time
print(f"{ans2=}, {timer=:.2f}s")
# submit(ans2)
