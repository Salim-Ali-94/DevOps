import random
import utility


def gameManager():

	while True:

		human = utility.promptUser(board)
		board[human] = "x"
		utility.renderBoard(board)
		utility.gameState(board)
		computer = random.choice(utility.openBlocks(board))
		board[computer] = "o"
		utility.renderBoard(board)
		utility.gameState(board)




if __name__ == "__main__":

	board = utility.initializeGame()
	gameManager()
