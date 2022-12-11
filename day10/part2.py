import sys


def parse_cycles(lines: list[str]):
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


def print_sprite_range(sprite_range):
    sprite_range_str = ""
    for x in range(0, 40):
        sprite_range_str += "#" if sprite_range.__contains__(x) else "."
    print(sprite_range_str)


x = 1
crt_row = ""
for i in range(0, 40):
    # for i in range(0, len(cycles)):
    cycle = i + 1
    # print("Start of cycle", cycle)

    if i > 0 and i % 40 == 0:
        print(crt_row)
        crt_row = ""

    row_offset = (int((i / 40) + 0.5) - 1) * 40
    print()
    sprite_range = range(row_offset + x - 1, row_offset + x + 2)

    crt_row += "#" if sprite_range.__contains__(i) else "."
    # print("Current CRT row:", crt_row)

    if cycles[i] != 0:
        x += cycles[i]
        # print("End of cycle", cycle, ": finish executing addx",
        #       cycles[i], "(Register X is now", x, ")")
        # sprite_range = range(x - 1, x + 2)
        # print_sprite_range(sprite_range)
