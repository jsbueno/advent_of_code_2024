"""
Day 5, Part 1!

As usual, load the input as a string in "aa"

"""


class Rules:
    def __init__(self, rules):
        self.rules = dict()
        for rule_line in rules:
            self.update(rule_line)
    def update(self, rule_line):
        first, second = map(int, rule_line.split("|"))
        self.rules.setdefault(first, [set(), set()])[1].add(second)
        self.rules.setdefault(second, [set(), set()])[0].add(first)
    def check_section(self, section_line):
        section = [int(num) for num in section_line.split(",")]
        before_set = set(section)
        for pivot in reversed(section):
            before_set.remove(pivot)
            if self.rules[pivot][1].intersection(before_set):
                return 0
        return section[len(section) // 2]
r = Rules(rules)
sum(r.check_section(ss) for ss in sections)
rules, sections = aa.split("\n\n")
rules = rules.split("\n"); sections = sections.split("\n")
r = Rules(rules)

print(sum(r.check_section(ss) for ss in sections))


