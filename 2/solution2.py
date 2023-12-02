from pathlib import Path
from math import prod

with open(Path(__file__).parent / "input.txt", encoding="utf-8") as f:
    lines = f.read().strip().split('\n')

def power(line):
    cube_counts = {"red": [], "green": [], "blue": []}
    _gameno, hands_str = line.split(": ")

    for hand_str in hands_str.split("; "):
        for cube in hand_str.split(", "):
            count, color = cube.split()
            cube_counts[color].append(int(count))
    
    return prod(max(counts) for counts in cube_counts.values())

print(sum(power(line) for line in lines))
