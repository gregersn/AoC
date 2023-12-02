from dataclasses import dataclass
from typing import Iterable


@dataclass
class Pull:
    red: int = 0
    green: int = 0
    blue: int = 0

    def __add__(self, other):
        return self.__class__(
            self.red + other.red, self.green + other.green, self.blue + other.blue
        )

    def __radd__(self, other):
        if other == 0:
            return self
        else:
            return self.__add__(other)

    def __le__(self, other):
        return (
            self.red <= other.red
            and self.green <= other.green
            and self.blue <= other.blue
        )


def biggest_values(game: Iterable[Pull]):
    biggest = Pull()

    for pull in game:
        biggest.red = max(biggest.red, pull.red)
        biggest.green = max(biggest.green, pull.green)
        biggest.blue = max(biggest.blue, pull.blue)

    return biggest


with open("02/input", "r", encoding="utf8") as f:
    games = []
    while line := f.readline():
        game_info, game_pulls = line.split(":")
        game_id = int(game_info.split(" ")[1], 10)
        pulls = []
        for p in game_pulls.split(";"):
            pull = Pull()
            for cubes in p.split(","):
                number, color = cubes.strip().split(" ")
                setattr(pull, color, int(number, 10))
            pulls.append(pull)
        games.append(pulls)

# print(games)

test_data = Pull(12, 13, 14)

possible_sum: int = 0
power_sum: int = 0

for idx, game in enumerate(games):
    least_needed = biggest_values(game)
    if least_needed <= test_data:
        possible_sum += idx + 1
    game_power = least_needed.red * least_needed.green * least_needed.blue

    print(idx + 1, least_needed, game_power, power_sum)

    power_sum += game_power

print(possible_sum)
print(power_sum)
