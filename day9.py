from common import aoc_22_common as aoc_22
import re

MOVE_REGEX = re.compile("([RLUD]) (\d+)")
X = "x"
Y = "y"

move_descriptions = aoc_22.load_file("day9/input")
tail_visits = set()
total_moves = 0

class Move:
    def __init__(self, description):
        match = MOVE_REGEX.search(description)
        self.direction = match.group(1)
        self.distance = int(match.group(2))

    def __str__(self):
        return self.direction + " " + str(self.distance)

class Position:
    def __init__(self, x, y):
        self.x = x
        self.y = y

    def is_adjacent_or_identical(self, position):
        x_diff = abs(self.x - position.x)
        y_diff = abs(self.y - position.y)
        return x_diff < 2 and y_diff < 2

    def __str__(self):
        return "(" + str(self.x) + ", " + str(self.y) + ")"

class Rope:
    def __init__(self, length):
        self.positions = list()
        for i in range(0, length):
            self.positions.append(Position(0, 0))

    def __str__(self):
        return str([ str(p) for p in self.positions])

    def tail(self):
        return self.positions[len(self.positions) - 1]

    def move_head(self, move):
        multiplier = 1

        if (move.direction == "D" or move.direction == "L"):
            multiplier = -1

        head = self.positions[0]
        
        for i in range(0, move.distance):
            
            if move.direction == "U" or move.direction == "D":
                head.y += multiplier
            else:
                head.x += multiplier

            self.apply_single_move(1)
                    
    def apply_single_move(self, position_index):

        if (position_index < len(self.positions)):
            current = self.positions[position_index]
            previous = self.positions[position_index - 1]
            if not current.is_adjacent_or_identical(previous):
                # We need to adjust to catch it up
                x_diff = previous.x - current.x
                y_diff = previous.y - current.y

                if (x_diff == 0):
                    current.y = current.y + y_diff/2
                elif (y_diff == 0):
                    current.x = current.x + x_diff/2
                elif abs(x_diff) == abs(y_diff):
                    current.x = current.x + x_diff/2
                    current.y = current.y + y_diff/2
                elif(abs(x_diff) == 1): 
                    # Diagonal move
                    current.x = current.x + x_diff
                    current.y = current.y + y_diff/2
                elif(abs(y_diff) == 1):
                    current.x = current.x + x_diff / 2
                    current.y = current.y + y_diff
                else:
                    raise SystemExit("Failure")

                if (position_index == len(self.positions) -1):
                    tail_visits.add(str(self.tail()))

                self.apply_single_move(position_index + 1)

rope = Rope(10)
tail_visits.add(str(rope.tail()))


moves = [Move(x) for x in move_descriptions]

for move in moves:
    rope.move_head(move)

# 2594 too high
# 1995 too low
total_moves = sum([m.distance for m in moves])
print ("Tail visits: " + str(len(tail_visits)))