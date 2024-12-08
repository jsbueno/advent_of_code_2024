from functools import lru_cache
import itertools


def parse(aa):
    bb = aa.split("\n")
    cc = []
    for line in bb:
        target, operands = line.split(":")
        operands = tuple(map(int, operands.split()))
        cc.append((int(target), operands))
    return cc

# naive part 1:
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


#@lru_cache(1_000_000)
def process_operands(target, operands, part2=False):
    if len(operands) == 1:
        return {operands[0]}
    results = set()
    aux = str(operands[0])
    for partial in process_operands(target, operands[1:]):
        if (item:=operands[0] + partial) <= target:
            results.add(item)
        if (item:=operands[0] * partial) <= target:
            results.add(item)
        # if part2 and (item:=int(str(partial) +  )) <= target:
        #    results.add(item)
    return results

def process_operands(target, operands, partial, part2=False):
    if not operands:
        return {partial,}
    operations = [
        lambda item: item + partial,
        lambda item: item * partial
    ]
    if part2:
        operations.append(lambda item: int(str(partial) + str(item)))

    #if len(operands) == 1:
    #    return set(result for operation in operations if result:=operation(operands[0]) <= target)

    results = set()

    for operation in operations:
        if (next_item:= operation(operands[0])) <= target:
            results.update(process_operands(target, operands[1:], next_item, part2=part2))

    return results



def fast_check(target, operands, part2=False):
    if target in process_operands(target, operands[1:], partial=operands[0], part2=part2):
        return target
    return 0

#aa = """..."""
#cc = parse(aa)


def part1(cc):
    result = sum(fast_check(*line) for line in cc)
    return result

def part2(cc):
    result = sum(fast_check(*line, part2=True) for line in cc)
    return result




# %time sum(int(line[0]) for line in cc if check_line(line))
# %time part1(cc)

# %time part2(cc)
