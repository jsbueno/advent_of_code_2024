from terminedia import V2

DEBUG = True

MAXBUTTONS = 100

class Machine:
    COST_A = 3
    COST_B = 1

    def __init__(self, data):
        self.raw = data
        lines = []
        for line in data.split("\n"):
            _, content = line.split(": ")
            lines.append(V2(map(int, (comp.strip("XY=+, ") for comp in content.split() ))))
        self.A = lines[0]
        self.B = lines[1]
        self.prize = lines[2]

    def __repr__(self):
        return self.raw

    def find_presses(self):
        results  = []
        for i in range(MAXBUTTONS + 1):
            if (cost_a_x:=(self.prize.x - self.A.x * i)) % self.B.x !=0:
                continue

            if (self.prize.y - self.A.y * i) % self.B.y !=0:
                continue

            j = cost_a_x // self.B.x

            if not 0 <= j <=100:
                continue

            results.append(V2(i, j))
        if DEBUG and len(results) > 1:
            print(self)
            print(results)
            print()
        return results

    def find_press_cost(self):
        r = self.find_presses()
        if len(r) == 0:
            if DEBUG:
                print("No solution", self, "\n")
            return 0
        if len(r) == 1:
            p = r[0]
        else:
            p = min(r, key=lambda p: p.x * self.COST_A + p.y)
        return p.x * self.COST_A + p.y


# part 1
print(sum(Machine(d).find_press_cost() for d in aa.split("\n\n")))


