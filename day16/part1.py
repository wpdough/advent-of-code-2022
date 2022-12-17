import sys


class Valve:
    name: str
    flow_rate: int
    next: list["Valve"]

    def __init__(self, name, flow_rate):
        self.name = name
        self.flow_rate = flow_rate
        self.next = []

    def __repr__(self):
        next_valve_names = [valve.name for valve in self.next]
        return f"Valve {self.name} has flow rate {self.flow_rate} and leads to valves {next_valve_names}"


class Decision:
    valve: Valve
    on: bool

    def __init__(self, valve, on=False):
        self.valve = valve
        self.on = on

    def build_move(valve):
        return Decision(valve, False)

    def build_open(valve):
        return Decision(valve, True)

    def __repr__(self):
        return f"Decision: {self.valve.name} {'on' if self.on else 'move'}"


def parse_valves(lines):
    valves_input = []
    for line in lines:
        line = line.replace("Valve ", "").replace(" has flow rate=", ",").replace(
            "; tunnel leads to valves ", ",").replace("; tunnels lead to valves ", ",").replace(
            "; tunnel leads to valve ", ",").replace(", ", ",").replace(";", ",")
        parts = line.split(",")
        name = parts[0]
        flow_rate = int(parts[1])
        next = parts[2:]
        valves_input.append((name, flow_rate, next))
    return valves_input


def build_graph(lines):
    valves_input = parse_valves(lines)
    # turn the input into valves
    valves = [Valve(valve[0], valve[1]) for valve in valves_input]
    # hook em up to tunnels
    for valve in valves:
        next_valve_names = [
            next for next in valves_input if valve.name in next[2]]
        valve.next = [next for next in valves if next.name in [next[0]
                                                               for next in next_valve_names]]
    return valves


def decision_possibilities(path: list[Decision]):
    ahead = [
        Decision.build_move(valve) for valve in path[-1].valve.next]
    if not path[-1].on:
        ahead.append(Decision.build_open(path[-1].valve))
    return ahead


def path_has_unopened_within_steps(path: list[Decision], steps: int):
    opened = [decision.valve for decision in path if decision.on]
    # print("opened:", [valve.name for valve in opened])
    unopened_ahead = [
        valve for valve in path[-1].valve.next if valve not in opened]
    # check if the current valve links to a valve that is unopened and has pressure > 0
    if not path[-1].on or len(unopened_ahead) > 0:
        return True
    if steps == 0:
        return False
    return path_has_unopened_within_steps(path, steps - 1)


def find_valve_by_name(valves, name):
    return next(valve for valve in valves if valve.name == name)


def find_paths(path: list[Decision], paths: list[list[Decision]]):
    if len(path) == 30 or not path_has_unopened_within_steps(path, 30 - len(path)):
        print(len(paths))
        paths.append(path)
        return

    for decision in decision_possibilities(path):
        sprout = path.copy()
        sprout.append(decision)
        find_paths(sprout, paths)
    return paths


MINUTES = 5
f = open(sys.argv[1], "r")
lines = f.read().splitlines()
valves = build_graph(lines)

root = next(valve for valve in valves if valve.name == "AA")
paths = []
paths = find_paths([Decision.build_move(root)], paths)
print(paths)
