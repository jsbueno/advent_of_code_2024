
OPCODES = {
    0: "adv",
    1: "bxl",
    2: "bst",
    3: "jnz",
    4: "bxc",
    5: "out",
    6: "bdv",
    7: "cdv",
}

DEBUG = False

class ReadableOp:
    def __init__(self, callable):
        self.callable = callable
    def __call__(self, *a, **k):
        return self.callable(*a, **k)
    def __repr__(self):
        return self.callable.__name__.upper()

class Computer:
    def __init__(self, raw):
        self.raw = raw
        self.inst_opcodes = [ReadableOp(getattr(self, OPCODES[op])) for op in range(8)]
        self.reset()

    def reset(self):
        init, program = self.raw.split("\n\n")
        for register, line in zip("ABC", init.split("\n")):
            value = int(line.split(": ")[1])
            setattr(self, register, value)
        self.pc = 0
        self.tick = 0
        self.bytecode = [int(opcode) for opcode in program.split(": ")[1].split(",")]
        self.output = []

    def program(self, offset=0):
        return "\n".join(f"{self.inst_opcodes[self.bytecode[i]]} {self.bytecode[i + 1: i+2]}" for i in range(offset, len(self.bytecode), 2))

    def __repr__(self):
        registers = f"{self.A=}, {self.B=}, {self.C=}"
        return f"{registers}\n\n{self.program(0)}"

    def run(self):
        while self.pc < len(self.bytecode):
            self.exec_one()
        print()

    def exec_one(self):
        instr = self.inst_opcodes[bc:=self.bytecode[self.pc]]
        instr()
        if bc != 3: #  != "JNZ":
            self.pc += 2
        self.tick += 1
        if DEBUG and not self.tick %50:
            print ("\n", self.tick)

    @property
    def op(self):
        op = self.bytecode[self.pc + 1]
        if op <= 3:
            return op
        return getattr(self, chr(65 + op - 4))

    def adv(self):
        self.A = self.A // 2 ** self.op

    def bxl(self):
        self.B ^= self.bytecode[self.pc + 1]

    def bst(self):
        self.B = self.op % 8

    def jnz(self):
        val = (self.pc + 2) if self.A == 0 else self.bytecode[self.pc + 1]
        self.pc = val

    def bxc(self):
        self.B ^= self.C

    def out(self):
        val = self.op % 8
        self.output.append(val)
        print(val, end=",")

    def bdv(self):
        self.B = self.A // 2 ** self.op

    def cdv(self):
        self.C = self.A // 2 ** self.op

