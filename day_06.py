from terminedia import Directions, V2

from copy import copy

def turn_right(direction):
    c = Directions
    return {c.UP: c.RIGHT, c.RIGHT: c.DOWN, c.DOWN: c.LEFT, c.LEFT: c.UP}[direction]



class Map:
    def __init__(self, text_map):
        self.data = [list(line) for line in text_map.split("\n")]
        self.width = len(self.data[0])
        self.height = len(self.data)
        y, initial_row = [(i, line) for i, line in enumerate(self.data) if "^" in line][0]
        x = initial_row.index("^")
        self.initial_pos = V2(x,y)
        self.reset()

    def reset(self):
        self.seen = dict()
        self.pos = self.initial_pos
        self.seen[self.pos] = {Directions.UP,}
        self.direction = Directions.UP
        self.loop_count = 0
        self.recurse_count = 0
        self.obstacles = set()

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
        self.data[pos[1]][pos[0]] = val


class OutOfBoard(Exception): pass
class InLoop(Exception): pass

# Part1  - I have this funny feeling that just walking along the line step by step
# won't be enough for part2  (not yet seem as of this w.u.)
class WalkableMap(Map):
    def __init__(self, text_map, put_obstacles=False):
        super().__init__(text_map)
        self.put_obstacles = put_obstacles


    def walkline(self):
        while True:
            new_pos = self.pos + self.direction
            if (content:=self[new_pos]) is None:
                raise OutOfBoard()
            if content:
                break
            if self.put_obstacles:
                self.update_pos(new_pos)
            if self.direction in self.seen.get(new_pos, set()):
                raise InLoop()
            self.pos = new_pos
            self.seen.setdefault(new_pos, set()).add(self.direction)

    def walk(self):
        try:
            while True:
                self.walkline()
                self.direction = turn_right(self.direction)
                #print(f"Facing {self.direction} at {self.pos}")
        except OutOfBoard:
            return len(self.seen)

    def update_pos(self, new_pos):
        # override if ever intend to create animation
        if self[obst_pos:= (new_pos + self.direction)] is not False or obst_pos in self.obstacles:
            return
        try:
            original = self[obst_pos]
            self[obst_pos] = "#"
            modified_map = copy(self)
            modified_map.put_obstacles = False
            modified_map.reset()
            #modified_map.seen = copy(self.seen)
            self.recurse_count += 1
            if self.recurse_count % 50 == 0:
                print(f"inspecting possible obstacle # {self.recurse_count}")
            modified_map.walk()

        except InLoop:
            self.loop_count += 1
            self.obstacles.add(obst_pos)
        finally:
            self[obst_pos] = original
            del modified_map

    def part2(self):
        self.put_obstacles = True
        self.walk()
        return self.loop_count
