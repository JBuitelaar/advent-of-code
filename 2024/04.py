import time
from aocd.models import Puzzle

puzzle = Puzzle(2024,4)
data = puzzle.input_data

# Example:
# data = """MMMSXXMASM
# MSAMXMSMSA
# AMXSXMAAMM
# MSAMASMSMX
# XMASAMXAMM
# XXAMMXXAMA
# SMSMSASXSS
# SAXAMASAAA
# MAMMMXMMMM
# MXMXAXMASX"""


start_time = time.time()

grid = {r+c*1j: letter for r,row in enumerate(data.strip().split('\n')) for c,letter in enumerate(row)}

word="XMAS"

dirs = [1,-1,1j,-1j,1+1j,1-1j,-1+1j,-1-1j]

def is_xmas1(loc,dir):
    return all(grid.get(loc+dir*m, "") == letter for m,letter in enumerate(word))

ans1=sum(sum(is_xmas1(loc,dir) for dir in dirs) for loc in grid)

timer = time.time() - start_time
print(f"{ans1=}, {timer=:.2f}s")


def is_xmas2(loc):
    if grid.get(loc)!="A":
        return False
    # check clockwise:
    around = "".join([grid.get(loc+m,"") for m in [1+1j,-1+1j,-1-1j,1-1j]])
    return around in ("MMSS","SMMS","SSMM","MSSM")


ans2=sum(is_xmas2(loc) for loc in grid)
timer = time.time() - start_time
print(f"{ans2=}, {timer=:.2f}s")
