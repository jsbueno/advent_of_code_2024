from terminedia import V2, Rect

class Map:
    """Shamelessly copied from day 4 "TwoGrid"
    """
    def __init__(self, data):
        self.data = data
        self.lines = data.split("\n")
        self.frequencies = set(data)
        self.frequencies.remove(".")
        self.frequencies.remove("\n")

    def __getitem__(self, pos):
        if 0 > pos[0] or pos[0] >= self.width or 0 > pos[1] or pos[1] >= self.height:
            return None
        return self.lines[pos[1]][pos[0]]
    @property
    def width(self):
        return len(self.lines[0])
    @property
    def height(self):
        return len(self.lines)
    @property
    def rect(self):
        if not hasattr(self, "_rect"):
            self.rect = Rect(self.width, self.height)
        retur self._rect

    def __iter__(self):
        for y in range(self.height):
            for x in range(self.width):
                yield (pos:=V2(x, y)), self[pos]

    def find_antennas(self):
        self.antennas = antennas = dict()
        for pos, item in self:
            if item != ".":
                antennas.setdefault(item, set()).add(pos)


    def part1(self):
        self.find_antennas()
        nodes = set()
        for frequency, antennas in self.antennas.items():
            for antenna in antennas:
                for other_antenna in antennas:
                    if other_antenna is antenna:
                        continue
                    node_pos = antenna + (antenna - other_antenna)
                    if node_pos in self.rect:
                        nodes.add(node_pos)
        return len(nodes)

    def __repr__(self):
        return self.data

