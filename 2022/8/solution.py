from pathlib import Path

with open(Path(__file__).parent / "input.txt", encoding="utf-8") as f:
    lines = f.read().strip().split('\n')

hts = [list(map(int,line)) for line in lines]
# hts = [int(c) for line in lines for c in line]
hts_t = list(map(list, zip(*hts)))

count = 0
for iy, row in enumerate(hts):
    if iy == 0 or iy == len(hts)-1:
        # all visible
        count+=len(row)
    else:
        for ix, val in enumerate(row):
            if ix == 0 or ix == len(row)-1:
                count+=1
            elif max(row[:ix])<val or max(row[ix+1:])<val: 
                count+=1
            elif max(hts_t[ix][:iy])<val or max(hts_t[ix][iy+1:])<val:
                count+=1

print(count)

def count_lower(heights,tree_height):
    for it,v in enumerate(heights):
        if v>=tree_height:
            return it+1
    return len(list(heights))

counts = []
for iy in range(1,len(hts)-1):
    row = hts[iy]
    for ix in range(1,len(row)-1):
        val = row[ix]
        count = count_lower(list(reversed(row[:ix])),val)*count_lower(row[ix+1:],val)*count_lower(list(reversed(hts_t[ix][:iy])),val)*count_lower(hts_t[ix][iy+1:],val)
        counts.append(count)

print(max(counts))
