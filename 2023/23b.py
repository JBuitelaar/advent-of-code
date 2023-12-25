# Path finding 
# Both using networkx as hand-crafted
# I started doing it myself, but couldn't find my bug, so I switched to networkx
# After that I fixed my own

import time
from collections import defaultdict
from aocd.models import Puzzle

import networkx as nx
import matplotlib.pyplot as plt
from networkx.classes.function import path_weight

N,E,S,W = -1,1j,1,-1j

puzzle = Puzzle(2023,23)
data = puzzle.input_data
# data = puzzle.examples[0].input_data
# print(data)

start_time = time.time()
rows = data.split('\n')

# for row in rows:
#     print(row.replace("#","█"))


grid = {r+1j*c: v  for r,row in enumerate(rows) for c,v in enumerate(row) if v != '#'}
R = len(rows)
start_loc = 1j*rows[0].find(".")
end_loc = R-1+1j*rows[R-1].find(".")
start=(start_loc,1)
to_explore = [start]


# First we simplify the grid into a grah with only the places where we have a choice
graph = defaultdict(list)
dirs = [N,E,S,W]
seen = set()

last_node = None

G = nx.Graph()
G.add_node(start_loc)
edge_labels = {}


while to_explore:
    node,dir = to_explore.pop(0)

    if (node,dir) in seen:
        continue
    seen.add((node,dir))

    loc = node + dir
    node_dir=dir
    path_length=1
    while True:
        options = [d for d in dirs if d != -dir and loc+d in grid]

        if len(options) > 1:
            if loc not in G:
                G.add_node(loc)
            G.add_edge(node,loc,weight=path_length)
            edge_labels[(node,loc)] = path_length
            assert (loc,path_length) not in graph[node]
            graph[node].append((loc,path_length))

            # add the reverse
            assert (node,path_length) not in graph[loc]            
            graph[loc].append((node,path_length))
            seen.add((loc,-dir))

            for dir in options:
                to_explore.append((loc,dir))
            break
        if len(options) == 0:
            break
        path_length+=1
        dir = options[0]
        loc = loc + dir
        if loc==end_loc:
            assert not last_node, last_node
            last_node = node
            last_length = path_length
            G.add_node(loc)
            G.add_edge(node,loc,weight=path_length)
            edge_labels[(node,loc)] = path_length
            break

assert last_node

use_networkx = True

longest=0

if use_networkx:

    print(f"{G.number_of_nodes()} nodes with {G.number_of_edges()} edges")

    paths = nx.all_simple_paths(G, source=start_loc, target=end_loc)
    for p,path in enumerate(paths):
        res = path_weight(G,path,"weight")
        if res>longest:
            longest=res
            print(f"iteration {p}, longest={res}")
    print(f"Done, explored {p} iterations")

else:
    # slightly different because of the way I handled the last node
    # Plus this one double counts edges (except the last one)
    print(f"{len(graph)} nodes with {sum(len(v) for v in graph.values())} edges (double counting)")

    to_explore = [(start_loc,0,{start_loc})]
    p = 0
    while to_explore:
        loc, path_length,path = to_explore.pop(0)
        neighbours = graph[loc]
        for node,length in neighbours:
            if node in path:
                continue

            # path_length += length

            if node == last_node:
                p+=1
                length = path_length+length+last_length

                if length>longest:
                    longest=length
                    print(f"iteration {p}, longest={longest}")

                continue
            to_explore.append((node, path_length+length, path | {node}))

ans2=longest
timer = time.time() - start_time
print(f"{ans2=}, {timer=:.2f}s")

plt.figure(figsize=(15,8))
# I couldn't get the fixed nodes to work
pos = {n: (n.imag,-n.real) for n in G.nodes}
nx.draw(G, pos,with_labels=False)
nx.draw_networkx_edge_labels(G, pos,edge_labels=edge_labels)
plt.show()
