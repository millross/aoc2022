from common import aoc_22_common as aoc_22
import functools

def compare_lists(left, right):

        for i in range(0, len(left)):

            if (i > len(right) -1):
                return False

            if (type(left[i]) == type(right[i])):
                if (type(left[i]) is list):
                    result = compare_lists(left[i], right[i])
                    print(result)
                    if (result != None):
                        return result

                if (type(left[i]) is int):
                    if (left[i] < right[i]):
                        return True
                    elif (left[i] > right[i]):
                        return False
                    # If equal we continue checking

            if (type(left[i]) != type(right[i])):
                if (type(left[i]) is int):
                    return compare_lists([left[i]], right[i])
                else:
                    return compare_lists(left[i]    , [right[i]])

        # We have exhausted left, but have we also exhausted right?
        print("Exhausted left")
        if (len(left) < len(right)):
            return True

        # Inconclusive - inputs match exactly
        return None



class PacketPair:
    def __init__(self, packets_comprising_pair):
        self.left = eval(packets_comprising_pair[0])
        self.right = eval(packets_comprising_pair[1])

    def __str__(self):
        return str(self.left) + "|" + str(self.right)

    def inputs_in_right_order(self):
        left = self.left
        right = self.right

        return compare_lists(self.left, self.right)

packet_pairs = [PacketPair(packets) for packets in aoc_22.group_by_delimiter(aoc_22.load_file("day13/input"),"")]
pair = packet_pairs[1]
print (pair.inputs_in_right_order())

total_index_of_true = 0
for i in range(0, len(packet_pairs)):
    if packet_pairs[i].inputs_in_right_order():
        total_index_of_true += (i + 1)
print("Total " + str(total_index_of_true))

input_unsorted = []
for pair in packet_pairs:
    input_unsorted.append( pair.left)
    input_unsorted.append(pair.right)

DIVIDER_1 = [[2]]
DIVIDER_2 = [[6]]

input_unsorted.append(DIVIDER_1)
input_unsorted.append(DIVIDER_2)

def compare_packets(packet1, packet2):
    result = compare_lists(packet1, packet2)
    if (result):
        return - 1
    elif (not result):
        return 1
    else:
        return 0

sorted_packets = (sorted(input_unsorted, key=functools.cmp_to_key( compare_packets)))
# print (sorted(input_unsorted, key=functools.cmp_to_key( compare_packets)))
divider_1_index = 0
divider_2_index = 0

for i in range(0, len(sorted_packets)):
    print (sorted_packets[i])
    if (sorted_packets[i]) == DIVIDER_1:
        divider_1_index = i
    if (sorted_packets[i] == DIVIDER_2):
        divider_2_index = i

# The above indices are zero based but we want 1-based so add 1
print ((divider_1_index + 1) * (divider_2_index + 1))