import time
import itertools
from aocd.models import Puzzle

puzzle = Puzzle(2025, 2)

# data = puzzle.examples[0].input_data.replace("\n","")
data = puzzle.input_data
ranges = data.split(",")

start_time = time.time()

ans1 = ans2 = 0

for this_range in ranges:
    valid_ids = set()

    start, end = this_range.split("-")
    start_digits = len(start)

    for n_reps in range(2, len(end) + 1):
        if start_digits % n_reps:
            # if the start number contains a number of digits that can't be evenly divided into n_reps parts,
            # we can start with the smallest number with the correct number of digits.
            # number of digits is given by rounding up:
            first_candidate = 10 ** (start_digits // n_reps)
        else:
            first_candidate = int(start[: (start_digits) // n_reps])

        start_val = int(start)
        stop_at = int(end)
        for val in itertools.count(first_candidate):
            dup = int(str(val) * n_reps)
            if dup < start_val:
                continue
            if dup > stop_at:
                break
            valid_ids.add(dup)
            if n_reps == 2:
                ans1 += dup
    ans2 += sum(valid_ids)

timer = time.time() - start_time
print(f"{ans1=}, {ans2=}, {timer=:.2f}s")
