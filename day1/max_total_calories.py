import itertools as it

def group_calories(calories_list):
    grouped_strings = [list(group) for key, group in it.groupby(calories_list, lambda s: s == "") if not key]
    return grouped_strings

def load_calories_file():
    loaded = list()
    input_file_name = "input.txt"

    input_file = open(input_file_name)
    for (line) in input_file:
        loaded.append(line.strip())
    input_file.close()
    return loaded

def total_group(grouped_strings):
    numbers = [int(s) for s in grouped_strings]
    return sum(numbers)



loaded = load_calories_file()
grouped = group_calories(loaded)
totals = [total_group(g) for g in grouped]
print("Max total is: ")
print(max(totals))
print("Sum of top 3 totals is")
sorted_totals = sorted(totals, reverse = True)
top3 = sorted_totals[:3]
print(sum(top3))

