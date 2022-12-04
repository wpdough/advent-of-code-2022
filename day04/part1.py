import sys

f = open(sys.argv[1], "r")
lines = f.read().splitlines()


def sects_intersect(a, b):
    return (a[0] <= b[0] and a[1] >= b[1]) or (a[1] <= b[1] and a[0] >= b[0])


sum = 0
for line in lines:
    sects = [x.split("-") for x in line.split(",")]
    sects = [list(map(int, i)) for i in sects]
    if sects_intersect(sects[0], sects[1]) or sects_intersect(sects[1], sects[0]):
        sum += 1
print(sum)
