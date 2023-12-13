from functools import reduce
from itertools import groupby
import math
import sys
from typing import Iterator, Tuple
from functools import cache

# Python3 program to print prime
# factors and their powers
# using Sieve Of Eratosthenes

# Using SieveOfEratosthenes to
# find smallest prime factor
# of all the numbers.


# For example, if N is 10,
# s[2] = s[4] = s[6] = s[10] = 2
# s[3] = s[9] = 3
# s[5] = 5
# s[7] = 7
def sieveOfEratosthenes(N, s):
    # Create a boolean array
    # "prime[0..n]" and initialize
    # all entries in it as false.
    prime = [False] * (N + 1)

    # Initializing smallest factor
    # equal to 2 for all the even
    # numbers
    for i in range(2, N + 1, 2):
        s[i] = 2

    # For odd numbers less than
    # equal to n
    for i in range(3, N + 1, 2):
        if prime[i] == False:
            # s(i) for a prime is
            # the number itself
            s[i] = i

            # For all multiples of
            # current prime number
            for j in range(i, int(N / i) + 1, 2):
                if prime[i * j] == False:
                    prime[i * j] = True

                    # i is the smallest
                    # prime factor for
                    # number "i*j".
                    s[i * j] = i


# Function to generate prime
# factors and its power


def generatePrimeFactors(N: int):
    print(N)
    factors = []
    # s[i] is going to store
    # smallest prime factor
    # of i.
    s: list[int] = [0] * (N + 1)

    # Filling values in s[]
    # using sieve
    sieveOfEratosthenes(N, s)

    # Current prime factor of N
    curr = s[N]

    # Power of current prime factor
    cnt = 1

    # Printing prime factors and
    # their powers
    while N > 1:
        N //= s[N]

        # N is now N/s[N]. If new N
        # also has smallest prime
        # factor as curr, increment
        # power
        if curr == s[N]:
            cnt += 1
            continue

        factors.append((curr, cnt))

        # Update current prime factor
        # as s[N] and initializing
        # count as 1.
        curr = s[N]
        cnt = 1

    return factors


def find_next(
    factors1: list[tuple[int, int]], factors2: list[tuple[int, int]], steps: int = 1
):
    # print(factors1, factors2)
    primes = set([f[0] for f in factors1 + factors2])
    exponents = {f: 1 for f in primes}
    for f in factors2:
        exponents[f[0]] = f[1]

    for f in factors1:
        exponents[f[0]] -= f[1]

    return [(p, f + (exponents[p] * steps)) for p, f in factors2]


# @profile
def run_length_encode(data: str) -> Iterator[Tuple[str, int]]:
    """Returns run length encoded Tuples for string"""
    # A memory efficient (lazy) and pythonic solution using generators
    return ((x, sum(1 for _ in y)) for x, y in groupby(data))


# @profile
def verify_arrangement(report: str, stats: list[int]) -> bool:
    rle = run_length_encode(report)
    i = 0
    for g in rle:
        if g[0] == "#":
            if g[1] != stats[i]:
                return False
            i += 1
    return True


class unique_element:
    def __init__(self, value, occurrences):
        self.value = value
        self.occurrences = occurrences


# @profile
def perm_unique(elements):
    eset = set(elements)
    listunique = [unique_element(i, elements.count(i)) for i in eset]
    u = len(elements)
    return perm_unique_helper(listunique, [0] * u, u - 1)


# @profile
def perm_unique_helper(listunique, result_list, d):
    if d < 0:
        yield tuple(result_list)
    else:
        for i in listunique:
            if i.occurrences > 0:
                result_list[d] = i.value
                i.occurrences -= 1
                for g in perm_unique_helper(listunique, result_list, d - 1):
                    yield g
                i.occurrences += 1


# @profile
def replace(input: str, token: str, new: list[str]):
    new = list(new)
    return "".join((i if (i != token) else new.pop(0)) for (idx, i) in enumerate(input))


# @profile
def find_arrangements(input: str, unfold: int = 1) -> int:
    status, counts = input.split(" ")

    counts = [int(i, 10) for i in counts.split(",")]

    if unfold > 1:
        status = "?".join(
            [
                status,
            ]
            * unfold
        )

        counts = counts * unfold

    total_damaged = sum(counts)

    placed_damaged = sum([c == "#" for c in status])
    unknowns = sum([c == "?" for c in status])

    unplaced_damaged = total_damaged - placed_damaged
    unplaced_working = unknowns - unplaced_damaged

    # print(f"{total_damaged} damaged amongst {total} helixes, {unknowns} are unknown")

    if unknowns == (total_damaged - placed_damaged):
        return 1

    source = "#" * unplaced_damaged + "." * (unplaced_working)
    valid = set()
    # print(source)
    for t in perm_unique(source):
        new = replace(status, "?", t)
        if verify_arrangement(new, counts):
            valid.add(new)

    # return sum([c == "?" for c in status]) - (total_damaged - placed_damaged)
    # print(valid)
    return len(valid)


# @profile
def validate(status: str, counts: list[int]):
    groups = run_length_encode(status)

    i = 0
    for group in groups:
        if group[0] == "?":
            return True
        if group[0] == "#":
            if i == len(counts):
                return False

            if group[1] > counts[i]:
                return False
            i += 1

    return True


assert validate("???.###", [1, 1, 3]) == True

assert validate("#??.###", [1, 1, 3]) == True
assert validate(".??.###", [1, 1, 3]) == True

assert validate("##?.###", [1, 1, 3]) == False
assert validate(".#?.###", [1, 1, 3]) == True
assert validate("#.?.###", [1, 1, 3]) == True
assert validate("..?.###", [1, 1, 3]) == True


assert validate("###.###", [1, 1, 3]) == False
assert validate(".##.###", [1, 1, 3]) == False
assert validate("#.#.###", [1, 1, 3]) == True
assert validate("..#.###", [1, 1, 3]) == False

assert validate("##..###", [1, 1, 3]) == False
assert validate(".#..###", [1, 1, 3]) == False
assert validate("#...###", [1, 1, 3]) == False
assert validate("....###", [1, 1, 3]) == False


# @profile
def check(
    status: str,
    counts: list[int],
    unplaced_damaged: int,
    unplaced_working: int,
    pos: int = 0,
):
    valid = set()

    if not validate(status, counts):
        return valid

    if pos >= len(status):
        valid.add(status)
        return valid

    if status[pos] == "?":
        if unplaced_damaged > 0:
            valid |= check(
                status[:pos] + "#" + status[pos + 1 :],
                counts,
                unplaced_damaged - 1,
                unplaced_working,
                pos + 1,
            )
        if unplaced_working > 0:
            valid |= check(
                status[:pos] + "." + status[pos + 1 :],
                counts,
                unplaced_damaged,
                unplaced_working - 1,
                pos + 1,
            )
    else:
        return check(status, counts, unplaced_damaged, unplaced_working, pos + 1)

    return valid


def find_arrangements2(input: str, unfold: int = 1) -> int:
    status, counts = input.split(" ")

    counts = [int(i, 10) for i in counts.split(",")]

    total_damaged = sum(counts)
    placed_damaged = sum([c == "#" for c in status])
    unknowns = sum([c == "?" for c in status])
    unplaced_damaged = total_damaged - placed_damaged
    unplaced_working = unknowns - unplaced_damaged

    # if unknowns == (total_damaged - placed_damaged):
    #     return 1

    valid = set()
    print("Status", status)
    print("Counts", counts)
    print("Total damaged", total_damaged)
    print("Placed damaged", placed_damaged)
    print("Unknown", unknowns)
    print("Unplaced damaged", unplaced_damaged)
    print("Unplaced working", unplaced_working)

    count = 0
    valid = check(status, counts, unplaced_damaged, unplaced_working)
    count = len(valid)

    print("First count", count)

    # if unfold > 1 and status[-1] in [".", "?"]:
    # if status[0] in ["?"]:
    if unfold > 1:
        unfold_valid = check(
            status + ("?" + status) * (2 - 1),
            counts * 2,
            unplaced_damaged * 2,
            unplaced_working * 2 + 2 - 1,
        )
        print("Second count", len(unfold_valid))
        prime_factors_1 = generatePrimeFactors(count)
        prime_factors_2 = generatePrimeFactors(len(unfold_valid))
        res = find_next(prime_factors_1, prime_factors_2, 3)
        count = math.prod([pow(a, b) for a, b in res])
        print("Result count", count)

    print("***\n")
    # print(count)
    # print(generatePrimeFactors(count))
    return count


@cache
def count_ways(status: str, runs: tuple[int, ...]):
    if len(status) == 0:
        if len(runs) == 0:
            print("Found one")
            print(status, runs)
            return 1
        return 0

    if len(runs) == 0:
        if "#" in status:
            return 0

    if status[0] == "?":
        r1 = count_ways("#" + status[1:], runs)
        r2 = count_ways("." + status[1:], runs)
        return r1 + r2

    if status[0] == "#":
        if runs[0] > 1:
            new_runs = (runs[0] - 1, *runs[1:])
            if len(status) < runs[0]:
                return 0

            if status[1] == ".":
                return 0

            if status[1] == "?":
                return count_ways("#" + status[2:], new_runs)

            return count_ways(status[1:], new_runs)

        elif runs[0] == 1:
            if len(status) == 1 or status[1] == ".":
                return count_ways(status[1:], tuple(runs[1:]))

            elif status[1] == "?":
                return count_ways("." + status[2:], tuple(runs[1:]))

            else:
                return 0

        else:
            return 0

    if status[0] == ".":
        return count_ways(status[1:], runs)

    raise NotImplementedError(status, runs)


def find_arrangements3(input: str, unfold: int = 1) -> int:
    status, counts = input.split(" ")

    counts = [int(i, 10) for i in counts.split(",")]

    if unfold > 1:
        status = "?".join(
            [
                status,
            ]
            * unfold
        )

        counts = counts * unfold

    print("Status", status)
    print("Counts", counts)

    count = count_ways(status, tuple(counts))

    print("Count", count)
    return count


def arrangements(input: str, unfold: int = 1) -> list[int]:
    return [
        find_arrangements3(line.strip(), unfold)
        for line in input.split("\n")
        if line.strip()
    ]


# print(find_arrangements("?###???????? 3,2,1", unfold=1))
# print(find_arrangements("?###???????? 3,2,1", unfold=2))
# print(find_arrangements("?###???????? 3,2,1", unfold=3))

# print(find_arrangements2("?###???????? 3,2,1", unfold=1))
# print(find_arrangements2("?###???????? 3,2,1", unfold=2))
# print(find_arrangements2("?###???????? 3,2,1", unfold=3))
# print(find_arrangements2("?###???????? 3,2,1", unfold=4))
# print(find_arrangements2("?###???????? 3,2,1", unfold=5))
# print("")
# print(find_arrangements2(".??..??...?##. 1,1,3", unfold=1))
# print(find_arrangements2(".??..??...?##. 1,1,3", unfold=2))
# print(find_arrangements2(".??..??...?##. 1,1,3", unfold=3))
# print(find_arrangements2(".??..??...?##. 1,1,3", unfold=4))
# print(find_arrangements2(".??..??...?##. 1,1,3", unfold=5))

assert find_arrangements3("? 1") == 1
assert find_arrangements3("?? 1") == 2
assert find_arrangements3("??? 1") == 3
assert find_arrangements3("??? 1,1") == 1
assert find_arrangements3(".??? 1,1") == 1
assert find_arrangements3("#??? 1,1") == 2
assert find_arrangements3("???? 1,1") == 3
assert find_arrangements3("???? 2,1") == 1

assert find_arrangements3("##??? 2,1") == 2
assert find_arrangements3("..??? 2,1") == 0
assert find_arrangements3("#.??? 2,1") == 0
assert find_arrangements3("##??? 2,1") == 2
assert find_arrangements3("#???? 2,1") == 2, find_arrangements3("#???? 2,1")


assert find_arrangements3(".???? 2,1") == 1
assert find_arrangements3("????? 2,1") == 3

assert find_arrangements3("#????? 2,1") == 3
assert find_arrangements3(".????? 2,1") == 3
assert find_arrangements3("?????? 2,1") == 6, find_arrangements3("?????? 2,1")
assert find_arrangements3("??????? 2,1") == 10, find_arrangements3("??????? 2,1")
assert find_arrangements3("?###???????? 3,2,1") == 10


test_input = """???.### 1,1,3
.??..??...?##. 1,1,3
?#?#?#?#?#?#?#? 1,3,1,6
????.#...#... 4,1,1
????.######..#####. 1,6,5
?###???????? 3,2,1"""

print("Testing unfold = 1")
res = list(arrangements(test_input))
assert res == [1, 4, 1, 1, 4, 10], res

print("Testing unfold = 5")
res = list(arrangements(test_input, unfold=5))
assert res == [1, 16384, 1, 16, 2500, 506250], res


print("Solving unfold = 1")
res = list(arrangements(open("2023/12_input", "r", encoding="utf8").read()))
print(sum(res))


print("Solving unfold = 5")
res = list(arrangements(open("2023/12_input", "r", encoding="utf8").read(), unfold=5))
print(sum(res))
