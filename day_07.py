bb = aa.split("\n")
cc = []
for line in bb:
    target, operands = line.split(":")
    operands = tuple(map(int, operands.split()))
    cc.append((int(target), operands))

# part 1:
def check_line(line):
    target = int(line[0])
    operands = line[1]
    operator_source = "+*" * (len(operands) - 1)
    for operator_set in itertools.combinations(operator_source, len(operands) - 1):
        operand_source = iter(operands)
        value = next(operand_source)

        for operand, operator in zip(operand_source, operator_set):
            value = value + operand if operator == "+" else value * operand
        if value == target:
            return True
    return False




%time sum(int(line[0]) for line in cc if check_line(line))
