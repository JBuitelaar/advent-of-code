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
print(f"{data=}")

numberpad = [[7, 8, 9], [4, 5, 6], [1, 2, 3], [None, 0, "A"]]
npl = {
    str(numberpad[r][c]): r + c * 1j
    for r in range(4)
    for c in range(3)
    if numberpad[r][c] is not None
}
npl2 = {loc: v for v, loc in npl.items()}
dirpad = [[None, "^", "a"], ["<", "v", ">"]]
dpl = {
    dirpad[r][c]: 10 + r + (10 + c) * 1j
    for r in range(2)
    for c in range(3)
    if dirpad[r][c]
}
npl2.update({loc: v for v, loc in dpl.items()})

moves = {1: "v", -1: "^", 1j: ">", -1j: "<"}


def move_presses(start, target):
    # print(start,target)
    if start == target:
        return ["a"]
    res = []
    if start.imag != target.imag:
        move = 1j if target.imag > start.imag else -1j
        if start + move in npl2:
            for sub in move_presses(start + move, target):
                res.append(moves[move] + sub)

    if start.real != target.real:
        move = 1 if target.real > start.real else -1
        if start + move in npl2:
            for sub in move_presses(start + move, target):
                res.append(moves[move] + sub)
    return res


@cache
def move_key(start, target):
    return move_presses(npl[start], npl[target])


@cache
def move_arrow(start, target):
    return move_presses(dpl[start], dpl[target])


def steps_key(code, start="A"):
    ch, *rest_code = code
    key_arrows = move_key(start, ch)
    if not rest_code:
        return key_arrows
    next = steps_key(rest_code, ch)
    res = []
    for key_arrow in key_arrows:
        for n in next:
            res.append(key_arrow + n)
    return res


@cache
def steps_dir_all(code, start="a"):
    ch = code[0]
    rest_code = code[1:]
    # ch,*rest_code=code
    key_arrows = move_arrow(start, ch)
    if not rest_code:
        return key_arrows
    next = steps_dir_all(rest_code, ch)
    res = []
    for key_arrow in key_arrows:
        for n in next:
            res.append(key_arrow + n)
    # if len(res)>1:
    #     print(f"{code=}: {res}")

    return res


def length(arrc):
    return sum((len(k) + 1) * v for k, v in arrc.items())


@cache
def min_length(arrows, step):
    if step == 0:
        return len(arrows)
    subs = arrows[:-1].split("a")

    return sum(
        min(min_length(opt, step - 1) for opt in options)
        for options in (steps_dir_all(sub + "a") for sub in subs)
    )


lines = data.strip().split("\n")


def solve(dir_count):
    ans1 = 0
    for line in lines:
        num = int(line[:-1])
        keys = steps_key(line)
        v = min(min_length(k, dir_count) for k in keys)
        # print(line,v,num)
        ans1 += v * num
    return ans1


start_time = time.time()

ans1 = solve(2)

timer = time.time() - start_time
print(f"{ans1=}, {timer=:.2f}s")

ans2 = solve(25)

timer = time.time() - start_time
print(f"{ans2=}, {timer=:.2f}s")
