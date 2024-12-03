# paste input data as a single string into "aa"

reports = [tuple(map(int, line.split())) for line in aa.split("\n")]

def check_report(report, tolerance=0):
    prev = None
    direction = None
    for item in report:
        if prev is None:
            prev = item
            continue
        if not (1 <= abs(difference:=(item - prev)) <= 3):
            return False
        this_direction = "increase" if difference > 0 else "decrease"
        if this_direction != direction:
            if not direction:
                direction = this_direction
            else:
                return False
        prev = item
    return True



#part1
print(sum(check_report(report) for report in reports))

#part2:
#print(sum(check_report(report, tolerance=1) for report in reports))
