import re
from collections import defaultdict

with open("3/input.txt", encoding="utf-8") as f:
    lines = f.read().strip().split('\n')

line_length = len(lines[0])

def neighbours(lineno,start,end):
    if start>0:
        yield lineno, start-1
    if end < line_length:
        yield lineno, end
    for iy in range(max(start-1,0),min(end+1,line_length)):
        if lineno>0:
            yield lineno-1, iy
        if lineno<len(lines)-1:
            yield lineno+1, iy

gears = defaultdict(list)

def borders(lineno,start,end,value):
    found = False
    for x,y in neighbours(lineno,start,end):
        c = lines[x][y]
        if c not in "0123456789.":
            found = True
            if c == "*":
                gears[(x,y)].append(value)

    return found


count = 0
for ix, line in enumerate(lines):
    for m in re.finditer(r"(\d+)",line):
        start,end =m.span()
        value = int(m.group())
        
        if borders(ix,start,end,value):
            count+=value

print(count)

gear_total = 0
for v in gears.values():
    if len(v)==2:
        gear_total += v[0]*v[1]

print(gear_total)