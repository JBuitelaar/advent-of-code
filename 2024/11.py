import time
from collections import defaultdict, Counter
from aocd.models import Puzzle
from dotenv import load_dotenv

load_dotenv()

puzzle = Puzzle(2024, 11)

data = puzzle.input_data
print("input: ", data)
start_time = time.time()


def blink(numbers):
    res = defaultdict(int)
    for val, count in numbers.items():
        if val == 0:
            res[1] += count
        else:
            half_len, mod = divmod(len(str(val)), 2)
            if mod == 0:
                for k in divmod(val, 10**half_len):
                    res[k] += count
            else:
                res[val * 2024] += count
    return res


# data = "125 17"

numbers = Counter(map(int, data.strip().split()))

for j in range(75):
    numbers = blink(numbers)
    if j == 24:
        ans1 = sum(numbers.values())

ans2 = sum(numbers.values())

timer = time.time() - start_time
print(f"{ans1=}, {ans2=}, {timer=:.2f}s")
