"""puzzle_3
Author: soumitra.goswami@gmail.com
Puzzle Description:
The engineer explains that an engine part seems to be missing from the engine, but nobody can 
figure out which one. If you can add up all the part numbers in the engine schematic, it should
be easy to work out which part is missing.

The engine schematic (your puzzle input) consists of a visual representation of the engine. There
are lots of numbers and symbols you don't really understand, but apparently any number adjacent to
a symbol, even diagonally, is a "part number" and should be included in your sum. (Periods (.) do
not count as a symbol.)

Here is an example engine schematic:

467..114..
...*......
..35..633.
......#...
617*......
.....+.58.
..592.....
......755.
...$.*....
.664.598..

In this schematic, two numbers are not part numbers because they are not adjacent to a symbol: 114
(top right) and 58 (middle right). Every other number is adjacent to a symbol and so is a part 
number; their sum is 4361.

Of course, the actual engine schematic is much larger.

Part 1 Problem Statement:
What is the sum of all of the part numbers in the engine schematic?

Part 2:
The missing part wasn't the only issue - one of the gears in the engine is wrong. A gear is any 
`*` symbol that is adjacent to exactly two part numbers. Its gear ratio is the result of multiplying
those two numbers together.

Consider the same engine schematic again:

467..114..
...*......
..35..633.
......#...
617*......
.....+.58.
..592.....
......755.
...$.*....
.664.598..

In this schematic, there are two gears. The first is in the top left; it has part numbers 467 and
35, so its gear ratio is 16345. The second gear is in the lower right; its gear ratio is 451490. 
(The `*` adjacent to 617 is not a gear because it is only adjacent to one part number.) Adding up 
all of the gear ratios produces 467835.


Part 2 Problem Statement:
What is the sum of all of the gear ratios in your engine schematic?


"""
from __future__ import annotations

import re
import typing as t
import math
from pathlib import Path

FLAGS = re.VERBOSE | re.DOTALL | re.MULTILINE

SYMBOLS = re.compile(r"[^\da-z.\s]", FLAGS)
NUMBERS = re.compile(r"\d+", FLAGS)
STAR_SYMBOL = re.compile(r"[*]")


def decode_line(
    line: str,
    line_no: str,
    max_char: int,
    symbol_pos_table: t.List[int],
    number_table: t.List[t.Tuple[int]],
    debug_file: str,
    section: int = 1,
) -> t.Tuple[t.List[int], t.List[t.Tuple[int]], str]:
    """
    Returns possible game number for a given configuration in a bag.
    """
    if section == 1:
        symbol_iter = SYMBOLS.finditer(line)
    else:
        symbol_iter = STAR_SYMBOL.finditer(line)
    for m in symbol_iter:
        symbol_pos_table.append(max_char * line_no + m.start())

    number_iter = NUMBERS.finditer(line)
    for m in number_iter:
        digit_pos = max_char * line_no + m.start()
        end_pos = max_char * line_no + m.end()
        number_table.append((m.group(), digit_pos, end_pos))
    return symbol_pos_table, number_table, debug_file


def check_neighbourhood(
    start: int, end: int, symbol_table: t.List[int], max_char: int
) -> bool:
    line_number = math.floor(start / max_char)
    # Line Boundaries
    line_start = line_number * max_char
    line_end = line_start + max_char - 1
    prev_line_start = max(
        (line_number - 1) * max_char, 0
    )  # Clamp to top Left edge of the table
    prev_line_end = max(line_start - 1, 0)
    next_line_start = (line_number + 1) * max_char
    next_line_end = (line_number + 2) * max_char - 1

    left = [max(start - 1, line_start)]
    top = [
        max(start - max_char, prev_line_start),
        max(end - 1 - max_char, prev_line_start),
    ]
    right = [min(end, line_end)]
    top_right = [
        max(min(start - max_char + 1, prev_line_end), 0),
        max(min(end - max_char, prev_line_end), 0),
    ]
    top_left = [
        max(start - max_char - 1, prev_line_start),
        max(end - max_char - 2, prev_line_start),
    ]
    bottom_left = [
        max(start + max_char - 1, next_line_start),
        max(end + max_char - 2, next_line_start),
    ]
    bottom_right = [
        min(start + max_char + 1, next_line_end),
        min(end + max_char, next_line_end),
    ]
    bottom = [start + max_char, end + max_char - 1]

    # concatinating all the lists to create our table
    search_table = (
        top_left + top + top_right + left + right + bottom_left + bottom_right + bottom
    )
    search_table = set(search_table)
    common_elements = search_table.intersection(symbol_table)
    return len(common_elements) > 0


def decode_engine(
    symbol_table: t.List[int], number_table: t.List[t.Tuple[int]], max_char: int
) -> int:
    val = 0
    for group in number_table:
        number, start, end = group
        found_symbol = check_neighbourhood(start, end, symbol_table, max_char)

        if not found_symbol:
            continue
        val += int(number)

    return val


def identify_gears(
    number_table: t.List[t.Tuple[int]], symbol_pos: int, max_char: int
) -> list[int]:
    line_number = math.floor(symbol_pos / max_char)
    line_start = line_number * max_char
    line_end = line_start + max_char - 1
    prev_line_start = max(
        (line_number - 1) * max_char, 0
    )  # Clamp to top Left edge of the table
    prev_line_end = max(line_start - 1, 0)
    next_line_start = (line_number + 1) * max_char
    next_line_end = (line_number + 2) * max_char - 1
    gear_numbers = []
    symbol_neighbours = [
        max(symbol_pos - max_char - 1, prev_line_start),  # top_left
        symbol_pos - max_char,  # top
        max(min(symbol_pos - max_char + 1, prev_line_end), 0),  # top_right
        max(symbol_pos - 1, line_start),  # left
        min(symbol_pos + 1, line_end),  # right
        max(symbol_pos + max_char - 1, next_line_start),  # bottom right
        symbol_pos + max_char,  # bottom
        min(symbol_pos + max_char + 1, next_line_end),  # bottom_right
    ]

    for group in number_table:
        number, start, end = group
        number_range = range(start, end)
        if len(set(symbol_neighbours).intersection(number_range)) > 0:
            gear_numbers.append(int(number))

    if len(gear_numbers) == 2:
        return gear_numbers

    return [0]


def decode_gear(
    symbol_table: t.List[int], number_table: t.List[t.Tuple[int]], max_char: int
) -> int:
    """
    Calculates the product of minumum possible cubes for the game to be possible
    """
    val = 0
    for symbol_pos in symbol_table:
        gear_list: list[int] = identify_gears(number_table, symbol_pos, max_char)
        val += math.prod(gear_list)
    return val


def decode_file(fp: str, debug_fp: Path, section: int = 1) -> int:
    """
    Decodes a txt file provided for the puzzle and returns a sum of decoded values.
    """

    lines: t.List[str] = []
    with open(fp, "r", encoding="UTF-8") as fh:
        lines = fh.readlines()

    cummulative_sum = 0
    file_output = "DEBUG FILE\n"
    file_output += "FILE DEBUG\n\n"
    symbol_table = []
    number_table = []
    for i, line in enumerate(lines):
        max_char = len(line) if line[-1] != "\n" else len(line) - 1
        file_output += f"Line {i+1}-> {line}\n"
        symbol_table, number_table, file_output = decode_line(
            line, i, max_char, symbol_table, number_table, file_output, section
        )
    if section == 1:
        cummulative_sum += decode_engine(symbol_table, number_table, max_char)
    else:
        cummulative_sum += decode_gear(symbol_table, number_table, max_char)
    with open(debug_fp, "w", encoding="UTF-8") as out_file:
        out_file.write(file_output)

    return cummulative_sum


if __name__ == "__main__":
    dirpath = Path(__file__).parent
    filepath = Path(dirpath, "test.txt")
    filepath = Path(dirpath, "Puzzle3_Input.txt")
    debug_out = Path(dirpath, "debug_p3Out.txt")
    my_val = decode_file(filepath, debug_out, 1)
    print(f"P1 SUM: {my_val}")
    my_val = decode_file(filepath, debug_out, 2)
    print(f"P2 SUM: {my_val}")
