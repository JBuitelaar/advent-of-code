from aocd.models import Puzzle

puzzle = Puzzle(2019,1)
data = puzzle.input_data

masses = [int(v) for v in data.strip().split('\n')]

ans1 = sum(m//3-2 for m in masses)
print(f"{ans1=}")

def fuel_required(mass):
    res = mass//3-2
    if res<=0:
        return 0
    return res + fuel_required(res)

ans2 = sum(fuel_required(m) for m in masses)
print(f"{ans2=}")
