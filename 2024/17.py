import re
import time
from aocd.models import Puzzle
from dotenv import load_dotenv

load_dotenv()

puzzle = Puzzle(2024, 17)

data = puzzle.input_data

register_str, program_str = data.split("\n\n")
registers = tuple(map(int, re.findall(r"\d+", register_str)))
program = tuple(map(int, re.findall(r"\d+", program_str)))

start_time = time.time()

### PART 1 ###


def run_program(registers, instructions):
    regs = list(registers)

    def combo(operand):
        assert operand < 7
        return regs[operand - 4] if operand > 3 else operand

    res = []
    pointer = 0
    while pointer < len(instructions):
        opcode = instructions[pointer]
        operand = instructions[pointer + 1]

        match opcode:
            case 1:
                regs[1] = regs[1] ^ operand
            case 2:
                regs[1] = combo(operand) % 8
            case 3:
                if regs[0]:
                    pointer = operand
                    continue
            case 4:
                regs[1] = regs[1] ^ regs[2]
            case 5:
                res.append(combo(operand) % 8)
            case 0 | 6 | 7:
                # these opcodes have the same operation, but just write to a different registry
                regs[opcode % 5] = regs[0] // 2 ** combo(operand)
            case _:
                raise ValueError(opcode)
        pointer += 2
    return tuple(res)


res = run_program(registers, program)
ans1 = ",".join([str(v) for v in res])

timer = time.time() - start_time
print(f"{ans1=}, {timer=:.2f}s")


""" ### PART 2 ###
Looking at the program, it basically does this:

    output = []
    while A:
        B = A % 8
        B = B ^ 1
        C = A // 2**B
        A //= 8
        B = B ^ C
        B = B ^ 6
        out = B % 8
        output.append(out)

From this we can see that the inputs B and C don't matter, because they get overwritten at the beginning of the loop.
We can rewrite this to:
"""


def output(A):
    B = A % 8
    B = B ^ 1
    C = A // 2**B
    B = B ^ C
    B = B ^ 6
    return B % 8


def run_program2(A):
    res = []
    while A:
        res.append(output(A))
        A //= 8
    return tuple(res)


# verify that this is true:
assert run_program2(registers[0]) == res

"""
If we would write A in base 8, we chop off the last digit in every iteration (A//=8).
So we can work backwards. The first (base-8) digit of A should produce the last output.
I don't know how to invert the output function, but we can simply try every value 1-7
(not 0, because the program would have stopped in the previous iteraton).

For the second last output, we need a 2-digit number, where we already know the first one from previous step.
Again we can try every value for this digit, this time 0 is also allowed.

Note in every step there can be multiple solutions, but not every solution might be feasible in the next steps.
So we keep track of all options.
We end up with several potential values for A and we take the minimum.
"""

base = 8

candidates = [0]
for ix, val in enumerate(reversed(program)):
    range_start = ix == 0  # first iteration can not be 0
    new_candidates = []
    for A in candidates:
        A *= base
        for new_bits in range(range_start, base):
            v = A + new_bits
            if output(v) == val:
                new_candidates.append(v)
    assert len(new_candidates)
    candidates = new_candidates

# print(f"{candidates=}")
# Check that all candidates create the same output:
assert all(run_program2(c) == program for c in candidates)

ans2 = min(candidates)

timer = time.time() - start_time
print(f"{ans2=}, {timer=:.2f}s")
