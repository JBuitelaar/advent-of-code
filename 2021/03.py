import time
from aocd.models import Puzzle

puzzle = Puzzle(2021, 3)
data = puzzle.input_data
# data = puzzle.examples[0].input_data

start_time = time.time()

lines = data.strip().split("\n")
num_binaries = len(lines)
length = len(lines[0])
gamma = ""
epsilon = ""
for b in range(length):
    count = sum(int(line[b]) for line in lines)
    if count > num_binaries // 2:
        gamma += "1"
        epsilon += "0"
    else:
        gamma += "0"
        epsilon += "1"
ans1 = int(gamma, 2) * int(epsilon, 2)

timer = time.time() - start_time
print(f"{ans1=}, {timer=:.2f}s")


def get_score(candidates, oxygen=True):
    length = len(candidates[0])
    for b in range(length):
        num_binaries = len(candidates)
        count = sum(int(line[b]) for line in candidates)
        keep = "1" if (count >= num_binaries / 2) == oxygen else "0"
        candidates = [line for line in candidates if line[b] == keep]
        if len(candidates) == 1:
            break

    return int(candidates[0], 2)


ans2 = get_score(lines.copy(), True) * get_score(lines.copy(), False)

timer = time.time() - start_time
print(f"{ans2=}, {timer=:.2f}s")
