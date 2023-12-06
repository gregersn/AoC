from typing import List
from dataclasses import dataclass


@dataclass
class Range:
    start: int
    length: int

    @property
    def end(self):
        return self.start + (self.length - 1)


def map_ranges(range: Range, cutters: List[Range]):
    endpoints = set()
    start = range.start
    end = range.end

    endpoints.add(range.start)
    endpoints.add(range.end + 1)

    for cutter in sorted(cutters, key=lambda x: x.start):
        if cutter.start > start:
            endpoints.add(cutter.start)
        if cutter.end < end:
            endpoints.add(cutter.end)

    output = []
    print(sorted(endpoints))
    t = list(sorted(endpoints))
    for idx, value in enumerate(t[:-1]):
        output.append(Range(value, t[idx + 1] - value))

    print(output)
    assert sum([x.length for x in output]) == range.length
    return output


print(map_ranges(Range(10, 25), [Range(13, 4), Range(30, 10)]))
