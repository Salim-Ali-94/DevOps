import random
# import utility
from utility import promptUser, renderBoard, gameState, boardState, initializeGame
# from utility import *


def gameManager():

	while True:

		human = promptUser(board)
		board[human] = "x"
		renderBoard(board)
		gameState(board)
		computer = random.choice(boardState(board))
		board[computer] = "o"
		renderBoard(board)
		gameState(board)




if __name__ == "__main__":

	board = initializeGame()
	gameManager()
