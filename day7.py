from common import aoc_22_common as aoc_22
import re

# Need matchers for directory and file
FILE = re.compile("^(\d+).*$")
CD = re.compile("^\$ cd ([a-zA-Z0-9_].*)")
END_SUBDIRECTORY = "$ cd .."

THRESHOLD_PART_ONE = 100000
CAPACITY = 70000000
REQUIRED_UNUSED = 30000000

input_lines = aoc_22.load_file("day7/input")
print(input_lines)
input_lines_it = iter(input_lines)

dir_sizes = list()
root_size = 0

def next_command():
    return next(input_lines_it, None)

def process_directory(dir_name, end_dir_line):

    print ("Processing directory " + dir_name)

    x = ""
    directory_size = 0
    while(x != end_dir_line and x != None):
        print(str(end_dir_line))
        file_match = FILE.search(x)
        if (file_match) != None:
            directory_size += int(file_match.group(1))

        cd_match = CD.search(x)
        if (cd_match) != None:
            directory_size += process_directory(cd_match.group(1), END_SUBDIRECTORY)

        x = next_command()
    dir_sizes.append(directory_size)
    print (directory_size)
    return directory_size

current = ""
while (current != "$ cd /"):
    current = next_command()

size = process_directory("/", None)

print(dir_sizes)

filtered_dir_sizes = filter(lambda t: t <= 100000, dir_sizes)
total = sum(filtered_dir_sizes)
print(total)

# ===================== PART 2 =====================================
# Largest must be the root directory since it contains all others
largest = max(dir_sizes) 

current_unused = CAPACITY - largest
print ("Current unused " + str(current_unused))
minimum_to_delete = REQUIRED_UNUSED - current_unused
print ("Required to delete " + str(minimum_to_delete))

dir_to_delete = min(filter(lambda s: s >= minimum_to_delete, dir_sizes))
print (dir_to_delete)