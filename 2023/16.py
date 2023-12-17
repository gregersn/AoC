from dataclasses import dataclass


test_input = """.|...\\....
|.-.\\.....
.....|-...
........|.
..........
.........\\
..../.\\\\..
.-.-/..|..
.|....-|.\\
..//.|...."""


@dataclass
class Beam:
    x: int = 0
    y: int = 0
    dx: int = 1
    dy: int = 0


def direction_indicator(beam: Beam):
    if beam.dx == 1:
        return ">"

    if beam.dx == -1:
        return "<"

    if beam.dy == 1:
        return "v"

    if beam.dy == -1:
        return "^"


def trace_light(field: list[list[str]], pos: Beam):
    beams: list[Beam] = [
        pos,
    ]

    width = len(field[0])
    height = len(field)

    visits: list[list[set[str]]] = [
        [set() for _ in range(width)] for _ in range(height)
    ]

    while beams:
        beam = beams.pop(0)
        while beam.x >= 0 and beam.x < width and beam.y >= 0 and beam.y < height:
            if direction_indicator(beam) in visits[beam.y][beam.x]:
                beam.x = -1
                beam.y = -1
                break

            visits[beam.y][beam.x].add(direction_indicator(beam))
            current = field[beam.y][beam.x]
            if current == ".":
                beam.x += beam.dx
                beam.y += beam.dy
            elif current == "|":
                if abs(beam.dx) == 1:
                    beams.append(Beam(beam.x, beam.y - 1, 0, -1))
                    beams.append(Beam(beam.x, beam.y + 1, 0, 1))
                    beam.x = -1
                    beam.y = -1
                else:
                    beam.x += beam.dx
                    beam.y += beam.dy
            elif current == "-":
                if abs(beam.dy) == 1:
                    beams.append(Beam(beam.x - 1, beam.y, -1, 0))
                    beams.append(Beam(beam.x + 1, beam.y, 1, 0))
                    beam.x = -1
                    beam.y = -1
                else:
                    beam.x += beam.dx
                    beam.y += beam.dy
            elif current == "/":
                if beam.dy == -1:
                    beam.dy = 0
                    beam.dx = 1
                elif beam.dy == 1:
                    beam.dy = 0
                    beam.dx = -1
                elif beam.dx == -1:
                    beam.dx = 0
                    beam.dy = 1
                elif beam.dx == 1:
                    beam.dx = 0
                    beam.dy = -1

                beam.x += beam.dx
                beam.y += beam.dy
            elif current == "\\":
                if beam.dy == -1:
                    beam.dy = 0
                    beam.dx = -1
                elif beam.dy == 1:
                    beam.dy = 0
                    beam.dx = 1
                elif beam.dx == -1:
                    beam.dx = 0
                    beam.dy = -1
                elif beam.dx == 1:
                    beam.dx = 0
                    beam.dy = 1

                beam.x += beam.dx
                beam.y += beam.dy
            else:
                raise NotImplementedError(current)

    output = []
    for y in range(width):
        output.append(list())
        for x in range(height):
            if field[y][x] != ".":
                output[y].append(field[y][x])
            else:
                output[y].append(
                    len(visits[y][x])
                    if len(visits[y][x]) > 1
                    else list(visits[y][x])[0]
                    if len(visits[y][x]) > 0
                    else "."
                )
    return output, [["#" if len(s) > 0 else "." for s in row] for row in visits]


def count_energized(field: list[list[str]]) -> int:
    return sum(sum(c == "#" for c in row) for row in field)


def load_input(field: str) -> list[list[str]]:
    return [list(row.strip()) for row in field.split("\n") if row.strip()]


test_field = load_input(test_input)
line_length = len(test_field[0])
for line in test_field:
    assert len(line) == line_length

for row in trace_light(load_input(test_input), Beam(0, 0)):
    print(row)

assert count_energized((trace_light(load_input(test_input), Beam(0, 0)))[1]) == 46


data = load_input(open("2023/16_input", "r", encoding="utf8").read())
print(
    count_energized(
        (
            trace_light(
                data,
                Beam(0, 0),
            )
        )[1]
    )
)

largest = 0
height = len(data)
width = len(data[0])
print(f"Input data is {width} x {height}")

for y in range(height):
    largest = max(count_energized(trace_light(data, Beam(0, y, 1, 0))[1]), largest)
    largest = max(
        count_energized(trace_light(data, Beam(width - 1, y, -1, 0))[1]), largest
    )

for x in range(width):
    largest = max(count_energized(trace_light(data, Beam(x, 0, 0, 1))[1]), largest)
    largest = max(
        count_energized(trace_light(data, Beam(x, height - 1, 0, -1))[1]), largest
    )


print(largest)
