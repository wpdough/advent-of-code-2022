import sys


class Monkey:
    inspections = 0

    def __init__(self, item_indexes: 'list[int]', worry_expr, test_divisor, test_true_receiver, test_false_receiver):
        self.item_indexes = item_indexes
        self.worry_expr = worry_expr
        self.test_divisor = test_divisor
        self.test_true_receiver = test_true_receiver
        self.test_false_receiver = test_false_receiver

    def operation(self, old):
        return eval(self.worry_expr, {}, {"old": old})

    def test(self, num):
        return self.test_true_receiver if num % self.test_divisor == 0 else self.test_false_receiver

    def incr_inspections(self):
        self.inspections += 1


input = open(sys.argv[1], "r").read()

items = []
monkeys: 'list[Monkey]' = []
for monkey_lines in input.split("\n\n"):
    for line in monkey_lines.split("\n"):
        if line.__contains__("Starting items"):
            starting_items = [int(x) for x in line.split(": ")[1].split(", ")]
            item_indexes = []
            for item_index in starting_items:
                item_indexes.append(len(items))
                items.append(item_index)
        if line.__contains__("Operation"):
            worry_expr = line.replace("Operation: new = ", "").strip()
        if line.__contains__("Test"):
            test_divisor = int(line.replace(
                "Test: divisible by ", "").strip())
        if line.__contains__("If true"):
            test_true_receiver = int(line.replace(
                "If true: throw to monkey", "").strip())
        if line.__contains__("If false"):
            test_false_receiver = int(line.replace(
                "If false: throw to monkey", "").strip())
    monkey = Monkey(item_indexes, worry_expr, test_divisor,
                    test_true_receiver, test_false_receiver)
    monkeys.append(monkey)

for round in range(20):
    for i in range(len(monkeys)):
        monkey = monkeys[i]
        print("Monkey", i)
        items_to_remove = []
        for item_index in monkey.item_indexes:
            item_worry_level = items[item_index]
            print("  Monkey inspects an item with a worry level of", item_worry_level)
            item_worry_level = monkey.operation(item_worry_level)
            monkey.incr_inspections()
            print("    Worry level is operated to", item_worry_level)
            item_worry_level = int(item_worry_level / 3)
            print(
                "    Monkey gets bored with item. Worry level is divided by 3 to", item_worry_level)
            items[item_index] = item_worry_level
            monkey_throw_target = monkey.test(item_worry_level)
            print("    Item with worry level", item_worry_level,
                  "is thrown to monkey", monkey_throw_target)
            items_to_remove.append(item_index)
            monkeys[monkey_throw_target].item_indexes.append(item_index)
        for item_to_remove in items_to_remove:
            monkey.item_indexes.remove(item_to_remove)
        print()

    print("After round", round+1)
    for i in range(len(monkeys)):
        monkey_items = []
        for item_index in monkeys[i].item_indexes:
            item = items[item_index]
            monkey_items.append(item)
        print("Monkey", i, monkey_items)
    print()

monkeys.sort(reverse=True, key=lambda m: m.inspections)
print(monkeys[0].inspections * monkeys[1].inspections)
