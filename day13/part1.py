import sys


def in_order(left, right):
    if type(left) == int and type(right) == int:
        if left < right:
            return True
        if left > right:
            return False

    if type(left) == list and type(right) == list:

        num_comparisons = min(len(left), len(right))
        for i in range(num_comparisons):
            result = in_order(left[i], right[i])
            if not result == None:
                return result
        left_will_run_out = len(left) < len(right)
        if left_will_run_out:
            return True
        right_will_run_out = len(right) < len(left)
        if right_will_run_out:
            return False

    if type(left) == int and type(right) == list:
        return in_order([left], right)
    if type(right) == int and type(left) == list:
        return in_order(left, [right])


f = open(sys.argv[1], "r")
lines = f.read().split("\n\n")

sum = 0
for i in range(len(lines)):
    line = lines[i]
    left = eval(line.split("\n")[0])
    right = eval(line.split("\n")[1])
    if (in_order(left, right)):
        sum += i + 1
print(sum)
