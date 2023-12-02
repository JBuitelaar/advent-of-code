import re
from pathlib import Path
from copy import deepcopy

with open(Path(__file__).parent / "input.txt", encoding="utf-8") as f:
    txt = f.read()

start_pos, instructions = txt.split("\n\n")

start_stacks = [[] for _ in range(9)]

for line in reversed(start_pos.split("\n")[:-1]):
    crates = [line[d+1] for d in range(0,len(line),4)]
    for i, crate in enumerate(crates):
        if crate != " ":
            start_stacks[i].append(crate)

print(start_stacks)
all_stacks = deepcopy(start_stacks)
print(start_pos)


reg = r"^move (\d+) from (\d+) to (\d+)$"

for line in instructions.split("\n"):
    m = re.match(reg, line)
    assert m, line
    (amount, source, target) = map(int, m.groups())
    for _ in range(amount):
        all_stacks[target-1].append(all_stacks[source-1].pop())

print("".join(s[-1] for s in all_stacks))

all_stacks = deepcopy(start_stacks)

for line in instructions.split("\n"):
    m = re.match(reg, line)
    assert m, line
    (amount, source, target) = map(int, m.groups())
    to_move = all_stacks[source-1][-amount:]
    all_stacks[source-1] = all_stacks[source-1][:-amount]
    all_stacks[target-1].extend(to_move)

print("".join(s[-1] for s in all_stacks))
