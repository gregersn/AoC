from functools import cache
from collections import OrderedDict


@cache
def hash_step(step: str, current: int = 0):
    return ((current + ord(step)) * 17) % 256


@cache
def holiday_hash(indata: str):
    value = 0
    for c in indata:
        value = hash_step(c, value)
    return value


@cache
def decode_operation(operation: str):
    token = "=" if "=" in operation else "-"
    label, lens = operation.split(token)

    return label, token, lens


print(holiday_hash("HASH"))

test_input = """rn=1,cm-,qp=3,cm=2,qp-,pc=4,ot=9,ab=5,pc-,pc=6,ot=7"""

hashes = [holiday_hash(s) for s in test_input.split(",")]
print(hashes)
assert sum(hashes) == 1320


def arrange_boxes(instructions: str):
    boxes = [OrderedDict() for _ in range(256)]

    for operation in instructions.split(","):
        label, token, lens = decode_operation(operation)
        box = holiday_hash(label)
        if token == "=":
            boxes[box][label] = lens
        else:
            if label in boxes[box]:
                del boxes[box][label]
    return boxes


powers = 0
for idx, box in enumerate(arrange_boxes(test_input)):
    if box:
        for slot, (label, lens) in enumerate(box.items()):
            powers += (1 + idx) * (slot + 1) * int(lens, 10)

assert powers == 145


real_input = open("2023/15_input", "r", encoding="utf8").read().strip()
step1_hashes = [holiday_hash(s) for s in real_input.split(",")]
print(sum(step1_hashes))

boxes = arrange_boxes(real_input)
powers = 0
for idx, box in enumerate(boxes):
    if box:
        for slot, (label, lens) in enumerate(box.items()):
            powers += (1 + idx) * (slot + 1) * int(lens, 10)

print(powers)
