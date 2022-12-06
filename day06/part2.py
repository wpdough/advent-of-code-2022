import sys

f = open(sys.argv[1], "r")
line = f.read().strip()

for i in range(14, len(line)):
    seq = line[i-14:i]
    unique = len(set(seq)) == 14
    if unique:
        print(i)
        break
