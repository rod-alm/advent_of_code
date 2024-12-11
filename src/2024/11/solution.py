from functools import cache
from pathlib import Path

SCRIPT_DIR = Path(__file__).parent


def load_data() -> str:
    with open(SCRIPT_DIR / "input.txt") as f:
        data = f.read()
    return data


def parse_data(data: str) -> list[int]:
    return [int(num) for num in data.strip().split(" ")]


@cache
def count_stones(stone: int, n: int) -> int:
    if n <= 0:
        return 1

    if stone == 0:
        return count_stones(1, n - 1)

    elif len(str(stone)) % 2 == 0:
        stone_str = str(stone)
        idx = len(str(stone)) // 2
        return count_stones(int(stone_str[:idx]), n - 1) + count_stones(
            int(stone_str[idx:]), n - 1
        )
    else:
        return count_stones(2024 * stone, n - 1)


def part1(stones: list[int]) -> int:
    return sum(count_stones(s, n=25) for s in stones)


def part2(stones: list[int]) -> int:
    return sum(count_stones(s, n=75) for s in stones)


def tests():
    raw_data = "125 17"
    stones = parse_data(raw_data)

    assert part1(stones) == 55312


if __name__ == "__main__":
    tests()

    data = parse_data(load_data())
    print("Part 1:", part1(data))
    print("Part 2:", part2(data))
