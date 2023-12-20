from dataclasses import field, dataclass
import math
import re
from typing import Literal, Optional, Union

case_pattern = re.compile(
    r"(?P<source>\w)(?P<operator>[<>])(?P<condition>\d+):(?P<destination>\w+)"
)


@dataclass
class Node:
    destination: Union[str, "Workflow"]
    source: Optional[str] = None
    operator: Optional[Literal["<", ">"]] = None
    condition: Optional[int] = None


@dataclass
class Workflow:
    name: str
    nodes: list[Node] = field(default_factory=list)


def parse_part(part: str):
    part_info = {}
    for rating in part[1:-1].split(","):
        k, v = rating.split("=")
        part_info[k] = int(v, 10)

    return part_info


def parse_rule(raw: str):
    if res := case_pattern.match(raw):
        source = res.group("source")
        operator = res.group("operator")
        condition = int(res.group("condition"), 10)
        destination = res.group("destination")

        n = Node(destination, source, operator, condition)
        return n
    n = Node(raw)
    return n


def parse_workflow(wf: str):
    name, flow = wf[:-1].split("{")
    wf = Workflow(name)
    raw_rules = flow.split(",")
    for rule in raw_rules:
        wf.nodes.append(parse_rule(rule))

    return wf


def load_input(indata: str):
    workflows = {}
    parts = []

    workflow_mode = True
    for line in indata.split("\n"):
        if line == "":
            workflow_mode = False
            continue

        if workflow_mode:
            workflow = parse_workflow(line.strip())
            workflows[workflow.name] = workflow
        else:
            parts.append(parse_part(line.strip()))

    return workflows, parts


def part_value(part: dict[str, int]):
    return sum(part.values())


def process_part(part: dict[str, int], workflows: dict[str, Workflow]) -> bool:
    print(part)
    current = workflows["in"]
    while current:
        print(f"In {current.name}")
        for case in current.nodes:
            print("Case;", case)
            if case.operator:
                print(f"Checking: {part[case.source]} {case.operator} {case.condition}")
                if case.operator == "<":
                    if part[case.source] < case.condition:
                        print("Setting new current: ", case.destination)
                        if case.destination == "A":
                            print("ACCEPTED")
                            return True
                        if case.destination == "R":
                            print("REJECTED")
                            return False
                        current = workflows[case.destination]
                        break
                elif case.operator == ">":
                    if part[case.source] > case.condition:
                        print("Setting new current: ", case.destination)
                        if case.destination == "A":
                            print("ACCEPTED")
                            return True
                        if case.destination == "R":
                            print("REJECTED")
                            return False
                        current = workflows[case.destination]
                        break
                else:
                    raise NotImplementedError(case)
            elif case.destination in workflows:
                current = workflows[case.destination]
                break

            elif case.destination == "R":
                print("REJECTED")
                return False

            elif case.destination == "A":
                print("ACCEPTED")
                return True
    raise NotImplementedError()


def process_parts(parts: list[dict[str, int]], workflows: dict) -> list[dict[str, int]]:
    return [part for part in parts if process_part(part, workflows)]


def get_workflow_values(
    workflow: Workflow, workflows: dict[str, Workflow], values: dict[str, int]
):
    print(workflow)
    if workflow.nodes:
        for node in workflow.nodes:
            values.update(get_node_values(node, workflows, values))
    else:
        raise NotImplementedError(workflow)

    return values


def get_node_values(node: Node, workflows: dict[str, Workflow], values: dict[str, int]):
    print(node)
    if node.destination not in ["A", "R"]:
        values.update(
            get_workflow_values(workflows[node.destination], workflows, values)
        )

    elif node.destination == "A":
        ## Add these values
        if node.operator == "<":
            values[node.source][1] = min(node.condition, values[node.source][1])
        elif node.operator == ">":
            values[node.source][0] = max(node.condition, values[node.source][0])
    elif node.destination == "R":
        pass
    else:
        raise NotImplementedError(node)
    return values


import random


def calculate_combinations(workflows: dict[str, Workflow]):
    values = {"x": [1, 4000], "m": [1, 4000], "a": [1, 4000], "s": [1, 4000]}

    new_values = {k: random.randint(*v) for (k, v) in values.items()}
    print(new_values)

    return math.prod([ma - mi for (mi, ma) in values.values()])


test_input = """px{a<2006:qkq,m>2090:A,rfg}
pv{a>1716:R,A}
lnx{m>1548:A,A}
rfg{s<537:gd,x>2440:R,A}
qs{s>3448:A,lnx}
qkq{x<1416:A,crn}
crn{x>2662:A,R}
in{s<1351:px,qqz}
qqz{s>2770:qs,m<1801:hdj,R}
gd{a>3333:R,R}
hdj{m>838:A,pv}

{x=787,m=2655,a=1222,s=2876}
{x=1679,m=44,a=2067,s=496}
{x=2036,m=264,a=79,s=2244}
{x=2461,m=1339,a=466,s=291}
{x=2127,m=1623,a=2188,s=1013}
"""

test_results = [7540, None, 4623, None, 6951]

test_total = 19114

workflows, ratings = load_input(test_input)


for rating, result in zip(ratings, test_results):
    if result is not None:
        assert part_value(rating) == result

res = process_parts(ratings, workflows)
assert len(res) == 3, res

assert sum(part_value(p) for p in res) == 19114

print(" Stufs ")
res = calculate_combinations(workflows)
assert res == 167409079868000, res


step1_input = open("2023/19_input", "r", encoding="utf8").read()
workflows, ratings = load_input(step1_input)
res = process_parts(ratings, workflows)
print(sum(part_value(p) for p in res))
