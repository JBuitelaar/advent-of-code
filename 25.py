import time
import math
from aocd.models import Puzzle
import networkx as nx
import matplotlib.pyplot as plt

puzzle = Puzzle(2023,25)

# data = """jqt: rhn xhk nvd
# rsh: frs pzl lsr
# xhk: hfx
# cmg: qnr nvd lhk bvb
# rhn: xhk bvb hfx
# bvb: xhk hfx
# pzl: lsr hfx nvd
# qnr: nvd
# ntq: jqt hfx bvb xhk
# nvd: lhk
# lsr: lhk
# rzs: qnr cmg lsr rsh
# frs: qnr lhk lsr"""

data = puzzle.input_data
start_time = time.time()

lines = data.strip().split('\n')

G = nx.from_dict_of_lists({k: v.split() for k,v in [line.split(": ") for line in lines]})
to_cut = nx.minimum_edge_cut(G)

assert len(to_cut)==3
G.remove_edges_from(to_cut)

ans1=math.prod(len(x) for x in nx.connected_components(G))

timer = time.time() - start_time
print(f"{ans1=}, {timer=:.2f}s")

show_graph = False

if show_graph:
    plt.figure()
    nx.draw(G, with_labels=True)
    plt.show()
