from collections import OrderedDict
from aocd.models import Puzzle

puzzle = Puzzle(2023,15)
data = puzzle.input_data
# example = puzzle.examples[0]
# data = example.input_data
lines = data.strip().split(',')

def get_score(line):
    res = 0
    for c in list(line):
        res = ((res+ord(c))*17)%256
    return res

ans1=sum(get_score(line) for line in lines)
print(f"{ans1=}")

def read(line):
    remove = line.endswith("-")
    if remove:
        label,focus = line[:-1],0
    else:
        (label, focus) = line.split("=")
    return (label, int(focus),remove)

boxes = [OrderedDict() for _ in range(256)]
for line in lines:
    label,focus,remove=read(line)
    b = get_score(label)
    box = boxes[b]
    if remove:
        if label in box:
            del box[label]
    else:
        # either update or append
        box[label] = focus
    # print(boxes)

ans2=sum(ix*v*j for j,box in enumerate(boxes,1) for ix, v in enumerate(box.values(),1))

print(f"{ans2=}")
# from aocd import submit
# submit(ans2)