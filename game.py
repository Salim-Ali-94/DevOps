import random
import utility


def gameManager():

	human = utility.promptUder(board)
	board[human] = "x"
	utility.renderBoard(board)
	computer = random.choice(utility.openBlocks(board))
	board[computer] = "o"
	utility.renderBoard(board)




if __name__ == "__main__":

	board = utility.initializeGame()
	gameManager()
