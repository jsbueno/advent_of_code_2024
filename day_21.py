from terminedia import V2, Directions
from functools import cached_property
from operator import lt, gt
from itertools import cycle

dirmap = {
    "^": Directions.UP,
    "<": Directions.LEFT,
    ">": Directions.RIGHT,
    "v": Directions.DOWN
}

def reverse_dict(dct):
    return {v: k for k,v in dct.items()}

mapdir = reverse_dict(dirmap)

class KeyPad:

    layout = {
        pos: key for pos, key in zip(
            (V2(x, y) for y in range(4) for x in range(3)),
            "789456123.0A"
        )
    }

    def __init__(self, target_seq):
        self.target_seq = target_seq

    @cached_property
    def colayout(self):
        return reverse_dict(self.layout)

    @cached_property
    def width(self):
        return max(self.layout.keys(), key=lambda k: k[0])[0] + 1

    @cached_property
    def height(self):
        return max(self.layout.keys(), key=lambda k: k[1])[1] + 1

    def find_seq(self):
        seq = ""
        current_coord = self.colayout["A"]

        # one of the puzzle's key-points is that
        # if a keypress can be repeated, it should be
        # repeated
        # (this way, the robot on the upper-layer
        # control pad just stays fixed at "A")

        seek_source = cycle((
            ("^", lt, 1),
            ("v", gt, 1),
            ("<", lt, 0),
            (">", gt, 0),
        ))

        for item in self.target_seq:
            target_coord = self.colayout[item]
            key_at_pad, operator, axis = next(seek_source)
            while current_coord != target_coord:
                new_coord = current_coord + dirmap[key_at_pad]
                if (
                        operator(target_coord[axis], current_coord[axis]) and
                        self.layout[new_coord] != "."
                ):
                    current_coord = new_coord
                    seq += key_at_pad
                else:
                    # look what other directions are needed
                    # just if the current direction won't be needed anymore:
                    key_at_pad, operator, axis = next(seek_source)

                # else:
                # ... for both layouts, gap is always
                # at one cormer and we can't get "stuck"
                # behind a gap. so, nothing to do in "else"

            seq += "A"
        return seq

    def __repr__(self):
        return "\n\n".join("   ".join(self.layout[col, row]  for col in range(self.width))   for row in range(self.height))

class ControlPad(KeyPad):

    layout = {
        pos: key for pos, key in zip(
            (V2(x, y) for y in range(2) for x in range(3)),
            ".^A<v>"
        )
    }


def find_seqs(open_door_seq):
    # really, problem must be read to make sense of this:
    #global radiation_seq
    vacuum_seq = KeyPad(open_door_seq).find_seq()
    radiation_seq = ControlPad(vacuum_seq).find_seq()
    #print(radiation_seq)
    icy_seq = ControlPad(radiation_seq).find_seq()
    #historian_seq = ControlPad(icy_seq).find_seq()
    return icy_seq

def part1(data):
    return sum(int(line.strip("A")) * len(find_seqs(line)) for line in data.split("\n"))
