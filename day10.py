from common import aoc_22_common as aoc_22
import re

ADDX_SPEC_RE = re.compile("addx (-?\d+)")

instruction_spec = aoc_22.load_file("day10/input")

class Instruction:

    def __init__(self,cycle_count, function):
        self.cycle_count = cycle_count
        self.function = function

    def process(self, cycles, input_value):
        for i in range (self.cycle_count):
            cycles.append(input_value)
        return self.function(input_value)

class InstructionFactory:
    def create(self, spec_line):
        
        if spec_line == "noop":
            return Instruction(1, lambda x: x)

        addx_match = ADDX_SPEC_RE.search(spec_line)
        if addx_match != None:
            return Instruction(2, lambda x: x + int(addx_match.group(1)))

        return None


cycles = []
value = 1

factory = InstructionFactory()

for spec_line in instruction_spec:
    if (factory.create(spec_line) == None):
        print(spec_line)
    value = factory.create(spec_line).process(cycles, value)


cycles_of_interest = range(20, 221, 40)

if (len(cycles) >= 220):
    # Calculate the signal strength 
    signal_strengths = [ c * cycles[c - 1] for c in cycles_of_interest ]
    print (sum(signal_strengths))

print("------------------Part 2 -------------------")
cycles_grouped = [cycles[i:i + 40] for i in range(0, len(cycles), 40)]
print(cycles_grouped)

def to_print(index, x):
    if index > x - 2 and index < x + 2:
        return "#"
    else:
        return "."

# print(is_index_in_sprite(2, 16))

for group in cycles_grouped:
    row = ""
    for index in range(0, len(group)):
        row = row + to_print(index, group[index])

    print(row)