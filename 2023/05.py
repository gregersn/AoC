test_data = """seeds: 79 14 55 13

seed-to-soil map:
50 98 2
52 50 48

soil-to-fertilizer map:
0 15 37
37 52 2
39 0 15

fertilizer-to-water map:
49 53 8
0 11 42
42 0 7
57 7 4

water-to-light map:
88 18 7
18 25 70

light-to-temperature map:
45 77 23
81 45 19
68 64 13

temperature-to-humidity map:
0 69 1
1 0 69

humidity-to-location map:
60 56 37
56 93 4"""


from dataclasses import dataclass, field
from typing import Dict, List, Optional


@dataclass
class MapRange:
    destination: int
    source: int
    length: int

    def convert(self, source: int) -> Optional[int]:
        diff = source - self.source
        if diff >= 0 and diff <= self.length:
            return self.destination + diff


@dataclass
class Map:
    source: str
    destination: str
    ranges: List[MapRange] = field(default_factory=list)


def convert(value: int, maps: List[MapRange]):
    for _map in maps:
        if val := _map.convert(value):
            return val
    return value


@dataclass
class Data:
    seeds: List[int]
    maps: Dict[str, Map] = field(default_factory=dict)


def seed_location(seed: int, seed_data: Data) -> int:
    print(f"Seed: {seed}")
    current_map = seed_data.maps["seed"]
    value = convert(seed, current_map.ranges)
    print(f"{current_map.source} -> {current_map.destination}: {value}")

    while current_map.destination != "location":
        current_map = seed_data.maps[current_map.destination]
        value = convert(value, current_map.ranges)
        print(f"{current_map.source} -> {current_map.destination}: {value}")

    return value


def load_data(data: str):
    line_pos = 0
    mode = None
    lines = data.split("\n")
    seeds = [
        int(x.strip(), 10) for x in (lines[line_pos].split(":"))[1].split(" ") if x
    ]

    line_pos += 1

    source = None
    destination = None
    current_map = None

    seed_data = Data(seeds=seeds)

    while line_pos < len(lines):
        print(repr(lines[line_pos]))
        if ":" in lines[line_pos]:
            if current_map is not None:
                seed_data.maps[current_map.source] = current_map

            mode = lines[line_pos].split(" ")[0]

            source, destination = mode.split("-to-")
            current_map = Map(source, destination)
        elif lines[line_pos] in ["\n", ""]:
            pass
        else:
            destination_range_start, source_range_start, range_length = [
                int(x, 10) for x in lines[line_pos].split(" ")
            ]
            current_map.ranges.append(
                MapRange(destination_range_start, source_range_start, range_length)
            )

        line_pos += 1

    if current_map is not None:
        seed_data.maps[current_map.source] = current_map

    return seed_data


def find_closest_location(data: Data):
    closest = seed_location(data.seeds[0], data)
    for seed in data.seeds[1:]:
        closest = min(closest, seed_location(seed, data))

    return closest


data = load_data(test_data)

# print(data)

assert seed_location(79, data) == 82
assert seed_location(14, data) == 43
assert seed_location(55, data) == 86
assert seed_location(13, data) == 35

assert find_closest_location(data) == 35


data = load_data(open("2023/05/input", "r", encoding="utf8").read())

print(find_closest_location(data))
