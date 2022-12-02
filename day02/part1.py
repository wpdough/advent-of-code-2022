import sys

f = open(sys.argv[1], "r")
lines = f.readlines()
lines = map(lambda line: line.replace("\n", ""), lines)
lines = map(lambda line: line.replace("X", "A").replace("Y", "B").replace("Z", "C"), lines)
lines = list(lines)

rock = "A"
paper = "B"
scissors = "C"

def shape_score(choice):
	return 1 if choice == rock else 2 if choice == paper else 3

def outcome_score(opponent_choice, player_choice):
	if opponent_choice == player_choice:
		return 3
	elif player_choice == rock and opponent_choice == scissors:
		return 6
	elif player_choice == paper and opponent_choice == rock:
		return 6
	elif player_choice == scissors and opponent_choice == paper:
		return 6
	else:
		return 0

scores = []
for line in lines:
	choices = line.split(" ")
	shape = shape_score(choices[1])
	outcome = outcome_score(choices[0], choices[1])
	round_score = shape + outcome
	scores.append(round_score)

total_score = sum(scores)
print(total_score)
