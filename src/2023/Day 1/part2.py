from pathlib import Path 
from typing import List
import re

SCRIPT_DIR = Path(__file__).parent.absolute()
INPUT_FILE = SCRIPT_DIR / 'input.txt'

NAMES_TO_DIGITS = {
    "one": "1",
    "two": "2",
    "three": "3",
    "four": "4",
    "five": "5",
    "six": "6",
    "seven": "7",
    "eight": "8",
    "nine": "9",
}


def get_digits(line: str) -> List[int]:
    # positive lookahead to find overlapping matches (e.g "oneight")
    pat = "(?=({0}))|\d".format('|'.join(NAMES_TO_DIGITS))
    numbers = []
    for match in re.finditer(pat, line):
        if match.group(0).isdigit():
            num = match.group(0)
        else:
            num = NAMES_TO_DIGITS[match.group(1)]
        numbers.append(int(num))
    return numbers


def get_calibration_value(line: str) -> int:
    digits = get_digits(line)
    return 10*digits[0] + digits[-1]


def calibration_values_sum(text: str) -> int:
    return sum(get_calibration_value(line) for line in text.strip().split("\n"))


def run_tests():
    text = """
        two1nine
        eightwothree
        abcone2threexyz
        xtwone3four
        4nineeightseven2
        zoneight234
        7pqrstsixteen
    """
          
    assert calibration_values_sum(text) == 281
    
    assert get_digits("oneasaseight") == [1, 8]
    assert get_digits("oneight") == [1, 8]
    assert get_digits("1aa2bbthreeccfour") == [1, 2, 3, 4]


if __name__ == '__main__':
    run_tests()
    
    with INPUT_FILE.open() as f:
        text = f.read().strip()
        res = calibration_values_sum(text)
        print("2nd answer:", res)