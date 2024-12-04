"""
Day 4.


Load the input into "aa"

"""
# % pip install terminedia

from terminedia import V2
# V2 is a 2d vector object similar to a NamedTuple
# but allowing additions. `pygame.Vector2` would also work
# here. Or, since we only need addition, it is a few


DIRECTIONS = [V2(x, y) for x in (-1, 0, 1) for y in (-1, 0, 1) if x != 0 or y != 0]

# aa = open("input.txt").read()
class TwoGrid:
    def __init__(self, data):
        self.lines = data.split("\n")
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
    def __iter__(self):
        for y in range(self.height):
            for x in range(self.width):
                yield (pos:=V2(x, y)), self[pos]
    def find_word(self, word="XMAS"):
        count = 0
        for pos, char in self:
            if char != word[0]:
                continue
            for direction in DIRECTIONS:
                current_pos = pos
                for letter in word:
                    if self[current_pos] != letter:
                        break
                    current_pos += direction
                else:
                    count += 1
        return count
    # these could be refactored to include
    # an "offset" parameter,  along with  "directions" and "required matches"
    #  but, NAH
    def find_ex(self, word="MAS"):
        target = word[len(word) // 2]
        total_count = 0
        for pos, char in self:
            if char != target:
                continue
            count = 0
            for direction in DIAGONALS:
                current_pos = pos - len(word) // 2 * direction
                for letter in word:
                    if self[current_pos] != letter:
                        break
                    current_pos += direction
                else:
                    count += 1
            if count == 2:
                total_count += 1
        return total_count

    def __repr__(self):
        return("\n".join(self.lines))

bb = TwoGrid(aa)

# part 1:
print(bb.find_word())

# part 2:
print(bb.find_ex())
