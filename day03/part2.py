import sys


def char_to_priority(char: str):
    if char.isupper():
        return ord(char) - 39
    return ord(char) - 97


def input_items(compart_str: str):
    items_priority = [0 for i in range(52)]
    for char in compart_str:
        idx = char_to_priority(char)
        items_priority[idx] += 1
    return items_priority


f = open(sys.argv[1], "r")
lines = f.read().splitlines()

priority_sum = 0
for i in range(0, len(lines) // 3):
    # split input into groups of 3 lines
    group = lines[i*3:i*3+3]
    # map backpack into a list of item counts, with index being item priority base 0
    backpacks = list(map(lambda backpack: input_items(backpack), group))
    # for each possible priority
    for j in range(0, 52):
        # if all backpacks contain item
        if (backpacks[0][j] > 0 and backpacks[1][j] > 0 and backpacks[2][j] > 0):
            # tally the item's priority value (it's index + 1)
            priority_sum += j + 1
print(priority_sum)
