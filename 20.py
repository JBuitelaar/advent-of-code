# Another lcm problem, this time with a graph

import sys
import time
import math
from collections import defaultdict, deque
from aocd.models import Puzzle


puzzle = Puzzle(2023,20)
data = puzzle.input_data
# data = puzzle.examples[0].input_data
# print(data,"\n")
# print(data[:1000])

# data1 = """broadcaster -> a
# %a -> inv, con
# &inv -> b
# %b -> con
# &con -> output"""




lines = data.strip().split('\n')

module_targets = {}
types = {}
sources = defaultdict(list)
states_ff = {}
states_cj = {}

# Print the graph at https://mermaid.live/
mermaid = []

for line in lines:
    source_str, target_str = line.split(" -> ")
    dests = target_str.split(", ")
    if source_str != "broadcaster":
        type_ = source_str[0]
        source = source_str[1:]
        types[source] = type_
        if type_ == "%":
            states_ff[source] = False
    else:
        broadcast_to = dests
        source = "broadcaster"
    module_targets[source] = dests
    for target in dests:
        if source_str == "broadcaster":
            source="broadcaster"
            priority = 0
        elif source == "th":
            priority = 3
        elif target == "th":
            priority = 2
        else:
            priority = 1
        sources[target].append(source)
        mermaid.append((priority,f"{source}({source_str}) --> {target}"))

for name,type_ in types.items():
    if type_ == "&":
        conj_sources = sources[name]
        if len(conj_sources) == 1:
            # easy, no need to remember the state
            # print(f"found singleton {name}")
            types[name] = "!"
        else:
            assert len(conj_sources) >1
            states_cj[name] = dict.fromkeys(conj_sources, False)


# you can paste this at mermaid.live:
print("\n\nflowchart TD")
for p,line in sorted(mermaid):
    print(line)


# There are 4 independent loops, so we can find the LCM of the loop lengths
mymap = {
    "ch": "xf",
    "hd": "qn",
    "sr": "xn",
    "bx": "zl",
}

start_time = time.time()

counter = [0,0]  # low, high

mytargets = mymap.values()
found = {}


for ix in range(1,100000):    
    todo = deque([("broadcaster", False, "button")])

    while todo:
        (module, high, source) = todo.popleft()
        # print(f"{source} -{'high' if high else 'low'}-> {module}")
        
        counter[high] += 1
        if module in mytargets and not high and module not in found:
            found[module] = ix
            print(f"signal at button press {ix}: {source}=>{module}")
            if set(found.keys()) == set(mytargets):
                ans2 = math.lcm(*found.values())
                timer = time.time() - start_time
                print(f"{ans2=}, {timer=}")
                sys.exit(0)

        if module == "broadcaster":
            for target in broadcast_to:
                todo.append((target, high, module))
            continue

        if module not in module_targets:
            if  module not in ("rx","output"):
                print(module)
            continue

        module_type = types[module]
        dests = module_targets[module]
        if module_type == "%":
            if high:
                continue
            out_high = not states_ff[module]
            states_ff[module] = not states_ff[module]
        elif module_type == "!":
            out_high = not high
        else:
            assert module_type == "&"
            if module not in states_cj:
                states_cj[module] = dict.fromkeys(sources[module], False)
            state = states_cj[module]
            state[source] = high
            out_high = not all(state.values())
            
        for dest in dests:
            todo.append((dest, out_high, module))

    if ix == 1000:
        ans1 = math.prod(counter)
        timer = time.time() - start_time
        print(f"{ans1=}, {timer=}")

