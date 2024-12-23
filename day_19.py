def doit(pattern, towels, cache=None):
    if cache is None:
        cache = {}
    if pattern in cache:
        return cache[pattern]
    count = 0
    for towel in towels:
        if not pattern.startswith(towel):
            continue
        new_pattern = pattern.removeprefix(towel)
        if new_pattern:
            count += doit(new_pattern, towels, cache)
        else:
            count += 1
    cache[pattern] = count
    return count


# aa = """..."""  #puzzle input as usual
#bb, cc = (parts:=aa.split("\n\n"))[0].split(", "), parts[1].split()

# part1:
%time sum(bool(doit(pattern, bb)) for pattern in cc)

# part2:  :-D
%time sum(doit(pattern, bb) for pattern in cc)
