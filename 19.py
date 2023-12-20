import time
import math
from aocd.models import Puzzle

puzzle = Puzzle(2023,19)
data = puzzle.input_data
# data = puzzle.examples[0].input_data
# print(data)

start_time= time.time()
instr,parts_str = data.split('\n\n')
instrs = instr.split('\n')

def read_routes(routes):
    res = []
    default = routes.pop()
    for route in routes:
        cond,dest = route.split(":")
        comp = cond[1]
        assert comp in ("<",">")
        part = cond[0]
        val = int(cond[2:])
        res.append((part,comp=="<",val,dest))

    # quite a few instructions at the end don't add anything, because the default is the same anyway
    # so we can remove those:
    while res and res[-1][3] == default:
        # print(routes, default)
        res.pop()
    res.append(default)
    return res

workflows = {}
for instr in instrs:
    splitchar = instr.find("{")
    routes = instr[splitchar+1:-1].split(",")
    workflows[instr[:splitchar]]=read_routes(routes)

parts = []
for ln in parts_str.split("\n"):
    pp = ln[1:-1].split(",")
    parts.append({p:int(v) for p,v in [p.split("=") for p in pp]})

# PART 1
    
def get_next(instr,part):
    for (p,less_than,val,dest) in instr[:-1]:
        if less_than:
            if part[p] < val:
                return dest
        else: 
            if part[p] > val:
                return dest
    return instr[-1]

ans1=0  
for part in parts:
    name = "in"
    while name not in ("R","A"):
        instr = workflows[name]
        name = get_next(instr,part)
    if name == "A":
        ans1+=sum(part.values())

timer = time.time() - start_time
print(f"{ans1=}, {timer=}")

# PART 2

def find_ranges():
    results = []
    ranges = {k: (1,4000) for k in "xmas"}
    to_do = [("in",ranges)]

    while to_do:
        current,ranges = to_do.pop()
        if current == "R":
            continue
        if current == "A":
            results.append(ranges)
            continue
        workflow = workflows[current]
        for (p,less_than,val,dest) in workflow[:-1]:
            ranges2=ranges.copy()
            lo,hi = ranges2[p]
            if less_than:
                ranges2[p] = (lo,min(hi,val-1))
                ranges[p] = (max(lo,val),hi)
            else:
                ranges2[p] = (max(lo,val+1),hi)
                ranges[p] = (lo,min(hi,val))

            # if the condition is True:
            to_do.append((dest,ranges2))
        
        # if all conditions are false:
        to_do.append((workflow[-1],ranges.copy()))
            
    return results

all_limits = find_ranges()

# for p in all_limits:
#     print([tuple(x) for x in p.values()])
ans2=sum(math.prod(max(r[1]-r[0]+1,0) for r in limits.values()) for limits in all_limits)
timer = time.time() - start_time
print(f"{ans2=}, {timer=}")

