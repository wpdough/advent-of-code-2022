import sys


def parse_cycles(lines):
    cycles = []
    for line in lines:
        if line == "noop":
            cycles.append(0)
        if line.startswith("addx"):
            cycles.append(0)
            cycles.append(int(line.split()[1]))
    return cycles


f = open(sys.argv[1], "r")
lines = f.read().splitlines()
cycles = parse_cycles(lines)

x = 1
crt_row = ""
for i in range(0, len(cycles)):
    cycle = i + 1

    if i > 0 and i % 40 == 0:
        print(crt_row)
        crt_row = ""

    row_offset = i - i % 40
    sprite_range = range(row_offset + x - 1, row_offset + x + 2)

    crt_row += "#" if sprite_range.__contains__(i) else "."

    if cycles[i] != 0:
        x += cycles[i]

print(crt_row)
