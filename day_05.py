"""
Day 5, Part 1!

As usual, load the input as a string in "aa"

"""


class Rules:
    rules: dict[int, tuple[set, set]]

    def __init__(self, rules):
        self.rules = dict()
        for rule_line in rules:
            self.update(rule_line)

    def update(self, rule_line):
        first, second = map(int, rule_line.split("|"))
        # should be after the current position
        self.rules.setdefault(first, (set(), set()))[1].add(second)
        # should be before the current position
        self.rules.setdefault(second, (set(), set()))[0].add(first)

    def convert(self, section_line):
        # make this in an indepotent way - so we can work both in part 1 and do_part2

        # note to self: next time, just parse the integers before processing!
        return [int(num) for num in section_line.split(",")] if isinstance(section_line, str) else section_line

    def check_section(self, section_line: str | list[int], mode: str="part 1") -> int | tuple[str, int]:
        section = self.convert(section_line)
        before_set = set(section)
        for pivot in reversed(section):
            before_set.remove(pivot)
            if self.rules[pivot][1].intersection(before_set):
                if mode == "part 1":
                    return 0
                return "incorrect", pivot
        if mode == "part 1":
            return section[len(section) // 2]
        return "correct", section[len(section) // 2]

    def fix_section(self, section):
        original = section
        section = section[:]
        degeneration_detector_counter = 0
        seen = set()
        while (result:=self.check_section(section, mode="part 2"))[0] == "incorrect":
            pivot = result[1]
            index = section.index(pivot)
            seen.add(tuple(section))
            for other_page in self.rules[pivot][1]:
                try:
                    other_index = section.index(other_page)
                except ValueError:
                    continue
                if other_index >= index:
                    continue
                break
                new_section = section[:]
                new_section[index] = other_page
                new_section[other_index] = pivot
                if tuple(new_section) in seen:
                    continue
                section = new_section
            degeneration_detector_counter += 1
            if degeneration_detector_counter > 30:
                raise RuntimeError(f"Things not working for {original}")
        return section[len(section) // 2]

    def do_part2(self, sections):
        filtered = []
        for section_line in sections:
            section = self.convert(section_line)
            if not self.check_section(section):
                filtered.append(section)
        print(f"attempting to fix {len(filtered)} listings")
        result = sum(self.fix_section(section) for section in filtered)




rules, sections = aa.split("\n\n")
rules = rules.split("\n"); sections = sections.split("\n")
sections = [[int(num) for num in line.split(",")] for line in sections]
r = Rules(rules)

print(sum(r.check_section(ss) for ss in sections))


