test_map = """...........
.....###.#.
.###.##..#.
..#.#...#..
....#.#....
.##..S####.
.##..#...#.
.......##..
.##.#.####.
.##..##.##.
...........
"""

test_six_step = """...........
.....###.#.
.###.##.O#.
.O#O#O.O#..
O.O.#.#.O..
.##O.O####.
.##.O#O..#.
.O.O.O.##..
.##.#.####.
.##O.##.##.
...........
"""


def load(indata: str):
    return [list(row.strip()) for row in indata.split("\n") if row.strip()]


def step(map: list[list[str]]):
    height = len(map)
    width = len(map[0])
    positions = [
        (x, y)
        for y in range(len(map))
        for x in range(len(map[0]))
        if map[y][x] in ["S", "O"]
    ]

    extend = False
    for x, y in positions:
        map[y][x] = "."
        if x == 0 or y == 0 or x == width - 1 or y == height - 1:
            extend = True

    offset_x = 0
    offset_y = 0
    if extend:
        new_map = []
        for row in map:
            new_map.append(row * 3)
        map = new_map * 3
        offset_x = width
        offset_y = height

    for x, y in positions:
        if map[y + offset_y][x + offset_x - 1] == ".":
            map[y + offset_y][x + offset_x - 1] = "O"

        if map[y + offset_y - 1][x + offset_x] == ".":
            map[y + offset_y - 1][x + offset_x] = "O"

        if map[y + offset_y + 1][x + offset_x] == ".":
            map[y + offset_y + 1][x + offset_x] = "O"

        if map[y + offset_y][x + offset_x + 1] == ".":
            map[y + offset_y][x + offset_x + 1] = "O"

    return map


def count_positions(map: list[list[str]]):
    return sum(c in ["O", "S"] for row in map for c in row)


input_map = load(test_map)

for _ in range(6):
    input_map = step(input_map)

assert input_map == load(test_six_step)
print(count_positions(input_map))

input_map = load(test_map)

for _ in range(100):
    input_map = step(input_map)

assert count_positions(input_map) == 6536


step1_map = load(open("2023/21_input", "r", encoding="utf8").read())
for _ in range(64):
    step1_map = step(step1_map)

print(count_positions(step1_map))

step1_map = load(open("2023/21_input", "r", encoding="utf8").read())
for _ in range(64):
    step1_map = step(step1_map)
