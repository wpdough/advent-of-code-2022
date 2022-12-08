import sys

f = open(sys.argv[1], "r")
lines = f.read().splitlines()

grid: list[list[int]] = []
for line in lines:
    trees = []
    for tree in line:
        trees.append(int(tree))
    grid.append(trees)


def calc_score(grid, treeX, treeY):
    treeHeight = grid[treeY][treeX]

    left = 0
    for x in reversed(range(0, treeX)):
        left += 1
        if grid[treeY][x] >= treeHeight:
            break

    right = 0
    for x in range(treeX + 1, len(grid)):
        right += 1
        if grid[treeY][x] >= treeHeight:
            break

    up = 0
    for y in reversed(range(0, treeY)):
        up += 1
        if grid[y][treeX] >= treeHeight:
            break

    down = 0
    for y in range(treeY + 1, len(grid[treeY])):
        down += 1
        if grid[y][treeX] >= treeHeight:
            break

    return up * down * left * right


high_score = 0
for x in range(0, len(grid[0])):
    for y in range(0, len(grid)):
        score = calc_score(grid, x, y)
        if score > high_score:
            high_score = score
print(high_score)
