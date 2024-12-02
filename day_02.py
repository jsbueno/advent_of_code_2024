# paste input data as a single string into "aa"

reports = [tuple(map(int, line.split())) for line in aa.split("\n")]

def check_report(report):
    prev = None
    direction = 0
    for item in report:
        if prev is None:
            prev = item
            continue
        if not (1 <= abs(difference:=(item - prev)) <= 3):
            return False
        this_direction = "increase" if difference > 0 else "decrease"
        if not direction:
            direction = this_direction
        elif this_direction != direction:
            return False
        prev = item
    return True

print(sum(check_report(report) for report in reports))
