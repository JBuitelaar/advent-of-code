import itertools
from aocd.models import Puzzle

puzzle = Puzzle(2023,11)
data = puzzle.input_data
# example = puzzle.examples[0]
# data = example.input_data
# print("example answers: ",example.answer_a, example.answer_b)
# print(data)
# print(data[:1000])

rows = data.strip().split('\n')

galaxies = set()
row2= set()
col2=set()
for r, row in enumerate(rows):
    for c,v in enumerate(row):
        if v == "#":
            galaxies.add((r,c))
            row2.add(r)
            col2.add(c)

incr_r = [r for r in range(max(row2)) if r not in row2]
incr_col = [c for c in range(max(col2)) if c not in col2]

def expand_universe(incr):
    res=set()
    for r,c in galaxies:
        r+=sum(incr for v in incr_r if v<r)
        c+=sum(incr for v in incr_col if v<c)    
        res.add((r,c))
    return res

def sum_dist(locations):
    res = 0
    for comb in itertools.combinations(locations,2):
        dist = int(abs(comb[0][0]-comb[1][0])+abs(comb[0][1]-comb[1][1]))
        res+=dist
    return res

for incr in [1, 1e6-1]:
    galaxies_exp=expand_universe(incr)
    ans = sum_dist(galaxies_exp)
    print(ans)
