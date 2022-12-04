import sys
import re

f = open(sys.argv[1], "r")
lines = f.read().splitlines()

sum = 0
for line in lines:
    coords = [int(str) for str in re.split(r"[,-]", line)]
    sectA = range(coords[0], coords[1] + 1)
    sectB = range(coords[2], coords[3] + 1)
    if len(set(sectA).intersection(sectB)):
        sum += 1

print(sum)
