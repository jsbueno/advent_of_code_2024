"""Day 3 part 1 -

Load the input into "aa" and then:
"""

import re

mul = lambda x,y: x * y

cc = re.findall(r"mul\(\d+?,\d+?\)", aa)

print(sum(eval(expr) for expr in cc))

# part 2:

enabled = True
do = lambda: globals().__setitem__("enabled", True) or 0
dont = lambda: globals().__setitem__("enabled", False) or 0
cc = re.findall(r"(mul\(\d+?,\d+?\)|don't\(\)|do\(\))", aa)
print(sum(eval(expr.replace("'", "")) for expr in cc))

