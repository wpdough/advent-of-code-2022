import sys

input = open(sys.argv[1], "r").read()
elves = input.split("\n\n")

result = list(map(lambda asdf: sum(map(lambda str: int(str), filter(lambda item: item != '',
                                                                    asdf.split("\n")))), elves))
result.sort()
result.reverse()

print(result[0])
