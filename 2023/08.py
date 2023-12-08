import math
import re
from dataclasses import dataclass
from typing import Dict, List


@dataclass
class Node:
    name: str
    left: "Node" = None
    right: "Node" = None

    def __str__(self):
        return f"{self.name} = ({self.left.name}, {self.right.name})"

    def __repr__(self):
        return str(self)


def load_data(data: str):
    lines = data.split("\n")

    node_pattern = re.compile(r"(\w\w\w) = \((\w\w\w), (\w\w\w)\)")
    instructions = lines.pop(0)
    lines.pop(0)

    nodes: Dict[str, Node] = {}
    for line in lines:
        line = line.strip()
        if not line:
            continue
        name, left, right = node_pattern.match(line).groups()
        if left in nodes:
            left_node = nodes[left]
        else:
            left_node = Node(left)
            nodes[left] = left_node

        if right in nodes:
            right_node = nodes[right]
        else:
            right_node = Node(right)
            nodes[right] = right_node

        if name in nodes:
            node = nodes[name]
            node.left = left_node
            node.right = right_node
        else:
            node = Node(name, left_node, right_node)

        nodes[name] = node

    return instructions, nodes


test_data = """LLR

AAA = (BBB, BBB)
BBB = (AAA, ZZZ)
ZZZ = (ZZZ, ZZZ)"""


def test_load_data():
    instructions, nodes = load_data(test_data)
    assert instructions == "LLR"
    assert len(nodes) == 3
    assert nodes["AAA"].name == "AAA"
    assert nodes["BBB"].name == "BBB"
    assert nodes["AAA"].left.name == "BBB"
    assert nodes["BBB"].right.name == "ZZZ"


def navigate(instructions: str, nodes: Dict[str, Node]) -> List[Node]:
    current_node = nodes["AAA"]
    instruction_pointer = 0
    current_instruction = instructions[instruction_pointer]
    visited_nodes = []

    while current_node.name != "ZZZ":
        if current_instruction == "L":
            current_node = current_node.left
        elif current_instruction == "R":
            current_node = current_node.right

        instruction_pointer += 1
        current_instruction = instructions[instruction_pointer % len(instructions)]
        visited_nodes.append(current_node)

    return visited_nodes


def ghost_navigation(instructions: str, nodes: Dict[str, Node]) -> List[Node]:
    current_nodes = [node for node in nodes.values() if node.name.endswith("A")]
    instruction_pointer = 0
    current_instruction = instructions[instruction_pointer]
    cycle_length = [None for _ in range(len(current_nodes))]
    endswith_z = [n.name.endswith("Z") for n in current_nodes]
    while not all(cycle_length):
        if current_instruction == "L":
            current_nodes = [node.left for node in current_nodes]
        elif current_instruction == "R":
            current_nodes = [node.right for node in current_nodes]
        else:
            raise NotImplementedError(current_instruction)

        endswith_z = [n.name.endswith("Z") for n in current_nodes]

        instruction_pointer += 1
        current_instruction = instructions[instruction_pointer % len(instructions)]

        if any(endswith_z):
            print(instruction_pointer, current_nodes)
            cycle_length[endswith_z.index(True)] = instruction_pointer

        # print(current_nodes)

    factors = set()
    for cycle in cycle_length:
        print(cycle)
        i = 2
        prime = True
        while i <= ((cycle + 1) // 2):
            print(cycle, i)
            if cycle % i == 0:
                factors.add(i)
                prime = False
            i += 1
        if prime:
            factors.add(cycle)
    print(factors)
    return math.prod(factors)


test_load_data()

instructions, nodes = load_data(test_data)

res = navigate(instructions, nodes)
assert len(res) == 6, res

test_data_2 = """LR

11A = (11B, XXX)
11B = (XXX, 11Z)
11Z = (11B, XXX)
22A = (22B, XXX)
22B = (22C, 22C)
22C = (22Z, 22Z)
22Z = (22B, 22B)
XXX = (XXX, XXX)"""

instructions, nodes = load_data(test_data_2)

res = ghost_navigation(instructions, nodes)
assert res == 6, res


instructions, nodes = load_data(open("2023/08_input", "r", encoding="utf8").read())
res = navigate(instructions, nodes)
print(len(res))

instructions, nodes = load_data(open("2023/08_input", "r", encoding="utf8").read())
res = ghost_navigation(instructions, nodes)
print(res)
