from terminedia import V2, Directions


class Map:
    """Shamelessly copied from day 4 "TwoGrid" and then from Day 8
    """
    def __init__(self, data):
        self.data = data
        self.lines = data.split("\n")


    def __getitem__(self, pos):
        if pos not in self.rect:
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
            self._rect = Rect(self.width, self.height)
        return self._rect

    def __iter__(self):
        for y in range(self.height):
            for x in range(self.width):
                yield (pos:=V2(x, y)), self[pos]

    def __repr__(self):
        return self.data

class Map12(Map):
    def find_region(self, pos: V2, seen:set) -> "(area, perimeter)":
        if pos in seen:
            #tile in a region already accounted for:
            return (0, 0)
        to_explore_tiles = {pos,}
        region_tiles = {pos,}
        region_marker = self[pos]
        perimeter = 0
        while to_explore_tiles:
            new_tiles = set()
            for tile in to_explore_tiles:
                for direction in Directions:
                    new_tile = V2(tile + direction)
                    if self[new_tile] == region_marker:
                        if new_tile not in region_tiles:
                            new_tiles.add(new_tile)
                            region_tiles.add(new_tile)
                    else:
                        perimeter += 1
            to_explore_tiles = new_tiles
        seen.update(region_tiles)
        return len(region_tiles), perimeter


    def part1(self):
        seen = set()
        cost = 0
        for pos, content in self:
            region = self.find_region(pos, seen)
            cost += region[0] * region[1]
        return cost



