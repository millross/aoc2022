from common import aoc_22_common as aoc_22

class RangeDef:
    def __init__(self, range_string):
        limits = [int(s) for s in range_string.split("-")]
        self.min = limits[0]
        self.max = limits[1]

    def containsRange(self, other):
        return self.min <= other.min and self.max >= other.max

    def overlapsWith(self,other):
        return (self.min <= other.max and self.max >= other.max) or (other.min <= self.max and other.max >= self.min)

class Pairing:
    def __init__(self, line):
        ranges = line.split(",")
        self.assignments_1 = RangeDef(ranges[0])
        self.assignments_2 = RangeDef(ranges[1])

    def has_superset_assignment(self):
        return (self.assignments_1.containsRange(self.assignments_2))  or (self.assignments_2.containsRange(self.assignments_1))

    def overlaps(self):
        return self.assignments_1.overlapsWith(self.assignments_2)

lines = aoc_22.load_file("day4/input")
pairings = [Pairing(line) for line in lines]
filtered = list(filter(lambda p: p.has_superset_assignment(), pairings))
print (len(filtered))

testRange1 = RangeDef("32-52")
testRange2 = RangeDef("33-51")
testPairing = Pairing("34-82,33-81")
print(testPairing.has_superset_assignment())

testPairing_2 = Pairing("6-96,98-99")
print(testPairing_2.overlaps())

filtered_2 = list(filter(lambda p: p.overlaps(), pairings))
print (len(filtered_2))