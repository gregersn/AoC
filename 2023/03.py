from dataclasses import dataclass
from typing import List


test_input = """
467..114..
...*......
..35..633.
......#...
617*......
.....+.58.
..592.....
......755.
...$.*....
.664.598.."""

test_answer = 4361
test_gear_ratios = 467835


@dataclass
class Symbol:
    row: int
    column: int
    symbol: str


@dataclass
class Number:
    row: int
    column: int
    end: int
    number: int


@dataclass
class Gear:
    symbol: Symbol
    ratio1: Number
    ratio2: Number


def locate_symbols(schematic: List[str]) -> List[Symbol]:
    coordinates = []

    height = len(schematic)
    width = len(schematic[0])

    for y in range(height):
        row = schematic[y]
        assert len(row) == width
        for x in range(width):
            if row[x] != "." and not row[x].isdigit():
                coordinates.append(Symbol(y, x, row[x]))

    return coordinates


def locate_numbers(schematic: List[str]) -> List[Number]:
    numbers = []

    height = len(schematic)
    width = len(schematic)

    for y in range(height):
        row = schematic[y]
        assert len(row) == width
        x = 0
        while x < width:
            if row[x].isdigit():
                start = x
                while (x + 1) < len(row) and row[x + 1].isdigit():
                    x += 1
                end = x

                number_source = row[start : end + 1]
                number = int(number_source, 10)

                numbers.append(Number(y, start, end, number))
            x += 1

    return numbers


def adjacent(symbol: Symbol, number: Number) -> bool:
    if symbol.row > number.row + 1 or symbol.row < number.row - 1:
        # print("Not adjacent, rows too far apart: ", symbol, number)
        return False

    if symbol.row == number.row and (
        symbol.column == number.column - 1 or symbol.column == number.end + 1
    ):
        # print("Adjacent: ", symbol, number)
        return True

    if symbol.row == number.row - 1 or symbol.row == number.row + 1:
        if symbol.column >= number.column - 1 and symbol.column <= number.end + 1:
            # print("Adjacent: ", symbol, number)
            return True

    # print("Not adjacent: ", symbol, number)
    return False


def locate_part_numbers(schematic: str) -> List[int]:
    part_numbers = []
    transformed_schematic = [
        row.strip() for row in schematic.split("\n") if len(row) > 1
    ]

    symbols = locate_symbols(transformed_schematic)
    numbers = locate_numbers(transformed_schematic)

    while numbers:
        number = numbers.pop(0)
        for symbol in symbols:
            if adjacent(symbol, number):
                part_numbers.append(number.number)
                break

    return part_numbers


def locate_gears(symbols: List[Symbol], numbers: List[Number]):
    potentials = [symbol for symbol in symbols if symbol.symbol == "*"]

    gears: List[Gear] = []

    for potential in potentials:
        adjacants = []
        for number in numbers:
            if adjacent(potential, number):
                adjacants.append(number)

            if len(adjacants) > 2:
                break

        if len(adjacants) == 2:
            gears.append(Gear(potential, adjacants[0], adjacants[1]))

    return gears


def locate_gear_ratios(schematic: str) -> List[int]:
    transformed_schematic = [
        row.strip() for row in schematic.split("\n") if len(row) > 1
    ]

    symbols = locate_symbols(transformed_schematic)
    numbers = locate_numbers(transformed_schematic)

    gears = locate_gears(symbols, numbers)
    ratios = [gear.ratio1.number * gear.ratio2.number for gear in gears]

    return ratios


result = sum(locate_part_numbers(test_input))
assert result == test_answer, result

gear_ratios = sum(locate_gear_ratios(test_input))
assert gear_ratios == test_gear_ratios, result

actual_input = open("03/input", "r", encoding="utf8").read()
result = sum(locate_part_numbers(actual_input))
print(result)

restul = sum(locate_gear_ratios(actual_input))
print(restul)
