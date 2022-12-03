
def load_backpacks_file():
    loaded = list()
    input_file_name = "input-3"

    input_file = open(input_file_name)
    for (line) in input_file:
        loaded.append(line.strip())
    input_file.close()
    return loaded

def priority(type):
    ascii_val = ord(type)
    if (ascii_val) > 96:
        return ascii_val - 96
    else:
        return ascii_val - 38

def form_line_groups(lines):
    group_size = 3
    groups = list()
    for i in range (0, len(lines), 3):
        groups.append(ElfGroup(lines[i], lines[i + 1], lines[i + 2]))
    return groups


class ElfGroup:
    def __init__(self, backpack1, backpack2, backpack3):
        self.backpack_1 = backpack1
        self.backpack_2 = backpack2
        self.backpack_3 = backpack3

    def common_type(self):
        common_types = set(self.backpack_1).intersection(self.backpack_2).intersection(self.backpack_3)
        (element, ) = common_types
        return element

class Backpack:
    def __init__(self, line):
        length = len(line)
        cutoff = length // 2
        self.compartment_1 = line[:cutoff]
        self.compartment_2 = line[cutoff:length]

    def common_type(self):
        common_types = set(self.compartment_1).intersection(self.compartment_2)
        # Specified to only have one common type
        (element, ) = common_types
        return element

# def separate_compartments():
lines = load_backpacks_file()
priorities = [priority(Backpack(l).common_type()) for l in lines]
print (sum(priorities))

# Part 2
print ("Part 2")
# group = ElfGroup("wMqvLMZHhHMvwLHjbvcjnnSBnvTQFn", "ttgJtRGJQctTZtZT", "CrZsJsPPZsGzwwsLwLmpwMDw")
# print (group.common_type())
groups = form_line_groups(lines)
priorities = [priority(g.common_type()) for g in groups]
print (sum(priorities))