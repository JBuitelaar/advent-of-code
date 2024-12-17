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

    output = []
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
                output.append(combo(operand) % 8)
            case 0 | 6 | 7:
                # these opcodes have the same operation, but just write to a different registry
                regs[opcode % 5] = regs[0] // 2 ** combo(operand)
            case _:
                raise ValueError(opcode)
        pointer += 2
    return tuple(output)


first_output = run_program(registers, program)
ans1 = ",".join([str(v) for v in first_output])

timer = time.time() - start_time
print(f"{ans1=}, {timer=:.2f}s")

### PART 2 ###


# Looking at the program, it's basically this:
# We can see that the initial value of B and C don't matter, because they get set at the beginning.
def run_program2(A):
    output = []
    while A:
        B = A % 8
        B = B ^ 1
        C = A // 2**B % 8  # added %8
        A //= 8
        B = B ^ C
        B = B ^ 6
        out = B % 8
        output.append(out)
    return tuple(output)


# verify that this is true:
assert run_program2(registers[0]) == first_output

"""
Now we see that in every iteration A is divided by 8 and nothing else happens to it.
Since all operations are bitwise, if we write A in binary, we basically chop off the last 3 bits.
So at the last iteration before 0, the value must be between 1 and 7. 
We can try all these 7 numbers to see which one produces the LAST output.
That way we find the first 3 bits of A.
Now going one step back, we have a 6-bit number. We already know the first 3, so again we have
to only check the 8 options for the last 3 bits to produce the 2nd last output.
This we can repeat until we have found the value for A that produces all outputs.

Note that there can be multiple solutions in each step, but not all might work later on. 
So we need to keep track of all possible values for A.

For this we really only need to know the first output that is produced by a number. 
That simplifies the program even further:
"""


def first_output(A):
    B = A % 8
    B = B ^ 1
    C = A // 2**B
    B = B ^ C
    B = B ^ 6
    return B % 8


candidates = [0]
for ix, val in enumerate(reversed(program)):
    range_start = (
        ix == 0
    )  # first iteration can not be 0, as that would exit the program
    new_candidates = []
    for A in candidates:
        A *= 8
        for new_bits in range(range_start, 8):
            v = A + new_bits
            if first_output(v) == val:
                new_candidates.append(v)
    assert len(new_candidates)
    candidates = new_candidates

# print(f"{candidates=}")
# All candidates create the same output:
assert all(run_program2(c) == program for c in candidates)

ans2 = min(candidates)

timer = time.time() - start_time
print(f"{ans2=}, {timer=:.2f}s")
