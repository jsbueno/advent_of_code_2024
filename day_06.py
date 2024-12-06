
from terminedia import Directions, V2


def turn_right(self, direction):
    c = Directions
    return {c.UP: c.RIGHT, c.RIGHT: c.DOWN, c.DOWN: c.LEFT, c.LEFT: c.UP}[direction]



class Map:
    def __init__(self, text_map):
        self.data = text_map.split("\n")
        self.width = len(self.data[0])
        self.height = len(self.data)
        self.reset()
    def reset(self):
        self.seen = set()
        y, initial_row = [(i, line) for i, line in enumerate(self.data) if "^" in line][0]
        x = initial_row.index("^")
        self.pos = V2(x, y)
        self.seen.add(self.pos)
        self.direction = Directions.UP
    def __repr__(self):
        return f"<Map {self.width} x {self.height}, {len(self.seem)} visited, guard at {self.pos}"
    def __getitem__(self, pos):
        if pos[0] < 0 or pos[1] < 0:
            return None
        try:
            return self.data[pos[1]][pos[0]] == "#"
        except IndexError:
            return None


class OutOfBoard(Exception): pass

# Part1  - I have this funny feeling that just walking along the line step by step
# won't be enough for part2  (not yet seem as of this w.u.)
class WalkableMap(Map):
    def walkline(self):
        while True:
            new_pos = self.pos + self.direction
            if content:=self[new_pos] is None:
                raise OutOfBoard()
            if content:
                break
            self.pos = new_pos
            self.seen.add(new_pos)

    def walk(self):
        try:
            while True:
                self.walkline()
                self.direction = turn_right(self.direction)
                print(f"Facing {self.direction} at {self.pos}")
        except OutOfBoard:
            return len(self.seen)




    def update_pos(self):
        # override if ever intend to create animation
        pass
