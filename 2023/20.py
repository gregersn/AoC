from dataclasses import field, dataclass


@dataclass
class Module:
    name: str
    type: str = ""
    destinations: list[str] = field(default_factory=list)
    state: bool = False  # Flip-flop state
    incoming_signals: dict[str, bool] = field(default_factory=dict)  # For conjunction

    def incoming(self, incoming: bool, sender: str, output: bool = True):
        if output:
            print(f"{sender} -{"high" if incoming else "low"}-> {self.name}")
        match self.type:
            case "%":
                if not incoming:
                    self.state = not self.state
                    return [(m, self.state, self.name) for m in self.destinations]
            case "&":
                if sender not in self.incoming_signals:
                    self.incoming_signals[sender] = False
                self.incoming_signals[sender] = incoming

                result = not all(self.incoming_signals.values())
                return [(m, result, self.name) for m in self.destinations]
            case "broadcaster":
                return [(m, incoming, self.name) for m in self.destinations]

            case _:
                pass


class Processor:
    queue: list[tuple[str, bool, str]]
    modules: dict[str, Module]
    button_pushes: int = 0
    low_pulses: int = 0
    high_pulses: int = 0
    output: bool = True

    def __init__(self, modules: dict[str, Module], output: bool = True):
        self.queue = []
        self.modules = modules
        self.output = output

    def button(self):
        if self.queue:
            raise SystemError(
                "Do not press the button while there are operations on the queue"
            )
        self.queue += self.modules["broadcaster"].incoming(
            False, "button", output=self.output
        )
        self.low_pulses += 1
        self.button_pushes += 1

    def tick(self):
        if not self.queue:
            raise Exception("Stack underflow error")

        destination, state, sender = self.queue.pop(0)
        if state:
            self.high_pulses += 1
        else:
            self.low_pulses += 1

        if destination in self.modules:
            module = self.modules[destination]
            res = module.incoming(state, sender, output=self.output)
            if res is not None:
                self.queue += res


test_config = """broadcaster -> a, b, c
%a -> b
%b -> c
%c -> inv
&inv -> a
"""

test_config_2 = """broadcaster -> a
%a -> inv, con
&inv -> b
%b -> con
&con -> output
"""


test_result = """button -low-> broadcaster
broadcaster -low-> a
broadcaster -low-> b
broadcaster -low-> c
a -high-> b
b -high-> c
c -high-> inv
inv -low-> a
a -low-> b
b -low-> c
c -low-> inv
inv -high-> a
"""


def load_config(indata: str):
    modules: dict[str, Module] = {}
    modules["output"] = Module("output")
    for line in indata.split("\n"):
        if not line.strip():
            continue

        module, destinations = line.split(" -> ")
        if module[0] in ["%", "&"]:
            module_type = module[0]
            name = module[1:]
        else:
            module_type = "broadcaster"
            name = module

        mod = Module(name, module_type)
        modules[name] = mod

        mod.destinations = destinations.split(", ")

    for name, module in modules.items():
        for dest in module.destinations:
            if dest not in modules:
                continue
            if modules[dest].type == "&":
                modules[dest].incoming_signals[name] = False

    return modules


print("Running test config")
modules = load_config(test_config)
computer = Processor(modules)
computer.button()
while computer.queue:
    computer.tick()
print("")

print("Push test config 1000 times")
computer = Processor(modules, output=False)
for _ in range(1000):
    computer.button()
    while computer.queue:
        computer.tick()

assert computer.button_pushes == 1000
assert computer.high_pulses == 4000, computer.high_pulses
assert computer.low_pulses == 8000, computer.low_pulses
assert computer.low_pulses * computer.high_pulses == 32_000_000
print("")


print("Running test config 2")
modules = load_config(test_config_2)
computer = Processor(modules)
computer.button()
while computer.queue:
    computer.tick()

print("\nSecond push")
computer.button()
while computer.queue:
    computer.tick()

print("\nThird push")
computer.button()
while computer.queue:
    computer.tick()

print("\nFourth push")
computer.button()
while computer.queue:
    computer.tick()


print("Push test config 2 1000 times")
computer = Processor(modules, output=False)
for _ in range(1000):
    computer.button()
    while computer.queue:
        computer.tick()

assert computer.button_pushes == 1000
assert computer.low_pulses == 4250, computer.low_pulses
assert computer.high_pulses == 2750, computer.high_pulses
assert computer.low_pulses * computer.high_pulses == 11_687_500


print("")


print("Running input config")
modules = load_config(open("2023/20_input", "r", encoding="utf8").read())
computer = Processor(modules, output=False)
for _ in range(1000):
    computer.button()
    while computer.queue:
        computer.tick()

print(computer.button_pushes)
print(computer.low_pulses)
print(computer.high_pulses)
print(computer.low_pulses * computer.high_pulses)
print("")
