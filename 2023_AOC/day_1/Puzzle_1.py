"""Puzzle_1
Author: soumitra.goswami@gmail.com
Description:
    The newly-improved calibration document consists of lines of text; each line originally contained a 
    specific calibration value that the Elves now need to recover. On each line, the calibration value 
    can be found by combining the first digit and the last digit (in that order) to form a single 
    two-digit number. 
    
    What is the sum of all of the calibration values
Example:
    Input:
        two1nine - 29 
        eightwothree - 83
        abcone2threexyz - 13
        xtwone3four - 24
        4nineeightseven2 - 42
        zoneight234 - 14
        7pqrstsixteen - 76
    Result:
        Sum : 281
"""

from __future__ import annotations

import typing as t

import re
from pathlib import Path

FLAGS = re.VERBOSE | re.DOTALL | re.MULTILINE

numbers = {
    "zero": 0,
    "one": 1,
    "two": 2,
    "three": 3,
    "four": 4,
    "five": 5,
    "six": 6,
    "seven": 7,
    "eight": 8,
    "nine": 9,
}

# regex to find first instance of the digit
DIGIT = re.compile(r"(?=(one|two|three|four|five|six|seven|eight|nine|\d))", FLAGS)


def to_int(idx: str) -> int:
    """
    Deserializes the fed in string to return an int.
    """
    if idx in numbers.keys():
        return numbers[idx]
    else:
        return int(idx)


def decode_line2(line: str) -> int:
    """
    Matches the regex pattern and finds the required numbers
    """
    val = -1
    digits = DIGIT.findall(line)
    if len(digits) > 0:
        val = to_int(digits[0]) * 10 + to_int(digits[-1])
    return val


def decode_file(fp: str) -> int:
    """
    Decodes a txt file provided for the puzzle and returns a sum of decoded values.
    """
    lines: t.List[str] = []
    with open(fp, "r", encoding="UTF-8") as fh:
        lines = fh.readlines()

    cummulative_sum = 0
    for i, line in enumerate(lines):
        val = decode_line2(line)
        if val < 0:
            raise ValueError(f"Incorrect value in line {i}")

        cummulative_sum += val
        # print(f"source: {line}")
        # print(f"Line {i+1}, Val: {val}, Sum: {sum}")

    return cummulative_sum


if __name__ == "__main__":
    dirpath = Path(__file__).parent
    filepath = Path(dirpath, "test.txt")
    filepath = Path(dirpath, "InputCode.txt")

    my_sum = decode_file(filepath)
    print(f"FINAL SUM: {my_sum}")
