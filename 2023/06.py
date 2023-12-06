from dataclasses import dataclass
from typing import List
import math

test_input = """Time:      7  15   30
Distance:  9  40  200"""


@dataclass
class Race:
    time: int
    distance: int


def load_input(data: str):
    timeline, distanceline = data.split("\n")
    times = [
        int(x.strip(), 10) for x in timeline.strip().split(":")[1].strip().split(" ") if x
    ]
    distances = [
        int(x.strip(), 10)
        for x in distanceline.strip().split(":")[1].strip().split(" ") if x
    ]

    assert len(times) == len(distances)

    return (times, distances)

def load_input2(data: str):
    times, distances = load_input(data)
    _time = int("".join([str(t) for t in times]), 10)
    _distance = int("".join([str(t) for t in distances]), 10)

    return (_time, _distance)

def ways(time: int, distance: int):
    way = 0
    for hold_time in range(time):
        travel = (time - hold_time) * hold_time
        if travel > distance:
            way += 1
    
    return way

def calculate(times: List[int], distances: List[int]):
    total = math.prod([ways(*x) for x in zip(times, distances)])
    return total

data = load_input(test_input)

assert calculate(*data) == 288

data = load_input(open('2023/06/input', 'r', encoding='utf8').read())
print(calculate(*data))

data2 = load_input2(test_input)
assert ways(*data2) == 71503

data2 = load_input2(open('2023/06/input', 'r', encoding='utf8').read())
print(ways(*data2))
