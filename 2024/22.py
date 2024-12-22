import time
from collections import defaultdict
from aocd.models import Puzzle
from dotenv import load_dotenv

load_dotenv()

puzzle = Puzzle(2024, 22)

data = puzzle.input_data
lines = data.strip().split("\n")
initial_numbers = [int(n) for n in lines]

start_time = time.time()

### PART 1 ###

iterations = 2000


def mix_and_prune(secret, v):
    return (secret ^ v) % 2**24


def calc_next(n):
    n = mix_and_prune(n, n * 64)
    n = mix_and_prune(n, n // 32)
    n = mix_and_prune(n, n * 2048)
    return n


def calc_part1(initial_number):
    n = initial_number
    for _ in range(iterations):
        n = calc_next(n)
    return n


ans1 = sum(calc_part1(n) for n in initial_numbers)

timer = time.time() - start_time
print(f"{ans1=}, {timer=:.2f}s")

### PART 2 ###


def price_by_seq(initial_number):
    seq_len = 4
    n = initial_number
    prices = [n % 10]
    for _ in range(iterations):
        n = calc_next(n)
        prices.append(n % 10)
    changes = [prices[i + 1] - prices[i] for i in range(iterations)]
    res = {}
    for start_ix in range(iterations + 1 - seq_len):
        key = tuple(changes[start_ix : start_ix + seq_len])
        if key not in res:
            res[key] = prices[start_ix + 4]
    return res


def get_total(initial_numbers):
    res = defaultdict(int)
    for initial_number in initial_numbers:
        changes = price_by_seq(initial_number)
        for key, price in changes.items():
            res[key] += price
    return max(res.values())


ans2 = get_total(initial_numbers)

timer = time.time() - start_time
print(f"{ans2=}, {timer=:.2f}s")
