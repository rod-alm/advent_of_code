from pathlib import Path
from typing import Iterator, Optional

SCRIPT_DIR = Path(__file__).parent

Map = list[list[int]]
Position = tuple[int, int]


def load_data() -> str:
    with open(SCRIPT_DIR / "input.txt") as f:
        data = f.read()
    return data


def parse_data(data: str) -> Map:
    return [[int(x) for x in line.strip()] for line in data.strip().splitlines()]


def part1(data: Map) -> int:
    return sum(trailhead_score(data, head) for head in trailhead_gen(data))


def trailhead_gen(data: Map) -> Iterator[Position]:
    for i, row in enumerate(data):
        for j, height in enumerate(row):
            if height == 0:
                yield (i, j)


def trailhead_score(
    data: Map, curr: Position, visited: Optional[set[Position]] = None
) -> int:
    i, j = curr
    curr_height = data[i][j]
    visited = visited or set()
    visited.add(curr)

    if curr_height == 9:
        return 1

    score = 0
    for n, m in neighbours_gen(data, curr):
        if (data[n][m] == curr_height + 1) and ((n, m) not in visited):
            score += trailhead_score(data, (n, m), visited)

    return score


def neighbours_gen(data: Map, pos: Position) -> Iterator[Position]:
    i, j = pos
    neighbours = [(i - 1, j), (i, j - 1), (i + 1, j), (i, j + 1)]
    for n, m in neighbours:
        if (0 <= n < len(data)) and (0 <= m < len(data[0])):
            yield (n, m)


def part2(data) -> int:
    return sum(trailhead_rating(data, head) for head in trailhead_gen(data))


def trailhead_rating(data: Map, curr: Position) -> int:
    i, j = curr
    curr_height = data[i][j]

    if curr_height == 9:
        return 1

    score = 0
    for n, m in neighbours_gen(data, curr):
        if data[n][m] == curr_height + 1:
            score += trailhead_rating(data, (n, m))

    return score


def tests():
    raw_data = """
    89010123
    78121874
    87430965
    96549874
    45678903
    32019012
    01329801
    10456732
    """
    data = parse_data(raw_data)
    assert part1(data) == 36
    assert part2(data) == 81


if __name__ == "__main__":
    tests()

    data = parse_data(load_data())
    print("Part 1:", part1(data))
    print("Part 2:", part2(data))
