import itertools
import math
from aocd.models import Puzzle

puzzle = Puzzle(2023,8)
data = puzzle.input_data
# example = puzzle.examples[0]
# data = example.input_data
# print("example answers: ",example.answer_a, example.answer_b)
# print(data)

lines = data.strip().split('\n')
dirs = [int(c=="R") for c in lines[0]]
mapping = {ln[0:3]: (ln[7:10], ln[12:15]) for ln in lines[2:]}

loc = "AAA"
for step, direction in enumerate(itertools.cycle(dirs),1):
    loc = mapping[loc][direction]
    if loc == "ZZZ":
        ans1 = step
        break

print(f"{ans1=}")

def count_until(loc):
    for step, direction in enumerate(itertools.cycle(dirs),1):
        loc = mapping[loc][direction]
        if loc.endswith("Z"):
            return step, loc
            
start_locs = [k for k in mapping.keys() if k[2] == "A"]
res = [count_until(start_loc) for start_loc in start_locs]
steps = [r[0] for r in res]

ans2 = math.lcm(*steps)
print(f"{ans2=}")

# this can only work if the cycle repeats:
res2 = [count_until(r[1]) for r in res]
assert res2 == res
# and the directions also repeats at every cycle
assert all(v==int(v) for v in [s/len(dirs) for s in steps])
