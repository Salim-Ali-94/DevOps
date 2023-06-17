import os
import sys
from constants import WINNING_STATES


boardState = lambda board, player = " ": [key for key, value in board.items() if (value == player)]
extractStates = lambda board: { "x": boardState(board, "x"),
								"o": boardState(board, "o") }

def action(board):

	best = -10
	positions = boardState(board)
	position = positions[0]

	for cell in positions:

		board[cell] = "o"
		score = minmax(board, "x")
		board[cell] = " "

		if (score > best):

			best = score
			position = cell

	return position


def minmax(board, player):

	if checkTerminal(board):

		return evaluateScore(board)

	positions = boardState(board)
	score = -10 if (player == "o") else 10

	for cell in positions:

		board[cell] = player
		reward = minmax(board, "x" if (player == "o") else "o")
		board[cell] = " "
		score = max(score, reward) if (player == "o") else min(score, reward)

	return score


def checkTerminal(board):

	if ((len(boardState(board)) == 0) or
		checkStates(board)):

		return True

	return False


def evaluateScore(board):

	states = extractStates(board)
	x = states["x"]
	o = states["o"]

	for state in WINNING_STATES:

		X, O = 0, 0

		for position in state:

			if position in x:

				X += 1

			elif position in o:

				O += 1

			if (X >= 3):

				return -1

			elif (O >= 3):

				return 1

	return 0


def renderBoard(board):

	os.system("cls")
	print()
	print("\t     |     |     ")
	print(f"\t  {board['1']}  |  {board['2']}  |  {board['3']}  ")
	print("\t     |     |     ")
	print("\t-----+-----+-----")
	print("\t     |     |     ")
	print(f"\t  {board['4']}  |  {board['5']}  |  {board['6']}  ")
	print("\t     |     |     ")
	print("\t-----+-----+-----")
	print("\t     |     |     ")
	print(f"\t  {board['7']}  |  {board['8']}  |  {board['9']}  ")
	print("\t     |     |     ")
	print()


def initializeGame():

	board = { "1": " ",
			  "2": " ",
			  "3": " ",
			  "4": " ",
			  "5": " ",
			  "6": " ",
			  "7": " ",
			  "8": " ",
			  "9": " " }

	return board


def promptUser(board):

	renderBoard(board)
	position = input()

	while (position.lower().lstrip().rstrip() not in boardState(board)):

		renderBoard(board)
		position = input()

	return position


def gameState(board):

	if ((len(boardState(board)) == 0) or
		checkStates(board)):

		sys.exit()


def checkStates(board):

	states = extractStates(board)
	x = states["x"]
	o = states["o"]

	for state in WINNING_STATES:

		X, O = 0, 0

		for position in state:

			if position in x:

				X += 1

			elif position in o:

				O += 1

			if ((X >= 3) or
				(O >= 3)):

				return True

	return False
