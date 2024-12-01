# copy template.py 2024/01.py
import re
import time
import itertools
import math
from collections import defaultdict, Counter, deque
from functools import reduce, cache
from dataclasses import dataclass
from aocd.models import Puzzle
from aocd import submit

puzzle = Puzzle(2024,1)
# data = puzzle.input_data
data = puzzle.examples[0].input_data
print(data)
# print(data[:1000])

start_time = time.time()

lines = data.strip().split('\n')
# [line for line in lines]
# ns = [list(map(int, re.findall("\\d+", line))) for line in lines]

ans1 = 0
timer = time.time() - start_time
print(f"{ans1=}, {timer=:.2f}s")
# submit(ans1)

ans2=0
timer = time.time() - start_time
print(f"{ans2=}, {timer=:.2f}s")


# submit(ans2)
