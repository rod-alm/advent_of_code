"""
Adapted from: https://github.com/antcap96/advent_of_code/blob/main/python/year2024/year2024/day7.py
"""

import operator as op
from dataclasses import dataclass
from pathlib import Path
from typing import Callable

SCRIPT_DIR = Path(__file__).parent


@dataclass
class Equation:
    operands: list[int]
    result: int


@dataclass
class InverseOperation:
    apply: Callable[[int, int], int]
    is_valid: Callable[[int, int], bool]


def is_divisible_by(result: int, by: int) -> bool:
    return result % by == 0


def remove_suffix_digits(result: int, suffix: int) -> int:
    return int(str(result).removesuffix(str(suffix)))


def number_ends_with(result: int, suffix: int) -> bool:
    return result > suffix and str(result).endswith(str(suffix))


inverse_add = InverseOperation(op.sub, is_valid=op.gt)
inverse_mul = InverseOperation(op.floordiv, is_valid=is_divisible_by)
inverse_concat = InverseOperation(remove_suffix_digits, is_valid=number_ends_with)


def load_data() -> str:
    with open(SCRIPT_DIR / "input.txt") as f:
        data = f.read()
    return data


def parse_data(data: str) -> list[Equation]:
    equations = []
    for line in data.strip().splitlines():
        result, rhs = line.split(": ")
        operands = [int(x) for x in rhs.strip().split(" ")]
        equations.append(Equation(operands, int(result)))
    return equations


def is_solvable(numbers: list[int], result: int, inv_operators: list[InverseOperation]):
    match numbers:
        case [first]:
            return first == result

        case [*remaining, last]:
            return any(
                is_solvable(remaining, op.apply(result, last), inv_operators)
                for op in inv_operators
                if op.is_valid(result, last)
            )


def total_calibration_result(
    equations: list[Equation], allowed_opr: list[InverseOperation]
) -> int:
    return sum(
        eq.result
        for eq in equations
        if is_solvable(eq.operands, eq.result, allowed_opr)
    )


def part1(equations: list[Equation]) -> int:
    return total_calibration_result(equations, [inverse_add, inverse_mul])


def part2(equations: list[Equation]) -> int:
    return total_calibration_result(
        equations, [inverse_add, inverse_mul, inverse_concat]
    )


def tests():
    raw_data = """
    190: 10 19
    3267: 81 40 27
    83: 17 5
    156: 15 6
    7290: 6 8 6 15
    161011: 16 10 13
    192: 17 8 14
    21037: 9 7 18 13
    292: 11 6 16 20
    """
    equations = parse_data(raw_data)
    assert part1(equations) == 3749
    assert part2(equations) == 11387


if __name__ == "__main__":
    tests()

    data = parse_data(load_data())
    print("Part 1:", part1(data))
    print("Part 2:", part2(data))
