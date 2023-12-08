"""puzzle_2
Author: soumitra.goswami@gmail.com
Puzzle Description:
the Elf shows you a small bag and some cubes which are either red, green, or blue. 
Each time you play this game, he will hide a secret number of cubes of each color in the bag, 
and your goal is to figure out information about the number of cubes.

To get information, once a bag has been loaded with cubes, the Elf will reach into the bag, 
grab a handful of random cubes, show them to you, and then put them back in the bag. 
He'll do this a few times per game.

You play several games and record the information from each game (your puzzle input). 
Each game is listed with its ID number (like the 11 in Game 11: ...) followed 
by a semicolon-separated list of subsets of cubes that were revealed from the bag 
(like 3 red, 5 green, 4 blue).

For example, the record of a few games might look like this:

    Game 1: 3 blue, 4 red; 1 red, 2 green, 6 blue; 2 green
    Game 2: 1 blue, 2 green; 3 green, 4 blue, 1 red; 1 green, 1 blue
    Game 3: 8 green, 6 blue, 20 red; 5 blue, 4 red, 13 green; 5 green, 1 red
    Game 4: 1 green, 3 red, 6 blue; 3 green, 6 red; 3 green, 15 blue, 14 red
    Game 5: 6 red, 1 blue, 3 green; 2 blue, 1 red, 2 green

In game 1, three sets of cubes are revealed from the bag (and then put back again). 
The first set is 3 blue cubes and 4 red cubes; the second set is 1 red cube, 2 green cubes, 
and 6 blue cubes; the third set is only 2 green cubes.

P1 Problem Statement: The Elf would first like to know which games would have been possible if the bag 
contained only 12 red cubes, 13 green cubes, and 14 blue cubes?

Part 2
As you continue your walk, the Elf poses a second question: in each game you played, what is the fewest 
number of cubes of each color that could have been in the bag to make the game possible?

Again consider the example games from earlier:

    Game 1: 3 blue, 4 red; 1 red, 2 green, 6 blue; 2 green
    Game 2: 1 blue, 2 green; 3 green, 4 blue, 1 red; 1 green, 1 blue
    Game 3: 8 green, 6 blue, 20 red; 5 blue, 4 red, 13 green; 5 green, 1 red
    Game 4: 1 green, 3 red, 6 blue; 3 green, 6 red; 3 green, 15 blue, 14 red
    Game 5: 6 red, 1 blue, 3 green; 2 blue, 1 red, 2 green


In game 1, the game could have been played with as few as 4 red, 2 green, and 6 blue cubes. If any color 
had even one fewer cube, the game would have been impossible.
Game 2 could have been played with a minimum of 1 red, 3 green, and 4 blue cubes.
Game 3 must have been played with at least 20 red, 13 green, and 6 blue cubes.
Game 4 required at least 14 red, 3 green, and 15 blue cubes.
Game 5 needed no fewer than 6 red, 3 green, and 2 blue cubes in the bag.

The power of a set of cubes is equal to the numbers of red, green, and blue cubes multiplied together. 
The power of the minimum set of cubes in game 1 is 48. In games 2-5 it was 12, 1560, 630, and 36, 
respectively. Adding up these five powers produces the sum 2286.

P2 Problem Statement :For each game, find the minimum set of cubes that must have been present. 
What is the sum of the power of these sets?
"""
from __future__ import annotations

import re
import typing as t
import math
from pathlib import Path

SETS = re.compile(r"(\d+)\:([^\n]*)")
SET = re.compile(r"\s([^;\n]*)")
CUBES = re.compile(r"(\d+)\s((?:red|blue|green))")


def decode_line(
    line, allowed_config: dict[str, int], debug_file: str
) -> t.Tuple(int, str):
    """
    Returns possible game number for a given configuration in a bag.
    """
    # Extracts the complete game which contains all the sets
    sets_groups = SETS.findall(line)[0]
    # Extracts the game ID
    game = int(sets_groups[0])
    sets = sets_groups[1]

    # Extracts individual sets for the game
    set_groups = SET.findall(sets)
    # Calculates the total number of cubes possible in a bag
    cube_list = allowed_config.values()
    total_cubes = sum(cube_list)

    for cur_set in set_groups:
        # Extracts individual cube values from a set
        cubes_groups = CUBES.findall(cur_set)
        cube_sum = 0
        debug_file += f"\tSet: {cubes_groups}\n"
        # Checks if each set is compatible with the given configuration
        for cube in cubes_groups:
            cube_type = cube[1]
            cube_num = int(cube[0])
            cube_sum += cube_num
            allowed_cubes = allowed_config[cube_type]
            debug_file += (
                f"\tcube type: {cube_type}, num: {cube_num}, allowed:{allowed_cubes}\n"
            )
            if allowed_cubes < cube_num:
                return 0, debug_file
        # Check if the total number of cubes in a set is larger than number of cubes in given configuration
        debug_file += f"\tSet Cube Sum: {cube_sum}\n"
        if cube_sum > total_cubes:
            return 0, debug_file
    # Return the successful game ID
    return game, debug_file


def decode_line_p2(
    line, allowed_colors: t.List[str], debug_file: str
) -> t.Tuple(int, str):
    """
    Calculates the product of minumum possible cubes for the game to be possible
    """

    # Extracts the complete game which contains all the sets
    sets_groups = SETS.findall(line)[0]
    sets = sets_groups[1]

    # Extracts individual sets for the game
    set_groups = SET.findall(sets)

    # Initializes return value
    cube_prod = 0
    min_cubes: dict[str, int] = {
        allowed_colors[i]: 0 for i in range(0, len(allowed_colors))
    }
    for cur_set in set_groups:
        # Extracts individual cube values from a set
        cubes_groups = CUBES.findall(cur_set)
        debug_file += f"\tSet: {cubes_groups}\n"

        # Finds the minimum number of cubes required for the game to be possible
        for cube in cubes_groups:
            cube_type = cube[1]
            cube_num = int(cube[0])
            min_cubes[cube_type] = max(cube_num, min_cubes[cube_type])

    # Generates the required product from minimum cubes calculated
    debug_file += f"\tMinimum Cubes required: {min_cubes}\n"
    cube_prod = math.prod(min_cubes.values())
    debug_file += f"\tSet Power(Min_Red*MinGreen*Min_Blue): {cube_prod}\n"

    return cube_prod, debug_file


def decode_file(
    fp: str, allowed_config: dict[str, int] | t.List[str], debug_fp: Path
) -> int:
    """
    Decodes a txt file provided for the puzzle and returns a sum of decoded values.
    """
    is_p1 = isinstance(allowed_config, dict)
    if is_p1:
        cube_list = allowed_config.values()
        total_cubes = sum(cube_list)

    lines: t.List[str] = []
    with open(fp, "r", encoding="UTF-8") as fh:
        lines = fh.readlines()

    cummulative_sum = 0
    file_output = "DEBUG FILE\n"
    file_output += f"Allowed Config : {allowed_config} \n"
    if is_p1:
        file_output += f"Total Cubes in Bag: {total_cubes} \n\n"
    file_output += "FILE DEBUG\n\n"
    for i, line in enumerate(lines):
        file_output += f"Line {i+1}-> {line}\n"
        if is_p1:
            val, file_output = decode_line(line, allowed_config, file_output)
        else:
            val, file_output = decode_line_p2(line, allowed_config, file_output)
        if val < 0:
            raise ValueError(f"Incorrect value in line {i}")

        cummulative_sum += val
        file_output += f"\tVal: {val}, Sum: {cummulative_sum}\n"

    file_output += f"\nCUMMULATIVE_SUM: {cummulative_sum}"
    with open(debug_fp, "w", encoding="UTF-8") as out_file:
        out_file.write(file_output)

    return cummulative_sum


if __name__ == "__main__":
    dirpath = Path(__file__).parent
    filepath = Path(dirpath, "test.txt")
    filepath = Path(dirpath, "Puzzle2_Input.txt")
    debug_out = Path(dirpath, "debug_p2Out.txt")
    my_val = decode_file(filepath, {"red": 12, "green": 13, "blue": 14}, debug_out)
    print(f"P1 SUM: {my_val}")
    my_val = decode_file(filepath, ["red", "green", "blue"], debug_out)
    print(f"P2 SUM: {my_val}")
