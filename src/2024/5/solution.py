from pathlib import Path
from dataclasses import dataclass
from collections import defaultdict
from functools import cmp_to_key, partial


SCRIPT_DIR = Path(__file__).parent

Rules = dict[int, list[int]]
Update = list[int]

@dataclass
class PageUpdates:
    rules: Rules
    updates: list[Update]


def load_data() -> str:
    with open(SCRIPT_DIR / "input.txt") as f:
        data = f.read()
    return data


def parse_data(data: str) -> PageUpdates:
    rules_data, upd_data = data.split("\n\n")

    rules = defaultdict(list)
    for rule in rules_data.strip().split("\n"):
        before, after = rule.strip().split("|")
        rules[int(after)].append(int(before))
    
    updates = [
        [int(p) for p in upd.split(",")] 
        for upd in upd_data.strip().split("\n")
    ]
    return PageUpdates(rules, updates)


def part1(data: PageUpdates) -> int:
    res = 0
    for upd in data.updates:
        if is_update_valid(upd, data.rules):
            res += upd[len(upd) // 2]
    return res


def is_update_valid(update: Update, rules: Rules) -> bool:
    pages_pos = {x: i for i, x in enumerate(update)}
    for curr, curr_pos in pages_pos.items():
        for page in rules[curr]:
            if pages_pos.get(page, -1) > curr_pos:
                return False
    return True


def part2(data: PageUpdates) -> int:
    res = 0
    for upd in data.updates:
        if not is_update_valid(upd, data.rules):
            upd = sort_update(upd, data.rules)
            res += upd[len(upd) // 2]
    return res


def sort_update(update: Update, rules: Rules) -> Update:
    def cmp_pages(x: int, y: int, rules: Rules) -> int:
        if x in rules[y]:
            return -1
        if y in rules[x]:
            return 1
        return 0
    
    return sorted(update, key=cmp_to_key(partial(cmp_pages, rules=rules)))


def tests():
    raw_data = """
        47|53
        97|13
        97|61
        97|47
        75|29
        61|13
        75|53
        29|13
        97|29
        53|29
        61|53
        97|53
        61|29
        47|13
        75|47
        97|75
        47|61
        75|61
        47|29
        75|13
        53|13

        75,47,61,53,29
        97,61,53,29,13
        75,29,13
        75,97,47,61,53
        61,13,29
        97,13,75,29,47
    """
    
    data = parse_data(raw_data)
    for upd in data.updates[:3]:
        assert is_update_valid(upd, data.rules)
        
    for upd in data.updates[3:]:
        assert not is_update_valid(upd, data.rules)
    
    assert part1(data) == 143
    assert part2(data) == 123


if __name__ == "__main__":
    data = parse_data(load_data())

    tests()

    print("Part 1:", part1(data))
    print("Part 2:", part2(data))