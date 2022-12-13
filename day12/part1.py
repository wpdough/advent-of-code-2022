import sys


class Point:

    def __init__(self, x, y):
        self.x = x
        self.y = y

    def __repr__(self):
        return f"({self.x}, {self.y})"

    def __eq__(self, obj):
        return self.x == obj.x and self.y == obj.y


TRANSLATIONS = [Point(0, 1), Point(1, 0), Point(-1, 0), Point(0, -1)]


def translate(point: Point, amount: Point):
    return Point(point.x + amount.x, point.y + amount.y)


def print_grid(grid: list[str]):
    for y in range(len(grid)):
        line = ""
        for x in range(len(grid[0])):
            line += grid[y][x]
        print(line)


def find_cell(target: str):
    for y in range(len(grid)):
        for x in range(len(grid[0])):
            if grid[y][x] == target:
                return Point(x, y)
    return None


def in_bounds(grid: list[str], x: int, y: int):
    return x >= 0 and y >= 0 and x < len(grid[0]) and y < len(grid)


def valid_translation(grid: list[str], origin: Point, target: Point):
    if not in_bounds(grid, target.x, target.y):
        return False
    origin_char = grid[origin.y][origin.x]
    target_char = grid[target.y][target.x]
    if (target_char == "E"):
        target_char = "z"
    ord_diff = ord(target_char) - ord(origin_char)
    return (origin_char == "S" or target_char == "E" or ord_diff <= 1)


def get_valid_translations(grid: list[str], origin: Point):
    translations = []
    for translation in TRANSLATIONS:
        target = translate(origin, translation)
        if valid_translation(grid, origin, target):
            translations.append(target)
    return translations


def find_paths(grid: list[str], paths: list[list[Point]], current_path: list[Point]):
    current = current_path[-1]
    if grid[current.y][current.x] == "E":
        paths.append(current_path)
        return

    print(len(current_path))

    translations = get_valid_translations(grid, current)
    for translation in translations:
        if not current_path.__contains__(translation):
            offshoot = current_path.copy()
            offshoot.append(translation)
            find_paths(grid, paths, offshoot)


f = open(sys.argv[1], "r")
grid = f.read().splitlines()

origin = find_cell("S")
paths = []
find_paths(grid, paths, [origin])

paths.sort(reverse=False, key=lambda path: len(path))
print(len(paths[0]))
for point in paths[0]:
    print(point, grid[point.y][point.x])
