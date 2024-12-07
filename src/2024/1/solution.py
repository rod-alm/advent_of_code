from pathlib import Path
from collections import Counter

SCRIPT_DIR = Path(__file__).parent

def load_data():
    left, right = [], []
    with open(SCRIPT_DIR / "input.txt") as f:
        for line in f:
            x, *_ , y = line.split(" ")
            left.append(int(x))
            right.append(int(y))
    return left, right


def part1(left, right):
    total_diff = sum(abs(x-y) for x, y in zip(sorted(left), sorted(right)))
    print("Part 1:", total_diff)


def part2(left, right):
    right_counts = Counter(right)
    similarity_score = sum(x * right_counts[x] for x in left)
    print("Part 2:", similarity_score)


left, right = load_data()
part1(left, right)
part2(left, right)


