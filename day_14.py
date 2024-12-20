import terminedia as TM

class V2(TM.V2):
    def __mod__(self, other):
        return type(self)(self[0] % other[0], self[1] % other[1])


class RobotBin:
    def __init__(self, map_):
        self.map = map_
        self.bins = dict()

    def __setitem__(self, pos, value):
        if pos[1] < self.map.size.y // 2:
            bin_y = 0
        elif pos[1] > self.map.size.y // 2:
            bin_y = 1
        else:
            bin_y = None

        if pos[0] < self.map.size.x // 2:
            bin_x = 0
        elif pos[0] > self.map.size.x // 2:
            bin_x = 1
        else:
            bin_x = None

        self.bins[bin_x, bin_y] = self.bins.get((bin_x, bin_y), 0) + value

    def __repr__(self):
        return self.bins

    def result(self):
        return self.bins[0, 0] * self.bins[1, 0] * self.bins[0, 1] * self.bins[1, 1]



class Bot:
    def __init__(self, map_, line):
        self.line = line
        self.map = map_
        parts = line.split()
        self.start_pos = V2(map(int, parts[0].strip("p=").split(",")))
        self.speed = V2(map(int, parts[1].strip("v=").split(",")))
    def pos_at(self, round):
        return (self.start_pos + round * self.speed) % self.map.size

    def __repr__(self):
        return self.line

class Map:
    def __init__(self, width, height):
        self.size = V2(width, height)
        self.step = 0

    def load_bots(self, data):
        lines = data.split("\n")
        self.bots = []
        for line in lines:
            self.bots.append(Bot(self, line))

    def part1(self, step=100):
        bins = RobotBin(self)
        for robot in self.bots:
            bins[robot.pos_at(step)] = 1
        return bins.result()

    def sync(self):
        self.snapshot = {}
        for bot in self.bots:
            p = bot.pos_at(self.step)
            self.snapshot[p] = self.snapshot.get(p, 0) + 1


    def __repr__(self):
        self.sync()
        lines = []
        for y in range(0, self.size.y):
            line = ""
            for x in range(0, self.size.x):
                line += "." if (b:=self.snapshot.get((x, y))) is None else str(min(b, 9))
            lines.append(line)
        return "\n".join(lines)


mm = Map(101, 103)
# mm.load_bots(aa)
# print(mm.part1(100))

# part2 -
xia = []
for step in range(0, 8000):
    if len({bot.pos_at(step) for bot in mm.bots}) == len(mm.bots):
        xis.append(step)

print(xis)
