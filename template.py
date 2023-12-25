import time
import itertools
import math
from collections import defaultdict, Counter
from functools import reduce, cache
# import networkx as nx
from aocd.models import Puzzle
import webbrowser
chrome_path = r"C:\Program Files\Google\Chrome\Application\chrome.exe"
webbrowser.register('chrome', None, webbrowser.BackgroundBrowser(chrome_path),preferred=True)

puzzle = Puzzle(2024,1)
# data = puzzle.input_data
data = puzzle.examples[0].input_data
print(data)
# print(data[:1000])

start_time = time.time()

lines = data.strip().split('\n')
# [ for line in lines]

ans1 = 0
timer = time.time() - start_time
print(f"{ans1=}, {timer=:.2f}s")
# from aocd import submit
# submit(ans1)
ans2=0
timer = time.time() - start_time
print(f"{ans2=}, {timer=:.2f}s")