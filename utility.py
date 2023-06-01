

def renderBoard(board):


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

	'''function to reset all game variables'''

	board = { "1": "",
			 "2": "",
			 "3": "",
			 "4": "",
			 "5": "",
			 "6": "",
			 "7": "",
			 "8": "",
			 "9": "" }

	return board
