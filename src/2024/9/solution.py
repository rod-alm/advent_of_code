from pathlib import Path
from dataclasses import dataclass

SCRIPT_DIR = Path(__file__).parent


@dataclass(order=True)
class FileBlock:
    start: int
    size: int
    id: int

    @property
    def checksum(self):
        return sum(i * self.id for i in range(self.start, self.start + self.size))

    def __str__(self):
        return str(self.id) * self.size


@dataclass(order=True)
class FreeBlock:
    start: int
    size: int

    def __str__(self):
        return "." * self.size


@dataclass
class DiskMap:
    file_blocks: list[FileBlock]
    empty_blocks: list[FreeBlock]


def load_data() -> str:
    with open(SCRIPT_DIR / "input.txt") as f:
        data = f.read()
    return data


def parse_data(data: str) -> DiskMap:
    file_blocks = []
    empty_blocks = []
    file_id = 0
    start = 0
    for i, size in enumerate(data.strip()):
        if i % 2 == 0:
            file_blocks.append(FileBlock(start, int(size), file_id))
            file_id += 1
        else:
            empty_blocks.append(FreeBlock(start, int(size)))
        start += int(size)

    return DiskMap(file_blocks, empty_blocks)


def move_files_part1(disk_map: DiskMap) -> list[FileBlock]:
    free_blocks = disk_map.empty_blocks[::-1]
    file_blocks = disk_map.file_blocks[:]
    moved_blocks: list[FileBlock] = []

    while free_blocks[-1].start < file_blocks[-1].start:
        free = free_blocks.pop(-1)
        block = file_blocks.pop(-1)
        space_remaining = free.size - block.size

        if space_remaining >= 0:
            moved_blocks.append(
                FileBlock(start=free.start, size=block.size, id=block.id)
            )
            if space_remaining > 0:
                free_blocks.append(
                    FreeBlock(start=free.start + block.size, size=space_remaining)
                )
        else:
            moved_blocks.append(
                FileBlock(start=free.start, size=free.size, id=block.id)
            )
            file_blocks.append(
                FileBlock(start=block.start, size=block.size - free.size, id=block.id)
            )

    return sorted(moved_blocks + file_blocks)


def compute_filestystem_checksum(file_blocks: list[FileBlock]) -> int:
    return sum(block.checksum for block in file_blocks)


def part1(disk_map: DiskMap) -> int:
    file_blocks = move_files_part1(disk_map)
    return compute_filestystem_checksum(file_blocks)


def move_files_part2(disk_map: DiskMap) -> list[FileBlock]:
    free_blocks = disk_map.empty_blocks
    file_blocks = disk_map.file_blocks

    for block in reversed(file_blocks):
        free_idx = 0
        free = free_blocks[free_idx]

        while (
            (free.size < block.size)
            and (free.start < block.start)
            and (free_idx < len(free_blocks) - 1)
        ):
            free_idx += 1
            free = free_blocks[free_idx]

        space_remaining = free.size - block.size

        if (space_remaining >= 0) and (free.start < block.start):
            block.start = free.start

            if space_remaining > 0:
                free.start += block.size
                free.size = space_remaining
            else:
                free_blocks.pop(free_idx)

            free_blocks.append(FreeBlock(start=block.start, size=block.size))

    return sorted(file_blocks)


def part2(disk_map) -> int:
    file_blocks = move_files_part2(disk_map)
    return compute_filestystem_checksum(file_blocks)


def tests():
    raw_data = "2333133121414131402"
    disk_map = parse_data(raw_data)
    assert part1(disk_map) == 1928
    assert part2(disk_map) == 2858


if __name__ == "__main__":
    tests()

    data = parse_data(load_data())
    print("Part 1:", part1(data))
    print("Part 2:", part2(data))
