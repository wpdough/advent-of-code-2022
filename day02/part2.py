import sys

f = open(sys.argv[1], "r")
lines = f.readlines()
lines = map(lambda line: line.replace("\n", ""), lines)
lines = list(lines)

class Result:
	def __init__(self, code, points):
		self.code = code
		self.points = points

LOSE = Result("X", 0)
DRAW = Result("Y", 3)
WIN = Result("Z", 6)
POSSIBLE_RESULTS = [LOSE, DRAW, WIN]

def find_result_for_outcome(code):
	for result in POSSIBLE_RESULTS:
		if (result.code == code):
			return result

ROCK = "A"
PAPER = "B"
SCISSORS = "C"
CHOICES = [ROCK, PAPER, SCISSORS]

def shape_score(choice):
	return 1 if choice == ROCK else 2 if choice == PAPER else 3

def evaluate_round(opponent_choice, player_choice):
	if opponent_choice == player_choice:
		return DRAW
	elif player_choice == ROCK and opponent_choice == SCISSORS:
		return WIN
	elif player_choice == PAPER and opponent_choice == ROCK:
		return WIN
	elif player_choice == SCISSORS and opponent_choice == PAPER:
		return WIN
	else:
		return LOSE

def choose_shape(opponent_choice, desired_result):
	for choice in CHOICES:
		outcome = evaluate_round(opponent_choice, choice)
		if outcome == desired_result:
			return choice

scores = []
for line in lines:
	input = line.split(" ")
	opponent_choice = input[0]
	desired_result = find_result_for_outcome(input[1])
	player_choice = choose_shape(input[0], desired_result)
	score = shape_score(player_choice) + desired_result.points
	scores.append(score)

total_score = sum(scores)
print(total_score)
