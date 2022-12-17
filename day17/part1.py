import sys


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
            print("".join(row))
        print()

    def print_rock(self, rock, pos):
        for y in range(len(self.grid)):
            str = ""
            for x in range(len(self.grid[y])):
                if pos.x <= x < pos.x + len(rock[0]) and pos.y <= y < pos.y + len(rock) and rock[y - pos.y][x - pos.x] == "#":
                    str += "@"
                else:
                    str += self.grid[y][x]
            print(str)
        print()


DIR_DOWN = Point(0, 1)

DIRS = {
    ">": Point(1, 0),
    "<": Point(-1, 0),
    "^": Point(0, -1),
    "v": DIR_DOWN
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
for rock_num in range(3):
    rock = rocks.next()
    pos = ROCK_START_POS
    rock_grid = Grid(CHAMBER_WIDTH, len(rock) + ROCK_START_GAP)
    grid.grid = rock_grid.grid + grid.grid
    while True:
        grid.print_rock(rock, pos)
        dir_is_unmovable_down = directions.peek(
        ) == DIR_DOWN and not can_move_dir(grid, rock, pos, DIR_DOWN)
        if dir_is_unmovable_down:
            print("Can't pull over any further!")
            break
        if can_move_dir(grid, rock, pos, directions.peek()):
            print("Dir is", directions.peek(), "and can move")
            pos = pos.translate(directions.next())
        if can_move_dir(grid, rock, pos, DIR_DOWN):
            pos = pos.translate(DIR_DOWN)
        else:
            print("Rock can't fall one down, stopping")
            break
    grid.print_rock(rock, pos)
    # commit the rock to the grid
    for y in range(len(rock)):
        for x in range(len(rock[y])):
            if rock[y][x] == "#":
                grid.set(pos.x + x, pos.y + y, "#")
    grid.trim()
    print("Comitted rock to grid")
    grid.print()

    # Notes:
    # - Collision can be detected if subset of shape is covering subset of grid
