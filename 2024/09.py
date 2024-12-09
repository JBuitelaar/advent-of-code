import time
from collections import deque
from aocd.models import Puzzle
from dotenv import load_dotenv

load_dotenv()

puzzle = Puzzle(2024, 9)

# data = puzzle.examples[0].input_data
data = puzzle.input_data

### PART 1 ###
start_time = time.time()

input = deque([int(v) for v in data.strip()])

right_file = input.pop()
left_id = -1
right_id = len(input) // 2
res = []
try:
    while True:
        # first there's a file...
        file = input.popleft()
        left_id += 1
        for _ in range(file):
            res.append(left_id)

        # ...followed by space to fill
        space = input.popleft()
        for _ in range(space):
            if right_file == 0:
                input.pop()  # throw away the empty space
                right_file = input.pop()
                right_id -= 1
            res.append(right_id)
            right_file -= 1
except IndexError:
    for _ in range(min(space, right_file)):
        res.append(right_id)

ans1 = sum(ix * v for ix, v in enumerate(res))

timer = time.time() - start_time
print(f"{ans1=}, {timer=:.2f}s")

### PART 2 ###
input = deque([int(v) for v in data.strip()])

files = []
spaces = []
val = 0
loc = 0
try:
    while True:
        file_size = input.popleft()
        files.append((loc, file_size, val))
        loc += file_size
        space = input.popleft()
        spaces.append((loc, space))
        loc += space
        val += 1
except IndexError:
    pass

done = []
try:
    while True:
        file = files.pop()
        (loc, file_size, val) = file
        try:
            ix, new_loc, space = next(
                (ix, loc, space)
                for ix, (loc, space) in enumerate(spaces)
                if space >= file_size
            )
        except StopIteration:
            # file doesn't move:
            done.append(file)
        else:
            # file moves to new_loc. Update the free space:
            spaces[ix] = (new_loc + file_size, space - file_size)
            done.append((new_loc, file_size, val))
        # this space is after the next file to move and we never move backwards:
        spaces.pop()
except IndexError:
    done.extend(files)

ans2 = sum(sum(range(loc, loc + length)) * val for loc, length, val in done)

timer = time.time() - start_time
print(f"{ans2=}, {timer=:.2f}s")
# submit(ans2)
