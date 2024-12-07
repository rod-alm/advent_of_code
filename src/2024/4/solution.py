from pathlib import Path
from enum import Enum

SCRIPT_DIR = Path(__file__).parent

def load_data() -> list[list[str]]:
    with open(SCRIPT_DIR / "input.txt") as f:
        data = [[x for x in line] for line in f]
    return data

class Directions(Enum):
    N = (-1, 0)  
    S = (1, 0)   
    E = (0, 1)   
    W = (0, -1)  
    NE = (-1, 1) 
    NW = (-1, -1) 
    SE = (1, 1)  
    SW = (1, -1) 

    def move(self, start: tuple[int, int], steps: int = 1) -> tuple[int, int]:
        y0, x0 = start
        dy, dx = self.value
        return (y0 + steps * dy, x0 + steps * dx)


def search_word_rec(data: list[list[str]], word: str, start: tuple[int, int], directions: Directions) -> int:
    if word == "":
        return 1
    
    y1, x1 = start

    if not (0 <= y1 < len(data)) or not (0 <= x1 < len(data[0])):
        return 0
    
    y2, x2 = directions.move(start, steps=1)

    if data[y1][x1] == word[0]:
        return search_word_rec(data, word[1:], (y2, x2), directions)
    else:
        return 0


def search_word(data: list[list[str]], word: str, start: tuple[int, int], direction: Directions) -> int:
    yf, xf = direction.move(start, steps=len(word)-1)
    
    if not (0 <= yf < len(data)) or not (0 <= xf < len(data[0])):
        return 0
    
    for i, c in enumerate(word):
        y, x = direction.move(start, steps=i)
        if data[y][x] != c:
            return 0
    return 1


def get_word(data: list[list[str]], start: tuple[int, int], direction: Directions, size: int) -> str:
    yf, xf = direction.move(start, steps=size-1)
    word = []
    for i in range(size):
        y, x = direction.move(start, steps=i)
        word.append(data[y][x])
    return "".join(word)

    
def part1(data: list[list[str]]) -> int:
    matches = 0
    for i, row in enumerate(data):
        for j, char in enumerate(row):
            if char == "X":
                for d in Directions:
                    matches += search_word(data, "XMAS", (i, j), d)
    return matches


def is_xmas_puzzle(data, center: tuple[int, int]):
    pos1 = Directions.NE.move(center, steps=1)
    word1 = get_word(data, pos1, Directions.SW, size=3)
    if word1 not in ("MAS", "SAM"):
        return 0
    
    pos2 = Directions.NW.move(center, steps=1)
    word2 = get_word(data, pos2, Directions.SE, size=3)
    if word2 not in ("MAS", "SAM"):
        return 0
    return 1

def part2(data: list[list[str]]) -> int:
    matches = 0
    for i, row in enumerate(data[1:-1], start=1):
        for j, char in enumerate(row[1:-1], start=1):
            if char == "A":
                matches += is_xmas_puzzle(data, (i, j))
    return matches


def tests():
    test_data = """
        MMMSXXMASM
        MSAMXMSMSA
        AMXSXMAAMM
        MSAMASMSMX
        XMASAMXAMM
        XXAMMXXAMA
        SMSMSASXSS
        SAXAMASAAA
        MAMMMXMMMM
        MXMXAXMASX
    """
    test_data = [list(line.strip()) for line in test_data.strip().split("\n")]
    assert part1(test_data) == 18


data = load_data() 
tests()

print("Part 1:", part1(data))
print("Part 2:", part2(data))