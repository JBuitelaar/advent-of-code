import time
from functools import cache
from aocd.models import Puzzle
from dotenv import load_dotenv

load_dotenv()

puzzle = Puzzle(2024, 19)

# data = puzzle.examples[0].input_data
# print(f"Example: \n{data}\n{"="*80}")

data = puzzle.input_data
towels_str, design_str = data.strip().split("\n\n")

towels = towels_str.split(", ")

designs = design_str.split("\n")

### PART 1 ###


@cache
def is_possible(design):
    if design == "":
        return True

    return any(
        is_possible(design[len(towel) :])
        for towel in towels
        if design.startswith(towel)
    )


start_time = time.time()

ans1 = sum(is_possible(design) for design in designs)
timer = time.time() - start_time
print(f"{ans1=}, {timer=:.2f}s")


### PART 2 ###


@cache
def design_count(design):
    if design == "":
        return 1

    return sum(
        design_count(design[len(towel) :])
        for towel in towels
        if design.startswith(towel)
    )


ans2 = sum(design_count(design) for design in designs)

timer = time.time() - start_time
print(f"{ans2=}, {timer=:.2f}s")
