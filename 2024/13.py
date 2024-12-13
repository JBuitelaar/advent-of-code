import re
import time
from aocd.models import Puzzle
from dotenv import load_dotenv
import sys
from sympy.solvers.simplex import lpmin
from sympy import Eq
from sympy import symbols
from sympy.solvers.simplex import InfeasibleLPError
from sympy import solve

sys.setrecursionlimit(10**6)
load_dotenv()

puzzle = Puzzle(2024, 13)

# data = puzzle.examples[0].input_data
# print(f"Example: \n{data}\n{"="*80}")
data = puzzle.input_data


def cost(ax, ay, bx, by, x, y):
    """Calculate cost by solving the equations manually

    We have:
    ax*A+bx*B=x
    ay*A+by*B=y
    We want to minimize 3A+B
    Multiply the first equation by ay and the second by ax and subtract, so A drops out:
    (bx*ay-by*ax)*B=x*ay-y*ax
    If this has an integer solution we can back out A by filling B into the first (or second) equation
    The numbers also can't be negative

    Note there could be multiple solutions, but that's not the case here.
    So also no need to check for the minimum cost.
    """
    bb = bx * ay - by * ax
    z = x * ay - y * ax
    assert not (bb == 0 and z == 0)  # multiple solutions
    b, mod = divmod(z, bb)

    if mod != 0 or b < 0:
        return 0

    a = (x - b * bx) // ax
    if a < 0:
        return 0

    return a * 3 + b


A, B = symbols("A B", integer=True, positive=True)


def cost_sympy_min(ax, ay, bx, by, x, y):
    """Calculate cost by solving the minimization problem using sympy

    This is more generic, as there could be multiple solutions. In practice, there aren't.
    """

    try:
        ans, vals = lpmin(
            A * 3 + B, [Eq(A * ax + B * bx, x), Eq(ay * A + by * B, y), A >= 0, B >= 0]
        )
    except InfeasibleLPError:
        return 0
    else:
        if all(val.is_integer for val in vals.values()):
            return ans
        else:
            return 0


def cost_sympy(ax, ay, bx, by, x, y):
    """Calculate cost by solving the equations using sympy"""
    ans = solve([Eq(A * ax + B * bx, x), Eq(ay * A + by * B, y)], [A, B])
    if ans:
        return ans[A] * 3 + ans[B]
    else:
        return 0


def calculate_cost(machine, cost_calculator, increment=0):
    ax, ay, bx, by, x, y = map(int, re.findall("\\d+", machine))
    x += increment
    y += increment
    return cost_calculator(ax, ay, bx, by, x, y)


# several ways to solve it:
cost_calculator = cost
# cost_calculator=cost_sympy
# cost_calculator=cost_sympy_min

### PART 1 ###
start_time = time.time()
machines = data.split("\n\n")

ans1 = sum(calculate_cost(machine, cost_calculator) for machine in machines)
timer = time.time() - start_time
print(f"{ans1=}, {timer=:.2f}s")

### PART 2 ###
incr = 10000000000000
ans2 = sum(calculate_cost(machine, cost_calculator, incr) for machine in machines)
timer = time.time() - start_time
print(f"{ans2=}, {timer=:.2f}s")
