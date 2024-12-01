import time
from aocd.models import Puzzle
from dataclasses import dataclass, field

puzzle = Puzzle(2021, 4)
data = puzzle.input_data
# data = puzzle.examples[0].input_data

start_time = time.time()

draw, *cards = data.strip().split("\n\n")
draws = list(map(int, draw.split(",")))
draws


@dataclass
class Card:
    vals: list[int]
    marked: list[bool] = field(default_factory=lambda: [False] * 25)

    def __repr__(self):
        res = "\n"

        for ix, m in enumerate(self.marked):
            v = self.vals[ix]
            res += "XX " if m else f"{v:2d} "
            if not (ix + 1) % 5:
                res += "\n"
        return res

    def finished(self, ix):
        quotient, remainder = divmod(ix, 5)
        row_start = quotient * 5
        return all(card.marked[j] for j in range(row_start, row_start + 5)) or all(
            card.marked[j * 5 + remainder] for j in range(5)
        )

    def mark(self, draw):
        try:
            ix = self.vals.index(draw)
        except ValueError:
            return False
        self.marked[ix] = True

        if self.finished(ix):
            val = sum(v for v, m in zip(self.vals, self.marked) if not m)
            return draw * val
        return False


cards = [Card([int(v) for v in card.replace("\n", " ").split()]) for card in cards]
ans1 = ans2 = 0
for draw in draws:
    if ans2:
        break
    remaining_cards = []
    for card in cards:
        score = card.mark(draw)

        if score:
            if not ans1:
                ans1 = score
                timer = time.time() - start_time
                print(f"{ans1=}, {timer=:.2f}s")

            if len(cards) == 1:
                ans2 = score
                timer = time.time() - start_time
                print(f"{ans2=}, {timer=:.2f}s")
                break
        else:
            remaining_cards.append(card)
    cards = remaining_cards
