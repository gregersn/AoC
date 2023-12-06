from dataclasses import dataclass, field
from math import inf
from typing import Dict, List, Optional

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


@dataclass
class SeedRange:
    start: int
    length: int


@dataclass
class MapRange:
    destination: int
    source: int
    length: int

    def convert(self, source: int) -> Optional[int]:
        diff = source - self.source
        if diff >= 0 and diff <= self.length:
            return self.destination + diff

    def lookup(self, destination: int) -> Optional[int]:
        diff = destination - self.destination
        if diff >= 0 and diff <= self.length:
            return self.source + diff


@dataclass
class Map:
    source: str
    destination: str
    ranges: List[MapRange] = field(default_factory=list)

    def sort(self):
        self.ranges.sort(key=lambda x: x.destination)

    def convert(self, value: int):
        for _map in self.ranges:
            if val := _map.convert(value):
                return val
        return value

    def lookup(self, value: int):
        for _map in self.ranges:
            if val := _map.lookup(value):
                return val

        return value


@dataclass
class Data:
    seeds: List[SeedRange]
    maps: Dict[str, Map] = field(default_factory=dict)
    lookups: Dict[str, Map] = field(default_factory=dict)

    def sort(self):
        for map in self.maps.values():
            map.sort()


def seed_location(seed: int, seed_data: Data) -> int:
    # print(f"Seed: {seed}")
    current_map = seed_data.maps["seed"]
    value = current_map.convert(seed)
    assert current_map.lookup(value) == seed
    # print(f"{current_map.source} -> {current_map.destination}: {value}")

    while current_map.destination != "location":
        current_map = seed_data.maps[current_map.destination]
        prev_value = value
        value = current_map.convert(prev_value)
        assert prev_value == current_map.lookup(value), (
            current_map.lookup(value),
            value,
            prev_value,
            current_map,
        )
        # print(f"{current_map.source} -> {current_map.destination}: {value}")

    return value


def location_seed(location: int, seed_data: Data) -> int:
    print(f"Location: {location}")
    current_map = seed_data.lookups["location"]
    value = current_map.lookup(location)
    assert current_map.convert(value) == location
    print(f"{current_map.destination} -> {current_map.source}: {value}")
    while current_map.source != "seed":
        current_map = seed_data.lookups[current_map.source]
        prev_value = value
        value = current_map.lookup(value)
        assert current_map.convert(value) == prev_value
        print(f"{current_map.destination} -> {current_map.source}: {value}")

    return value


def load_data(data: str):
    line_pos = 0
    mode = None
    lines = data.split("\n")
    seed_ranges = [
        int(x.strip(), 10) for x in (lines[line_pos].split(":"))[1].split(" ") if x
    ]

    seeds = [
        SeedRange(seed_ranges[i], seed_ranges[i + 1])
        for i in range(0, len(seed_ranges), 2)
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
                seed_data.lookups[current_map.destination] = current_map

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
        seed_data.lookups[current_map.destination] = current_map

    return seed_data


def find_closest_location(data: Data):
    closest = inf
    ranges = len(data.seeds)
    for idx, seed_range in enumerate(data.seeds):
        print(f"Running range {idx + 1} of {ranges}")
        for seed in range(seed_range.start, seed_range.start + seed_range.length):
            closest = min(closest, seed_location(seed, data))

    return closest


def find_closest_location_2(data: Data):
    location = 1
    seed = None
    seed_in_range = False

    while not seed_in_range:
        seed = location_seed(location, data)
        location += 1
        for seed_range in data.seeds:
            if (
                seed >= seed_range.start
                and seed <= seed_range.start + seed_range.length
            ):
                seed_in_range = True

    assert seed_location(seed, data) == location
    return location


data = load_data(test_data)


mapping = data.maps["humidity"]
print(mapping)
for i in range(100):
    value = mapping.convert(i)
    print(f"Converting {i} to {value}")
    assert mapping.lookup(value) == i, (value, i)

assert find_closest_location(data) == 46
assert find_closest_location_2(data) == 46


data = load_data(open("2023/05/input", "r", encoding="utf8").read())

print(find_closest_location(data))
