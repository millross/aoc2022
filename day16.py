from common import aoc_22_common as aoc_22
import re

# VALVE_DEF_REGEX = re.compile("^Valve ([A-Z]{2}) has flow rate=(\d+); tunnels lead to valves [A-Z]{2} , [A-Z]{2}, [A-Z]{2}")
VALVE_DEF_REGEX = re.compile("^Valve ([A-Z]{2}) has flow rate=(\d+); tunnels? leads? to valves? ([A-Z]{2}(?:, \d+)*)")


line_defs = aoc_22.load_file("day16/test_input")
STARTING_VALVE = "AA"

class Valve: 
    def __init__(self):
        match = VALVE_DEF_REGEX.search(l)
        if match == None:
            print("Failed to match:  " + l)
            raise ValueError("Cannot extract valve definition from line: " + l)

        self.valve_name = match.group(0)
        self.flow_rate = int(match.group(1))


for l in line_defs:
    match = VALVE_DEF_REGEX.search(l)
    if match == None:
        print("Failed to match:  " + l)
        raise ValueError("Cannot extract valve definitions")
