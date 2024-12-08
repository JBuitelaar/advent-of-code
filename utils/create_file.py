"""create a file for the next puzzle"""

import os
import re
from datetime import date

today = date.today()


def filename(year, day):
    return f"{year}/{day:02d}.py"


year = today.year
day = today.day

# create file for today or tomorrow:
if os.path.exists(filename(year, day)):
    day += 1

fn = filename(year, day)

assert not os.path.exists(fn), f"{fn} already exists"

with open("template.py", "r") as f:
    content = f.read()

content = re.sub(r"Puzzle\(\d{4},\d{1,2}\)", f"Puzzle({year},{day})", content, 1)

filename = f"{year}/{day:02d}.py"

with open(filename, "w") as f:
    f.write(content)

print(f"Created {filename}")
