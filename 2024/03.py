import re
import time
from aocd.models import Puzzle

puzzle = Puzzle(2024, 3)
input_str = puzzle.input_data
# input_str = puzzle.examples[0].input_data

start_time = time.time()

MUL_PATTERN = r"mul\(\d+,\d+\)"


def mult(mul_str):
    vals = re.findall(r"\d+", mul_str)
    return int(vals[0]) * int(vals[1])


matches = re.findall(MUL_PATTERN, input_str)
ans1 = sum(mult(match) for match in matches)
timer = time.time() - start_time
print(f"{ans1=}, {timer=:.2f}s")


# input_str="xmul(2,4)&mul[3,7]!^don't()_mul(5,5)+mul(32,64](mul(11,8)undo()?mul(8,5))"

DO = "do()"
DONT = "don't()"

matches = re.findall("|".join([re.escape(DO), re.escape(DONT), MUL_PATTERN]), input_str)

ans2 = 0
on = True
for match in matches:
    if match == DONT:
        on = False
    elif match == DO:
        on = True
    elif not on:
        continue
    else:
        assert match.startswith("mul"), f"Error: {match=}, {DONT=}"
        ans2 += mult(match)

timer = time.time() - start_time
print(f"{ans2=}, {timer=:.2f}s")
