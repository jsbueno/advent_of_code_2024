
from terminedia import Directions, V2


def turn_right(direction):
    c = Directions
    return {c.UP: c.RIGHT, c.RIGHT: c.DOWN, c.DOWN: c.LEFT, c.LEFT: c.UP}[direction]



class Map:
    def __init__(self, text_map):
        self.data = [list(line) for line in text_map.split("\n")]
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
        return f"<Map {self.width} x {self.height}, {len(self.seen)} visited, guard at {self.pos}"
    def __getitem__(self, pos):
        if pos[0] < 0 or pos[1] < 0:
            return None
        try:
            return self.data[pos[1]][pos[0]] == "#"
        except IndexError:
            return None

    def __setitem__(self, pos, val):
        self[pos[1]][pos[0] = val


class OutOfBoard(Exception): pass

# Part1  - I have this funny feeling that just walking along the line step by step
# won't be enough for part2  (not yet seem as of this w.u.)
class WalkableMap(Map):
    def walkline(self):
        while True:
            new_pos = self.pos + self.direction
            if (content:=self[new_pos]) is None:
                raise OutOfBoard()
            if content:
                break
            self.update_pos(new_pos)
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


# Part2  - Maybe it will be simpler than I feared -
# but let's just make things "WET" at this exact point!

# or rather,,,let's not. Once I had the
# hook for every step set up already,
# I will just use that one.


class LoopableMap(WalkableMap):
    def reset(self):
        super().reset()
        self.trace = dict()
        self.obstacles = set()
        self.trace[self.pos] = Directions.UP

    def doit_part2(self):
        self.walk()
        return len(self.obstacles)

    def look_right(self, direction, new_pos, new_obs):
        # if we meet a path already traced, and on the same direction to our right:
        direction = turn_right(direction)
        pos = new_pos

        seen_here = dict()
        try:
            self[new_obs] = "#"
            while self[pos] is not None:
                while self[pos] is False:
                    if direction in seen_here.get(pos, set()):
                        # we are in a loop while looking right!
                        return False
                    seen_here.setdefault(pos, set()).add(direction)
                    pos = pos + direction
                    if self.trace.get(pos) == direction:
                        return True
                if self[pos]:
                    # step back, turn right and keep looking
                    pos = pos - direction
                    direction = turn_right(direction)
                    if self.trace.get(pos) == direction:
                        return True
        finally:
            self[new_obs] = "."

        return False


    def update_pos(self, new_pos):
        # animation hook re-purposed for shamelessly solving part2
        if self[obs_pos:=(new_pos + self.direction)] is False:
            if new_pos in self.trace and self.trace[new_pos] == turn_right(self.direction):
            # I really thought it would be this simple!  :-p  -
                self.obstacles.add(obs_pos)
            elif self.look_right(self.direction, new_pos ,obs_pos):
            # but no, we should look right!
                self.obstacles.add(obs_pos)
        self.trace[new_pos] = self.direction
