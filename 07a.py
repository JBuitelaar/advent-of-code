from collections import Counter 
from aocd.models import Puzzle
import webbrowser
chrome_path = r"C:\Program Files\Google\Chrome\Application\chrome.exe"
webbrowser.register('chrome', None, webbrowser.BackgroundBrowser(chrome_path),preferred=True)

puzzle = Puzzle(2023,7)
data = puzzle.input_data
# example = puzzle.examples[0]
# data = example.input_data
# print("example answers: ",example.answer_a, example.answer_b)
# print(data)

lines = data.strip().split('\n')

vals = {"T": 10, "J": 11, "Q": 12, "K": 13, "A": 14}

def scores(cards):
    count = Counter(cards).values()
    values = [vals.get(c) or int(c) for c in cards]
    return [ -len(count),max(count)]+values

hands = [(cards,int(value),scores(cards)) for cards,value in [line.split() for line in lines ]]
hands = sorted(hands,key=lambda r:r[2])
ans1=sum(ix*hand[1] for ix,hand in enumerate(hands,1))
print([hand[0] for hand in hands[-10:]])
print(f"{ans1=}")
