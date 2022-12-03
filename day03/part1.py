import sys


def char_to_priority(char: str):
    if char.isupper():
        return ord(char) - 39
    return ord(char) - 97


def input_items(compart_str: str):
    items_priority = [0 for element in range(52)]
    for char in compart_str:
        idx = char_to_priority(char)
        items_priority[idx] += 1
    return items_priority


def input_compart(line: str):
    compart_a = line[0:len(line)//2]
    compart_b = line[len(line)//2:len(line)]
    return [compart_a, compart_b]


f = open(sys.argv[1], "r")
lines = f.read().splitlines()

priority_sum = 0
for line in lines:
    compartments = input_compart(line)
    compartment_a = input_items(compartments[0])
    compartment_b = input_items(compartments[1])
    for i in range(0, 52):
        if compartment_a[i] > 0 and compartment_b[i] > 0:
            priority_sum += i + 1

print(priority_sum)
