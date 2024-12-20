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
BOXL, BOXR = "[]"

class Map:
    def __init__(self, raw, part2=False):
        map_, movements = raw.split("\n\n")
        self.original_map = [list(line) for line in map_.split()]

        self.movements = movements.replace("\n", "")
        self.part2 = part2
        self.reset()

    def _wideemup(self):
        # should only be called from "reset"
        new_map = []
        for line in self.map:
            new_line = []
            new_map.append(new_line)
            for item in line:
                if item == BOX:
                    new_line += [BOXL, BOXR]
                elif item == BOT:
                    new_line += [BOT, EMPTY]
                else:
                    new_line += list(item * 2)
        self.map = new_map

    def reset(self):
        self.map = deepcopy(self.original_map)
        if self.part2:
            self._wideemup()
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

        def move_part1(pos):
            nonlocal move
            if pos not in self.rect:
                return False
            if (item:=self[pos]) in  (BOX, BOXL, BOXR):
                boxes_to_push.append((pos, item))
            elif item == WALL:
                return False
            elif item == EMPTY:
                move = True
                return False
            return True

        def add_box(pos):
            item = self[pos]
            if item == BOXL:
                box = [(pos, BOXL), (pos + Directions.RIGHT, BOXR)]
            elif item == BOXR:
                box = [(pos + Directions.LEFT, BOXL), (pos, BOXR)]
            return box
        def move_part2(pos):
            nonlocal move
            last_front = box_front[-1] if box_front else None
            if not last_front:
                item = self[pos]
                if item in (BOXL, BOXR):
                    box_front.append(add_box(pos))
                    return True
                return move_part1(pos)

            new_front = []
            skip = False
            for front_pos, _ in last_front:
                if skip:
                    skip = False
                    continue
                pos = front_pos + direction
                if (item:=self[pos]) == WALL:
                    # move = False
                    return False
                elif item == BOXL:
                    new_front.extend([(pos, BOXL), (pos + Directions.RIGHT, BOXR)])
                    skip = True
                elif item == BOXR:
                    new_front.extend([(pos + Directions.LEFT, BOXL), (pos, BOXR)])

            if not new_front:
                move = True
                return False
            box_front.append(new_front)
            return True

        boxes_to_push = []
        box_front = []
        move = False
        while True:
            pos += direction
            if self.part2 and direction in (Directions.UP, Directions.DOWN):
                move_func = move_part2
            else:
                move_func = move_part1

            if not move_func(pos):
                break

        if move:
            if not self.part2 or direction in (Directions.LEFT, Directions.RIGHT):
                for box_pos, box_part in reversed(boxes_to_push):
                    self[pos] = box_part
                    pos = box_pos
            else:
                for box_line in reversed(box_front):
                    for box_pos, item in box_line:
                        new_pos = box_pos + direction
                        self[new_pos] = item
                        self[box_pos] = EMPTY
                pos = self.pos + direction
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
        return sum(100 * pos.y + pos.x for pos, item in self if item in (BOX, BOXL))


# part 1:

#mm = Map(aa)
#z = [_ for _ in mm.walk()]
#print(mm.value)

