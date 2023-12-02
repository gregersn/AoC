THEM = ["A", "B", "C"]
US = ["X", "Y", "Z"]


def result(them: str, us: str):
    if THEM.index(them) == US.index(us):
        return 3


with open("2022/02/input", "r", encoding="utf-8") as f:
    print(f.read())
