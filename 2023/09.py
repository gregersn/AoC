from itertools import pairwise
from typing import Callable


test_input = """0 3 6 9 12 15
1 3 6 10 15 21
10 13 16 21 30 45"""


def load_input(input: str) -> list[list[int]]:
    output = []

    lines = input.split("\n")
    for line in lines:
        output.append([int(x, 10) for x in line.strip().split(" ") if line])

    return output


def extrapolate(input: list[int]) -> list[int]:
    if not any(input):
        return input + [
            0,
        ]

    prev = extrapolate([(b - a) for (a, b) in pairwise(input)])
    return input + [input[-1] + prev[-1]]


def extrapolate2(input: list[int]) -> list[int]:
    if not any(input):
        return [
            0,
        ] + input

    prev = extrapolate2([(b - a) for (a, b) in pairwise(input)])
    return [input[0] - prev[0]] + input


def extrapolate_data(
    input: list[list[int]], extrapolator: Callable[[list[int]], list[int]]
) -> list[list[int]]:
    return [extrapolator(line) for line in input]


def total_new(input: list[list[int]], pos: int = -1):
    return sum([v[pos] for v in input])


data = load_input(test_input)

assert extrapolate(data[0]) == [0, 3, 6, 9, 12, 15, 18], extrapolate(data[0])

assert total_new(extrapolate_data(data, extrapolate)) == 114

assert extrapolate2(data[2]) == [5, 10, 13, 16, 21, 30, 45], extrapolate2(data[2])


data = load_input(open("2023/09_input", "r", encoding="utf8").read())

print(total_new(extrapolate_data(data, extrapolate)))
print(total_new(extrapolate_data(data, extrapolate2), 0))
