from dataclasses import dataclass


test_input = """R 6 (#70c710)
D 5 (#0dc571)
L 2 (#5713f0)
D 2 (#d2c081)
R 2 (#59c680)
D 2 (#411b91)
L 5 (#8ceee2)
U 2 (#caa173)
L 1 (#1b58a2)
U 2 (#caa171)
R 2 (#7807d2)
U 3 (#a77fa3)
L 2 (#015232)
U 2 (#7a21e3)
"""


@dataclass
class Vertex:
    x: int
    y: int


DIRECTIONS = {
    "U": Vertex(0, -1),
    "D": Vertex(0, 1),
    "L": Vertex(-1, 0),
    "R": Vertex(1, 0),
}

NtoD = ["R", "D", "L", "U"]


def load_instructions(instructions: str):
    result = []
    for line in instructions.split("\n"):
        if not line.strip():
            continue
        d, l, c = line.split(" ")

        result.append((DIRECTIONS[d], int(l, 10), c))

    return result


def dig_edges(instructions: str) -> list[Vertex]:
    current = Vertex(0, 0)
    vertices = [current]
    for direction, length, color in instructions:
        current = Vertex(
            current.x + direction.x * length,
            current.y + direction.y * length,
        )
        vertices.append(current)

    return vertices


def calc_length(vertices: list[Vertex]):
    prev = vertices[-1]
    total = 0

    for v in vertices:
        d = abs(v.x - prev.x) + abs(v.y - prev.y)
        total += d
        prev = v
    return total


def dig_fill(instructions: str):
    edges = dig_edges(instructions)
    p0 = edges[0]
    s = 0
    for p1 in edges[1:-1]:
        s += (p0.y + p1.y) * (p0.x - p1.x)
        p0 = p1

    return abs(s // 2) + calc_length(edges) // 2 + 1


def rewrite_instructions(instructions: str):
    new_instructions = []
    for c, l, real_instruction in instructions:
        length = int(real_instruction[2:-2], 16)
        direction = NtoD[int(real_instruction[-2], 10)]

        new_instructions.append((DIRECTIONS[direction], length, ""))

    return new_instructions


instructions = load_instructions(test_input)
edges = dig_edges(instructions)
edge_length = calc_length(edges)
assert edge_length == 38, edge_length

area = dig_fill(instructions)
assert area == 62, area


instructions = rewrite_instructions(instructions)
res = dig_fill(instructions)
assert res == 952408144115

input_data = open("2023/18_input", "r", encoding="utf8").read()
instructions = load_instructions(input_data)
print(dig_fill(instructions))

instructions = rewrite_instructions(instructions)
print(dig_fill(instructions))
