import math


test_input = """2413432311323
3215453535623
3255245654254
3446585845452
4546657867536
1438598798454
4457876987766
3637877979653
4654967986887
4564679986453
1224686865563
2546548887735
4322674655533"""


test_result_path = """2>>34^>>>1323
32v>>>35v5623
32552456v>>54
3446585845v52
4546657867v>6
14385987984v4
44578769877v6
36378779796v>
465496798688v
456467998645v
12246868655<v
25465488877v5
43226746555v>"""

test_result = 102


def load_input(indata: str):
    return [[int(x, 10) for x in line] for line in indata.split("\n")]


class Cart:
    x: int = 0
    y: int = 0
    dx: int = 0
    dy: int = 0


def find_path(field: list[list[int]]):
    width = len(field[0])
    height = len(field)

    value_map = [[0] * width for _ in range(height)]

    for y in range(height - 1, -1, -1):
        for x in range(width - 1, -1, -1):
            value_map[y][x] = field[y][x] + (width - 1 - x) + (height - 1 - y)

            min_neighbour = math.inf

            if x < (width - 1) or y < (height - 1):
                if x < (width - 1):
                    min_neighbour = min(min_neighbour, value_map[y][x + 1])
                if y < (height - 1):
                    min_neighbour = min(min_neighbour, value_map[y + 1][x])

                value_map[y][x] += min_neighbour

    for line in value_map:
        print(line)

    cart = Cart()
    straight = 0
    path: list[tuple[int, int]] = [(cart.x, cart.y)]
    while (cart.y != height - 1) or (cart.x != width - 1):
        next_pos = []

        if cart.y > 0 and cart.dy != 1 and not (cart.dy == -1 and straight >= 2):
            next_pos.append((0, -1))

        if cart.x > 0 and cart.dx != 1 and not (cart.dx == -1 and straight >= 2):
            next_pos.append((-1, 0))

        if (
            cart.y < height - 1
            and cart.dy != -1
            and not (cart.dy == 1 and straight >= 2)
        ):
            next_pos.append((0, 1))

        if (
            cart.x < width - 1
            and cart.dx != -1
            and not (cart.dx == 1 and straight >= 2)
        ):
            next_pos.append((1, 0))

        min_pos = next_pos.pop(0)
        min_value = value_map[cart.y + min_pos[1]][cart.x + min_pos[0]]

        while len(next_pos):
            pos = next_pos.pop(0)
            if value_map[cart.y + pos[1]][cart.x + pos[0]] < min_value:
                min_value = value_map[cart.y + pos[1]][cart.x + pos[0]]
                min_pos = pos

        if cart.dx == min_pos[0] and cart.dy == min_pos[1]:
            straight += 1
        else:
            straight = 0

        cart.x += min_pos[0]
        cart.y += min_pos[1]
        cart.dx = min_pos[0]
        cart.dy = min_pos[1]

        path.append((cart.x, cart.y))
        print(cart.x, cart.y)

    print(path)
    print(len(path))

    return path


def heat_loss(field: list[list[int]], path: list[tuple[int, int]]):
    loss = 0
    cart = Cart()
    while path:
        move = path.pop(0)
        cart.x = move[0]
        cart.y = move[1]
        print(cart.x, cart.y)
        loss += field[cart.y][cart.x]

    return loss


test_field = load_input(test_input)
res = heat_loss(test_field, find_path(test_field))

assert res == test_result, res
