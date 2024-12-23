from terminedia import V2, Directions, Rect

MAXINT = 2 ** 31
DEBUG = False

class Map:
    def __init__(self, size, data, tick=0):
        self.rect = Rect(size)
        self.data = [V2(eval(line)) for line in data.split()]
        self.tick = tick
    @property
    def tick(self):
        return self._tick
    @tick.setter
    def tick(self, value):
        self.fallen = set(self.data[0:value])
        self._tick = value
    def __getitem__(self, pos):
        if not pos in self.rect:
            return None
        return pos in self.fallen
    def __repr__(self):
        lines = []
        for row in range(self.rect.height):
            line = ""
            for col in range(self.rect.width):
                line += "#" if (row, col) in self.fallen else "."
            lines.append(line)
        return "\n".join(lines)

    def walk(self, start=(0,0), end=None):
        if end is None:
            end = self.rect.width_height - (1,1)
        start = V2(start)
        distances = {start: 0}
        self.distances = distances  # allow some introspection
        heads = [start,]
        while heads:
            new_heads = []
            for head in heads:
                current = distances[head]
                next_dist = current + 1
                for direction in Directions:
                    pos = head + direction
                    if self[pos] is not False:
                        continue
                    if distances.get(pos, MAXINT) > next_dist:
                        distances[pos] = next_dist
                        new_heads.append(pos)
            heads = new_heads
        if DEBUG:
            print(distances)
        return distances[end]


m = Map((7,7), aa1)
m
m.tick=12


### part2 will easily be printed by brute-force (less than 60s):
#for t in range(1024, len(mm.data)):
    #try:
        #mm.tick = t
        #mm.walk()
    #except KeyError:
        #print(t, mm.data[t - 1])
        #break

# otherwise, just do a binary search on the breaking byte,
# to get back into ms range
