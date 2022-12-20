from common import aoc_22_common as aoc_22
from common.position import Position


# We're going to assume positive y = upwards for the purposes of this
# Floor is therefore at a y value of 0, rocks are defined relative to bottom left position of the space they can potentially occupy


class ShapeDefinition:
    def __init__(self, relative_positions):
        self.underside = {}
        for position in relative_positions:
            if position.x not in self.underside:
                self.underside[position.x] = position.y
            
            if (self.underside[position.x] > position.y):
                self.underside[position.x] = position.y
            
        self.relative_positions = relative_positions
        # We only populate x and y for bottom left of shape when we initialise the actual shape

        self.width = max(pos.x for pos in relative_positions) + 1

class Rock:
    def __init__(self, definition, x, state):
        self.min_x = x
        self.min_y = state.max_height + 4
        self.definition = definition
        self.landed = False

    def can_apply_x_variation(self, delta, state, debug):
        if (self.min_x + self.definition.width - 1 + delta) > MAX_X or (self.min_x + delta < 0):
            return False
        for pos in self.definition.relative_positions:
            potential_x = self.min_x + pos.x + delta
            potential_y = self.min_y + pos.y
            if (debug):
                print("Checking " + str(Position(potential_x, potential_y)))
                print("Blocked " + str(state.blocked))
                print (str(Position(potential_x, potential_y)) in state.blocked)
            if state.is_blocked_horizontal(potential_x, potential_y, debug):
                return False

        return True

    def apply_x_variation(self, delta, state, debug):
        if debug: 
            print("Applying delta " + str(delta) + " to position " + str(Position(self.min_x, self.min_y)))
        if self.can_apply_x_variation(delta, state, debug):
            self.min_x = self.min_x + delta
        else:
            if debug:
                print("Cannot move")
        if debug:
            print("Position after delta: " + str(Position(self.min_x, self.min_y)))

    def is_at_rest(self, state):
        underside = self.definition.underside
        for x in underside.keys():
            next_y = underside[x] + self.min_y - 1
            if (state.is_blocked_vertical(x + self.min_x, next_y)):
                return True
        return False

    def drop(self, increment):
        self.min_y = self.min_y - increment
        

# For tracking our mutable state
class State:
    def __init__(self, jets):
        self.jets = jets
        self.max_height = 0
        self.max_heights = [0, 0, 0, 0, 0, 0 ,0]
        self.blocked = set()
        self.jet_index = 0
        self.rollover_at = len(jets)

    def pop_move(self):
        x_move = JET_MOVES[self.jets[self.jet_index]]
        self.jet_index += 1
        if self.jet_index == self.rollover_at:
            self.jet_index = 0
        return x_move

    def is_blocked_vertical(self, x, y):
        return self.max_heights[x] >= y

    def is_blocked_horizontal(self, x, y, debug):
        return str(Position(x, y)) in self.blocked

    def block(self, rock, debug):
        for pos in rock.definition.relative_positions:
            x = rock.min_x + pos.x
            y = rock.min_y + pos.y
            if debug:
                print("Considering blocking " + str(x))
            blocked_max = self.max_heights[x]
            if self.max_heights[x] < y:
                self.max_heights[x] = y

            self.blocked.add(str(Position(x, y)))

    def update_max_height(self, rock):
        for pos in rock.definition.relative_positions:
            y = rock.min_y + pos.y
            if self.max_height < y:
                self.max_height = y


def step(rock, state, debug):
    move = state.pop_move()
    if (debug):
        print("Move; " + str(move))
    rock.apply_x_variation(move, state, debug)
    if not rock.is_at_rest(state):
        rock.drop(1)
    else:
        rock.landed = True
    if debug:
        print("New rock position: " + str(Position(rock.min_x, rock.min_y)))

def track_shape(state, rock, debug = False):
    # Use state to keep track of what's blocked
    while (not rock.landed):
        step(rock, state, debug)
        
    # We're at rest so now need to block the locations associated with this rock
    state.block(rock, debug)
    state.update_max_height(rock)

MAX_X = 6
SHAPES = list()
SHAPES.append(ShapeDefinition([Position(0, 0), Position(1, 0), Position(2, 0), Position(3, 0)]))
SHAPES.append(ShapeDefinition([Position(1, 0), Position(0, 1), Position(1, 1), Position(1, 2), Position(2, 1)]))
SHAPES.append(ShapeDefinition([Position(0, 0), Position(1, 0), Position(2, 0), Position(2, 1), Position(2, 2)]))
SHAPES.append(ShapeDefinition([Position(0, 0), Position(0, 1), Position(0, 2), Position(0, 3)]))
SHAPES.append(ShapeDefinition([Position(0, 0), Position(1, 0), Position(0, 1), Position(1, 1)]))

JET_MOVES = {"<": -1, ">": 1}
LIMIT = 1
SHAPES_COUNT = len(SHAPES)


jet_defs = aoc_22.load_file("day17/input")[0]
print(str(len(jet_defs)))
state = State(jet_defs)

for rock_num in range(0, 2022):
    # print("Running rock: " + str(rock_num))
    rock = Rock(SHAPES[rock_num % SHAPES_COUNT], 2, state)
    track_shape(state, rock)
    print(str(Position(rock.min_x, rock.min_y)))
print("3160 is too high, need to investigate further, annoyingly test example is correct")
print(max(state.max_heights))

    
