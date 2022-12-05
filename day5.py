from common import aoc_22_common as aoc_22
import collections
import re

P = re.compile("move (\d+) from (\d) to (\d)")

class Stacks:
    def __init__(self):
        self.by_state_index = {}
        self.by_stack_id = {}
        self.state_indices = list()
        self.stack_ids = list()

    def init_stack(self, state_index, stack_id):
        stack = collections.deque()
        self.by_state_index[state_index] = stack
        self.state_indices.append(state_index)
        self.stack_ids.append(stack_id)
        self.by_stack_id[stack_id] = stack

    def stack_with_id(self, stack_id):
        return self.by_stack_id[stack_id]

    def stack_with_state_index(self, stack_index):
        return self.by_state_index[stack_index]

    def add_state_line(self, state_line):
        for i in range (len(state_line)):
            candidate = state_line[i]
            if (candidate not in " []"):
                self.stack_with_state_index(i).append(candidate)

    def display_stacks(self):
        for id in self.stack_ids:
            print(id)
            print(self.by_stack_id[id])

    def apply_move(self, move):
        for i in range (0, move.number_to_move):
            popped = self.stack_with_id(move.move_from).pop()
            self.stack_with_id(move.move_to).append(popped)

    def apply_part_two_move(self, move):
        intermediate_stack = collections.deque()
        for i in range (0, move.number_to_move):
            popped = self.stack_with_id(move.move_from).pop()
            intermediate_stack.append(popped)

        intermediate_stack.reverse()
        self.stack_with_id(move.move_to).extend(intermediate_stack)
        



    def stack_tops(self):
        tops = ""
        for id in self.stack_ids:
            top = self.by_stack_id[id].pop()
            tops += top
        return tops

class Move:
    def __init__(self, move_line):
        match = P.search(move_line)
        self.number_to_move = int(match.group(1))
        print ("To move " + str(self.number_to_move))
        self.move_from = match.group(2)
        self.move_to = match.group(3)

def create_stack_mappings(stack_index_line):
    # Create a dictionary of "index" to character index and stack
    mappings = Stacks()
    for i in range (len(stack_index_line)):
        candidate = stack_index_line[i]
        if (candidate not in " []"):
            stack = collections.deque()
            mappings.init_stack(i, candidate)

    return mappings 

def parse_initial_state(initial_state_text):
    stack_index_line = initial_state_text[len(initial_state_text) - 1]
    stacks = create_stack_mappings(stack_index_line)
    for i in range (len(initial_state_text) - 2, -1, -1):
        state_line = initial_state_text[i]
        stacks.add_state_line(state_line)
    return stacks


lines = aoc_22.load_file("day5/input")
data_sets = aoc_22.group_by_delimiter(lines, "")
initial_state_unparsed = data_sets[0]
moves = data_sets[1]

# Use deque as a stack. We'll use append and pop (i.e. stack head is right hand end)
stacks = parse_initial_state(initial_state_unparsed)
stacks.display_stacks()

for move in moves:
    print(move)
    move_obj = Move(move)
    stacks.apply_move(move_obj)
    stacks.display_stacks()

print (stacks.stack_tops())

print ("Part 2")
stacks = parse_initial_state(initial_state_unparsed)
stacks.display_stacks()
for move in moves:
    print(move)
    move_obj = Move(move)
    stacks.apply_part_two_move(move_obj)
    stacks.display_stacks()
print (stacks.stack_tops())

# move = Move(moves[0])
# print(moves[0])
# stacks.apply_move(move)
# stacks.display_stacks()

