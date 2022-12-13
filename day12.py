from common import aoc_22_common as aoc_22
from queue import PriorityQueue

def get_height(height):
    if (height == "S"):
        return 0
    elif (height == "E"):
        return 25
    else:
        return ord(height) - ord('a')

def get_position_id(x, y):
    return "(" + str(x) + ", " + str(y) + ")"


class Position:
    def __init__(self, x, y, map_rows):
        self.x = x
        self.y = y
        self.height = map_rows[y][x]
        self.valid_paths = {}
        ew_length = len(map_rows[0])
        ns_length = len(map_rows)
        for neighbour_x in range (max(x -1, 0), min(x+2, ew_length)):
            for neighbour_y in range (max(y - 1, 0), min(y + 2, ns_length)):
                same_x = neighbour_x == x
                same_y = neighbour_y == y
                if (same_y and not same_x) or (same_x and not same_y):
                    neighbour_height = map_rows[neighbour_y][neighbour_x]
                    if (get_height(neighbour_height) >= (get_height(self.height) - 1)):
                        self.valid_paths[get_position_id(neighbour_x, neighbour_y)] = 1
    
    def __str__(self):
        return get_position_id(self.x, self.y)

class Step:
    def __init__(self, destination, score):
        self.destination = destination
        self.score = score

class Node:
    def __init__(self, position):
        self.position = str(position)
        self.valid_paths = position.valid_paths

    def __str__(self):
        return self.position

map_rows = aoc_22.load_file("day12/input")

# Compile dictionary of positions and valid paths
visited = set()
positions = {}
unvisited = PriorityQueue()
added = set()

def key(distance, path):
    return str(distance) + "-" + path

y = 0
start = None
end = ""
for row in map_rows:
    x = 0
    for c in row:
        position = Position(x, y, map_rows)
        positions[str(position)] = position
        if map_rows[y][x] == "E":
            # Let's do this in reverse
            node = Node(position)
            start = node
            start.distance = 0
            unvisited.put((0, str(position), start))
           
        if (map_rows[y][x]) == "S":
             end = str(position)

        x += 1
    y += 1

while not unvisited.empty():
    node = unvisited.get()

    for path in node[2].valid_paths.keys():
        if (not path in visited):
            # If we've already visited then we've found an equal or shorter path to this node
            path_node = Node(positions[path])
            path_node.distance = node[0] + node[2].valid_paths[path]
            if not key(path_node.distance, path) in added:
                unvisited.put((path_node.distance, path, path_node)) 
                # No point in visiting the same point at the same distance again
                added.add(key(path_node.distance, path))

            if (path == end):
                min_length = path_node.distance
                print("Shortest distance: " + str(min_length))

    visited.add(node[1])

start.distance = 0
unvisited = PriorityQueue()
unvisited.put((0, str(positions[start.position]), start))
visited = set()
added = set()
min_length = 10000
while not unvisited.empty():
    node = unvisited.get()

    for path in node[2].valid_paths.keys():
        if (not path in visited):
            # If we've already visited then we've found an equal or shorter path to this node
            position = positions[path]
            path_node = Node(position)
            path_node.distance = node[0] + node[2].valid_paths[path]
            if not key(path_node.distance, path) in added:
                unvisited.put((path_node.distance, path, path_node)) 
                # No point in visiting the same point at the same distance again
                added.add(key(path_node.distance, path))


                length = path_node.distance
                if (length < min_length):
                    print("Shorter distance: " + str(min_length))
                    min_length = length

    visited.add(node[1])

print(min_length)
        # node = Node(position)

#         node = Node(position)
#         if map_rows[y][x] == "E":
#             # Let's do this in reverse
#             start = node
#             start.distance = 0
        
#         nodes = nodes + node



