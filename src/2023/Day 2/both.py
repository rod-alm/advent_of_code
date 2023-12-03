from pathlib import Path 
from dataclasses import dataclass

SCRIPT_DIR = Path(__file__).parent.absolute()
INPUT_FILE = SCRIPT_DIR / 'input.txt'


@dataclass(eq=True)
class CubesSet:
    red: int = 0
    green: int = 0
    blue: int = 0
    
    @property
    def power(self) -> int:
        return self.red * self.green * self.blue
    
    def __contains__(self, other: "CubesSet") -> "CubesSet":
        for color in ["red", "blue", "green"]:
            if getattr(other, color) > getattr(self, color):
                return False
        return True
    

class Game:
    BAG = CubesSet(red=12, green=13, blue=14)
    
    def __init__(self, id: id, samples: list[CubesSet]):
        self.id = id
        self.samples = samples
        
    def __str__(self):
        return f"Game {self.id}: {self.samples}"
    
    @classmethod
    def from_string(cls, line: str) -> "Game":
        def parse_sample(sample_str: str) -> CubesSet:
            cubes_sample = {}
            for cube in sample_str.split(","):
                qty, color = cube.strip().split(" ")
                cubes_sample[color] = int(qty)
            return CubesSet(**cubes_sample)
        
        id, samples = line.lstrip("Game ").split(":")
        id = int(id)
        samples = [parse_sample(s) for s in samples.split("; ")]
        return cls(id, samples)
    
    def is_valid(self) -> bool:
        return all(s in self.BAG for s in self.samples)
      
    def get_least_power(self) -> int:
        return self.smallest_valid_bag().power
    
    def smallest_valid_bag(self) -> CubesSet:
        min_sample = CubesSet(
            red = max(s.red for s in self.samples),
            green = max(s.green for s in self.samples),
            blue = max(s.blue for s in self.samples)
        )
        return min_sample
            
    
def parse_input() -> list[Game]:
    with INPUT_FILE.open() as f:
        games = [Game.from_string(line) for line in f]
    return games
        
        
def sum_valid_ids(games: list[Game]) -> int:
    return sum(g.id for g in games if g.is_valid())    


def total_least_power(games: list[Game]) -> int:
    return sum(g.get_least_power() for g in games)


def run_tests():
    games_str = """
        Game 1: 3 blue, 4 red; 1 red, 2 green, 6 blue; 2 green
        Game 2: 1 blue, 2 green; 3 green, 4 blue, 1 red; 1 green, 1 blue
        Game 3: 8 green, 6 blue, 20 red; 5 blue, 4 red, 13 green; 5 green, 1 red
        Game 4: 1 green, 3 red, 6 blue; 3 green, 6 red; 3 green, 15 blue, 14 red
        Game 5: 6 red, 1 blue, 3 green; 2 blue, 1 red, 2 green
    """
    games = [Game.from_string(line) for line in games_str.strip().split("\n")]

    g = games[0]
    assert g.samples[0] == CubesSet(blue=3, red=4, green=0)
    assert g.id == 1
    assert g.is_valid()
    assert g.smallest_valid_bag() == CubesSet(blue=6, red=4, green=2)
    assert g.get_least_power() == 48
    
    g = games[2]
    assert g.samples[1] == CubesSet(blue=5, red=4, green=13)
    assert g.id == 3
    assert not g.is_valid()
    
    assert sum_valid_ids(games) == 8
    assert total_least_power(games) == 2286


if __name__ == "__main__":
    run_tests()
    games = parse_input()
    first_answer = sum_valid_ids(games)
    second_answer = total_least_power(games)
    print("1st answer:", first_answer)
    print("2nd answer:", second_answer)