import time
import itertools
from collections import defaultdict
import copy
from aocd.models import Puzzle
from dotenv import load_dotenv

load_dotenv()

puzzle = Puzzle(2024, 23)

# data = puzzle.examples[0].input_data
# print(f"Example: \n{data}\n{"="*80}")

data = puzzle.input_data

lines = data.strip().split("\n")

input_graph = defaultdict(set)
for line in lines:
    c1, c2 = line.split("-")
    input_graph[c1].add(c2)
    input_graph[c2].add(c1)


start_time = time.time()
### PART 1 ###

ans1 = 0

graph = copy.deepcopy(input_graph)
while len(graph) > 1:
    c1, connections = graph.popitem()
    for c2, c3 in itertools.combinations(connections, 2):
        if c2 in graph[c3]:
            if any(c.startswith("t") for c in (c1, c2, c3)):
                fs = frozenset([c1, c2, c3])
                ans1 += 1
    for c2 in connections:
        graph[c2].remove(c1)


timer = time.time() - start_time
print(f"{ans1=}, {timer=:.2f}s")


### PART 2 ###


def all_connected(graph, connections) -> bool:
    for c2, c3 in itertools.combinations(connections, 2):
        if c2 not in graph[c3]:
            return False
    return True


def solve2(input_graph):
    max_len = max(len(s) for s in input_graph.values())
    for group_len in range(max_len, 3, -1):
        print(f"looking for groups of length {group_len}...")
        graph = copy.deepcopy(input_graph)
        while len(graph) >= group_len:
            c1, connections = graph.popitem()
            if len(connections) >= group_len - 1:
                for sub_comb in itertools.combinations(connections, group_len - 1):
                    if all_connected(graph, sub_comb):
                        return ",".join(sorted(list(sub_comb) + [c1]))


ans2 = solve2(input_graph)
timer = time.time() - start_time
print(f"{ans2=}, {timer=:.2f}s")
