from dataclasses import dataclass
from enum import Enum
from functools import cached_property, total_ordering
from itertools import groupby
import operator
from typing import List

CARD_RANK = ["A", "K", "Q", "J", "T", "9", "8", "7", "6", "5", "4", "3", "2", "X"]


class HandType(Enum):
    five_of_a_kind = 1
    four_of_a_kind = 2
    full_house = 3
    three_of_a_kind = 4
    two_pair = 5
    one_pair = 6
    high_card = 7


@dataclass
@total_ordering
class Hand:
    hand: str
    bid: int
    joker: bool = False

    @cached_property
    def type(self):
        if self.joker and "J" in self.hand:
            hist = {
                k: len(list(v)) for k, v in groupby(sorted(self.hand.replace("J", "")))
            }
            if len(hist.keys()) == 0:
                return HandType.five_of_a_kind

            most = max(hist.items(), key=operator.itemgetter(1))[0]
            hist = {
                k: len(list(v))
                for k, v in groupby(sorted(self.hand.replace("J", most)))
            }
        else:
            hist = {k: len(list(v)) for k, v in groupby(sorted(self.hand))}

        if len(hist.keys()) == 1:
            return HandType.five_of_a_kind
        if len(hist.keys()) == 2:
            if max(hist.values()) == 4:
                return HandType.four_of_a_kind
            if max(hist.values()) == 3:
                return HandType.full_house
        if len(hist.keys()) == 3:
            if max(hist.values()) == 3:
                return HandType.three_of_a_kind
            if max(hist.values()) == 2:
                return HandType.two_pair
        if len(hist.keys()) == 4:
            return HandType.one_pair
        return HandType.high_card

    def __lt__(self, other: object):
        if isinstance(other, Hand):
            if self.type.value == other.type.value:
                if self.joker:
                    pairings = zip(
                        self.hand.replace("J", "X"),
                        other.hand.replace("J", "X"),
                    )
                else:
                    pairings = zip(self.hand, other.hand)
                for pair in pairings:
                    if pair[0] != pair[1]:
                        return CARD_RANK.index(pair[0]) < CARD_RANK.index(pair[1])
            return self.type.value < other.type.value

        return None


test_input = """32T3K 765
T55J5 684
KK677 28
KTJJT 220
QQQJA 483"""


def load_input(data: str, joker: bool = False):
    loaded_hands: List[Hand] = []
    for line in data.split("\n"):
        parts = line.split(" ")
        loaded_hands.append(Hand(parts[0], int(parts[1], 10), joker))

    return loaded_hands


def total_cards(inputhands: List[Hand]):
    return sum(
        [((len(inputhands) - idx) * hand.bid) for (idx, hand) in enumerate(inputhands)]
    )


hands = load_input(test_input)

sorted_hands = sorted(hands)
assert sorted_hands == [
    Hand(hand="QQQJA", bid=483),
    Hand(hand="T55J5", bid=684),
    Hand(hand="KK677", bid=28),
    Hand(hand="KTJJT", bid=220),
    Hand(hand="32T3K", bid=765),
], sorted_hands

assert total_cards(sorted_hands) == 6440, total_cards(sorted_hands)

hands = load_input(open("2023/07/input", "r", encoding="utf8").read())
sorted_hands = sorted(hands)
print(total_cards(sorted_hands))


hands = load_input(test_input, joker=True)
sorted_hands = sorted(hands)
assert sorted_hands == [
    Hand(hand="KTJJT", bid=220, joker=True),
    Hand(hand="QQQJA", bid=483, joker=True),
    Hand(hand="T55J5", bid=684, joker=True),
    Hand(hand="KK677", bid=28, joker=True),
    Hand(hand="32T3K", bid=765, joker=True),
], sorted_hands

assert total_cards(sorted_hands) == 5905, total_cards(sorted_hands)


hands = load_input(open("2023/07/input", "r", encoding="utf8").read(), joker=True)
sorted_hands = sorted(hands)
print(total_cards(sorted_hands))
