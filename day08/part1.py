import sys


def is_visible(grid: list[list[int]], treeX: int, treeY: int):
    treeHeight = grid[treeY][treeX]

    top = True
    for y in range(0, treeY):
        if grid[y][treeX] >= grid[treeY][treeX]:
            top = False

    bottom = True
    for y in range(treeY + 1, len(grid[treeY])):
        if grid[y][treeX] >= grid[treeY][treeX]:
            bottom = False

    left = True
    for x in range(0, treeX):
        if grid[treeY][x] >= treeHeight:
            left = False

    right = True
    for x in range(treeX + 1, len(grid)):
        if grid[treeY][x] >= treeHeight:
            right = False

    return top or bottom or left or right


f = open(sys.argv[1], "r")
lines = f.read().splitlines()

grid: list[list[int]] = []
for line in lines:
    trees = []
    for tree in line:
        trees.append(int(tree))
    grid.append(trees)

num_trees_visible = 0
for x in range(1, len(grid) - 1):
    for y in range(1, len(grid[x]) - 1):
        if is_visible(grid, x, y):
            num_trees_visible += 1

grid_width = len(grid[0])
grid_height = len(grid)
num_border_trees = 2 * grid_width + 2 * grid_height - 4
print(num_trees_visible + num_border_trees)
