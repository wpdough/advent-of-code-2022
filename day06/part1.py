import sys

f = open(sys.argv[1], "r")
line = f.read().strip()

for i in range(4, len(line)):
    seq = line[i-4:i]
    unique = len(set(seq)) == 4
    if unique:
        print(i)
        break
