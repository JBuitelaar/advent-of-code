import time
from functools import reduce
from aocd.models import Puzzle
from dotenv import load_dotenv

load_dotenv()

puzzle = Puzzle(2024, 15)

# Basic example for part 1:
# data="""
# ########
# #..O.O.#
# ##@.O..#
# #...O..#
# #.#.O..#
# #...O..#
# #......#
# ########

# <^^>>>vv<v>>v<<"""

# # Basic example for part 2:
# data = """
# #######
# #...#.#
# #.....#
# #..OO@#
# #..O..#
# #.....#
# #######

# <vv<<^^<<^^"""

# data = puzzle.examples[0].input_data
# print(f"Example: \n{data}\n{"="*80}")

data = puzzle.input_data
start_time = time.time()

maze, moves = data.strip().split("\n\n")
moves = moves.replace("\n", "")

dirs = -1, 1, -1j, 1j
N, S, W, E = dirs
dir_map = dict(zip("^v<>", dirs))


def insert(rows, loc, v):
    r, c = int(loc.real), int(loc.imag)
    rows[r][c] = v


class Grid:
    """A grid with a robot and boxes
    we keep track of the location of the walls (fixed), robot and boxes (moving)
    """

    def __init__(self, maze, box_char="O"):
        maze_lines = maze.strip().split("\n")
        self.nrows = len(maze_lines)
        self.ncols = len(maze_lines[0])
        walls = set()
        boxes = set()
        for r, row in enumerate(maze_lines):
            for c, v in enumerate(row):
                loc = r + 1j * c
                if v == box_char:
                    boxes.add(loc)
                elif v == "@":
                    self.robot = loc
                elif v == "#":
                    walls.add(loc)
        self.walls = walls
        self.boxes = boxes

    def __str__(self):
        rows = [["."] * self.ncols for _ in range(self.nrows)]
        for loc in self.walls:
            insert(rows, loc, "#")
        for loc in self.boxes:
            insert(rows, loc, "O")
        insert(rows, self.robot, "@")
        return "\n".join("".join(r) for r in rows)

    def find_box(self, loc):
        # Return the box location of there is a box at loc, None otherwise
        if loc in self.boxes:
            return loc
        return None

    def box_locs(self, box):
        # Return all locations occupied by this box
        return {box}

    def push_boxes(self, boxes, dir):
        nxt_locs = reduce(set.union, (self.box_locs(loc + dir) for loc in boxes))
        if any(loc in self.walls for loc in nxt_locs):
            return False
        nxt_boxes = [self.find_box(loc) for loc in nxt_locs]
        nxt_boxes = {b for b in nxt_boxes if b and b not in boxes}
        if (not nxt_boxes) or self.push_boxes(nxt_boxes, dir):
            for loc in boxes:
                self.boxes.remove(loc)
                self.boxes.add(loc + dir)
            return True
        return False

    def move(self, dir):
        nxt = self.robot + dir
        if nxt in self.walls:
            return
        box = self.find_box(nxt)
        if (box is None) or self.push_boxes({box}, dir):
            self.robot = nxt

    def execute_moves(self, moves, verbose=False):
        for move in moves:
            self.move(dir_map[move])
            if verbose:
                print(f"\nmove {move}:\n{self}")

    def sum_coord(self):
        return sum(int(loc.imag + loc.real * 100) for loc in self.boxes)


### PART 1 ###
grid = Grid(maze)
# print(f"\nInitial state:\n{grid}")
grid.execute_moves(moves)
# print(f"\nFinal state:\n{grid}")
ans1 = grid.sum_coord()

timer = time.time() - start_time
print(f"{ans1=}, {timer=:.2f}s")

### PART 2 ###


class Grid2(Grid):
    """Grid with larger boxes
    We identify boxes by the left part of the box.
    """

    def __init__(self, maze):
        maze2 = (
            maze.replace(".", "..")
            .replace("@", "@.")
            .replace("O", "O.")
            .replace("#", "##")
        )
        super().__init__(maze2)

    def find_box(self, loc):
        if loc + W in self.boxes:
            return loc + W
        return super().find_box(loc)

    def box_locs(self, box):
        return {box, box + E}

    def __str__(self):
        return super().__str__().replace("O.", "[]")


grid = Grid2(maze)
# print(f"\nInitial state:\n{grid}")
grid.execute_moves(moves)
# print(f"\nFinal state:\n{grid}")
ans2 = grid.sum_coord()

timer = time.time() - start_time
print(f"{ans2=}, {timer=:.2f}s")
