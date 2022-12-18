import re
from common import aoc_22_common as aoc_22
import functools

SENSOR_REGEX = re.compile("Sensor at x=(-?\d+), y=(-?\d+): closest beacon is at x=(-?\d+), y=(-?\d+)")

sensor_defs = aoc_22.load_file("day15/input")

class Position:
    def __init__(self, x, y):
        self.x = x
        self.y = y
    
    def __str__(self):
        return "(" + str(self.x) + ", " + str(self.y) + ")"

class SensorInfo:
    def __init__(self, line):
        position_match = SENSOR_REGEX.search(line)
        if position_match == None:
            # Unexpected input
            print ("Unexpected input: " + line)
            raise ValueError(line)

        self.position = Position(int(position_match.group(1)), int(position_match.group(2)))
        self.nearest_beacon = Position(int(position_match.group(3)), int(position_match.group(4)))

    def __str__(self):
        return "Sensor at " + str(self.position) + " with nearest beacon at " + str(self.nearest_beacon)

class PartRow:
    def __init__(self, y, start_x, end_x):
        self.beginning = start_x
        self.end = end_x
        self.y = y

    def __str__(self):
        return str(Position(self.beginning, self.y)) + " to " + str(Position(self.end, self.y))

    def length(self):
        return self.end - self.beginning + 1

    def overlaps(self, other):
        return (self.end > other.end and self.beginning < other.end) or (self.beginning < other.beginning and self.end > other.beginning)
    
    def combine(self, other):
        self.beginning = min(self.beginning, other.beginning)
        self.end = max(self.end, other.end)

class Diamond:
    def __init__(self, sensor_position, nearest_beacon):
        print("Determining diamond for sensor at " + str(sensor_position))
        relative_position = Position(nearest_beacon.x - sensor_position.x, nearest_beacon.y - sensor_position.y)
        # Nominal radius is the maximum x or y radius - in fact we don't apply a circle, we apply a diamond, hence calling it nominal radius
        nominal_radius = abs(relative_position.x) + abs(relative_position.y)
        # Next line adds 1 to allow for the row containing the sensor, we also need to do the equivalent on its column
        height = 1 + (2 * nominal_radius) 
        width = 1 + (2 * nominal_radius)
        top = sensor_position.y - nominal_radius
        left = sensor_position.x - nominal_radius

        part_rows = {}

        for y in range (top, top + height + 1):
            width = height - (2 * abs(sensor_position.y - y))
            range_left = sensor_position.x - int(0.5 * width)
            range_right = sensor_position.x + int(0.5 * width)
            
            part_rows[y] = PartRow(y, range_left, range_right)

        self.not_beacons = part_rows

def excluded_positions(sensor_info):
    # Determine the diamond of "there can be no beacon here positions" excluding known beacon position
    # for a given sensor
    # Return a list of "PartRows", one per row of the diamond
    # Let's start by determining the apexes
    return Diamond(sensor_info.position, sensor_info.nearest_beacon)

def count_excluded_positions_at_y(excluded_blocks, known_beacons, y):
    if not y in excluded_blocks:
        return 0

    # Use of a set handles overlaps between blocks
    excluded_positions = set()

    for block in excluded_blocks[y]:
        for x in range(block.beginning, block.end + 1):
            position = Position(x, y)
            # If we're a beacon we shouldn't be counted
            if str(position) not in known_beacons:
                excluded_positions.add(str(Position(x, y))) 

    return len(excluded_positions)

sensor_readings = [SensorInfo(l) for l in sensor_defs]
diamonds = [Diamond(s.position, s.nearest_beacon) for s in sensor_readings]

excluded_blocks_by_row = {}
beacons = set([str(s.nearest_beacon) for s in sensor_readings])

for diamond in diamonds:
    for y in diamond.not_beacons.keys():
        if not y in excluded_blocks_by_row:
            excluded_blocks_by_row[y] = list()
        excluded_blocks_by_row[y].append(diamond.not_beacons[y])

# Part 1
print(count_excluded_positions_at_y(excluded_blocks_by_row, beacons, 2000000))

# Part 2
def get_tuning_frequency(x, y):
    return (4000000 * x) + y

LIMIT = 4000000

def compare_blocks(block1, block2):
    return block1.beginning - block2.beginning

def find_first_possible_beacon_position(excluded_blocks, limit):
    for y in excluded_blocks.keys():
        # Exclude any outside limit
        if y >= 0 and y <= limit:
            # Now examine blocks

            if (y == 2932891):
                ends = sorted([block.end for block in excluded_blocks_by_row[y]])
                print ("Ends: " + str(ends))
            sorted_blocks = sorted(excluded_blocks_by_row[y], key=functools.cmp_to_key(compare_blocks))
            excluded = None
            for block in sorted_blocks:
                if (y == 2932891):
                    print(str(block))
                # Exclude any blocks which don't fall within the range we need
                if (block.end >= 0 and block.beginning <= limit):
                    beginning = max(block.beginning, 0)
                    end = min(block.end, limit)

                if (excluded == None):
                    if (beginning > 0):
                        # We've found our first beacon position as our first block beginning was above the lower limit
                        return Position(0, y)

                    excluded = PartRow(y, beginning, end)

                if (block.beginning - excluded.end) > 1:
                    # We have found our beacon as there is a gap between the end of the space we have covered and the next lowest block beginning for this row
                    return Position(excluded.end + 1, y)

                if end > excluded.end:
                    excluded.end = end

                if (y == 2932891):
                    print("Excluded: " + str(excluded))

                if (excluded.end > limit):
                    continue

            # We fall through, so we need to check one last thing here
            if (excluded.end < limit):
                # We never reached the end
                return (excluded.end + 1, y)

beacon_position = find_first_possible_beacon_position(excluded_blocks_by_row, LIMIT)
print (str(beacon_position))
print ("12608534932891 is too high")
print ("11932670524696 is too low")
print("I think the y should be above " + str(2524696))
print (get_tuning_frequency(beacon_position.x, beacon_position.y))

            


