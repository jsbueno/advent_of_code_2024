
def step(x):
    if x == 0:
        return 1
    if not (lenx := len(str_x := str(x))) % 2:
        return int(str_x[:lenx // 2]), int(str_x[lenx // 2:])
    return x * 2024

# part1 (not really using the cache yet)
def doit1(initial, steps=25, cache=()):
    results = []
    for number in initial:
        values = step(number)
        results.extend(values) if isinstance(values, tuple) else results.append(values)
    if steps > 1:
        return doit1(results, steps - 1, cache)
    return results


# part2
cache = {}
lencache = {}
def doit2(initial:int|list, steps=25) -> int:

    if isinstance(initial, list):
        results = []
        for item in initial:
            results.append(doit2(item, steps))
            print("plim")
        return sum(results)
    if (initial, steps) in lencache:
        return lencache[initial, steps]
    if steps == 0:
        cache[initial, 0] = [initial]
        lencache[initial, 0] = 1
        return 1
    if steps % 5:
        raise ValueError("use multiple of 5 steps")
    # get numbers at step 5
    if (initial, 5) in cache:
        numbers = cache[initial, 5]
    else:
        numbers = doit1([initial], 5)
        cache[initial, 5] = numbers
        lencache[initial, 5] = len(numbers)
    step_down = steps - 5

    results = []
    for number in numbers:
        results.append(doit2(number, step_down))
    total = sum(results)
    lencache[initial, steps] = total
    return total














# bb = list(map(int, aa.split()))
# print(len(doit1(bb)))



