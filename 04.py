from aocd.models import Puzzle
puzzle = Puzzle(2023,4)
data = puzzle.input_data
# example = puzzle.examples[0]
# data = example.input_data
print(data)

lines = data.strip().split('\n')

line = lines[0]
last = len(line)

ans1 = 0

last_card = len(lines)
card_count = [1]*last_card

for ix, line in enumerate(lines):
    _card,num_str = line.split(":")
    win_str, hand_str = num_str.split(" | ")

    winning_numbers = set(win_str.split())
    numbers = set(hand_str.split())
    count = len(winning_numbers&numbers)
    if count:
        ans1 += 2**(count-1)

    for v in range(ix+1,min(last_card,ix+1+count)):
        card_count[v] += card_count[ix]

print(ans1)
ans2 = sum(card_count)
print(ans2)
