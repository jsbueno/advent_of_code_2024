from terminedia import V2, Directions, Rect


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

class Continue3(Exception): pass

class Map12(Map):

    def coalesce_perimeters(self, perimeters: list[set[tuple[V2, str]]]) -> int:
        if DEBUG:
            print(len(perimeters), end=" -> ")

        groupped = True
        while groupped:
            if DEBUG:
                print("\n", perimeters)
            groupped = False
            to_remove = []
            for i, peri_1 in enumerate(perimeters):
                try:
                    for peri_2 in perimeters[i + 1:]:
                        for item in peri_1:
                            if (any(
                                 abs(item[0].x - item_2[0].x) == 1 and item[1] == item_2[1] == "horizontal" or
                                 abs(item[0].y - item_2[0].y) == 1 and item[1] == item_2[1] == "vertical"
                                    ) for item_2 in peri_2):
                                peri_2.update(peri_1)
                                groupped = True
                                to_remove.append(i)
                                raise Continue3
                except Continue3:
                    pass
            if DEBUG:
                print(to_remove)
            for j in reversed(to_remove):
                del perimeters[j]
        if DEBUG:
            print(len(perimeters), "\n")
        return len(perimeters)

    def find_region(self, pos: V2, seen:set, part2=False) -> "(area, perimeter, sides)":
        if pos in seen:
            #tile in a region already accounted for:
            return (0, 0, 0)
        to_explore_tiles = {pos,}
        region_tiles = {pos,}
        region_marker = self[pos]
        perimeter = 0
        perimeters: list[set[tuple[v2, str]]] = []
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
                        perimeters.append(
                            {(
                                (tile + ((1, 0) if direction == (1, 0) else (0, 1) if direction == (0, 1) else (0, 0))),
                                "horizontal" if direction  in ((0, 1), (0, -1)) else "vertical"
                            ),}
                        )
            to_explore_tiles = new_tiles
        seen.update(region_tiles)
        sides = 0
        if part2:
            sides = self.coalesce_perimeters(perimeters)

        return len(region_tiles), perimeter, sides


    def calc_cost(self, part):
        seen = set()
        cost = 0
        for pos, content in self:
            region = self.find_region(pos, seen, part=="part2")
            cost += region[0] * (region[1] if part == "part1" else region[2])
        return cost

    def part1(self):
        return self.calc_cost("part1")

    def part2(self):
        return self.calc_cost("part2")


