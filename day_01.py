# part 1

# put raw input into "aa"

lines = [tuple(map(int, line.split())) for line in aa.split("\n")]
list1, list2 = zip(*lines)
list1 = sorted(list1); list2 = sorted(list2)
distances = [abs(item1 - item2) for item1, item2 in zip(list1, list2)]
print(sum(distances))

# part2


from collections import Counter
counted = Counter(list2)
#sum(item * counted.get(item, 0) for item in list1     )
# but first, we rather check if "list1"  actually has only
# unique entries - just compare the results of:
len(list1), len(set(list1))
len(list2), len(set(list2))
# now the final result
print(sum(item * counted.get(item, 0) for item in list1))


