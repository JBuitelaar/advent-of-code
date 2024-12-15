import time
from aocd.models import Puzzle
from dotenv import load_dotenv

load_dotenv()

puzzle = Puzzle(2024, 15)

# data = puzzle.examples[0].input_data

# data = """
# #######
# #...#.#
# #.....#
# #..OO@#
# #..O..#
# #.....#
# #######
#
# <vv<<^^<<^^"""

# data="""
# ########
# #..O.O.#
# ##@.O..#
# #...O..#
# #.#.O..#
# #...O..#
# #......#
# ########
#
# <^^>>>vv<v>>v<<"""

# print(f"Example: \n{data}\n{"="*80}")

data = puzzle.input_data
start_time = time.time()

maze, moves = data.strip().split("\n\n")
steps = "".join(moves.split())

dirs = -1, 1, -1j, 1j
N, S, W, E = dirs

dir_map = {"<": W, ">": E, "^": N, "v": S}


def print_grid(grid, loc):
    R = max(int(loc.real) for loc in grid) + 1
    C = max(int(loc.imag) for loc in grid) + 1
    for r in range(R):
        row = ["@" if r + 1j * c == loc else grid[r + 1j * c] for c in range(C)]
        print("".join(row))
    print("\n\n")


def read_grid(maze):
    maze_lines = maze.strip().split("\n")
    grid = {
        r + 1j * c: v for r, row in enumerate(maze_lines) for c, v in enumerate(row)
    }
    start_loc = next(loc for loc, v in grid.items() if v == "@")
    grid[start_loc] = "."
    return grid, start_loc


def push_boxes_simple(grid, box_loc, dir):
    """Try to push the box in box_loc in the direction, including all connected boxes
    return True if successful
    Doesn't matter if the box has size 1 (O) or 2 ([]), as long as we're pushing [] from left/right
    """
    nxt = box_loc + dir
    if grid[nxt] == "#":
        return False
    if grid[nxt] == "." or push_boxes_simple(grid, nxt, dir):
        # there's an empty space, or there's a box that we can push away
        grid[nxt] = grid[box_loc]
        grid[box_loc] = "."
        return True
    return False


def move_robot(grid, loc, steps, move_box_func):
    """execute all robot steps
    move_box_func is a function to move a box (element)
    """
    for step in steps:
        dir = dir_map[step]

        nxt = loc + dir
        if grid[nxt] == "#":
            pass
        elif grid[nxt] == "." or move_box_func(grid, nxt, dir):
            loc = nxt
        # print(f"{step=}\n")
        # print_grid(grid,loc)

    return grid, loc


def sum_coord(grid, box_char):
    return sum(int(loc.imag + loc.real * 100) for loc in grid if grid[loc] == box_char)


### PART 1 ###
start_grid, start_loc = read_grid(maze)
# print_grid(start_grid,start_loc)

grid, loc = move_robot(start_grid.copy(), start_loc, steps, push_boxes_simple)

ans1 = sum_coord(grid, "O")
timer = time.time() - start_time
print(f"{ans1=}, {timer=:.2f}s")


### PART 2 ###
maze = maze.replace("O", "[]").replace(".", "..").replace("@", "@.").replace("#", "##")
start_grid, start_loc = read_grid(maze)
# print_grid(grid,start_loc)


def move_boxes_updown(grid, boxes, step):
    for lc, b in boxes.items():
        grid[lc] = "."
        grid[lc + step] = b


def push_boxes_updown(grid, boxes, dir):
    # Try to push the boxes in the direction, including all connected boxes
    # return True if successful
    next_space = [b + dir for b in boxes]
    next_objects = [grid[b] for b in next_space]
    if all(b == "." for b in next_objects):
        # all spaces are empty, so we can simply move:
        move_boxes_updown(grid, boxes, dir)
        return True
    if any(b == "#" for b in next_objects):
        # some wall is blocking the way. We can't move
        return False
    # there are boxes in the way. We need to try to push them as well
    next_boxes = {}
    for lc in next_space:
        t = grid[lc]
        if t == "[":
            next_boxes[lc] = "["
            next_boxes[lc + E] = "]"
        elif t == "]":
            next_boxes[lc + W] = "["
            next_boxes[lc] = "]"
    if push_boxes_updown(grid, next_boxes, dir):
        move_boxes_updown(grid, boxes, dir)
        return True
    return False


def push_boxes_part2(grid, box_loc, dir) -> bool:
    if dir in [W, E]:
        return push_boxes_simple(grid, box_loc, dir)

    # step in [N,S].
    # First add the other box part:
    box = {box_loc: grid[box_loc]}
    if grid[box_loc] == "]":
        box[box_loc + W] = "["
    else:
        box[box_loc + E] = "]"
    return push_boxes_updown(grid, box, dir)


grid, loc = move_robot(start_grid.copy(), start_loc, steps, push_boxes_part2)

ans2 = sum_coord(grid, "[")


timer = time.time() - start_time
print(f"{ans2=}, {timer=:.2f}s")

print("Final grid:")
print_grid(grid, loc)
