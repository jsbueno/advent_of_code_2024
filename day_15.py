from terminedia import V2, Rect, Directions
from copy import copy, deepcopy

dir_map = {
    "^": Directions.UP,
    ">": Directions.RIGHT,
    "V": Directions.DOWN,
    "v": Directions.DOWN,
    "<": Directions.LEFT
}

BOT, WALL, BOX, EMPTY = "@#O."

class Map:
    def __init__(self, raw):
        map_, movements = raw.split("\n\n")
        self.original_map = [list(line) for line in map_.split()]

        self.movements = movements.replace("\n", "")
        self.reset()
    def reset(self):
        self.map = deepcopy(self.original_map)
        self.pos = [pos for pos, item in self if item==BOT][0]
        self.cursor = 0

    @property
    def width(self):
        return len(self.map[0])
    @property
    def height(self):
        return len(self.map)
    @property
    def rect(self):
        if not hasattr(self, "_rect"):
            self._rect = Rect(self.width, self.height)
        return self._rect
    def __repr__(self):
        return "\n".join("".join(line) for line in self.map)
    def __iter__(self):
        for y in range(0, self.height):
            for x in range(0, self.width):
                yield (pos:=V2(x, y)), self[pos]
    def __getitem__(self, pos):
        return self.map[pos[1]][pos[0]]

    def __setitem__(self, pos, value):
        self.map[pos[1]][pos[0]] = value

    def move_one(self):
        pos = self.pos
        try:
            direction = dir_map[self.movements[self.cursor]]
        except IndexError:
            raise StopIteration()
        boxes_to_push = []
        pos_hist = []
        move = False
        while True:
            pos += direction
            if pos not in self.rect: break
            if (item:=self[pos]) == BOX:
                boxes_to_push.append(pos)
            elif item == WALL:
                break
            elif item == EMPTY:
                move = True
                break
        if move:
            for box in reversed(boxes_to_push):
                self[pos] = BOX
                pos = box
            self[pos] = BOT
            self[self.pos] = EMPTY
            self.pos = pos
        self.cursor += 1

    def walk(self):
        self.reset()
        while True:
            yield
            try:
                self.move_one()
            except StopIteration:
                return

    @property
    def value(self):
        return sum(100 * pos.y + pos.x for pos, item in self if item == BOX)


# part 1:

#mm = Map(aa)
#z = [_ for _ in mm.walk()]
#print(mm.value)

