import time
import itertools
from sympy import solve, symbols
from aocd.models import Puzzle

puzzle = Puzzle(2023,24)
data = puzzle.input_data
min_d, max_d = 200000000000000, 400000000000000

# data = puzzle.examples[0].input_data
# min_d, max_d = 7, 27

start_time = time.time()

hails = [[tuple(map(int,v.split(", "))) for v in line.split(" @ ")] for line in data.strip().split('\n')]

ans1=0
for h1,h2 in itertools.combinations(hails,2):
    (x1,y1,z1),(dx1,dy1,dz1) = h1
    (x2,y2,z2),(dx2,dy2,dz2) = h2
    if dx1/dx2 == dy1/dy2:  # parallel
        continue

    # they cross when:
    # x1 + dx1*t1 = x2 + dx2*t2
    # y1 + dy1*t1 = y2 + dy2*t2
    # divide by dx1 and dy2 and subtract the two equations to drop t1. 
    # Then solve for t2
    t2 = (x1/dx1-y1/dy1-x2/dx1+y2/dy1)/(dx2/dx1-dy2/dy1)
    if t2<0:
        continue
    # and plug back in to get t1
    t1 = (x2+dx2*t2-x1)/dx1
    if t1<0:
        continue

    x = x1+dx1*t1
    y = y1+dy1*t1
    if min_d<=x<=max_d and min_d<=y<=max_d:
        ans1+=1

timer = time.time() - start_time
print(f"{ans1=}, {timer=:.2f}s")

variables = symbols('x,y,z,dx,dy,dz')
x,y,z,dx,dy,dz=variables

vars = list(variables)
equations = []
for ix,hail in enumerate(hails[:3],1):
    t = symbols(f"t{ix}")
    vars.append(t)
    (x1,y1,z1),(dx1,dy1,dz1) = hail
    equations.append(x1-x+(dx1-dx)*t)
    equations.append(y1-y+(dy1-dy)*t)
    equations.append(z1-z+(dz1-dz)*t)


result = solve(equations,vars,dict=True)
assert len(result)==1
res = result[0]

ans2=sum(res[k] for k in (x,y,z))
timer = time.time() - start_time
print(f"{ans2=}, {timer=:.2f}s")
