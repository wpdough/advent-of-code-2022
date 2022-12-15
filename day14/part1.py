import sys


class Point:
    def __init__(self, x: int, y: int) -> None:
        self.x = x
        self.y = y

    def __repr__(self) -> str:
        return "(" + str(self.x) + "," + str(self.y) + ")"

    def translate(self, x: int, y: int):
        return Point(self.x + x, self.y + y)

    def __eq__(self, other):
        return self.x == other.x and self.y == other.y


SAND_DROP_POINT = Point(500, 0)


class Graph:
    contents: list[str] = []
    x_offset = 0
    y_offset = 0

    def __init__(self, paths: list[list[Point]]) -> None:
        min_x = 2147000000  # max cash
        max_x = 0
        max_y = 0

        for path in paths:
            for point in path:
                if point.x < min_x:
                    min_x = point.x
                if point.x > max_x:
                    max_x = point.x
                if point.y > max_y:
                    max_y = point.y

        self.x_offset = min_x
        width = max_x - min_x + 1
        height = max_y + 1

        for y in range(height):
            line = ""
            for x in range(width):
                line += "."
            self.contents.append(line)

        for path in paths:
            for i in range(len(path) - 1):
                start = path[i]
                end = path[i + 1]
                if start.x == end.x:
                    for y in range(min(start.y, end.y), max(start.y, end.y) + 1):
                        self.set_char(Point(start.x, y), "#")
                if start.y == end.y:
                    for x in range(min(start.x, end.x), max(start.x, end.x) + 1):
                        self.set_char(Point(x, start.y), "#")
        self.set_char(SAND_DROP_POINT, "+")

    def move_sand(self, p=Point(500, 0)) -> Point:
        if not self.in_bounds(p):
            return p

        one_down = p.translate(0, 1)
        if self.space_unoccupied(one_down):
            return one_down

        one_left_down = p.translate(-1, 1)
        if self.in_abyss(one_left_down) or self.space_unoccupied(one_left_down):
            return one_left_down

        one_right_down = p.translate(1, 1)
        if self.in_abyss(one_right_down) or self.space_unoccupied(one_right_down):
            return one_right_down

        return p

    def drop_one_sand(self) -> Point:
        p = SAND_DROP_POINT
        while True:
            new_p = graph.move_sand(p)
            if new_p == p:
                break
            p = new_p
        if not self.in_abyss(p):
            self.set_char(p, "o")
        return p

    def space_unoccupied(self, p: Point):
        return self.in_bounds(p) and (self.get_char(p) != "#" and self.get_char(p) != "o")

    def in_bounds(self, p: Point):
        framed_point = p.translate(-self.x_offset, -self.y_offset)
        return framed_point.x >= 0 and framed_point.y >= 0 and framed_point.x < len(self.contents[0]) and framed_point.y < len(self.contents)

    def in_abyss(self, p: Point):
        return not self.in_bounds(p) or (p.y == len(self.contents) - 1 and self.get_char(p) == ".")

    def get_char(self, p: Point):
        return self.contents[p.y - self.y_offset][p.x - self.x_offset]

    def set_char(self, p: Point, c: str) -> None:
        x = p.x - self.x_offset
        y = p.y - self.y_offset
        self.contents[y] = self.contents[y][:x] + c + self.contents[y][x + 1:]

    def print(self) -> None:
        for row in range(len(self.contents)):
            print(row, self.contents[row])


f = open(sys.argv[1], "r")
lines = f.read().splitlines()

paths = []
for line in lines:
    path_parts = line.split(" -> ")
    path = [Point(int(part.split(",")[0]), int(part.split(",")[1]))
            for part in path_parts]
    paths.append(path)

graph = Graph(paths)

grains_dropped = 0
while True:
    grain = graph.drop_one_sand()
    if graph.in_abyss(grain):
        break
    grains_dropped += 1

print(grains_dropped)
