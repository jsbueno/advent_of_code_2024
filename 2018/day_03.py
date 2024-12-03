class Rect:
    def __init__(self, line):
        self.id, coords = line.split(" @ ")
        xy, wh = coords.split(": ")
        self.x, self.y = map(int, xy.split(","))
        self.w, self.h = map(int, wh.split("x"))
    def __repr__(self):
        return f"{self.id} @ {self.x}, {self.y}: {self.w}, {self.h}"
    def __contains__(self, coord):
        x, y = coord
        return self.x <= x < self.x + self.w and self.y <= y < self.y + self.h
    def __iter__(self):
        for y in range(self.y, self.y + self.h):
            for x in range(self.x, self.x + self.w):
                yield (x, y)

bb = aa.split("\n")
cc = [Rect(line) for line in bb]

# part1:
def doit(patches):
    occupied = set()
    already_counted = set()
    used = 0
    for rect in patches:
        tiles = set(rect)
        intersections = tiles.intersection(occupied)
        intersections -= already_counted
        already_counted.update(intersections)
        used += len(intersections)
        occupied.update(tiles)
    return used

print(f"AoC 2018, day 3, part 1: {doit(cc)}")
# part2:

from collections import Counter

def doit_part2(patches):
    occupied = Counter()
    # already_counted = set()
    used = 0
    for rect in patches:
        tiles = set(rect)
        intersections = tiles.intersection(occupied)
        occupied.update(tiles)
        # intersections -= already_counted
        # already_counted.update(intersections)
        # used += len(intersections)
    for rect in patches:
        if all(occupied[coord] == 1 for coord in rect):
            return rect

print(f"AoC 2018, day 3, part 2: {doit_part2(cc)}")
