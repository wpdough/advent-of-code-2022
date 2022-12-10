import sys

f = open(sys.argv[1], "r")
lines = f.read().splitlines()

cycles = []
for line in lines:
    if line == "noop":
        cycles.append(0)
    if line.startswith("addx"):
        cycles.append(0)
        cycles.append(int(line.split()[1]))

x = 1
sum = 0
for i in range(0, len(cycles)):
    cycle = i + 1
    if (cycle - 20) % 40 == 0:
        sum += cycle * x
    x += cycles[i]
print(sum)
