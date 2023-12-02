from typing import List


elves: List[int] = []

with open("2022/01/input", "r", encoding="utf8") as f:
    elf_total = 0
    while line := f.readline():
        if line == "\n":
            elves.append(elf_total)
            elf_total = 0
        else:
            elf_total += int(line, 10)


print(elves)

print(max(elves))

print(sum(list(sorted(elves, reverse=True)[0:3])))
