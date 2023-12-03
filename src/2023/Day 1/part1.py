from pathlib import Path 
from typing import List

SCRIPT_DIR = Path(__file__).parent.absolute()
INPUT_FILE = SCRIPT_DIR / 'input.txt'


def get_calibration_values(text: str) -> List[int]:
    values = []
    for line in text.strip().split("\n"):
        digits = [c for c in line if c.isdigit()]
        val = int(digits[0] + digits[-1])
        values.append(val)
    return values


def run_tests():
    text = """
    1abc2
    pqr3stu8vwx
    a1b2c3d4e5f
    treb7uchet
    """
    expected = [12, 38, 15, 77]
    assert get_calibration_values(text) == expected


if __name__ == '__main__':
    run_tests()

    with INPUT_FILE.open() as f:
        res = sum(get_calibration_values(f.read()))
        
    print("1st answer:", res)