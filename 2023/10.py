from aocd.models import Puzzle

puzzle = Puzzle(2023,10)
data = puzzle.input_data

rows = data.strip().split('\n')

def find_S(rows):
    """find location of S, replace it with the pipe and choose the previous location"""
    for r,row in enumerate(rows):
        c = row.find("S")
        if c != -1:
            return (r,c)

loc_S = find_S(rows)
r,c = loc_S
print(f"S found at {(r,c)}")
print("check the tiles around it and determine the pipe at location S")
for r2 in range(r-1,r+2):
    print(rows[r2][c-1:c+2])

print("manually override pipe and choose previous location")
# (choose 1 of the 2 options)
s_pipe = None # "7"
prev_loc = None # (r,c-1)
assert s_pipe, "Enter s_pipe and prev_loc manually"

# replace S:
row = rows[r]
rows[r] = row[:c]+s_pipe+row[c+1:]


def get_next(current_tile,prev_tile):
    r,c = current_tile
    r0,c0 = prev_tile
    pipe = rows[r][c]

    if pipe == "-":
        return r,c+c-c0
    elif pipe == "|":
        return r+r-r0,c
    elif pipe == "F":
        return (r+1,c) if r==r0 else (r,c+1)
    elif pipe == "7":
        return (r+1,c) if r==r0 else (r,c-1)
    elif pipe == "J":
        return (r-1,c) if r==r0 else (r,c-1)
    elif pipe == "L":
        return (r-1,c) if r==r0 else (r,c+1)
    raise(ValueError(f"ERROR: {pipe} not recognized"))

current_loc = loc_S
step = 0
loop = set()
while True:
    loop.add(current_loc)
    step += 1
    next_loc = get_next(current_loc,prev_loc)

    if next_loc == loc_S:
        assert step%2==0
        ans1 = step//2
        break
    prev_loc, current_loc = current_loc, next_loc

print(f"{ans1=}")


ins = set()

# A tile has 4 corners, with pipes connecting (the center of) two sides.
# To determine if a tile is inside, we can just look at any of the 4 corners.
# We take the top left.
# Now we start from the left boundary of the field, which is out
# as we move right and we come across a pipe, we are inside. Next pipe we're out again, etc
# So we just need to count the pipes.
# Since we're looking at the top left corner and move horizontally,
# we only need to look at pipes to the top of the tile (i.e. J, L, |)

for r, row in enumerate(rows):
    is_out = True
    for c, v in enumerate(row):
        if (r,c) in loop:
            if rows[r][c] in "JL|":
                is_out = not is_out
        elif not is_out:
            ins.add((r,c))

ans2=len(ins)
            
print(f"{ans2=}")

# print:
heavy = "┏┛┗┓┃━"
light = "┌┘└┐│─"
char_map = dict(zip("FJL7|-",light))

def get_char(loc):
    if loc in loop:
        return char_map[rows[loc[0]][loc[1]]]
    elif loc in ins:
        return "█"
    else:
        return "░"


drawing = ["".join(get_char((r,c)) for c in range(len(row))) for r, row in enumerate(rows)]
for row in drawing:
    print(row)


