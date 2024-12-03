"""Day 3 part 1 -

Load the input into "aa" and then:
"""

import re

mul = lambda x,y: x * y

cc = re.findall(r"mul\(\d+?,\d+?\)", aa)

print(sum(eval(expr) for expr in cc))
