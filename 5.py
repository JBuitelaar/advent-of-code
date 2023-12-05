from itertools import batched
from aocd.models import Puzzle

puzzle = Puzzle(2023,5)
data = puzzle.input_data
# example = puzzle.examples[0]
# data = example.input_data
# print("example answers: ",example.answer_a, example.answer_b)

groups = data.strip().split('\n\n')
seeds = [int(v) for v in groups[0].split(":")[1].strip().split()]
all_maps = []
for group in groups[1:]:
    maps = group.split(":")[1].strip().split("\n")
    mapping = [[int(v) for v in line.split()] for line in maps]
    # map to range and offset: [src0, src1), offset
    mapping = [[src,src+range,dest-src] for dest,src,range in mapping]
    all_maps.append(mapping)

seed_ranges = [[start,start+range] for start,range in batched(seeds,2)]
# print(seed_ranges)
# print(all_maps)

def map_value(mapping,input):
    for src0,src1,offset in mapping:
        if src0<=input<src1:
            return input+offset
    return input

for mapping in all_maps:
    seeds = [map_value(mapping,seed) for seed in seeds]

ans1 = min(seeds)
print(ans1)


def map_ranges(mapping,input_ranges,output_ranges):
    if not input_ranges:
        return output_ranges
    input0,input1 = input_ranges.pop()
    for src0,src1,offset in mapping:
        if input0<src1 and input1>src0:
            overlap_start = max(input0,src0)
            overlap_end = min(input1,src1)
            output_ranges.append( [overlap_start+offset,overlap_end+offset])
            if input0<src0:
                input_ranges.append([input0,src0])
            if input1>src1:
                input_ranges.append([src1,input1])
            return map_ranges(mapping,input_ranges,output_ranges)

    output_ranges.append([input0,input1])
    return map_ranges(mapping,input_ranges,output_ranges)

for mapping in all_maps:
    seed_ranges = map_ranges(mapping,seed_ranges,[])

ans2=min(x for [x,y] in seed_ranges)

print(ans2)
