from dataclasses import dataclass
from typing import Dict, List


test_input = """Card 1: 41 48 83 86 17 | 83 86  6 31 17  9 48 53
Card 2: 13 32 20 16 61 | 61 30 68 82 17 32 24 19
Card 3:  1 21 53 59 44 | 69 82 63 72 16 21 14  1
Card 4: 41 92 73 84 69 | 59 84 76 51 58  5 54 83
Card 5: 87 83 26 28 32 | 88 30 70 12 93 22 82 36
Card 6: 31 18 13 56 72 | 74 77 10 23 35 67 36 11"""


def run_cards(input: str):
    total = 0
    for card in input.splitlines():
        card_id, numbers = card.strip().split(":")
        winning_numbers, my_numbers = numbers.strip().split("|")

        winners = [
            int(x.strip(), 10) for x in winning_numbers.strip().split(" ") if x.strip()
        ]
        mine = [int(x.strip(), 10) for x in my_numbers.strip().split(" ") if x.strip()]

        matches = len(set(winners) & set(mine))
        points = pow(2, matches - 1) if matches else 0
        total += points

    return total


@dataclass
class Card:
    winners: List[int]
    actual: List[int]
    card_id: int

    def score(self):
        return len(set(self.winners) & set(self.actual))


def run_real_cards(input: str):
    cards: List[Card] = []
    my_cards: Dict[int, int] = {}

    for card in input.splitlines():
        card_id, numbers = card.strip().split(":")
        winning_numbers, my_numbers = numbers.strip().split("|")

        winners = [
            int(x.strip(), 10) for x in winning_numbers.strip().split(" ") if x.strip()
        ]
        mine = [int(x.strip(), 10) for x in my_numbers.strip().split(" ") if x.strip()]

        cards.append(Card(winners, mine, int(card_id.split(" ")[-1], 10)))

    for card in cards:
        my_cards[card.card_id] = 1

    for card_id, count in my_cards.items():
        score = cards[card_id - 1].score()
        for i in range(score):
            my_cards[card_id + i + 1] += count

    print(my_cards)
    return sum(my_cards.values())


assert run_cards(test_input) == 13
result = run_real_cards(test_input)
assert result == 30, result


print(run_cards(open("2023/04/input", "r", encoding="utf-8").read()))
print(run_real_cards(open("2023/04/input", "r", encoding="utf-8").read()))
