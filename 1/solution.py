from aocd.models import Puzzle

puzzle = Puzzle(2023,1)
data = puzzle.input_data
lines = data.strip().split('\n')

def get_number_1(_line,_ix,char):
    return int(char)

digits = ["one","two","three","four","five","six","seven","eight","nine"]
digit_map = dict(zip(digits,range(1,10)))

def get_number_2(line,ix,char):
    try:
        val = int(char)
        return val
    except ValueError:
        for digit, value in digit_map.items():
            if line[ix:].startswith(digit):
                return value
    raise ValueError("Could not find number")


def solve(lines,get_number_fun):
    sum = 0
    for line in lines:
        first = None
        last = None
        for ix, char in enumerate(line):
            try:
                val = get_number_fun(line,ix,char)
            except ValueError:
                continue
            if first is None:
                first = val
            last = val
        number = 10*first+last
        sum+=number
    return sum

solution_1 = solve(lines,get_number_1)
print(f"{solution_1=}")

solution_2 = solve(lines,get_number_2)
print(f"{solution_2=}")