from aocd.models import Puzzle

puzzle = Puzzle(2023,13)
data = puzzle.input_data
# example = puzzle.examples[0]
# data = example.input_data

lines = data.strip()

blocks = lines.split('\n\n')

def get_diff_count(row1,row2):
    return sum(v1!=v2 for v1,v2 in zip(row1,row2))

def is_reflection_row(lines,rowno,smudges=0):
    diff_count = 0
    offset = 0
    while True:
        r1 = rowno-offset-1
        r2 = rowno+offset
        diff_count += get_diff_count(lines[r1],lines[r2])
        if diff_count>smudges:
            return False
        if r1==0 or r2==len(lines)-1:
            return diff_count==smudges
        offset+=1

def find_reflection_row(lines,smudges=0):
    for rowno in range(1,len(lines)):
        if is_reflection_row(lines,rowno,smudges):
            return rowno
    return 0

def block_score(block,smudges=0):
    lines = block.split("\n")
    reflection_row = find_reflection_row(lines,smudges)
    if reflection_row:
        return 100*reflection_row

    # transpose:
    lines = list(map(list, zip(*lines)))
    reflection_col = find_reflection_row(lines,smudges)
    return reflection_col

def solve(blocks,smudges=0):
    return sum(block_score(block,smudges) for block in blocks)

ans1 = solve(blocks,0)
print(f"{ans1=}")

ans2 = solve(blocks,1)
print(f"{ans2=}")