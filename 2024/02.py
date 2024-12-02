import time
from aocd.models import Puzzle

puzzle = Puzzle(2024,2)
data = puzzle.input_data
# print(data[:400], '...\n')

start_time = time.time()

reports = [[int(v) for v in line.split()] for line in data.strip().split('\n')]

def valid1(report):
    diffs = [y-x for x,y in zip(report[:-1],report[1:])]
    mind= min(diffs)
    maxd= max(diffs)
    return (mind>0 and maxd<4) or (maxd<0 and mind>-4)

def valid2(report):
    if valid1(report):
        return True
    else:
        # just try removing elements 1 by 1. Not very efficient, but very easy:
        for i in range(len(report)):
            if valid1(report[:i]+report[i+1:]):
                return True
            
    return False


ans1=sum(valid1(report) for report in reports)

timer = time.time() - start_time
print(f"{ans1=}, {timer=:.2f}s")

ans2=sum(valid2(report) for report in reports)

timer = time.time() - start_time
print(f"{ans2=}, {timer=:.2f}s")

