import sys
import re


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


f = open(sys.argv[1], "r")
lines = f.read().splitlines()
input = parse_input(lines)

stacks = [[] for x in input.stacks[0]]
for stack in input.stacks:
    for i in range(0, len(input.stacks[0])):
        crate = stack[i]
        if crate != "":
            stacks[i].insert(0, crate)

for move in input.moves:
    origin_idx = move[1] - 1
    target_idx = move[2] - 1
    quantity = move[0]
    for i in range(0, quantity):
        crate = stacks[origin_idx].pop()
        stacks[target_idx].append(crate)

message = ""
for stack in stacks:
    message += stack.pop()
print(message)
