import time
from functools import cache
from aocd.models import Puzzle
from dotenv import load_dotenv

load_dotenv()

puzzle = Puzzle(2024, 21)


data = """
029A
980A
179A
456A
379A"""

data = puzzle.input_data


def read_pad(pad_list):
    return {
        str(val): r + c * 1j
        for r, row in enumerate(pad_list)
        for c, val in enumerate(row)
        if val != "."
    }


def inverse(d):
    return {v: k for k, v in d.items()}


number_pad = [[7, 8, 9], [4, 5, 6], [1, 2, 3], [".", 0, "A"]]
arrow_pad = [[".", "^", "a"], ["<", "v", ">"]]

number_locs = read_pad(number_pad)
number_grid = inverse(number_locs)

arrow_locs = read_pad(arrow_pad)
arrow_grid = inverse(arrow_locs)

moves = {1: "v", -1: "^", 1j: ">", -1j: "<"}


def move_presses(start, target, grid):
    if start == target:
        return ["a"]
    res = []
    if start.imag != target.imag:
        move = 1j if target.imag > start.imag else -1j
        if start + move in grid:
            for sub in move_presses(start + move, target, grid):
                res.append(moves[move] + sub)

    if start.real != target.real:
        move = 1 if target.real > start.real else -1
        if start + move in grid:
            for sub in move_presses(start + move, target, grid):
                res.append(moves[move] + sub)
    return res


@cache
def move_number(start, target):
    return move_presses(number_locs[start], number_locs[target], number_grid)


@cache
def move_arrow(start, target):
    return move_presses(arrow_locs[start], arrow_locs[target], arrow_grid)


def steps_number(code, start="A"):
    # arrows to press to make the numberpad robot enter the code
    ch, *rest_code = code
    key_arrows = move_number(start, ch)
    if not rest_code:
        return key_arrows
    next = steps_number(rest_code, ch)
    res = []
    for key_arrow in key_arrows:
        for n in next:
            res.append(key_arrow + n)
    return res


@cache
def steps_arrow(code, start="a"):
    # arrows to press to make the next (arrow) robot enter code
    ch = code[0]
    rest_code = code[1:]
    key_arrows = move_arrow(start, ch)
    if not rest_code:
        return key_arrows
    next = steps_arrow(rest_code, ch)
    res = []
    for key_arrow in key_arrows:
        for n in next:
            res.append(key_arrow + n)

    return res


@cache
def min_length(arrows, step):
    # step 1 is the robot we're controlling
    if step == 0:
        return len(arrows)
    if "a" in arrows[:-1]:
        subs = arrows[:-1].split("a")
        return sum(min_length(sub + "a", step) for sub in subs)

    options = steps_arrow(arrows)

    return min(min_length(opt, step - 1) for opt in options)


lines = data.strip().split("\n")


def solve(dir_count):
    ans1 = 0
    for line in lines:
        num = int(line[:-1])
        keys = steps_number(line)
        v = min(min_length(k, dir_count) for k in keys)
        ans1 += v * num
    return ans1


start_time = time.time()

ans1 = solve(2)

timer = time.time() - start_time
print(f"{ans1=}, {timer=:.2f}s")

ans2 = solve(25)

timer = time.time() - start_time
print(f"{ans2=}, {timer=:.2f}s")
