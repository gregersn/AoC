digits = ["0", "1", "2", "3", "4", "5", "6", "7", "8", "9"]
numbers = ["one", "two", "three", "four", "five", "six", "seven", "eight", "nine"]


def part1():
    total = 0
    with open("01/input", "r", encoding="utf8") as f:
        while line := f.readline():
            number = None
            digit = None
            for c in line:
                if c in digits:
                    digit = c
                    if number is None:
                        number = digit

            number += digit

            total += int(number, 10)

    print(total)


def parse_number_string(string: str):
    idx = 0
    candidates = numbers
    while idx < len(string) and len(candidates) > 1:
        c = string[idx]
        candidates = [n for n in candidates if len(n) > idx and n[idx] == c]
        idx += 1

    if len(candidates) == 1:
        if string.startswith(candidates[0]):
            return str(numbers.index(candidates[0]) + 1)

    return None


def parse_line(line: str):
    number = None
    digit = None

    for idx, c in enumerate(line):
        if c in digits:
            digit = c
            if number is None:
                number = digit
        elif res := parse_number_string(line[idx:]):
            digit = str(res)

            if number is None:
                number = digit

    number += digit

    return int(number, 10)


def part2():
    total = 0
    with open("01/input", "r", encoding="utf8") as f:
        while line := f.readline():
            res = parse_line(line)
            total += res
    print(total)


part1()
part2()
