from pathlib import Path

with open(Path(__file__).parent / "input.txt", encoding="utf-8") as f:
    lines = f.read().strip().split('\n')

containing = 0
overlapping = 0

def contained(range1,range2):
    return range1[0]<=range2[0] and range1[1]>=range2[1]

def overlap(range1,range2):
    if range1[0] > range2[0]:
        return range1[0]<=range2[1]
    else:
        return range2[0]<=range1[1]

for line in lines:
    first,second = [list(map(int,r.split("-"))) for r in line.split(",")]


    if contained(first,second) or contained(second,first):
        containing+=1
    if overlap(first,second):
        overlapping+=1

print(containing)
print(overlapping)
