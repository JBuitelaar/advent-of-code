from pathlib import Path

with open(Path(__file__).parent / "input.txt", encoding="utf-8") as f:
    txt = f.read().strip()

msg_size = 14

for msg_size in (4,14):
    ix = 0
    while len(set(txt[ix:ix+msg_size]))!=msg_size:
        ix += 1

    print(ix+msg_size)