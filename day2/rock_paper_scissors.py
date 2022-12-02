ROCK = 1
PAPER = 2
SCISSORS = 3

LOSE = 0
DRAW = 3
WIN = 6

OPPONENT_CODES = ["A", "B", "C"]
MY_CODES = ["X", "Y", "Z"]

def strategy_line_to_score(line):
    action_codes = line.split(" ")
    opponent_code = action_codes[0]
    my_code = action_codes[1]
    opponent_play = 1 + OPPONENT_CODES.index(opponent_code)
    my_play = 1 + MY_CODES.index(my_code)
    return score_for_round(my_play, opponent_play)

def result_score(me, opponent):
    if (me == opponent):
        return DRAW
    if ((me == ROCK and opponent == SCISSORS) or
        (me == SCISSORS and opponent == PAPER) or
        (me == PAPER and opponent == ROCK)):
        return WIN
    return LOSE

def score_for_round(me, opponent):
    return me + result_score(me, opponent)

def load_strategy_file():
    loaded = list()
    input_file_name = "input-2.txt"

    input_file = open(input_file_name)
    for (line) in input_file:
        loaded.append(line.strip())
    input_file.close()
    return loaded

def strategy_line_to_score_ii(line):
    action_codes = line.split(" ")
    opponent_code = action_codes[0]
    my_code = action_codes[1]
    opponent_play = 1 + OPPONENT_CODES.index(opponent_code)
    my_play = my_play_for_result(my_code, opponent_play)
    return score_for_round(my_play, opponent_play)

def my_play_for_result(my_code, opponent_play):
    if (my_code == "X"):
        return my_play_to_lose(opponent_play)
    if (my_code == "Y"):
        return my_play_to_draw(opponent_play)
    return my_play_for_win(opponent_play)

def my_play_for_win(opponent_play):
    if (opponent_play == SCISSORS):
        return ROCK
    return opponent_play + 1

def my_play_to_draw(opponent_play):
    return opponent_play

def my_play_to_lose(opponent_play):
    if (opponent_play == ROCK):
        return SCISSORS
    return opponent_play - 1


lines = load_strategy_file()
round_scores = [strategy_line_to_score(l) for l in lines]
total = sum(round_scores)
print(total)

print("Part 2")
# lines still the same but have different meaning
round_scores_ii = [strategy_line_to_score_ii(l) for l in lines]
total_ii = sum(round_scores_ii)
print(total_ii)
