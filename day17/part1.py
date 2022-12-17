import sys

DEBUG = False


def debug(*args):
    if DEBUG:
        print(*args)


class CircularQueue:

    def __init__(self, list):
        self.list = list

    def next(self):
        next = self.list.pop(0)
        self.list.append(next)
        return next

    def peek(self):
        return self.list[0]


class Point:
    def __init__(self, x, y):
        self.x = x
        self.y = y

    def translate(self, x, y):
        return Point(self.x + x, self.y + y)

    def translate(self, point):
        return Point(self.x + point.x, self.y + point.y)

    def __repr__(self) -> str:
        return f"Point({self.x}, {self.y})"

    def __eq__(self, other):
        return self.x == other.x and self.y == other.y


class Grid:
    def __init__(self, width, height):
        self.grid = []
        for y in range(height):
            row = ""
            for x in range(width):
                row += "."
            self.grid.append(row)

    def get(self, x, y):
        return self.grid[y][x]

    def trim(self):
        for y in range(len(self.grid)):
            if self.grid[y] != "." * self.width():
                self.grid = self.grid[y:]
                return
        self.grid = []

    def matches(self, x, y, value):
        in_bounds = x >= 0 and x < self.width() and y >= 0 and y < self.height()
        return in_bounds and self.get(x, y) == value

    def set(self, x, y, value):
        self.grid[y] = self.grid[y][:x] + value + self.grid[y][x + 1:]

    def width(self):
        return len(self.grid[0])

    def height(self):
        return len(self.grid)

    def print(self):
        for row in self.grid:
            debug("".join(row))
        debug()

    def print_rock(self, rock, pos):
        for y in range(len(self.grid)):
            str = ""
            for x in range(len(self.grid[y])):
                if pos.x <= x < pos.x + len(rock[0]) and pos.y <= y < pos.y + len(rock) and rock[y - pos.y][x - pos.x] == "#":
                    str += "@"
                else:
                    str += self.grid[y][x]
            debug(str)
        debug()


DIR_DOWN = Point(0, 1)

DIRS = {
    ">": Point(1, 0),
    "<": Point(-1, 0),
    "^": Point(0, -1),
    "v": DIR_DOWN
}

DIR_NAMES = {
    "right": Point(1, 0),
    "left": Point(-1, 0),
    "up": Point(0, -1),
    "down": DIR_DOWN
}

ROCKS = [
    ["####"],

    [".#.",
     "###,",
     ".#."],

    ["..#",
     "..#",
     "###"],

    ["#",
     "#",
     "#",
     "#"],

    ["##",
     "##"]]

CHAMBER_WIDTH = 7
ROCK_START_POS = Point(2, 0)
ROCK_START_GAP = 3
NUM_ROCKS = 2022


def can_move_dir(grid, rock, pos, dir):
    for y in range(len(rock)):
        for x in range(len(rock[y])):
            if rock[y][x] == "#":
                if not grid.matches(pos.x + x + dir.x, pos.y + y + dir.y, "."):
                    return False
    return True


f = open(sys.argv[1], "r")
directions = CircularQueue([DIRS[dir] for dir in f.read().strip()])
rocks = CircularQueue(ROCKS)

grid = Grid(CHAMBER_WIDTH, 0)
for rock_num in range(NUM_ROCKS):
    rock = rocks.next()
    pos = ROCK_START_POS
    rock_grid = Grid(CHAMBER_WIDTH, len(rock) + ROCK_START_GAP)
    grid.grid = rock_grid.grid + grid.grid

    debug("The first rock begins falling:")
    grid.print_rock(rock, pos)

    while True:
        next_dir_name = next(
            k for k, v in DIR_NAMES.items() if v == directions.peek())
        if can_move_dir(grid, rock, pos, directions.peek()):
            pos = pos.translate(directions.next())

            dir = directions.peek()
            debug("Jet of gas pushes rock", next_dir_name, ":")
            grid.print_rock(rock, pos)

        else:
            directions.next()
            debug("Jet of gas pushes rock",
                  next_dir_name, "but nothing happens:")
            grid.print_rock(rock, pos)

        if can_move_dir(grid, rock, pos, DIR_DOWN):
            pos = pos.translate(DIR_DOWN)
            debug("Rock falls 1 unit:")
            grid.print_rock(rock, pos)
        else:
            debug("Rock falls 1 unit, causing it to come to rest:")
            break

    # commit the rock to the grid
    for y in range(len(rock)):
        for x in range(len(rock[y])):
            if rock[y][x] == "#":
                grid.set(pos.x + x, pos.y + y, "#")

    grid.trim()
    grid.print()


print(grid.height())
