import sys


class Point:

    def __init__(self, x, y):
        self.x = int(x)
        self.y = int(y)

    def __repr__(self) -> str:
        return f"x={self.x}, y={self.y}"

    def __eq__(self, __o: object) -> bool:
        return self.x == __o.x and self.y == __o.y

    def __hash__(self) -> int:
        return hash((self.x, self.y))


class Sensor:

    def __init__(self, loc, beacon):
        self.loc = loc
        self.beacon = beacon

    def from_line(line: str):
        line = line.replace("Sensor at x=", "").replace("y=", "").replace(
            "closest beacon is at x=", "").replace("y=", "").replace(":", "").replace(",", "")
        loc = Point(int(line.split()[0]), int(line.split()[1]))
        beacon = Point(
            int(line.split()[2]), int(line.split()[3]))
        return Sensor(loc, beacon)

    def beacon_dist(self):
        return int(abs(self.loc.x - self.beacon.x) +
                   abs(self.loc.y - self.beacon.y))

    def polygon_width(self, y: int):
        dist = self.beacon_dist()
        min_y = self.loc.y - dist
        max_y = self.loc.y + dist
        if min_y <= y <= max_y:
            y_offset = abs(self.loc.y - y)
            w = (2 * dist + 1) - 2 * y_offset
            return w
        return 0

    def beacon_x_range_exclusive(self, y: int):
        if (self.polygon_width(y) > 0):
            width = self.polygon_width(y)
            offset = (width - 1) / 2
            start = int(self.loc.x - offset)
            end = int(self.loc.x + offset + 1)
            return (start, end)
        return None

    def __repr__(self) -> str:
        return f"Sensor at {self.loc} closest beacon is at {self.beacon}"


def range_contains_other(rangeA, rangeB):
    if rangeA[0] >= rangeB[0] and rangeA[0] < rangeB[1]:
        return True
    if rangeB[0] >= rangeA[0] and rangeB[0] < rangeA[1]:
        return True
    return False


def combine_range(rangeA, rangeB):
    start = min(rangeA[0], rangeB[0])
    end = max(rangeA[1], rangeB[1])
    return (start, end)


def sensor_combinable(sensor_range, sensor_ranges, y):
    for s in sensor_ranges:
        if range_contains_other(s, sensor_range):
            return True
    return False


def bound_range(range, max_x):
    return (max(range[0], 0), min(range[1], max_x))


def combined_first_match(sensor_ranges):
    for range_a in sensor_ranges:
        for range_b in sensor_ranges:
            if range_a != range_b and range_contains_other(range_a, range_b):
                new_range = list(sensor_ranges.copy())
                new_range.append(combine_range(range_a, range_b))
                new_range.remove(range_a)
                new_range.remove(range_b)
                return set(new_range)
    return sensor_ranges


def combine_ranges(sensor_ranges, max_x):
    sensor_ranges = set([bound_range(r, max_x) for r in sensor_ranges])
    while (True):
        new_sensor_ranges = combined_first_match(sensor_ranges)
        if new_sensor_ranges == sensor_ranges:
            return sensor_ranges
        sensor_ranges = new_sensor_ranges


def len_range(range):
    return range[1] - range[0]


f = open(sys.argv[1], "r")
max_x = int(sys.argv[2]) + 1
max_y = int(sys.argv[3]) + 1
sensors = [Sensor.from_line(line) for line in f.read().splitlines()]

for y in range(max_y):
    sensor_ranges = set([sensor.beacon_x_range_exclusive(y)
                        for sensor in sensors])
    sensor_ranges.remove(None)
    sensor_ranges = combine_ranges(sensor_ranges, max_x)
    if max_x - sum([len_range(r) for r in sensor_ranges]) > 0:
        x = min([r[1] for r in sensor_ranges])
        result = x * 4000000 + y
        print(result)
        break
