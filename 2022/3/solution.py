from pathlib import Path

with open(Path(__file__).parent / "input.txt", encoding="utf-8") as f:
    lines = f.read().strip().split('\n')

base_val = ord("A")-1
def priority(char):
    return ord(char.upper())-base_val + 26 * (char.isupper())

def parse_line(line):
    split_ix = int(len(line)/2)
    left,right = line[:split_ix], line[split_ix:]
    for char in left:
        if char in right:
            return priority(char)
        
    raise(ValueError("No common char found"))

print(sum(map(parse_line, lines)))

def parse_group(group):
    first = group[0]
    for item in first:
        if item in group[1] and item in group[2]:
            return priority(item)

groups = [lines[d:d+3] for d in range(0,len(lines),3)]
print(sum(parse_group(group) for group in groups))
