import sys
import re

f = open(sys.argv[1], "r")
lines = f.read().splitlines()


def parse_stack_line(line):
    vals = []
    str = line
    while (len(str) > 0):
        val = str[0:min(4, len(str))]
        vals.append(re.sub(r'[\s\[\]]', '', val))
        str = str[4:len(str)]
    return vals


for line in lines:
    if "[" in line:
        print(parse_stack_line(line))
