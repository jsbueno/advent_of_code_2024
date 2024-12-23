from terminedia import V2, Directions, Rect
from collections import Counter

DEBUG = False

WALL = "#"
TRACK = "."

class Map:
    """Shamelessly copied from day 4 "TwoGrid" and then from Day 8 and them Day 12
    """
    def __init__(self, data, part2=False, shortcut_dist = 20):
        self.data = data
        self.part2 = part2
        self.shortcut_dist = shortcut_dist
        self.reset()

    def reset(self):
        self.lines = []
        for y, line in enumerate(self.data.split("\n")):
            if (x:=line.find("S")) != -1:
                line = line.replace("S", ".")
                self.start = V2(x, y)
            if (x:=line.find("E")) != -1:
                line = line.replace("E", ".")
                self.end = V2(x, y)
            self.lines.append(list(line))
        self.distances = {}
        self.shortcuts = Counter()

    def __getitem__(self, pos):
        if pos not in self.rect:
            return None
        return self.lines[pos[1]][pos[0]]

    @property
    def rect(self):
        if not hasattr(self, "_rect"):
            self._rect = Rect(len(self.lines[0]), len(self.lines))
        return self._rect

    def __iter__(self):
        for y in range(self.height):
            for x in range(self.width):
                yield (pos:=V2(x, y)), self[pos]

    def walk(self):
        self.reset()
        heads = [self.start]
        self.distances[self.start] = 0
        while heads:
            new_heads = []
            for head in heads:
                dist  = self.distances[head] + 1
                for direction in Directions:
                    new_pos = head + direction
                    if self[new_pos] != TRACK:
                        continue
                    if self.distances.get(new_pos, 2**31) > dist:
                        self.distances[new_pos] = dist
                        new_heads.append(new_pos)
            heads = new_heads

    def find_shortcuts(self):
        self.walk()
        heads = [self.end]
        if self.part2:
            s = self.shortcut_dist
            #kernel = {V2(coord) for coord in product(range(-s, s + 1), repeat=2) if 2 <=  abs(coord[0]) + abs(coord[1])}
            kernel = {V2(coord) for coord in product(range(-s, s + 1), repeat=2) if 2 <=  abs(coord[0]) + abs(coord[1]) <= s}
        else:
            kernel = [d * 2 for d in Directions]

        while heads:
            new_heads = []
            for head in heads:
                current_distance = self.distances[head]
                for component in kernel:
                    cheated_pos = head + component
                    manh = abs(component.x) + abs(component.y)
                    if (new_dist:=self.distances.get(cheated_pos, 2 ** 31))< current_distance - manh:
                        self.shortcuts[current_distance - new_dist - manh] += 1
                for direction in Directions:
                    if self.distances.get(new_pos:=head + direction) == current_distance - 1:
                        new_heads.append(new_pos)
            heads = new_heads

    def __repr__(self):
        return self.data

# aa = """..."""
## part1:
# mm = Map(aa)

#mm.find_shortcuts()
#print(sum(value for k, value in mm.shortcuts.items() if k >= 100))


## part2:
# mm = Map(aa, part2=True)

#mm.find_shortcuts()  # takes < 15s
#print(sum(value for k, value in mm.shortcuts.items() if k >= 100))
