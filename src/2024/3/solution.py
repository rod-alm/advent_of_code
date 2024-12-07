import re
from pathlib import Path

SCRIPT_DIR = Path(__file__).parent

def load_data() -> str:
    with open(SCRIPT_DIR / "input.txt") as f:
        return f.read()


def parse_and_sum_muls(data: str) -> int:
    muls = []
    for pair in re.findall(r"mul\((\d+,\d+)\)", data):
        x, y = map(int, pair.split(","))
        muls.append(x*y)
    return sum(muls)


def part1(data: str):
    print("Part 1:", parse_and_sum_muls(data))


def part2(data: str):
    
    result = 0
    # split the string on '' characters that follow 'do()' or 'don't()'
    for substr in re.split(r"(?=do\(\)|don't\(\))\s*", data):
        if not substr.startswith("don't()"):
            result += parse_and_sum_muls(substr)

    print("Part 2:", result)

"""
def try_parse_mul(data: str, i: int):
    length = len(data)

    if data[i:i+4] == "mul(":
        i += 4
        x, y = "", ""
        while i < length and data[i].isdigit():
            x += data[i]
            i += 1
        if i < length and data[i] == ",":
            i += 1
        else: 
            return None, i
        while i < length and data[i].isdigit():
            y += data[i]
            i += 1
        if i < length and data[i] == ")":
            i += 1
        else:
            return None, i

def part1_no_regex(data: str):
    i = 0
    length = len(data)

    while i < length:
        pass
"""        
            

data = load_data()
part1(data)
part2(data)




