from math import prod

from aocd.models import Puzzle

puzzle = Puzzle(2023,2)
data = puzzle.input_data
lines = data.strip().split('\n')

max_cubes = {"red": 12, "green": 13, "blue": 14}

def game_score(line):
    gameno, hands_str = line.split(": ")

    for hand_str in hands_str.split("; "):
        for cube in hand_str.split(", "):
            count, color = cube.split()
            if int(count)>max_cubes[color]:
                return 0
    return int(gameno.split(" ")[1])

print(sum(game_score(line) for line in lines))


def power(line):
    cube_counts = {"red": [], "green": [], "blue": []}
    _gameno, hands_str = line.split(": ")

    for hand_str in hands_str.split("; "):
        for cube in hand_str.split(", "):
            count, color = cube.split()
            cube_counts[color].append(int(count))
    
    return prod(max(counts) for counts in cube_counts.values())

print(sum(power(line) for line in lines))
