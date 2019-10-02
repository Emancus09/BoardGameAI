from frozendict import frozendict
from collections import deque

#===================================#
#               Move                #
#===================================#
class InvalidMoveException(Exception):
	pass
	
class Move:
	def __init__(self, x, y):
		self._x = x
		self._y = y

#===================================#
#                AI                 #
#===================================#
	
class MiniMaxAB:
	def makeMove(self, gameState):
		#hard-code opening move for efficiency (makes opening 3 times faster)
		if gameState.getTurn() == 0:
			gameState.makeMove(Move(0,0))
			return
			
		#Use minimax to find remaining moves
		move = None
		if gameState.getTurn() % 2 == 0:
			val, move = self.getMinMove(gameState, -1, -2, 2)
		else:
			val, move = self.getMaxMove(gameState, -1, -2, 2)
		gameState.makeMove(move)

	def getMaxMove(self, gameState, height, alpha, beta):
		#Check if game state is final
		h = gameState.getWinner()
		if h != None:
			return (h, None)
		
		#Maximize heuristic
		maxMove = None
		maxValue = -2
	
		#Iterate over spaces
		for y in range(0,3):
			for x in range(0,3):
				#Try available moves
				if gameState.getSpace(x,y) == 0:
					move = Move(x, y)
					gameState.makeMove(move)
					#Get minimum value of move
					value, ignore = self.getMinMove(gameState, height - 1, alpha, beta)
					#Select move with maximum minimum value
					if value > maxValue:
						maxMove = move
						maxValue = value
					#Try another move
					gameState.undoMove()
					
					#Compare against alpha-beta
					if maxValue >= beta:
						return (maxValue, maxMove)
					if maxValue > alpha:
						alpha = maxValue
		
		return (maxValue, maxMove)

	def getMinMove(self, gameState, height, alpha, beta):
		#Check if game state is final
		h = gameState.getWinner()
		if h != None:
			return (h, None)
		
		#Minimize heuristic
		minMove = None
		minValue = 2
	
		#Iterate over spaces
		for y in range(0,3):
			for x in range(0,3):
				#Try available moves
				if gameState.getSpace(x,y) == 0:
					move = Move(x, y)
					gameState.makeMove(move)
					#Get maximum value of move
					value, ignore = self.getMaxMove(gameState, height - 1, alpha, beta)
					#Select move with minimum maximum value
					if value < minValue:
						minMove = move
						minValue = value
					#Try another move
					gameState.undoMove()

					#Compare against alpha-beta
					if minValue <= alpha:
						return (minValue, move)
					if minValue < beta:
						beta = minValue
		
		return (minValue, minMove)
		
#===================================#
#              Player               #
#===================================#

class Player:
	def __init__(self, name, ai):
		self.__name = name
		self.__ai = ai
		
	def getName(self):
		return self.__name
		
	def makeMove(self, gameState):
		self.__ai.makeMove(gameState)

#===================================#
#            Game State             #
#===================================#

class GameState:
	__translate = frozendict({
		-1 	: 'X',
		0 	: ' ',
		1 	: 'O'
	})

	def __init__(self, playerX, playerO):
		self.__spaces = [[0,0,0],[0,0,0],[0,0,0]]
		self.__playerX = playerX
		self.__playerO = playerO
		self.__turnStack = deque()
		self.__turn = 0

	def printState(self):
		print("+---+---+---+")
		for row in self.__spaces:
			print("|", end = "")
			for space in row:
				print(" %s " % self.__translate[space], end = "")
				print("|", end = "")
			print()
			print("+---+---+---+")
			
	def makeMove(self, move):
		if move._x < 0 or move._y < 0 or move._x > 2 or move._y > 2:
			raise InvalidMoveException('This space is out of bounds!')
		if (self.__spaces[move._y][move._x] != 0):
			raise InvalidMoveException('This space is already taken!')
		else:
			self.__turnStack.append(move)
			self.__spaces[move._y][move._x] = -1 if self.__turn % 2 == 0 else 1
			self.__turn += 1
			
	def undoMove(self):
		if len(self.__turnStack) == 0:
			return None
		else:
			prevTurn = self.__turnStack.pop()
			self.__spaces[prevTurn._y][prevTurn._x] = 0
			self.__turn -= 1
			
	def getWinner(self):
		#Check rows
		for row in self.__spaces:
			sumRow = 0;
			for space in row:
				sumRow += space;
			if sumRow == -3: return -1
			if sumRow == 3: return 1
			
		#Check columns
		for i in range(0,3):
			sumColumn = 0;
			for row in self.__spaces:
				sumColumn += row[i];
			if sumColumn == -3: return -1
			if sumColumn == 3: return 1
			
		#Check diagonals
		sumDiag = self.__spaces[0][0] + self.__spaces[1][1] + self.__spaces[2][2]
		if sumDiag == -3: return -1
		if sumDiag == 3: return 1
		sumDiag = self.__spaces[0][2] + self.__spaces[1][1] + self.__spaces[2][0]
		if sumDiag == -3: return -1
		if sumDiag == 3: return 1
		
		#Check tie
		for row in self.__spaces:
			for space in row:
				if space == 0:
					return None
		
		return 0
	
	def getTurn(self):
		return self.__turn
	
	def getSpace(self, x, y):
		return self.__spaces[y][x]
		
#===================================#
#               Main                #
#===================================#

#Initialize variables
players = [Player('X', MiniMaxAB()), Player('O', MiniMaxAB())]
game = GameState(players[0], players[1])
winner = None

#Game loop
while(winner == None):
	game.printState()
	input()
	players[game.getTurn() % 2].makeMove(game)
	winner = game.getWinner()
	
#Print final game state
game.printState()
#Print winner
if winner == 0:
	print("It's a tie!")
else:
	print("%d wins!" % winner)