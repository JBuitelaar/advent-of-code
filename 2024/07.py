import re
import time
from aocd.models import Puzzle

puzzle = Puzzle(2024,7)
data = puzzle.input_data
# data = puzzle.examples[0].input_data
# print(data)

start_time = time.time()

def is_valid(test,vals,part2=False):
    if len(vals)==1:
        return vals[0]==test
   
    *other_vals,last_val=vals
    if test<last_val:
        return False

    div,rem=divmod(test,last_val)
    if not rem:
        if is_valid(div,other_vals):
            return True
    if is_valid(test-last_val,other_vals):
        return True
    
    if part2:
        test_str = str(test)
        val_str = str(last_val)
        if test_str.endswith(val_str):
            return is_valid(int(test_str[:-len(val_str)]),other_vals)
    return False


lines = data.strip().split('\n')
inputs = [list(map(int, re.findall("\\d+", line))) for line in lines]


ans1=sum(test for test, *vals in inputs if is_valid(test,vals))

timer = time.time() - start_time
print(f"{ans1=}, {timer=:.2f}s")


ans2=sum(test for test, *vals in inputs if is_valid(test,vals,True))

timer = time.time() - start_time
print(f"{ans2=}, {timer=:.2f}s")
