import functools
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


def sort_signals(arr):
    # bubble sort
    n = len(arr)
    swapped = False
    for i in range(n-1):
        for j in range(0, n-i-1):
            if not in_order(arr[j], arr[j + 1]):
                swapped = True
                arr[j], arr[j + 1] = arr[j + 1], arr[j]
        if not swapped:
            return


DIVIDER_PACKET_A = [[2]]
DIVIDER_PACKET_B = [[6]]

f = open(sys.argv[1], "r")

lines = filter(lambda line: len(line) > 0, f.read().splitlines())
lines = [eval(x) for x in lines]
lines.append(DIVIDER_PACKET_A)
lines.append(DIVIDER_PACKET_B)
sort_signals(lines)

print((lines.index(DIVIDER_PACKET_A) + 1)
      * (lines.index(DIVIDER_PACKET_B) + 1))
