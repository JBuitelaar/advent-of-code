from pathlib import Path

with open(Path(__file__).parent / "input.txt", encoding="utf-8") as f:
    lines = f.read().strip().split('\n')

all_cals = []
total = 0


for line in lines:
    if line!="":
        total += int(line)
    else:
        all_cals.append(total)
        total=0

print(max(all_cals))
print(sum(sorted(all_cals)[-3:]))
