from common import aoc_22_common as aoc_22
import re
import operator
import math

STARTING_ITEMS_REGEX = re.compile("^\s*Starting items: ((\d+)(?:, \d+)*)")
OPERATION_REGEX = re.compile("^\s*Operation: new = old ([+*]) (\d+|old)")
TEST_REGEX = re.compile("^\s*Test: divisible by (\d+)")
DESTINATION_REGEX = re.compile("^\s*If (?:true|false): throw to monkey (\d)")
OPERATORS = { "+": operator.add, "*": operator.mul}

def get_starting_items(line):
    match = STARTING_ITEMS_REGEX.search(line)
    if (match == None):
        print("Problem with line: " + line)
        raise ValueError("Cannot extract starting items")
    items_as_string = match.group(1)
    return [int(s) for s in items_as_string.split(", ")]

def get_operation(line):
    match = OPERATION_REGEX.search(line)
    if (match == None):
        print("Problem with line: " + line)
        raise ValueError("Cannot extract operation")

    operator_string = match.group(1)
    adjustment = match.group(2)

    if (operator_string not in OPERATORS):
        print ("Unknown operator: " + operator_string)
        raise ValueError("Unknown operator for line " + line)

    if (adjustment == "old"):
        operation = lambda x: OPERATORS[operator_string](x, x)
    else:
        operation = lambda x: OPERATORS[operator_string](x, int(adjustment))

    return operation

def get_divisor(line):
    match = TEST_REGEX.search(line)
    if (match) == None:
        print("Problem with line: " + line)
        raise ValueError("Cannot extract test definition")
    return int(match.group(1))
    
def get_test(line):
    divisor = get_divisor(line)
    return lambda x: x % divisor == 0

def get_destination(line):
    match = DESTINATION_REGEX.search(line)
    if (match == None):
        print("Problem with line: " + line)
        raise ValueError("Cannot extract destination")
    return int(match.group(1))

class Monkey:
    def __init__(self, spec_lines):
        self.inspections = 0
        self.items = get_starting_items(spec_lines[1])
        self.operation = get_operation(spec_lines[2])
        self.test = get_test(spec_lines[3])
        self.divisor = get_divisor(spec_lines[3])
        self.true_destination = get_destination(spec_lines[4])
        self.false_destination = get_destination(spec_lines[5])

    def act(self, monkeys, relief_level, lcm):
        for item in self.items:
            if(relief_level > 1):
                value = int(self.inspect(item) / relief_level)
            else:
                value = self.inspect(item) % lcm

            if (self.test(value)):
                destination = self.true_destination
            else:
                destination = self.false_destination

            monkeys[destination].receive(value)
        
        self.items.clear()

    def inspect(self, worry_level):
        value = self.operation(worry_level)
        self.inspections += 1
        return value

    def receive(self,value):
        self.items.append(value)

monkey_specs = aoc_22.group_by_delimiter(aoc_22.load_file("day11/input"),"")

monkeys = [Monkey(s) for s in monkey_specs]

for i in range(0, 20):
    for monkey in monkeys:
        monkey.act(monkeys, 3, None)

inspections_sorted = sorted([m.inspections for m in monkeys], reverse=True)

print(inspections_sorted)
monkey_business = inspections_sorted[0] * inspections_sorted[1]
print("Monkey business = " + str(monkey_business))


print("======================== Part 2 - relief level 1 rather than 3, i.e. no modifier ==========================")
monkeys_unrelieved = [Monkey(s) for s in monkey_specs]

lcm = math.lcm(*[monkey.divisor for monkey in monkeys_unrelieved])
print(lcm)
for i in range(0, 10000):
    for monkey in monkeys_unrelieved:
        monkey.act(monkeys_unrelieved, 1, lcm)

part_2_inspections_sorted = sorted([m.inspections for m in monkeys_unrelieved], reverse=True)
print("Inspections, sorted " + str(part_2_inspections_sorted))
part_2_monkey_business = part_2_inspections_sorted[0] * part_2_inspections_sorted[1]
print("Monkey business without relief = " + str(part_2_monkey_business))
