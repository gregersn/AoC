from dataclasses import dataclass


@dataclass
class Pos:
    x: int
    y: int


class Pipe:
    pos: Pos
    distance: int = -1
    north: bool = False
    east: bool = False
    south: bool = False
    west: bool = False
    main_line: bool = False
    symbol: str = "."

    ground: bool = True
    inside: bool = False

    def __str__(self):
        if self.ground:
            return "."
        if self.north and self.south:
            return "|"

        if self.east and self.west:
            return "-"

        if self.north and self.west:
            return "J"

        if self.north and self.east:
            return "L"

        if self.south and self.west:
            return "7"

        if self.south and self.east:
            return "F"

        raise Exception(self.symbol, self.north, self.south, self.east, self.west)


class Map:
    pipes: list[list[Pipe]]
    start_pipe = None
    width: int
    height: int

    def __init__(self, width: int, height: int):
        self.pipes = [[Pipe() for _ in range(width)] for _ in range(height)]

        self.width = width
        self.height = height

        assert len(self.pipes) == height
        assert len(self.pipes[0]) == width

    def add_pipe(self, x: int, y: int, pipe_type: str, start: bool = False):
        pipe = Pipe()
        pipe.ground = False
        pipe.pos = Pos(x, y)
        pipe.symbol = pipe_type

        pipe.north = pipe_type in ["L", "J", "|"]
        pipe.south = pipe_type in ["F", "7", "|"]
        pipe.east = pipe_type in ["L", "F", "-"]
        pipe.west = pipe_type in ["J", "7", "-"]

        self.pipes[y][x] = pipe
        if pipe_type == "S" and start:
            self.start_pipe = self.pipes[y][x]

    def connect_start(self):
        assert self.start_pipe
        start = self.start_pipe
        start_pos = start.pos

        if (
            start_pos.x > 0
            and self.pipes[start_pos.y][start_pos.x - 1]
            and self.pipes[start_pos.y][start_pos.x - 1].east
        ):
            start.west = True

        if (
            start_pos.y > 0
            and self.pipes[start_pos.y - 1][start_pos.x]
            and self.pipes[start_pos.y - 1][start_pos.x].south
        ):
            start.north = True

        if (
            start_pos.x < self.width
            and self.pipes[start_pos.y][start_pos.x + 1]
            and self.pipes[start_pos.y][start_pos.x + 1].west
        ):
            start.east = True

        if (
            start_pos.y < self.height
            and self.pipes[start_pos.y + 1][start_pos.x]
            and self.pipes[start_pos.y + 1][start_pos.x].north
        ):
            start.south = True

        assert sum([start.north, start.south, start.east, start.west]) > 1, [
            start.north,
            start.south,
            start.east,
            start.west,
        ]

    def get_pipes(self):
        pipes = []
        for y in range(self.height):
            for x in range(self.width):
                if self.pipes[y][x]:
                    pipes.append(self.pipes[y][x])
        return pipes

    def map_distances(self):
        self.start_pipe.distance = 0
        checked: list[Pipe] = []
        queue: list[Pipe] = [self.start_pipe]
        while queue:
            current = queue.pop(0)
            current.main_line = True
            if current.north:
                north_pipe = self.pipes[current.pos.y - 1][current.pos.x]
                if north_pipe not in checked:
                    north_pipe.distance = current.distance + 1
                    queue.append(north_pipe)
            if current.south:
                south_pipe = self.pipes[current.pos.y + 1][current.pos.x]
                if south_pipe not in checked:
                    south_pipe.distance = current.distance + 1
                    queue.append(south_pipe)
            if current.west:
                west_pipe = self.pipes[current.pos.y][current.pos.x - 1]
                if west_pipe not in checked:
                    west_pipe.distance = current.distance + 1
                    queue.append(west_pipe)
            if current.east:
                east_pipe = self.pipes[current.pos.y][current.pos.x + 1]
                if east_pipe not in checked:
                    east_pipe.distance = current.distance + 1
                    queue.append(east_pipe)
            checked.append(current)

    def map_internal(self):
        """

        FJL7

        F7 = no change
        LJ = no change

        L7 = change
        FJ = change
        """
        for y in range(self.height):
            inside = False
            prev_pipe = None
            for x in range(self.width):
                current: Pipe = self.pipes[y][x]

                if current.main_line:
                    if str(current) == "-":
                        continue

                    if str(current) == "|":
                        inside = not inside
                    elif str(current) == "7" and str(prev_pipe) == "L":
                        inside = not inside
                    elif str(current) == "J" and str(prev_pipe) == "F":
                        inside = not inside

                if not current.main_line:
                    current.inside = inside

                prev_pipe = current

    def __str__(self):
        return "\n".join(
            [
                "".join(
                    [
                        str(p) if (not p.ground) else ("I" if p.inside else "O")
                        for p in line
                    ]
                )
                for line in self.pipes
            ]
        )

    def distances(self):
        return "\n".join(
            [
                "".join(
                    [
                        str(p.distance) if p is not None and not p.ground else "."
                        for p in line
                    ]
                )
                for line in self.pipes
            ]
        )

    def mainline(self):
        return "\n".join(
            [
                "".join(["#" if p is not None and p.main_line else "." for p in line])
                for line in self.pipes
            ]
        )


def load_input(input: str):
    lines = input.split("\n")
    height = len(lines)
    width = len(lines[0].strip())

    map = Map(width, height)
    for iy, line in enumerate(lines):
        for ix, pos_type in enumerate(line):
            if pos_type == ".":
                # Ground
                continue
            map.add_pipe(ix, iy, pos_type, pos_type == "S")

    map.connect_start()
    return map


def find_distance(map: Map):
    map.map_distances()
    map.map_internal()

    for line in map.pipes:
        print(", ".join([str(p.inside) for p in line]))

    print(map)
    print("")
    print(map.distances())
    print("")
    print(map.mainline())
    print("")
    return max([p.distance for p in map.get_pipes()]), sum(
        [pipe.inside for line in map.pipes for pipe in line]
    )


test_input = """.....
.S-7.
.|.|.
.L-J.
....."""

test_input2 = """..F7.
.FJ|.
SJ.L7
|F--J
LJ..."""

# assert find_distance(load_input(test_input)) == 4
# assert find_distance(load_input(test_input2)) == 8


test_input3 = """...........
.S-------7.
.|F-----7|.
.||.....||.
.||.....||.
.|L-7.F-J|.
.|..|.|..|.
.L--J.L--J.
..........."""

# find_distance(load_input(test_input3))

# print(find_distance(load_input(open("2023/10_input", "r", encoding="utf8").read())))

test_input4 = """.F----7F7F7F7F-7....
.|F--7||||||||FJ....
.||.FJ||||||||L7....
FJL7L7LJLJ||LJ.L-7..
L--J.L7...LJS7F-7L7.
....F-J..F7FJ|L7L7L7
....L7.F7||L7|.L7L7|
.....|FJLJ|FJ|F7|.LJ
....FJL-7.||.||||...
....L---J.LJ.LJLJ..."""


print(find_distance(load_input(test_input4)))


test_input5 = """FF7FSF7F7F7F7F7F---7
L|LJ||||||||||||F--J
FL-7LJLJ||||||LJL-77
F--JF--7||LJLJ7F7FJ-
L---JF-JLJ.||-FJLJJ7
|F|F-JF---7F7-L7L|7|
|FFJF7L7F-JF7|JL---7
7-L-JL7||F7|L7F-7F7|
L.L7LFJ|||||FJL7||LJ
L7JLJL-JLJLJL--JLJ.L"""

print(find_distance(load_input(test_input5)))


print(find_distance(load_input(open("2023/10_input", "r", encoding="utf8").read())))
