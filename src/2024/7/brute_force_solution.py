import itertools as it
import operator as op
from dataclasses import dataclass
from functools import reduce
from pathlib import Path
from typing import Callable, Sequence

SCRIPT_DIR = Path(__file__).parent

BinaryOperator = Callable[[int, int], int]


def concat(x: int, y: int) -> int:
    return int(f"{x}{y}")


@dataclass
class Equation:
    operands: list[int]
    result: int

    @property
    def num_operators(self):
        return len(self.operands) - 1

    def operators_are_valid(self, operators: Sequence[BinaryOperator]) -> bool:
        operators_iter = iter(operators)
        total = reduce(lambda x, y: next(operators_iter)(x, y), self.operands)
        return total == self.result


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


def is_solvable(eq: Equation, allowed_opr: Sequence[BinaryOperator]) -> bool:
    return any(
        eq.operators_are_valid(operators)
        for operators in it.product(allowed_opr, repeat=eq.num_operators)
    )


def total_calibration_result(
    equations: list[Equation], allowed_opr: Sequence[BinaryOperator]
) -> int:
    return sum(eq.result for eq in equations if is_solvable(eq, allowed_opr))


def part1(equations: list[Equation]) -> int:
    return total_calibration_result(equations, [op.add, op.mul])


def part2(equations: list[Equation]) -> int:
    return total_calibration_result(equations, [op.add, op.mul, concat])


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
    # print(part2(equations))
    assert part2(equations) == 11387


if __name__ == "__main__":
    tests()

    data = parse_data(load_data())
    print("Part 1:", part1(data))
    print("Part 2:", part2(data))
