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
class Continue4(Exception): pass

class Map12(Map):

    def coalesce_perimeters(self, perimeters: list[set[tuple[V2, "axis", "side"]]]) -> int:
        if DEBUG:
            print(len(perimeters), end=" -> ")

            #breakpoint()
        groupped = True
        while groupped:
            if DEBUG:
                print("\n", perimeters)
            groupped = False
            to_remove = []
            for i, peri_1 in enumerate(perimeters):
                try:
                    for peri_2 in perimeters[i + 1:]:
                        try:
                            for pos_1, direction_1, side_1 in peri_1:
                                for pos_2, direction_2, side_2 in peri_2:
                                    difference = pos_1 - pos_2
                                    if (
                                        side_2 != side_1 or direction_1 != direction_2 or
                                        direction_1 == "horizontal" and pos_1.y != pos_2.y or
                                        direction_1 == "vertical" and pos_1.x != pos_2.x

                                    ):
                                        raise Continue3()
                                    if (
                                            (direction_1 == "horizontal" and difference in (Directions.RIGHT, Directions.LEFT)) or
                                            (direction_1 == "vertical" and difference in (Directions.UP, Directions.DOWN))
                                    ):
                                        if DEBUG:
                                            print (f"merging {peri_1} into {peri_2}")
                                        peri_2.update(peri_1)
                                        groupped = True
                                        to_remove.append(i)
                                        raise Continue4
                        except Continue3:
                            pass
                except Continue4:
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
        perimeters: list[set[tuple[v2, str, str]]] = []
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
                                "horizontal" if direction  in ((0, 1), (0, -1)) else "vertical",
                                "inside" if direction in ((1, 0), (0, 1)) else "outside"
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


