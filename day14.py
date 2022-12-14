from common import aoc_22_common as aoc_22


class Vertex:
    def __init__(self, spec):
        coords = spec.split(",")
        self.position = Position(int(coords[0]), int(coords[1]))

class Position:
    def __init__(self, x, y):
        self.x = x
        self.y = y

    def __str__(self):
        return "(" + str(self.x) + ", " + str(self.y) + ")"

# Each line in the input defines a line or set of lines which are rock ledges/faces, so firstly we should construct some kind of representation of this
line_defs = aoc_22.load_file("day14/input")

blocked = {}
sand_col = 500

# Return its next position, or None if it is blocked from falling further
def next_position(position):
    new_y = position.y + 1
    if new_y in blocked:
        # Test if we can fall vertically
        if position.x not in blocked[new_y]:
            return Position(position.x, new_y)
        elif position.x - 1 not in blocked[new_y]:
            return Position(position.x - 1, new_y)
        elif position.x + 1 not in blocked[new_y]:
            return Position(position.x + 1, new_y)
        else: 
            return None
    else:
        # Not blocked by anything so fall vertically
        return Position(position.x, new_y)


# Return the position at which the sand comes to rest, or None if it will not come to rest
def drop_sand():
    sand_position = Position(500, 0)
    max_y = max(blocked.keys())
    while sand_position.y < max_y:
        # Keep moving the sand. if it comes to rest return its position. If we go past max depth with rocks, we return None as it will not come to rest
        # If it comes to rest, mark its position as blocked prior to returning
        new_position = next_position(sand_position)
        if new_position == None:
            # Further move is blocked
            if sand_position.y not in blocked:
                blocked[sand_position.y] = set()
            blocked[sand_position.y].add(sand_position.x)
            return sand_position
        sand_position = new_position
    print ("We will not come to rest, y = " + str(sand_position.y))
    return None

def part_two_next_position(max_depth, position):
    new_y = position.y + 1
    if new_y == max_depth:
        # We've hit the floor so return None
        print("Floor hit")
        return None

    if new_y in blocked:
        # Test if we can fall vertically
        if position.x not in blocked[new_y]:
            return Position(position.x, new_y)
        elif position.x - 1 not in blocked[new_y]:
            return Position(position.x - 1, new_y)
        elif position.x + 1 not in blocked[new_y]:
            return Position(position.x + 1, new_y)
        else: 
            return None
    else:
        # Not blocked by anything so fall vertically
        return Position(position.x, new_y)


def part_two_drop_sand(max_depth):
    sand_position = Position(500, 0)
    start = Position(500,0)
    max_y = max(blocked.keys()) + 2
    while sand_position.y < max_y:
        # Keep moving the sand. if it comes to rest return its position. If we go past max depth with rocks, we return None as it will not come to rest
        # If it comes to rest, mark its position as blocked prior to returning
        new_position = part_two_next_position(max_depth, sand_position)
        print(new_position)
        if new_position == None:
            # Further move is blocked
            if sand_position.x == start.x and sand_position.y == start.y:
                # The hole is blocked
                return None

            if sand_position.y not in blocked:
                blocked[sand_position.y] = set()
            blocked[sand_position.y].add(sand_position.x)
            return sand_position
        sand_position = new_position
    print ("We will not come to rest, this should not happen, y = " + str(sand_position.y))
    return None

for line in line_defs:
    vertices = [Vertex(coords) for coords in line.split(" -> ")]
    for index in range(0, len(vertices) - 1):
        start = vertices[index].position
        end = vertices[index + 1].position
        x_from = min(start.x, end.x)
        x_to = max(start.x, end.x)
        y_from = min(start.y, end.y)
        y_to = max(start.y, end.y)
        
        # Define a line between start and end
        for x in range(x_from, x_to + 1):
            for y in range (y_from, y_to + 1):
                filled = Position(x, y)
                if not y in blocked:
                    blocked[y] = set()
                blocked[y].add(x)

i = 0
while drop_sand() != None:
     i += 1

print(i)
blocked = {}
for line in line_defs:
    vertices = [Vertex(coords) for coords in line.split(" -> ")]
    for index in range(0, len(vertices) - 1):
        start = vertices[index].position
        end = vertices[index + 1].position
        x_from = min(start.x, end.x)
        x_to = max(start.x, end.x)
        y_from = min(start.y, end.y)
        y_to = max(start.y, end.y)
        
        # Define a line between start and end
        for x in range(x_from, x_to + 1):
            for y in range (y_from, y_to + 1):
                filled = Position(x, y)
                if not y in blocked:
                    blocked[y] = set()
                blocked[y].add(x)

j = 1
max_depth = max(blocked.keys()) + 2
print("Max depth is: " + str(max_depth))
while(part_two_drop_sand(max_depth) != None):
    j += 1


print(j)
# i = 0
#     print(drop_sand())