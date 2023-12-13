import sys


test_input = """#.##..##.
..#.##.#.
##......#
##......#
..#.##.#.
..##..##.
#.#.##.#.

#...##..#
#....#..#
..##..###
#####.##.
#####.##.
..##..###
#....#..#
"""

test_input_2 = """....#...####..#
.###.....####.#
###.#.##..#.#..
#.#.######...#.
#.#####.#..#.#.
...#......#.##.
####....#......
#.#..#..#####.#
##..#.##...#.##
...#.#.###.###.
..####.##...#.#
..####.##...#.#
...#.#..##.###.
...#.#..##.###.
..####.##...#.#
..####.##...#.#
...#.#.###.###."""


def difference(left: str, right: str):
    return [(a != b) for a, b in zip(left, right)]


def load_input(input: str):
    patterns = []

    pattern = []
    for line in input.split("\n"):
        if line.strip():
            pattern.append(line)
        else:
            patterns.append(pattern)
            pattern = []

    if pattern:
        patterns.append(pattern)
    return patterns


def rotate_pattern(pattern: list[str]):
    return [
        "".join([pattern[i][idx] for i in range(len(pattern))])
        for idx in range(len(pattern[0]))
    ]


def find_reflection(pattern: list[str], max_difference: int = 0):
    print("Pattern length", len(pattern))
    reflection_starts = []
    reflections = []
    for idx, line in enumerate(pattern[0:-1]):
        diff = sum(difference(line, pattern[idx + 1]))
        if diff <= max_difference:
            reflection_starts.append((idx, diff))

    if not reflection_starts:
        return None

    while reflection_starts:
        reflection_start, total_diff = reflection_starts.pop(0)
        print("Reflection start", reflection_start + 1)
        iterator = min(len(pattern) - 1 - (reflection_start + 1), reflection_start)
        print("Iterator", iterator)
        while iterator > 0:
            left = reflection_start - iterator
            right = reflection_start + iterator + 1
            # print(left, right)
            diff = sum(difference(pattern[left], pattern[right]))
            total_diff += diff
            if total_diff > max_difference:
                break
            iterator -= 1

        if iterator == 0 and total_diff == max_difference:
            reflections.append(reflection_start + 1)

    return reflections


test_patterns = load_input(test_input)

assert find_reflection(test_patterns[0]) == []
res = find_reflection(rotate_pattern(test_patterns[0]))
assert res == [5], res

assert find_reflection(test_patterns[1]) == [4]

test_patterns2 = load_input(test_input_2)


def find_smudges(pattern: list[str]):
    print("!!!")
    smudges = find_reflection(pattern, 1)
    print("Found smudges", smudges)
    return smudges
    print("!!!")
    potential_lines = []
    for idx, line_a in enumerate(pattern[0:-1]):
        for idx_b, line_b in enumerate(pattern[idx + 1 :]):
            res = difference(line_a, line_b)
            if sum(res) == 1:
                potential_lines.append((idx, res.index(True)))
    return potential_lines


def desmuge_pattern(pattern: list[str], smudge: tuple[int, int]):
    smudge_line = pattern[smudge[0]]
    new = "." if smudge_line[smudge[1]] == "#" else "#"

    return [
        *pattern[: smudge[0]],
        smudge_line[: smudge[1]] + new + smudge_line[smudge[1] + 1 :],
        *pattern[smudge[0] + 1 :],
    ]


print(find_smudges(test_patterns[0]))


def summarize_reflections(patterns: list[list[str]], desmudge: bool = False):
    verticals = []
    horizontals = []

    for idx, pattern in enumerate(patterns):
        print("----------------")
        horizontal_unsmudged = find_reflection(pattern)
        rotated_pattern = rotate_pattern(pattern)
        vertical_unsmudged = find_reflection(rotated_pattern)
        print("Horizontal and vertical: ", horizontal_unsmudged, vertical_unsmudged)

        if desmudge:
            horizontal_result = find_smudges(pattern)
            print("Horizontal smudges: ", horizontal_result)
            vertical_result = find_smudges(rotated_pattern)
            print("Vertical smudges:", vertical_result)
        else:
            horizontal_result = horizontal_unsmudged
            vertical_result = vertical_unsmudged

        if not vertical_result and not horizontal_result:
            print("\n".join(pattern))
            print("\n")
            print("\n".join(rotated_pattern))
            raise Exception()

        if horizontal_result:
            horizontals += horizontal_result

        if vertical_result:
            verticals += vertical_result

        print(verticals, horizontals)

        print("----------------")

    return sum(verticals) + sum(horizontals) * 100


print(summarize_reflections(test_patterns2))

print("\nTesting summarize")
assert summarize_reflections(test_patterns) == 405
print("\n")

print("\nTesting desmudging")
res = summarize_reflections(test_patterns, desmudge=True)
assert res == 400, res
print("\n")

print("Solving star 1")
print("")
puzzle_patterns = load_input(open("2023/13_input", "r", encoding="utf8").read())
print(summarize_reflections(puzzle_patterns))


print("Solving star 2")
print("")
puzzle_patterns = load_input(open("2023/13_input", "r", encoding="utf8").read())
print(summarize_reflections(puzzle_patterns, desmudge=True))

sys.exit(1)
