from __future__ import annotations

import typing as t

import os
import re 
from pathlib import Path

FLAGS = re.VERBOSE | re.DOTALL


numbers = {"zero":0, "one": 1, "two": 2, "three": 3, "four": 4, "five": 5, "six": 6, "seven": 7, "eight": 8, "nine": 9}


DIGIT = re.compile(r'(?:\d|zero|one|two|three|four|five|six|seven|eight|nine)')
DIGIT_REVERSE = re.compile(r"(?:\d|orez|eno|owt|eerht|ruof|evif|xis|neves|thgie|enin)")

def to_int(id: str):
    if id in numbers.keys():
        return numbers[id]
    else:
        return int(id)

def decode_line(line: str):
    first = DIGIT.search(line).group()
    val = -1
    line_reverse = line[::-1]
    last = DIGIT_REVERSE.search(line_reverse).group()
    last = last[::-1]
    val = to_int(first)*10 + to_int(last)
    return val

def decode_file(filepath: str):
    lines: t.List[str] = [] 
    with open(filepath) as fh:
        lines = fh.readlines()

    sum=0
    for i,line in enumerate(lines):
        val = decode_line(line)
        if val < 0:
            raise ValueError(f"Incorrect value in line {i}")
        
        sum += val
        #print(f"source: {line}")
        #print(f"Line {i+1}, Val: {val}, Sum: {sum}")
        
    return sum



dirpath = Path(__file__).parent
filepath = Path(dirpath, "test.txt")
filepath = Path(dirpath, "Inputcode.txt")


sum = decode_file(filepath)
print(f"FINAL SUM: {sum}")
