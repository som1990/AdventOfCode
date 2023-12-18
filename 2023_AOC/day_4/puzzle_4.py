from __future__ import annotations

import re
import typing as t
import math
from pathlib import Path

FLAGS = re.VERBOSE | re.DOTALL | re.MULTILINE
CARDS = re.compile(r"(\d)\: ([\d\s]+)\| ([\d\s]+)$", FLAGS)


def scratchcards_won(line):
    groups = CARDS.findall(line)[0]
    card_num = int(groups[0])
    winners_rawstr = groups[1]
    hand_rawstr = groups[2]

    winners = re.findall(r"\d+", winners_rawstr)
    winners = list(map(int, winners))
    hand = re.findall(r"\d+", hand_rawstr)
    hand = list(map(int, hand))

    cards_won = len(set(winners).intersection(hand))

    return cards_won


def decode_file(fp: str, section: int = 1) -> int:
    """
    Decodes a txt file provided for the puzzle and returns a sum of decoded values.
    """

    lines: t.List[str] = []
    with open(fp, "r", encoding="UTF-8") as fh:
        lines = fh.readlines()

    cummulative_sum = 0
    num_cards = [1] * len(lines)
    for i, line in enumerate(lines):
        if section == 1:
            cards_won = scratchcards_won(line)
            cummulative_sum += (2 ** (cards_won - 1)) if cards_won > 0 else 0
        else:
            cards_won = scratchcards_won(line)
            for id in range(cards_won):
                num_cards[i + id + 1] += num_cards[i]
            cummulative_sum += num_cards[i]

    return cummulative_sum


if __name__ == "__main__":
    dirpath = Path(__file__).parent
    filepath = Path(dirpath, "test.txt")
    filepath = Path(dirpath, "Puzzle4_Input.txt")

    my_val = decode_file(filepath, 1)
    print(f"P1 SUM: {my_val}")
    my_val = decode_file(filepath, 2)
    print(f"P2 SUM: {my_val}")
