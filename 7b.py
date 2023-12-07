from collections import Counter 
from aocd.models import Puzzle

puzzle = Puzzle(2023,7)
data = puzzle.input_data
# example = puzzle.examples[0]
# data = example.input_data
# print("example answers: ",example.answer_a, example.answer_b)

lines = data.strip().split('\n')

vals = {"T": 10, "J": 1, "Q": 12, "K": 13, "A": 14}

def scores(cards):
    count = Counter(cards)
    js = count.pop("J",0)
    if js == 5:
        v = -1
        max_count = 5
    else:
        max_count = max(count.values())+js
        v= -len(count)
    values = [vals.get(c) or int(c) for c in cards]
    return [v,max_count]+values

hands = [(cards,int(value),scores(cards)) for cards,value in [line.split() for line in lines ]]
hands = sorted(hands,key=lambda r:r[2])
print([hand[0] for hand in hands[-10:]])
ans2=sum(ix*hand[1] for ix,hand in enumerate(hands,1))
print(f"{ans2=}")
