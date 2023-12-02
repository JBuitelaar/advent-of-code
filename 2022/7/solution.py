from pathlib import Path
from dataclasses import dataclass
from typing import Optional
from functools import cached_property

with open(Path(__file__).parent / "input.txt", encoding="utf-8") as f:
    lines = f.read().strip().split('\n')

all_folders = dict()

@dataclass
class Folder:
    path: str
    parent: Optional["Folder"]
    size: int
    sub_folder_names: list[str]

    @cached_property
    def full_size(self):
        return sum([all_folders[f].full_size for f in self.sub_folder_names], 0) + self.size

    def __repr__(self) -> str:
        return f"Folder({self.path} ({self.size}) [{[f.split('/')[-1] for f in self.sub_folder_names]}])"

assert lines[0] == "$ cd /"

current_path = ""
current_folder = None

line_no = 0
while line_no < len(lines):
    line = lines[line_no]
    line_no += 1
    if line == "$ cd ..":
        current_size = 0
        current_folder = current_folder.parent
        current_path = current_folder.path
        # print(f"{current_path=}")
    elif line.startswith("$ cd "):
        name = line[5:]
        current_path += f"/{name}" if name != "/" else ""
        current_size = 0
        current_folder = Folder(current_path, current_folder, 0, [])
        all_folders[current_path]=current_folder
    elif line.startswith("$ ls"):
        while line_no < len(lines) and not lines[line_no].startswith("$"):
            line = lines[line_no]
            line_no += 1
            if line.startswith("dir "):
                child_name = line[4:]
                current_folder.sub_folder_names.append(f"{current_path}/{child_name}")
            else: 
                size, _name = line.split(" ")
                current_folder.size += int(size)

all_sizes = {k: v.full_size for k,v in all_folders.items()}

max_size = 100000
print(sum(v for k,v in all_sizes.items() if v<max_size))

total_size = all_sizes[""]
to_remove = total_size - 40000000
print(min(v for k,v in all_sizes.items() if v>to_remove))
