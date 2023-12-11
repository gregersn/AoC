import itertools
from dataclasses import dataclass


test_input = """...#......
.......#..
#.........
..........
......#...
.#........
.........#
..........
.......#..
#...#....."""


test_input_expanded = """....#........
.........#...
#............
.............
.............
........#....
.#...........
............#
.............
.............
.........#...
#....#......."""


def load_data(input: str) -> str:
    return input


def expand_map(map: str, expansion: int = 2) -> str:
    rows = map.split("\n")
    blank_rows = [idx for (idx, row) in enumerate(rows) if "#" not in row]
    columns = ["".join([row[i] for row in rows if row]) for i in range(len(rows[0]))]
    blank_columns = [idx for (idx, column) in enumerate(columns) if "#" not in column]

    expanded_columns = []
    for idx, column in enumerate(columns):
        if idx in blank_columns:
            for _ in range(expansion - 1):
                expanded_columns.append(column)
        expanded_columns.append(column)

    new_rows = [
        "".join([column[i] for column in expanded_columns])
        for i in range(len(expanded_columns[0]))
    ]
    expanded_rows = []
    for idx, row in enumerate(new_rows):
        if idx in blank_rows:
            for _ in range(expansion - 1):
                expanded_rows.append(row)
        expanded_rows.append(row)

    return "\n".join(expanded_rows)


def expand_map_coordinates(map: str, expansion: int = 2) -> str:
    rows = map.split("\n")
    blank_rows = [idx for (idx, row) in enumerate(rows) if "#" not in row]
    columns = ["".join([row[i] for row in rows if row]) for i in range(len(rows[0]))]
    blank_columns = [idx for (idx, column) in enumerate(columns) if "#" not in column]

    return (blank_rows, blank_columns)


@dataclass
class Galaxy:
    row: int
    column: int


def find_galaxies(
    map: str, expansions: tuple[list[int], list[int]] = ([], []), amount: int = 1
) -> list[Galaxy]:
    galaxies = []
    expanded_row_index = 0
    for row_index, row in enumerate(map.split("\n")):
        expanded_column_index = 0
        for column_index, column in enumerate(row):
            if column == "#":
                galaxies.append(Galaxy(expanded_row_index, expanded_column_index))

            if column_index in expansions[1]:
                expanded_column_index += amount
            else:
                expanded_column_index += 1

        if row_index in expansions[0]:
            expanded_row_index += amount
        else:
            expanded_row_index += 1

    return galaxies


def distance(a: Galaxy, b: Galaxy):
    return abs(b.row - a.row) + abs(b.column - a.column)


def find_distances(galaxies: list[Galaxy]):
    combinations = itertools.combinations(galaxies, 2)
    distances = [distance(a, b) for a, b in combinations]
    return distances


test_map = load_data(test_input)
expanded_test_map = expand_map(test_map)
assert expanded_test_map == test_input_expanded

expanded_test_coordinates = expand_map_coordinates(test_map, 2)
galaxies = find_galaxies(test_map, expanded_test_coordinates, 2)
assert len(galaxies) == 9
distances = find_distances(galaxies)
assert sum(distances) == 374

expanded_test_map = expand_map(test_map, 10)
galaxies = find_galaxies(expanded_test_map)
assert len(galaxies) == 9
distances = find_distances(galaxies)
assert sum(distances) == 1030

# expanded_test_map = expand_map(test_map, 100)
expanded_test_coordinates = expand_map_coordinates(test_map, 100)
galaxies = find_galaxies(test_map, expanded_test_coordinates, 100)
assert len(galaxies) == 9
distances = find_distances(galaxies)
assert sum(distances) == 8410, sum(distances)


step1_map = load_data(open("2023/11_input", "r", encoding="utf8").read())
expanded_step1_map = expand_map(step1_map)
step1_galaxies = find_galaxies(expanded_step1_map)
distances = find_distances(step1_galaxies)
print(sum(distances))

step2_expanded_coordinates = expand_map_coordinates(step1_map, 1_000_000)
step2_galaxies = find_galaxies(
    step1_map, expansions=step2_expanded_coordinates, amount=1_000_000
)
distances = find_distances(step2_galaxies)
print(sum(distances))
