import os


openBlocks = lambda board: [key for key, value in board.items() if (value == " ")]

def renderBoard(board):


	os.system("cls")
	print()
	print()
	print("     |     |     ")
	print(f"  {board['1']}  |  {board['2']}  |  {board['3']}  ")
	print("     |     |     ")
	print("-----+-----+-----")
	print("     |     |     ")
	print(f"  {board['4']}  |  {board['5']}  |  {board['6']}  ")
	print("     |     |     ")
	print("-----+-----+-----")
	print("     |     |     ")
	print(f"  {board['7']}  |  {board['8']}  |  {board['9']}  ")
	print("     |     |     ")
	print()
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

	utility.renderBoard(board)
	human = input(f"\n\nPlease select an available space: {', '.join(utility.openBlocks(board))}\n\n")

	while (human.lower().lstrip().rstrip() not in utility.openBlocks(board)):

		utility.renderBoard(board)
		human = input(f"\n\nPlease select an available space: {', '.join(utility.openBlocks(board))}\n\n")

	return human