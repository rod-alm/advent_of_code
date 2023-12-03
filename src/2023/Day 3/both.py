from pathlib import Path 
from typing import Iterator, Callable
from dataclasses import dataclass

SCRIPT_DIR = Path(__file__).parent.absolute()
INPUT_FILE = SCRIPT_DIR / 'input.txt'

def load_input() -> str:
    with INPUT_FILE.open() as f:
        return f.read()


# ---------- PART 1 ----------             
        
def numbers_with_digit_positions(text: str) -> Iterator[tuple[int, list[int, int]]]: 
    """ yields each number in text and the corresponding digit positions """
    for i, line in enumerate(text.strip().split("\n")):
        num = ""
        digit_positions = []
        for j, chr in enumerate(line.strip()):
            if chr.isdigit():
                digit_positions.append((i, j))
                num += chr
            else:
                if num:
                    yield (int(num), digit_positions)
                    num = ""
                    digit_positions = []
        if num:            
            yield (int(num), digit_positions)
            
            
def get_char_positions(
    eng_schema: str, 
    predicate: Callable[[str], bool]
) -> set[tuple[int, int]]:
    chr_positions = set()
    for i, line in enumerate(eng_schema.strip().split("\n")):
        for j, chr in enumerate(line.strip()):
            if predicate(chr):
                chr_positions.add((i, j))
    return chr_positions


def neighbors(chr_pos: tuple[int, int]) -> list[tuple[int, int]]:
    i, j = chr_pos
    neighs = [
        (i-1, j-1), (i-1, j), (i-1, j+1),
        (i, j-1), (i, j+1),  
        (i+1, j-1), (i+1, j), (i+1, j+1)
    ]
    return neighs


def is_symbol(chr: str) -> bool:
    return (not chr.isdigit()) and (chr != ".")


def is_adjacent_to_symbol(
    chr_pos: tuple[int, int], 
    sym_positions: set[tuple[int, int]]
) -> bool:
    return any(neigh_pos in sym_positions for neigh_pos in neighbors(chr_pos))


def get_part_numbers(eng_schema: str) -> list[int]:
    part_nums = []
    sym_positions = get_char_positions(eng_schema, is_symbol)
    for num, digit_positions in numbers_with_digit_positions(eng_schema):
        for (i, j) in digit_positions:
            if is_adjacent_to_symbol((i, j), sym_positions):
                part_nums.append(num)
                break
    return part_nums


def part_numbers_sum(eng_schema: str) -> int:
    return sum(get_part_numbers(eng_schema))


# ---------- PART 2 ---------- 

@dataclass
class Gear:
    pos: tuple[int, int]
    numbers: list[int]
    
    @property
    def ratio(self):
        return self.numbers[0] * self.numbers[1]


def get_numbers_lkp(eng_schema: str) -> dict[tuple[int, int], int]:
    num_lkp = {}
    for num, digit_positions in numbers_with_digit_positions(eng_schema):
        for pos in digit_positions:
            num_lkp[pos] = num
    return num_lkp


def get_gears(eng_schema: str) -> list[Gear]:
    gear_candidates_pos = get_char_positions(eng_schema, lambda chr: chr == "*")
    nums_lkp = get_numbers_lkp(eng_schema)
    gears = []
    
    for pos in gear_candidates_pos:
        gear_neigh_nums = {
            nums_lkp[neigh_pos] for neigh_pos in neighbors(pos)
            if neigh_pos in nums_lkp
        }
        if len(gear_neigh_nums) == 2:
            gear = Gear(pos, list(gear_neigh_nums))
            gears.append(gear)
    
    return gears


def gear_ratio_sum(eng_schema: str) -> int:
    return sum(gear.ratio for gear in get_gears(eng_schema))


def run_tests():
    eng_schema = """
        467..114..
        ...*......
        ..35..633.
        ......#...
        617*......
        .....+.58.
        ..592.....
        ......755.
        ...$.*....
        .664.598..
    """
    assert get_part_numbers(eng_schema) == [467, 35, 633, 617, 592, 755, 664, 598]
    assert part_numbers_sum(eng_schema) == 4361
    assert gear_ratio_sum(eng_schema) == 467835
    
    
if __name__ == '__main__':
    
    run_tests()
    eng_schema = load_input()
    first_answer = part_numbers_sum(eng_schema)
    second_answer = gear_ratio_sum(eng_schema)
    print("1st answer:", first_answer)
    print("2nd answer:", second_answer)
