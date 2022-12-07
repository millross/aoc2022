from common import aoc_22_common as aoc_22

def first_start_of_packet_marker(input_buffer, marker_length):
    i = marker_length
    while i <= len(input_buffer):
        candidate = input_buffer[(i - marker_length):i]
        if (all_different_characters(candidate)):
            return i
        i += 1
        
def all_different_characters(candidate):
    return len(set(candidate)) == len(candidate)

input_lines = aoc_22.load_file("day6/input")
print(first_start_of_packet_marker(input_lines[0], 4))
print(first_start_of_packet_marker(input_lines[0], 14))
