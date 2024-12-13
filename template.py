import re
import sys
import time
import itertools
import math
from collections import defaultdict, Counter, deque
from functools import reduce, cache
from dataclasses import dataclass
from aocd.models import Puzzle
from dotenv import load_dotenv
sys.setrecursionlimit(10**6)

load_dotenv()

puzzle = Puzzle(2024, 9)

from aocd import submit

# Throw this away before committing:
import webbrowser
from datetime import datetime, UTC

unlock = puzzle.unlock_time(local=False)
wait_time = (unlock - datetime.now(UTC)).total_seconds()
if wait_time > 300:
    print(f"problem available in {int(wait_time)//60} minutes. Try again later")
    exit()
elif wait_time > 0:
    print(f"problem available in {wait_time} seconds. Waiting...")
    time.sleep(wait_time + 0.01)
webbrowser.open(puzzle.url)


data = puzzle.examples[0].input_data
print(f"Example: \n{data}\n{"="*80}")

# data = puzzle.input_data
# print(data[:300],"...")

start_time = time.time()
### PART 1 ###
ans1 = 0

lines = data.strip().split("\n")
# [line for line in lines]
# ns = [list(map(int, re.findall("\\d+", line))) for line in lines]
for line in lines:
    vals = line.split()





timer = time.time() - start_time
print(f"{ans1=}, {timer=:.2f}s")
# submit(ans1)

### PART 2 ###
ans2 = 0




timer = time.time() - start_time
print(f"{ans2=}, {timer=:.2f}s")
# submit(ans2)
