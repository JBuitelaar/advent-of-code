import time
from aocd.models import Puzzle
from dotenv import load_dotenv

load_dotenv()

puzzle = Puzzle(2024, 25)

# data = puzzle.examples[0].input_data
data = puzzle.input_data

keylocks_strs = data.strip().split("\n\n")

start_time = time.time()
### PART 1 ###

keys = []
locks = []
for keylock_str in keylocks_strs:
    pattern = {
        r + 1j * c
        for r, row in enumerate(keylock_str.split("\n")[1:-1])
        for c, v in enumerate(row)
        if v == "#"
    }
    if keylock_str[0] == "#":
        locks.append(pattern)
    else:
        keys.append(pattern)

ans1 = sum(all(v not in key for v in lock) for key in keys for lock in locks)

timer = time.time() - start_time
print(f"{ans1=}, {timer=:.2f}s")
