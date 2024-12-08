import time
from collections import defaultdict
from aocd.models import Puzzle

puzzle = Puzzle(2024, 5)
data = puzzle.input_data
# data = puzzle.examples[0].input_data

start_time = time.time()
[rules, updates_str] = data.strip().split("\n\n")

before = defaultdict(set)
for rule in rules.split("\n"):
    # we don't need to convert to int, we can just compare the strings
    v1, v2 = rule.split("|")
    before[v2].add(v1)


def is_valid(vals):
    for i, v in enumerate(vals):
        if set(vals[i + 1 :]) & before[v]:
            return False
    return True


ans1 = ans2 = 0
for update in updates_str.split("\n"):
    vals = update.split(",")
    med_ix = len(vals) // 2

    if is_valid(vals):
        ans1 += int(vals[med_ix])
    else:
        # sort only the first half:
        ix = 0
        while ix <= med_ix:
            val = vals[ix]
            if set(vals[ix + 1 :]) & before[val]:
                # don't bother inserting, just move it to the very end
                vals.append(vals.pop(ix))
            else:
                ix += 1
        ans2 += int(val)

timer = time.time() - start_time
print(f"{ans1=}, {ans2=}, {timer=:.4f}s")
