from pathlib import Path
from enum import Enum
from typing import ClassVar


SCRIPT_DIR = Path(__file__).parent

Position = tuple[int, int]

class Directions(Enum):
    N = (-1, 0)  
    S = (1, 0)   
    E = (0, 1)   
    W = (0, -1)  

    def move(self, start: tuple[int, int], steps: int = 1) -> tuple[int, int]:
        y0, x0 = start
        dy, dx = self.value
        return (y0 + steps * dy, x0 + steps * dx)

    def rotate_clockwise(self) -> "Directions":
        new_direction = {
            Directions.N : Directions.E,
            Directions.E: Directions.S,
            Directions.S: Directions.W,
            Directions.W: Directions.N
        }[self]
        return new_direction
    

class Guard:
    DIRECTION_TO_CHAR: ClassVar[dict[Directions, str]] = {
        Directions.N: "^", 
        Directions.E: ">",
        Directions.S: "v",
        Directions.W: "<",
    }

    def __init__(self, direction: Directions, pos: Position):
        self.direction = direction
        self.pos = pos
        self.seen = {pos}

    def render(self):
        return self.DIRECTION_TO_CHAR[self.direction]
    
    def get_next_position(self):
        return self.direction.move(self.pos)
    
    def move(self):
        self.pos = self.direction.move(self.pos)
        self.seen.add(self.pos)

    def move_to(self, pos: Position):
        self.pos = pos
        self.seen.add(self.pos)


    def move_until_next_colision(self, map: "Map") -> tuple[Position, bool]:
        next_pos = self.get_next_position()
        while  not (map.is_boundary(next_pos) or map.is_obstacle(next_pos)):
            self.move_to(next_pos)
            next_pos = self.get_next_position()
            
        return self.pos, map.is_boundary(next_pos)
    

    def rotate_clockwise(self):
        self.direction = self.direction.rotate_clockwise()


    def number_of_distinct_positions(self):
        return len(self.seen)

"""
def distance(pos1: Position, pos2: Position) -> int:
    y1, x1 = pos1 
    y2, x2 = pos2
    return abs(x2 - x1) + abs(y2 - y1)
"""

def load_data() -> str:
    with open(SCRIPT_DIR / "input.txt") as f:
        data = f.read()
    return data


class Map:
    def __init__(self, data: list[list[str]]):
        self.data = data
        self.ncols = len(data[0])
        self.nrows = len(data)

    def is_obstacle(self, pos: Position) -> bool:
        i, j = pos
        return self.data[i][j] == "#"
    
    def is_boundary(self, pos: Position) -> bool:
        i, j = pos
        return (not (0 <= i < self.nrows)) or (not (0 <= j < self.ncols))
    
    """
    def get_next_colision(self, pos: Position, direction: Directions) -> tuple[Position, bool]:
        next_pos = direction.move(pos)
        while  not (self.is_boundary(next_pos) or self.is_obstacle(next_pos)):
            #print(pos, next_pos)
            pos = next_pos
            next_pos = direction.move(next_pos)
            
        return pos, self.is_boundary(next_pos)
    """
    
    def render(self, guard: Guard):
        i, j = guard.pos

        old_val = self.data[i][j]
        self.data[i][j] = guard.render()

        map_str = "\n".join("".join(row) for row in self.data)
        print("\n", map_str, "\n", sep="")
        self.data[i][j] = old_val



def find_guard(map_data: list[list[str]]) -> Guard:
    char_to_direction = {
       v: k for k, v in Guard.DIRECTION_TO_CHAR.items()
    }
    for i, row in enumerate(map_data):
        for j, val in enumerate(row):
            if val in char_to_direction:
                return Guard(
                    pos=(i, j), 
                    direction=char_to_direction[val]
                )

    raise ValueError("Start position not found")

def parse_data(data: str) -> tuple[Map, Guard]:
    map_data = [list(line.strip()) for line in data.strip().splitlines()]
    guard = find_guard(map_data)
    i, j = guard.pos 
    map_data[i][j] = "."

    return Map(map_data), guard

    
def part1(map_: Map, guard: Guard) -> int:
    while True:
        #map_.render(guard)
        next_pos, next_is_boundary = guard.move_until_next_colision(map_)

        if next_is_boundary:
            return guard.number_of_distinct_positions()
        else:
            guard.rotate_clockwise()


def part2(data: list[list[str]]) -> int:
    pass


def tests():
    raw_data = """
    ....#.....
    .........#
    ..........
    ..#.......
    .......#..
    ..........
    .#..^.....
    ........#.
    #.........
    ......#...
    """
    m, g = parse_data(raw_data)
    assert part1(m, g) == 41


if __name__ == "__main__":
    map_, guard = parse_data(load_data())
    #print(data)
    tests()

    print("Part 1:", part1(map_, guard))
    #print("Part 2:", part2(data))