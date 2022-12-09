from common import aoc_22_common as aoc_22

rows = aoc_22.load_file("day8/input")

# Compile a grid
columns = list()
first_line = rows[0]

def none_equal_or_greater(str, height):
    return len(list(filter(lambda h: int(h) >= height, str))) == 0

def all_shorter_either_side(str, index):
    before = str[:index]
    after = str[index + 1:]
    height = int(str[index])
    return none_equal_or_greater(before, height) or none_equal_or_greater(after, height)
    

def is_visible(row_index, column_index):
    if (row_index == 0 or column_index == 0):
        return True
    if (row_index == (len(rows) - 1) or (column_index == len(columns) -1)):
        return True
    row = rows[row_index]
    column = columns[column_index]
    # Visible if in either direction in either row or column all trees are shorter than this one
    return all_shorter_either_side(row, column_index) or all_shorter_either_side(column, row_index)

def viewing_distance_in_direction(heights, height):
    index = 1
    while (index < len(heights) and heights[index - 1] < height):
        index += 1
    return index

def get_before(str, index):
    if (index == 0):
        return []
    return list(str[index - 1:: -1])

def scenic_score_on_one_axis(str, index):
    before_in_order = get_before(str, index)
    after = list(str[index + 1:])
    height = int(str[index])
    heights_before = [int(s) for s in before_in_order]
    heights_after = [int(s) for s in after]
    return viewing_distance_in_direction(heights_before, height) * viewing_distance_in_direction(heights_after, height)    

def scenic_score(row_index, column_index):
    row = rows[row_index]
    column = columns[column_index]
    return scenic_score_on_one_axis(row, column_index) * scenic_score_on_one_axis(column, row_index)

for i in range(0, len(first_line)):
    columns.append ("")
    for j in range(0, len(rows)):
        columns[i] = columns[i] + (rows[j][i])

count_visible = 0
for i in range(0, len(rows) ):
    for j in range(0, len(columns)):
        if (is_visible(i, j)):
            count_visible += 1

print (str(count_visible))

print(scenic_score(23, 47))

max_scenic_score = 0
for i in range(0, len(rows) ):
    for j in range(0, len(columns)):
        score = scenic_score(i, j)
        if (score > max_scenic_score):
            max_scenic_score = score
print(max_scenic_score)
