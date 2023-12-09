from aocd.models import Puzzle

puzzle = Puzzle(2023,9)
data = puzzle.input_data
# example = puzzle.examples[0]
# data = example.input_data

lines = data.strip().split('\n')
lines = [[int(v) for v in line.split()] for line in lines]

def get_diffs(line):
    return [line[i]-line[i-1] for i in range(1,len(line))]

def next_val(line):
    diffs = get_diffs(line)
    if len(set(diffs))==1:
        return line[-1]+diffs[0]
    else:
        return line[-1]+ next_val(diffs)

ans1=sum(next_val(line) for line in lines)
print(f"{ans1=}")

def prev_val(line):
    diffs = get_diffs(line)
    if len(set(diffs))==1:
        return line[0]-diffs[0]
    else:
        return line[0]- prev_val(diffs)

ans2=sum(prev_val(line) for line in lines)
print(f"{ans2=}")

# even better: ans2=sum(next_val(line[::-1]) for line in lines)
