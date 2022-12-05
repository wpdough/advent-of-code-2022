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


def parse_move_line(line):
    line = line.replace("move ", "")
    line = line.replace(" from", "")
    line = line.replace(" to", "")
    return [int(num) for num in line.split(" ")]


class Input:
    def __init__(self, stacks, moves):
        self.stacks = stacks
        self.moves = moves


def parse_input(lines):
    stacks = []
    moves = []
    for line in lines:
        if "[" in line:
            stacks.append(parse_stack_line(line))
        if "move" in line:
            moves.append(parse_move_line(line))
    return Input(stacks, moves)


input = parse_input(lines)
print(input.stacks)
print(input.moves)
