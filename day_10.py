from terminedia import V2, Directions

class Map:
    def __init__(self, data):
        self.raw_data = data
        self.data = [[int(digit) for digit in line] for line in  data.split()]
        self.width = len(self.data[0])
        self.height = len(self.data)
    def __getitem__(self, pos):
        if pos[0] < 0 or pos[0] >= self.width or pos[1] < 0 or pos[1] >= self.height:
            return -1
        return self.data[pos[1]][pos[0]]
    def __iter__(self):
        for y in range(self.height):
            for x in range(self.width):
                yield (pos:=V2(x, y)), self[pos]
    def __repr__(self):
        return self.raw_data
    def find_heads(self):
        return [pos for pos, height in self if height == 0]
    def walk(self, start_pos):
        results = []
        branches = [start_pos,]
        summits = 0
        while branches:
            new_branches = []
            if DEBUG:
                print(branches)
            for pos in branches:
                current_height = self[pos]
                for direction in Directions:
                    if self[new_pos:=(pos + direction)] != current_height + 1:
                        continue
                    if current_height == 8:
                        summits += 1
                        if DEBUG:
                            print(new_pos)
                        continue
                    new_branches.append(new_pos)
            branches = new_branches
        return summits
    def part1(self):
        return sum(self.walk(head) for head in self.find_heads())
