import time
from aocd.models import Puzzle

puzzle = Puzzle(2022, 9)
data = puzzle.input_data
# data = puzzle.examples[0].input_data
# print(data)
# data="""R 5
# U 8
# L 8
# D 3
# R 17
# D 10
# L 25
# U 20"""
# print(data[:1000])

lines = data.strip().split("\n")
rows = [(ln[0], int(ln[2:])) for ln in lines]


moves = dict(R=1, L=-1, U=1j, D=-1j)


def sign(v):
    return 1 if v > 0 else -1


def print_grid(visited):
    min_x = int(min(loc.real for loc in visited))
    min_y = int(min(loc.imag for loc in visited))
    max_x = int(max(loc.real for loc in visited))
    max_y = int(max(loc.imag for loc in visited))
    rows = [["."] * (max_x - min_x + 1) for _ in range(max_y - min_y + 1)]
    for loc in visited:
        rows[int(loc.imag) - min_y][int(loc.real) - min_x] = "#"

    for row in reversed(rows):
        print("".join(row))


def solve(rope_length):
    rope = [0] * rope_length
    visited = set()
    for d, n in rows:
        m = moves[d]
        for _ in range(n):
            for i, loc_t in enumerate(rope):
                if i == 0:
                    loc_t += m
                    loc_h = None  # to make lint happy
                else:
                    if abs(loc_h.imag - loc_t.imag) <= 1 and abs(loc_h.real - loc_t.real) <= 1:
                        pass
                    elif loc_h.imag != loc_t.imag and loc_h.real != loc_t.real:
                        loc_t += sign(loc_h.imag - loc_t.imag) * 1j
                        loc_t += sign(loc_h.real - loc_t.real)
                    elif loc_h.imag == loc_t.imag:
                        loc_t += sign(loc_h.real - loc_t.real)
                    else:
                        loc_t += sign(loc_h.imag - loc_t.imag) * 1j
                    if i == len(rope) - 1:
                        visited.add(loc_t)
                loc_h = loc_t
                rope[i] = loc_t
    # print_grid(visited)
    return len(visited)


start_time = time.time()
ans1 = solve(2)
timer = time.time() - start_time
print(f"{ans1=}, {timer=:.2f}s")

ans2 = solve(10)
timer = time.time() - start_time
print(f"{ans2=}, {timer=:.2f}s")
