from pathlib import Path

with open(Path(__file__).parent / "input.txt", encoding="utf-8") as f:
    lines = f.read().strip().split('\n')

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
