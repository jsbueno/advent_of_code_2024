# paste input data as a single string into "aa"

reports = [tuple(map(int, line.split())) for line in aa.split("\n")]

def check_report(report):
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


def check_report2(report):
    if check_report(report):
        return True
    for i in range(len(report)):
        r2 = list(report)
        del r2[i]
        if check_report(r2):
            return True
    return False

#part1
print(sum(check_report(report) for report in reports))

#part2:
print(sum(check_report2(report) for report in reports))
