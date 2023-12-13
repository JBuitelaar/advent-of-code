import itertools
import math
import time
from functools import cache
from aocd.models import Puzzle

puzzle = Puzzle(2023,12)
data = puzzle.input_data
# example = puzzle.examples[2]
# data = example.input_data
# print("example answers: ",example.answer_a, example.answer_b)
# print(data)
# print(data[:1000])

def count_free(size,lenghts):
    """Number of combinations if we only have ?*size
    Let's say lengths = [3,1,2] to be put in an array of size=20
    Then the results looks like:
    [a]###.[b]##.[c]#[d]
    where a,b,c,d contain 0 or more dots.
    We can determine dot_count = a+b+c+d = size - (sum(lenghts) + len(lengths) - 1) = 20-8 = 12
    The number of combinations is the number of ways to put 4 separators in an array of 12+4
    """
    groups = len(lenghts)
    dot_count = size - (sum(lenghts) + groups - 1)
    if dot_count<0:
        return 0
    return math.comb(dot_count+groups,groups)

def count(row, lengths):
    # Very elegant(?), but slow
    if not lengths:
        # all dots
        return int("#" not in row)
    if row == "":
        return 0
    if sum(lengths)+len(lengths)-1>len(row):
        return 0
    if row.startswith("#"):
        L = lengths[0]
        # row should start with #s followed by . (unless there's only 1)
        if "." in row[:L] or (len(row)>L and row[L]=="#"):
            return 0
        return count(row[L+1:], lengths[1:])
    elif row.endswith("#"):
        L = lengths[-1]
        if "." in row[-L:] or (len(row)>L and row[-L-1]=="#"):
            return 0        
        return count(row[:-L-1], lengths[:-1])
    elif row.startswith(".") or row.endswith("."):
        # these we can just ignore.
        if set(row)=={"."}:
            return 0
        # remove all dots from the start and end
        start_ix = next(ix for ix,v in enumerate(row) if v!=".")
        end_ix = next(ix for ix in range(len(row),start_ix,-1) if row[ix-1]!=".")
        return count(row[start_ix:end_ix], lengths)
    loc_dot = row.find(".")
    if loc_dot>=0:
        # we can now look at the left and right side of the dot
        # only problem is that we don't know how many #s are on the left and right side
        # so we need to try all combinations
        # if there are multiple dots next to eachother we can skip them all:
        last_dot = loc_dot+1
        while row[last_dot]==".":
            last_dot+=1
        left = row[:loc_dot]
        right = row[last_dot:]
        res = 0
        for split_loc in range(len(lengths)+1):
            left_count = count(left, lengths[:split_loc])
            if left_count:
                res += left_count * count(right, lengths[split_loc:])
        return res
    
    # Now there are no more dots left, just #/?
    loc_hash = row.find("#")
    if loc_hash>=0:
        # I don't have any smart ideas, so let's just try to fill in one of the questionmarks
        # I'll take the first ? to the right of the #, 
        # as I think that will reduce the number of options fastest (no proof)
        loc = loc_hash
        while row[loc]=="#":
            loc += 1
        
        group_size = loc-loc_hash
        if group_size>max(lengths):
            return 0
        count_if_dot = count(row[:loc]+"."+row[loc+1:], lengths)
        count_if_dash = count(row[:loc]+"#"+row[loc+1:], lengths)
        return count_if_dot + count_if_dash

    # Finally, we only have ?s left. That's easy:
    return count_free(len(row), lengths)


lines = data.strip().split('\n')

@cache
def count2(row,groups):
    """much simpler, with caching"""
    if not groups:
        return int("#" not in row)
    if row == "":
        return 0
    if sum(groups)+len(groups)-1>len(row):
        return 0
    # if set(row)=={"?"}:  # doesn't actually help with speeding up
    #     return count_free(len(row), groups)
    res = 0
    if row[0] in "#?":
        L = groups[0]
        # row should start with #s followed by . (unless it's the end of the row)
        if "." not in row[:L] and (len(row)==L or row[L]!="#"):
            res += count2(row[L+1:], groups[1:])

    if row[0] in ".?":
        res += count2(row[1:], groups)
        
    return res


part2=True
ans=0
start = time.time()

for rix,line in enumerate(lines[0:]):
    info,counts = line.split()
    if part2:
        info = "?".join(itertools.repeat(info,5))
        counts = ",".join(itertools.repeat(counts,5))
    counts = tuple(int(x) for x in counts.split(","))
    # print(rix,info,counts)
    # val = count(info, counts)
    val = count2(info, counts)
    ans+=val

timer=time.time()-start
print(f"{ans=}, {timer=:.3f}s")
# print(count2.cache_info())