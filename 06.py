from aocd.models import Puzzle
import math

puzzle = Puzzle(2023,6)
data = puzzle.input_data
# example = puzzle.examples[0]
# data = example.input_data
# print("example answers: ",example.answer_a, example.answer_b)
print(data)

lines = data.strip().split('\n')
times, distances = [[int(v) for v in line.split(": ")[1].split()] for line in lines]


def sol_count(t,d):
    # Solve: (t-x)*x > d
    # x^2 - tx + d < 0
    # a = 1
    b = -t
    c = d
    discr = (b**2) - (4*c)
    if discr <= 0:
        return 0
    sol1 = (-b-math.sqrt(discr))/2
    sol2 = (-b+math.sqrt(discr))/2
    return math.ceil(sol2) - math.floor(sol1) - 1

ans1 = 1
for time,distance in zip(times,distances):
    count = sol_count(time,distance)
    # print(time,distance,count)
    ans1 *= count

print(f"{ans1=}")

time,distance = [int(line.split(": ")[1].replace(" ","")) for line in lines]
ans2 = sol_count(time,distance)
print(f"{ans2=}")
