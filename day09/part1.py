import sys

f = open(sys.argv[1], "r")
lines = f.read().splitlines()


def calc_translation(direction: str):
    amount = -1 if direction == "L" or direction == "D" else 1
    if direction == "L" or direction == "R":
        return (amount, 0)
    return (0, amount)


def is_tail_adjacent(head_loc, tail_loc):
    x_dist = abs(head_loc[0] - tail_loc[0])
    y_dist = abs(head_loc[1] - tail_loc[1])
    if x_dist == 1 and y_dist == 1:
        return True
    elif x_dist == 1 and y_dist == 0:
        return True
    elif x_dist == 0 and y_dist == 1:
        return True
    elif x_dist == 0 and y_dist == 0:
        return True
    return False


def calc_tail_translation(head_loc, tail_loc):
    x_dist = abs(head_loc[0] - tail_loc[0])
    y_dist = abs(head_loc[1] - tail_loc[1])
    if x_dist == 2 and y_dist == 0:
        amount = 1 if head_loc[0] > tail_loc[0] else -1
        return (amount, 0)
    elif x_dist == 0 and y_dist == 2:
        amount = 1 if head_loc[1] > tail_loc[1] else -1
        return (0, amount)
    elif x_dist == 2 and y_dist == 1:
        amountX = 1 if head_loc[0] > tail_loc[0] else -1
        amountY = 1 if head_loc[1] > tail_loc[1] else -1
        return (amountX, amountY)
    elif x_dist == 1 and y_dist == 2:
        amountX = 1 if head_loc[0] > tail_loc[0] else -1
        amountY = 1 if head_loc[1] > tail_loc[1] else -1
        return (amountX, amountY)
    return (0, 0)


head_loc = (0, 0)
tail_loc = (0, 0)
tail_locs = []

for line in lines:
    direction = line.split()[0]
    distance = int(line.split()[1])
    for i in range(0, distance):
        translate = calc_translation(direction)
        head_loc = (head_loc[0] + translate[0], head_loc[1] + translate[1])
        if not is_tail_adjacent(head_loc, tail_loc):
            tail_translate = calc_tail_translation(head_loc, tail_loc)
            tail_loc = (tail_loc[0] + tail_translate[0],
                        tail_loc[1] + tail_translate[1])
        tail_locs.append(tail_loc)

unique_tail_locs = len(set(tail_locs))
print(unique_tail_locs)
