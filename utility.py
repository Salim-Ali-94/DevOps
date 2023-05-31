

def displayBoard(board):

	print()
	print()
	print(f"     |     |     ")
	print(f"  {board['1']}  |  {board['2']}  |  {board['3']}  ")
	print(f"     |     |     ")
	print(f"-----+-----+-----")
	print(f"     |     |     ")
	print(f"  {board['4']}  |  {board['5']}  |  {board['6']}  ")
	print(f"     |     |     ")
	print(f"-----+-----+-----")
	print(f"     |     |     ")
	print(f"  {board['7']}  |  {board['8']}  |  {board['9']}  ")
	print(f"     |     |     ")
	print()
	print()


def initializeGame():

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