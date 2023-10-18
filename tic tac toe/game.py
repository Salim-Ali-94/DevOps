import utility


def gameManager():

	board = utility.initializeGame()

	while True:

		human = utility.promptUser(board)
		board[human] = "x"
		utility.renderBoard(board)
		utility.gameState(board)
		computer = utility.action(board)
		board[computer] = "o"
		utility.renderBoard(board)
		utility.gameState(board)




if __name__ == "__main__":

	gameManager()
