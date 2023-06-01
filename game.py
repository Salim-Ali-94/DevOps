import random
import utility


def gameManager():

	utility.renderBoard(board)
	human = input(f"\n\nPlease select an available space: {', '.join(utility.openBlocks(board))}\n\n")
	board[human] = "x"
	utility.renderBoard(board)
	computer = random.choice(utility.openBlocks(board))
	board[computer] = "o"
	utility.renderBoard(board)




if __name__ == "__main__":

	board = utility.initializeGame()
	gameManager()
