from common import aoc_22_common as aoc_22

# Move based on the index corresponding to original, i.e. the value at that index is the new position of the original value in the
# list

def move(indices, index, new_index, debug = False):
    if (new_index < 0 or new_index >= len(indices)):
        print("Unexpected move to a new index < 0 " + str(new_index) + " for index " + str(index))
        raise ValueError("Unexpected move to a new index < 0 for index " + str(index))
    l = len(indices)
    original_index = indices[index]
    # How do we adjust accordingly
    for i in range(0, l):
        current_index = indices[i]
        if original_index > new_index:
            if current_index >= new_index  and current_index < original_index:
            # We need to shuffle from original index upwards 1 to make room to shuttle it in
                indices[i] = current_index + 1
        else:
            if current_index <= new_index and current_index > original_index:
                indices[i] = current_index - 1
    indices[index] = new_index
    return indices

def mixed(encrypted, mixed_indices):
    adjusted = [0] * len(mixed_indices)
    for i in range(0, len(mixed_indices)):
        adjusted[mixed_indices[i]] = encrypted[i]
    return adjusted

def mix(encrypted, indices, index, debug = False):
    l = len(encrypted)
    shift = encrypted[index]
    original_index = indices[index]
    absolute_bounded_shift = calc_absolute_bounded_shift(indices, shift)
    if(debug):
        print("Original index: " + str(original_index))
        print("Shift: " + str(shift))
        print("Bounded shift: " + str(absolute_bounded_shift))


    if (original_index + absolute_bounded_shift) >= len(indices):
        new_index = 1 +  ((original_index + absolute_bounded_shift) % l)
    else:
        new_index = ((original_index + absolute_bounded_shift) % l) if (original_index + absolute_bounded_shift >= 0) else (l -1 + (original_index + absolute_bounded_shift))
    return move(indices, index, new_index, debug)

def calc_absolute_bounded_shift(indices, unbounded_shift):
    l = len(indices)
    return unbounded_shift % (l - 1)

def get_nth_value(decrypted, n):
    index = n % len(decrypted)
    return decrypted[index]

moved = move([0,1,2,3,4,5, 6], 3, 4)
print(moved)
print(mixed([4, 5, 6, 1, 7, 8, 9], moved))
moved = move([0, 1, 2, 3, 4, 5, 6], 1,  5)
print(moved)
print(mixed([4, -2, 5, 6, 7, 8, 9], moved))

print("Testing moving further left than length of the encrypted array")
encrypted = [1, 2, -12, 3, 4, 5]
indices = [0, 1, 2, 3, 4, 5]

print("Positive bounded shift calculation")
print(calc_absolute_bounded_shift(indices, 10))
print("Negative bounded shift calculation")
print(calc_absolute_bounded_shift(indices, -12))

updated = mix(encrypted, indices, 2, True)
print(updated)

print("Testing output completed")
lines = aoc_22.load_file("day20/test_input")
encrypted = [int(l) for l in lines]
length = len(encrypted)
original_indices = list(range(0, length))
adjusted_indices = list(range(0, length))
for x in range(0, length):
    mixed_indices = mix(encrypted, adjusted_indices, x, x == 2)
print(mixed_indices)

result = mixed(encrypted, mixed_indices)

zero_index = result.index(0)
print(result)
coordinates = list()
for x in range(1000, 4000, 1000):
    coordinates.append(get_nth_value(result, x + zero_index))

print(coordinates)
print(sum(coordinates))

print("Part II")
decryption_key = 811589153
part_2_encrypted = [(decryption_key * int(l)) for l in aoc_22.load_file("day20/input")]
part_2_length = len(part_2_encrypted)
original_part2_indices = list(range(0, part_2_length))
mixed_part2_indices = list(range(0, part_2_length))

print(-10 % 6)
print(part_2_encrypted)
for x in range(0, 10):
    for i in range(0, part_2_length):
        mixed_part2_indices = mix(part_2_encrypted, mixed_part2_indices, i) 

part_2_result = mixed(part_2_encrypted, mixed_part2_indices)
zero_index = part_2_result.index(0)

part_2_coordinates = list()
for x in range(1000, 4000, 1000):
    part_2_coordinates.append(get_nth_value(part_2_result, x + zero_index))

print(part_2_coordinates)
print(sum(part_2_coordinates))
