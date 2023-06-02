import os
import sys
from constants import WINNING_STATES


# openBlocks = lambda board, player = " ": [key for key, value in board.items() if (value == player)]
boardState = lambda board, player = " ": [key for key, value in board.items() if (value.lower().lstrip().rstrip() == player.lower().lstrip().rstrip())]
extractStates = lambda board: { "x": boardState(board, "x"),
								"o": boardState(board, "o") }

def renderBoard(board):


	os.system("cls")
	print()
	# print()
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
	# print()
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
	position = input(f"\n\nPlease select an available space: {', '.join(boardState(board))}\n\n")

	while (position.lower().lstrip().rstrip() not in boardState(board)):

		renderBoard(board)
		position = input(f"\n\nPlease select an available space: {', '.join(boardState(board))}\n\n")

	return position


def gameState(board):

	if ((len(boardState(board)) == 0) or
		(checkStates(board))):

		sys.exit()


def checkStates(board):

	states = extractStates(board)
	x = states["x"]
	o = states["o"]

	for state in WINNING_STATES:

		X, O = 0, 0

		for position in state:

			if position in x: X += 1
			elif position in o: O += 1

			if ((X >= 3) or
				(O >= 3)):

				return True

	return False
