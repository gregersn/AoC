from dataclasses import dataclass, field
from math import inf
import sys
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
class Range:
    start: int
    length: int

    @property
    def end(self):
        return self.start + self.length - 1


@dataclass
class MapRange:
    destination: int
    length: int
    source: int

    def convert(self, source: int) -> Optional[int]:
        diff = source - self.source
        if diff >= 0 and diff < self.length:
            return self.destination + diff


@dataclass
class Map:
    source: str
    destination: str
    ranges: List[MapRange] = field(default_factory=list)

    def sort(self):
        self.ranges.sort(key=lambda x: x.source)

    def convert(self, value: int):
        for _map in self.ranges:
            if val := _map.convert(value):
                return val
        return value


@dataclass
class Data:
    seeds: List[Range]
    maps: Dict[str, Map] = field(default_factory=dict)

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


def load_data(data: str):
    line_pos = 0
    mode = None
    lines = data.split("\n")
    seed_ranges = [
        int(x.strip(), 10) for x in (lines[line_pos].split(":"))[1].split(" ") if x
    ]

    seeds = [
        Range(seed_ranges[i], seed_ranges[i + 1]) for i in range(0, len(seed_ranges), 2)
    ]
    line_pos += 1

    source = None
    destination = None
    current_map = None

    seed_data = Data(seeds=seeds)

    while line_pos < len(lines):
        # print(repr(lines[line_pos]))
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
                MapRange(destination_range_start, range_length, source_range_start)
            )

        line_pos += 1

    if current_map is not None:
        seed_data.maps[current_map.source] = current_map

    return seed_data


def split_range_by_range(input: Range, splitter: Range):
    assert input.length > 0
    assert splitter.length > 0
    output: List[Range] = []
    leftover = Range(input.start, input.length)
    while leftover.length > 0:
        if leftover.start < splitter.start:
            if leftover.end < splitter.end:
                output.append(Range(leftover.start, leftover.length))
                leftover.length = 0
            else:
                output.append(
                    Range(leftover.start, min(splitter.start - 1, leftover.end))
                )
                leftover.start += output[-1].length
                leftover.length -= output[-1].length
        elif leftover.start >= splitter.start and leftover.start <= splitter.end:
            output.append(
                Range(
                    leftover.start, 1 + min(splitter.end, leftover.end) - leftover.start
                )
            )
            leftover.start += output[-1].length
            leftover.length -= output[-1].length
        elif leftover.start > splitter.end:
            output.append(Range(leftover.start, 1 + leftover.end - leftover.start))
            leftover.start += output[-1].length
            leftover.length = 0
        else:
            print(leftover)

    # print("Split range by range", input, splitter, output)
    assert len(output) > 0
    return output


def map_ranges(range: Range, cutters: List[Range]):
    print("** Map ranges: ")
    print(range)
    print(cutters)
    endpoints = set()
    start = range.start
    end = range.end

    endpoints.add(range.start)
    endpoints.add(range.end + 1)

    for cutter in sorted(cutters, key=lambda x: x.start):
        if cutter.end < start:
            continue
        if cutter.start > end:
            continue
        if cutter.start > start:
            if cutter.end > start:
                endpoints.add(cutter.start)
        elif cutter.end < end:
            if cutter.start < end:
                endpoints.add(cutter.end)

    output = []
    print(sorted(endpoints))
    t = list(sorted(endpoints))
    for idx, value in enumerate(t[:-1]):
        output.append(Range(value, t[idx + 1] - value))

    print(output)
    assert sum([x.length for x in output]) == range.length
    print("*****")

    return output


res = split_range_by_range(Range(1, 20), Range(4, 10))
assert res == [
    Range(1, 3),
    Range(4, 10),
    Range(14, 7),
], res


assert split_range_by_range(Range(start=82, length=1), Range(start=98, length=2)) == [
    Range(start=82, length=1)
]


assert split_range_by_range(Range(1, 10), Range(11, 20)) == [Range(1, 10)]
assert split_range_by_range(Range(21, 10), Range(11, 20)) == [Range(21, 10)]

assert split_range_by_range(Range(start=74, length=14), Range(64, 13)) == [
    Range(74, 3),
    Range(77, 11),
], split_range_by_range(Range(start=74, length=14), Range(64, 13))


def join_ranges(data: List[Range]):
    # print("--- join ranges --- ")
    data = data.copy()
    # print(data)
    data.sort(key=lambda x: x.start)
    output = [data[0]]
    for in_range in data[1:]:
        if in_range.start <= output[-1].end:
            output[-1].length = max(output[-1].end, in_range.end) - (
                output[-1].start - 1
            )
        else:
            output.append(in_range)
    # print(output)
    # assert total == sum([r.length for r in output])
    # print("--- // join ranges --- ")
    return output


assert join_ranges([Range(start=55, length=13), Range(start=79, length=14)]) == [
    Range(start=55, length=13),
    Range(start=79, length=14),
]

assert join_ranges([Range(81, 1), Range(81, 1)]) == [Range(81, 1)]


def map_seed_ranges(data: Data) -> List[Range]:
    data.sort()
    step = "seed"

    input_ranges = data.seeds.copy()
    input_ranges.sort(key=lambda x: x.start)

    # print(step, input_ranges)
    while step != "location":
        mapping = data.maps[step]
        assert isinstance(mapping, Map)

        layer_ranges = []
        output_ranges = []

        for input_range in input_ranges:
            output_ranges += map_ranges(
                input_range, [Range(r.source, r.length) for r in mapping.ranges]
            )
            # input_range = output_ranges.pop(-1)
            # output_ranges.append(input_range)

        output_ranges.sort(key=lambda x: x.start)
        # print("output ranges", output_ranges)

        for output_range in output_ranges:
            # print(
            #          f"Converting {output_range.start} to {mapping.convert(output_range.start)}, using {mapping.source} -> {mapping.destination}"
            #  )
            layer_ranges.append(
                Range(mapping.convert(output_range.start), output_range.length)
            )
        print(layer_ranges)
        layer_ranges = join_ranges(layer_ranges)
        input_ranges = layer_ranges.copy()
        input_ranges.sort(key=lambda x: x.start)
        step = mapping.destination
        # print(step, input_ranges)
    return layer_ranges


def find_closest_location(data: Data):
    print("### ")
    # total = sum([x.length for x in data.seeds])
    location_ranges = map_seed_ranges(data)
    location_ranges.sort(key=lambda x: x.start)
    print(location_ranges)
    # assert total == sum([x.length for x in location_ranges])
    return min([x.start for x in location_ranges])


data = load_data(test_data)

assert data.maps["seed"].convert(82) == 84
assert data.maps["soil"].convert(84) == 84
assert data.maps["fertilizer"].convert(84) == 84
assert data.maps["water"].convert(84) == 77
assert data.maps["light"].convert(77) == 45
assert data.maps["temperature"].convert(45) == 46
assert data.maps["humidity"].convert(46) == 46

res = find_closest_location(data)
assert res == 46, res


data = load_data(open("2023/05/input", "r", encoding="utf8").read())
print(find_closest_location(data))
