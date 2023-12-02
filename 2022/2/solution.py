from pathlib import Path

with open(Path(__file__).parent / "input.txt", encoding="utf-8") as f:
    lines = f.read().strip().split('\n')

lines = ["A Y","B X","C Z"]
values = dict(zip(["A", "B", "C","X","Y","Z"], [0,1, 2,0,1,2]))
results = { 0: 3, 1: 6, 2: 0}
def score(line):
    p1,p2=[values[x] for x in line.split(" ")]
    res = (p2-p1) % 3
    sc = p2+1+results[res]
    # print(res,p2,sc)
    return sc

print(sum([score(line) for line in lines]))
results = { 0: 0, 1: 3, 2: 6}

def score(line):
    p1,res=[values[x] for x in line.split(" ")]
    p2 = (p1+res-1) % 3
    sc = p2+1+results[res]
    # print(res,p1,p2,sc)
    return sc

print(sum([score(line) for line in lines]))
