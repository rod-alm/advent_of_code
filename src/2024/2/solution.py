from pathlib import Path
from collections import Counter

SCRIPT_DIR = Path(__file__).parent

def load_data() -> list[list[int]]:
    with open(SCRIPT_DIR / "input.txt") as f:
        data = [[int(x) for x in line.split(" ")] for line in f]
        return data

def is_report_safe(report: list[int]) -> bool:
    try:
        sign = (report[1] - report[0]) / abs(report[1] - report[0])
    except ZeroDivisionError:
        return False

    allowed = {sign * x for x in range(1, 4)}
    for x, y in zip(report, report[1:]):
        if y - x not in allowed:
            return False
        
    return True

    
def part1(data: list[list[int]]):
    print("Part 1:", sum(is_report_safe(report) for report in data))


def is_report_safe2(report: list[int], can_remove: bool = True) -> bool:
    try:
        sign = (report[1] - report[0]) / abs(report[1] - report[0])
    except ZeroDivisionError:
        if can_remove:
            return is_report_safe2(report[1:], can_remove=False)
        else:
            return False

    allowed = {sign * x for x in range(1, 4)}
    for idx, (x, y) in enumerate(zip(report, report[1:])):
        if y - x not in allowed:
            if can_remove:
                new_report = report[:idx] + report[idx+1:]
                return is_report_safe2(new_report, can_remove=False)
            else:
                return False
        
    return True

def get_sign(report: list[int]) -> int:
    diffs = [y-x for x, y in zip(report, report[1:])]
    increasing = sum(x for x in diffs if x > 0)
    zeros = sum(x for x in diffs if x==0)
    decreasing = len(diffs) - increasing - zeros
    max_count = max(zeros, increasing, decreasing)
    if (zeros >= 2) or (zeros == max_count):
        return 0 
    if increasing == max_count:
        return 1
    elif decreasing == max_count:
        return -1


def is_report_safe3(report: list[int]) -> bool:
    """
    can_remove = True

    if report[0] != report[1]:
        first_idx = 0
    else:
        if report[2] == report[1]:
            return False 
        first_idx = 1
        can_remove = False
    
    diff = report[first_idx + 1] - report[first_idx]
    sign = diff / abs(diff)
    """
    can_remove = True
    sign = get_sign(report)

    allowed = {sign * x for x in range(1, 4)}
    #for idx, (x, y) in enumerate(zip(report[first_idx:], report[first_idx+1:])):
    for idx, (x, y) in enumerate(zip(report[:], report[1:])):
        if y - x not in allowed:
            if can_remove:
                if idx == 0
                """
                try:
                    if report[idx + 2] - x not in allowed:
                        return False
                except IndexError:
                    return True
                """
            else:
                return False
            can_remove = False

    return True

def is_report_safe4(report):
    diffs = [y-x for x, y in zip(report, report[1:])]
    if diffs.count(0) >= 3:
        return False

def is_report_safe_brute_force(report):
    for i in range(0, len(report)):
        new_report = report[:i] + report[i+1:]
        if is_report_safe(new_report):
            return True
    return False

def part2(data):
    print("Part 2:", sum(is_report_safe_brute_force(report) for report in data))


data = load_data() 
part1(data)
part2(data)

import json

"""
tests = [[report, is_report_safe_brute_force(report)] for report in data]
with open(SCRIPT_DIR/"tests.json", "w") as f:
    json.dump(tests, f, indent=4)
"""
with open(SCRIPT_DIR/"tests.json", "r") as f:
    tests = json.load(f)


for i, (report, expected) in enumerate(tests):
    res = is_report_safe3(report)
    diffs = [y-x for x, y in zip(report, report[1:])]
    if res != expected:
        print(f"{i} - {report}, expected: {expected}, diffs: {diffs}")


"""
for report in data[:20]:
    diffs = [y-x for x, y in zip(report, report[1:])]
    print(f"\t({report}, {is_report_safe3(report)}),")
    #print(report, diffs, is_report_safe3(report))
"""