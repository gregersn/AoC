from itertools import groupby
from typing import Iterator


def run_length_encode(data: str) -> Iterator[tuple[str, int]]:
    """Returns run length encoded Tuples for string"""
    # A memory efficient (lazy) and pythonic solution using generators
    return ((x, sum(1 for _ in y)) for x, y in groupby(data))


test_input = """O....#....
O.OO#....#
.....##...
OO.#O....O
.O.....O#.
O.#..O.#.#
..O..#O..O
.......O..
#....###..
#OO..#....
"""


def calculate_load(rocks: list[list[str]], direction: int = 0):
    max_load = len(rocks)
    total = 0
    for idx, row in enumerate(rocks):
        total += sum([r == "O" for r in row]) * (max_load - idx)

    return total


def roll_rocks(rocks: list[str], direction: int = 0):
    print(rocks)
    if direction in [0, 2]:
        rocks = rotate_pattern(rocks)

    new_pattern = [gather_rocks(line) for line in rocks]

    if direction in [0, 2]:
        new_pattern = rotate_pattern(new_pattern)

    return new_pattern


def load_data(input: str):
    return [line.strip() for line in input.split("\n") if line.strip()]


def gather_rocks(rock_line: list[str], reverse: bool = True):
    return "#".join(
        ["".join(sorted(part, reverse=reverse)) for part in rock_line.split("#")]
    )


def rotate_pattern(pattern: list[str]):
    return [
        "".join([pattern[i][idx] for i in range(len(pattern))])
        for idx in range(len(pattern[0]))
    ]


test_data = load_data(test_input)

assert rotate_pattern(rotate_pattern(test_data)) == test_data

print("\n".join("".join(t) for t in test_data))
new_rocks = roll_rocks(test_data)
print("\n".join("".join(t) for t in test_data))
print(calculate_load(new_rocks))


input_data = load_data(open("2023/14_input", "r", encoding="utf8").read())
rolled_rocks = roll_rocks(input_data)
print(calculate_load(rolled_rocks))
