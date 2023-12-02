# Rock, paper, scissors

THEM = ["A", "B", "C"]

# Lose, draw, win
US = ["X", "Y", "Z"]


def result(them: str, us: str):
    if THEM.index(them) == US.index(us):
        return 3

    if THEM.index(them) == US.index(us) + 1 or (
        THEM.index(them) == 0 and US.index(us) == 2
    ):
        return 0

    if THEM.index(them) == US.index(us) - 1 or (
        THEM.index(them) == 2 and US.index(us) == 0
    ):
        return 6


def defined_result(them: str, result: str):
    if result == "X":
        return ((THEM.index(them) + 2) % 3) + 1 + 0

    if result == "Y":
        return THEM.index(them) + 1 + 3

    if result == "Z":
        return ((THEM.index(them) + 1) % 3) + 1 + 6


with open("02/input", "r", encoding="utf-8") as f:
    total = 0
    proper_total = 0
    while line := f.readline():
        them, us = line.strip().split(" ")
        outcome = result(them, us)
        proper_outcome = defined_result(them, us)
        print(line.strip(), outcome, proper_outcome)

        total += US.index(us) + 1 + outcome
        proper_total += proper_outcome

print(total)
print(proper_total)
