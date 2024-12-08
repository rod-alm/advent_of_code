import itertools as it
from collections import defaultdict
from dataclasses import dataclass
from pathlib import Path
from typing import Iterator

SCRIPT_DIR = Path(__file__).parent

F = str
Position = tuple[int, int]


@dataclass
class Antenna[F: str]:
    frequency: F
    pos: Position


class Map:
    def __init__(self, data: list[list[str]]):
        self.nrows = len(data)
        self.ncols = len(data[0])
        self.antennas: dict[F, list[Antenna[F]]] = self._parse_antennas(data)

    @staticmethod
    def _parse_antennas(data: list[list[str]]) -> dict[F, list[Antenna[F]]]:
        antennas = defaultdict(list)
        for i, row in enumerate(data):
            for j, freq in enumerate(row):
                if freq != ".":
                    antennas[freq].append(Antenna(freq, (i, j)))
        return antennas

    def is_within_bounds(self, pos: Position) -> bool:
        i, j = pos
        return (0 <= i < self.nrows) and (0 <= j < self.ncols)

    def antenna_pairs_gen(self) -> Iterator[tuple[Antenna[F], Antenna[F]]]:
        for antennas in self.antennas.values():
            for antenna_pair in it.combinations(antennas, 2):
                yield antenna_pair


def load_data() -> str:
    with open(SCRIPT_DIR / "input.txt") as f:
        data = f.read()
    return data


def parse_data(data: str):
    grid = [list(line.strip()) for line in data.strip().splitlines()]
    return Map(grid)


def part1(map_: Map) -> int:
    return len(get_antinodes_part1(map_))


def get_antinodes_part1(map_: Map) -> set[Position]:
    antinodes = set()
    for ant1, ant2 in map_.antenna_pairs_gen():
        y1, x1 = ant1.pos
        y2, x2 = ant2.pos
        dy, dx = (y2 - y1, x2 - x1)
        candidates = [(y2 + dy, x2 + dx), (y1 - dy, x1 - dx)]
        antinodes.update([pos for pos in candidates if map_.is_within_bounds(pos)])
    return antinodes


def part2(map_: Map) -> int:
    return len(get_antinodes_part2(map_))


def get_antinodes_part2(map_: Map) -> set[Position]:
    antinodes = set()
    for ant1, ant2 in map_.antenna_pairs_gen():
        dy, dx = (ant2.pos[0] - ant1.pos[0], ant2.pos[1] - ant1.pos[1])

        pos = ant2.pos
        while map_.is_within_bounds(pos):
            antinodes.add(pos)
            pos = (pos[0] + dy, pos[1] + dx)

        pos = ant1.pos
        while map_.is_within_bounds(pos):
            antinodes.add(pos)
            pos = (pos[0] - dy, pos[1] - dx)

    return antinodes


def tests():
    raw_data = """
    ............
    ........0...
    .....0......
    .......0....
    ....0.......
    ......A.....
    ............
    ............
    ........A...
    .........A..
    ............
    ............
    """
    map_ = parse_data(raw_data)
    assert part1(map_) == 14
    assert part2(map_) == 34


if __name__ == "__main__":
    tests()

    data = parse_data(load_data())
    print("Part 1:", part1(data))
    print("Part 2:", part2(data))
