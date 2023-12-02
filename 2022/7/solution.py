from pathlib import Path
from itertools import accumulate

with open(Path(__file__).parent / "input.txt", encoding="utf-8") as f:
    lines = f.read().strip().split('\n')

dirs = {"/": 0}

for line in lines:
    match line.split():
        case '$', 'cd', '/':
            curr = ['/']
        case '$', 'cd', '..':
            curr.pop()
        case '$', 'cd', x:
            curr.append(x+'/')
            dirs[''.join(curr)] = 0
        case '$', 'ls':
            pass
        case 'dir', _:
            pass
        case size, _:
            for p in accumulate(curr):
                dirs[p] += int(size)

max_size = 100000
print(sum(v for v in dirs.values() if v<max_size))

total_size = dirs["/"]
to_remove = total_size - 40000000
print(min(v for v in dirs.values() if v>to_remove))
