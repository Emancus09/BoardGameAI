import random
import time

from frozendict import frozendict
from collections import deque
import math

#===================================#
#               Move                #
#===================================#
class InvalidMoveException(Exception):
	pass
	
class Move:
	def __init__(self, x, y, prevX = None, prevY = None):
		self._x = x
		self._y = y
		self._prevX = prevX
		self._prevY = prevY

#===================================#
#                AI                 #
#===================================#
class HumanPlayer:
	def makeMove(self, gameState):
		while True:
			str = input("To place a piece, enter the coordinates of a blank space.\nTo move a piece, enter the coordinates of your own space followed by the coordinates of the target space.\nEnter move: ")
			if str == "undo":
				gameState.undoMove()
				gameState.undoMove()
				return
			args = str.split(" ")
			try:
				if len(args) == 2:
					gameState.makeMove(Move(ord(args[0].lower()) - ord('a'), int(args[1]) - 1))
				elif len(args) == 4:
					gameState.makeMove(Move(ord(args[2].lower()) - ord('a'), int(args[3]) - 1, ord(args[0].lower()) - ord('a'), int(args[1]) - 1))
				else:
					print("That is not a valid input! Try again.")
					continue
			except InvalidMoveException as e:
				print(e)
				continue
			except (ValueError, TypeError) as e:
				print("That is not a valid input! Try again.")
				continue
			break
	
class MiniMaxAB:

	def __init__(self, heuristic):
		self.evaluate = heuristic

	def makeMove(self, gameState):
		#hard-code opening move for efficiency (makes opening 3 times faster)
		if gameState._turn < 2:
			self.determineInitialKernel(gameState)
			gameState.makeMove(Move(self.__kernelX, self.__kernelY))
			print(f"Move made: {chr(self.__kernelX + 65)} {self.__kernelY + 1}")
			return
			
		#Use minimax to find remaining moves
		move = None
		depth = 2
		bound = 1000000 + depth - 1
		self.__moveStartTime = time.time()
		if gameState._turn % 2 == 0:
			val, move = self.getMinMove(gameState, depth, -bound, bound)
		else:
			val, move = self.getMaxMove(gameState, depth, -bound, bound)
		print(f"Time elapsed: {time.time() - self.__moveStartTime:.3f}")
		#Update kernel
		self.__kernelX = move._x
		self.__kernelY = move._y
		if (move._prevX != None):
			print(f"Move made: {chr(move._prevX + 65)} {move._prevY + 1} -> {chr(move._x + 65)} {move._y + 1}")
		else:
			print(f"Move made: {chr(move._x + 65)} {move._y + 1}")
		gameState.makeMove(move)

	def determineInitialKernel(self, gameState):
		#Try center
		self.__kernelX = int(gameState._sizex / 2)
		self.__kernelY = int(gameState._sizey / 2)
		#Otherwise, try spot to the right
		if (gameState._spaces[self.__kernelY][self.__kernelX] != 0):
			self.__kernelX = self.__kernelX + 1

	def getMaxMove(self, gameState, height, alpha, beta):
		#Check if game state is final
		winner = gameState.getWinner()
		if winner != None:
			return (winner * (1000000 + height), None)
			
		#If we have reached maximum search depth or if we have run out of computation time, evaluate game state
		if height == 0:# or (time.time() - self.__moveStartTime) > 4.99:
			return (self.evaluate(gameState), None)
		
		#Maximize heuristic
		maxMove = None
		maxValue = -1000000 - height
		
		piecesLeft = gameState._xPiecesLeft if gameState._turn % 2 == 0 else gameState._oPiecesLeft
		crrtPlayer = -1 if gameState._turn % 2 == 0 else 1
		#Iterate over spaces by spiraling around kernel
		for w2 in range(1, max(max(gameState._sizex - self.__kernelX - 1, self.__kernelX), max(gameState._sizey - self.__kernelY - 1, self.__kernelY)) + 1):
			#Create range of positions in Y to visit
			listY = range(self.__kernelY - w2, self.__kernelY + w2 + 1)
			#Randomly reorder this list
			rlistY = random.sample(listY, (self.__kernelY + w2 + 1) - (self.__kernelY - w2))
			#Ensure that spaces tested fall within bounds of board
			for y in [y for y in rlistY if y >= 0 and y < gameState._sizey]:
				#Create range of positions in X to visit
				listX = range(self.__kernelX - w2, self.__kernelX + w2 + 1)
				#Randomly reorder the list
				rlistX = random.sample(listX,(self.__kernelX + w2 + 1) - (self.__kernelX - w2))
				#Ensure that spaces tested fall within bounds of board and border of spiral
				for x  in [x for x in rlistX if x >= 0 and x < gameState._sizex and max(abs(x - self.__kernelX), abs(y - self.__kernelY)) == w2]:
					#Try placing piece
					if gameState._spaces[y][x] == 0 and piecesLeft > 0:
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
						if maxValue > alpha:
							alpha = maxValue
						if alpha >= beta:
							return (maxValue, maxMove)
					
					#Try shifting piece
					elif gameState._spaces[y][x] == crrtPlayer and gameState._shiftsLeft > 0:
						for i in [i for i in range(x - 1, x + 2) if i > -1 and i < gameState._sizex]:
							for j in [j for j in range(y - 1, y + 2) if (j > -1 and j < gameState._sizey and not(i == x and j == y) and (gameState._spaces[j][i] == 0))]:
								move = Move(i, j, x, y)
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
								if maxValue > alpha:
									alpha = maxValue
								if alpha >= beta:
									return (maxValue, maxMove)
									
		return (maxValue, maxMove)

	def getMinMove(self, gameState, height, alpha, beta):
		#Check if game state is final
		winner = gameState.getWinner()
		if winner != None:
			return (winner * (1000000 + height), None)
			
		#If we have reached maximum search depth or if we have run out of computation time, evaluate game state
		if height == 0:# or (time.time() - self.__moveStartTime) > 4.99:
			return (self.evaluate(gameState), None)
		
		#Minimize heuristic
		minMove = None
		minValue = 1000000 + height
	
		piecesLeft = gameState._xPiecesLeft if gameState._turn % 2 == 0 else gameState._oPiecesLeft
		crrtPlayer = -1 if gameState._turn % 2 == 0 else 1
		#Iterate over spaces by spiraling around kernel
		for w2 in range(1, max(max(gameState._sizex - self.__kernelX - 1, self.__kernelX), max(gameState._sizey - self.__kernelY - 1, self.__kernelY)) + 1):
			# Create range of positions in Y to visit
			listY = range(self.__kernelY - w2, self.__kernelY + w2 + 1)
			# Randomly reorder this list
			rlistY = random.sample(listY, (self.__kernelY + w2 + 1) - (self.__kernelY - w2))
			#Ensure that spaces tested fall within bounds of board
			for y in [y for y in rlistY if y >= 0 and y < gameState._sizey]:
				#Create range of positions in X to visit
				listX = range(self.__kernelX - w2, self.__kernelX + w2 + 1)
				#Randomly reorder the list
				rlistX = random.sample(listX,(self.__kernelX + w2 + 1) - (self.__kernelX - w2))
				#Ensure that spaces tested fall within bounds of board and border of spiral
				for x  in [x for x in rlistX if x >= 0 and x < gameState._sizex and max(abs(x - self.__kernelX), abs(y - self.__kernelY)) == w2]:
					#Try placing piece
					if gameState._spaces[y][x] == 0 and piecesLeft > 0:
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
						if minValue < beta:
							beta = minValue
						if beta <= alpha:
							return (minValue, move)
					
					#Try shifting piece
					elif gameState._spaces[y][x] == crrtPlayer and gameState._shiftsLeft > 0:
						for i in [i for i in range(x - 1, x + 2) if (i > -1 and i < gameState._sizex)]:
							for j in [j for j in range(y - 1, y + 2) if (j > -1 and j < gameState._sizey and gameState._spaces[j][i] == 0)]:
								move = Move(i, j, x, y)
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
								if minValue < beta:
									beta = minValue
								if beta <= alpha:
									return (minValue, move)
		
		return (minValue, minMove)
		
	#def evaluate(self, gameState):
	#	h = 0
	#
	#	#Iterate over spaces
	#	for y in range(1,gameState._sizey - 1):
	#		for x in range(2,gameState._sizex - 2):
	#			if gameState._spaces[y][x] != 0:
	#				nodeValue = 0
	#				for i in range(-1,2):
	#					nodeValue += gameState._spaces[y + i][x - 2] + gameState._spaces[y + i][x + 2]
	#					nodeValue += 0.75 * (gameState._spaces[y + i][x - 1] + gameState._spaces[y + i][x + 1])
	#				h += nodeValue
	#
	#	return h
		
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
		
	def canMove(self, gameState):
		#Get current player and number of pieces that they have left to place
		crrtPlayer = -1 if gameState._turn % 2 == 0 else 1
		piecesLeft = gameState._xPiecesLeft if crrtPlayer == -1 else gameState._oPiecesLeft
		
		#Player will always be able to move if they have more pieces
		if piecesLeft > 0:
			return True
			
		#Otherwise, we need to check if player's tiles have any free neighboring tiles
		for x in range(0, gameState._sizex):
			for y in range(0, gameState._sizey):
				if gameState._spaces[y][x] == crrtPlayer:
					#Calculate bounds for surrounding tiles
					leftBound = max(0, x-1)
					topBound = max(0, y-1)
					rightBound = min(gameState._sizex-1, x+1)
					bottomBound = min(gameState._sizey-1, y+1)
					#Check for free spaces in surrounding tiles
					for i in range(leftBound, rightBound+1):
						for j in range(topBound, bottomBound+1):
							#This loop will check if center tile is free as well. Since center tile is occupied by current player, this will have no effect.
							if gameState._spaces[j][i] == 0:
								return True
		
		#If player can neither place nor move a piece, they can not move
		return False

#===================================#
#            Game State             #
#===================================#

class GameState:
	translate = frozendict({
		-1 	: 'X',
		0 	: ' ',
		1 	: 'O'
	})

	def __init__(self):
		self._xPiecesLeft = 15
		self._oPiecesLeft = 15
		self._shiftsLeft = 30
		self._sizex = 12
		self._sizey = 10
		self._spaces = [[0 for x in range(self._sizex)] for y in range(self._sizey)]
		self.__turnStack = deque()
		self._turn = 0

	def printState(self):
		#Print header
		print("===================== X-RUDDER =====================")
		print(" - Turn: %d (%s)" % (self._turn, GameState.translate[-1 if self._turn % 2 == 0 else 1]))
		print(" - Pieces left for X: %d" % self._xPiecesLeft)
		print(" - Pieces left for O: %d" % self._oPiecesLeft)
		print(" - Shifts left: %d" % self._shiftsLeft)
		print("====================================================")
	
		#Print column heads
		print("   |", end = "")
		for x in range(0, self._sizex):
			print(" %s |" % chr(ord('A') + x) , end = "")
		print()
		
		#Print by row
		print("---+" * (self._sizex + 1))
		for y in range(self._sizey, 0, -1):
			print(" %*d|" % (2, y), end = "")
			for space in self._spaces[y-1]:
				print(" %s |" % self.translate[space], end = "")
			print()
			print("---+" * (self._sizex + 1))
			
	def makeMove(self, move):
		#Check that move is valid
		#Check that move is within range
		if move._x < 0 or move._y < 0 or move._x > (self._sizex - 1) or move._y > (self._sizey - 1):
			raise InvalidMoveException('This space is out of bounds!')
		#Check that space is not taken
		if self._spaces[move._y][move._x] != 0:
			raise InvalidMoveException('This space (%d, %d) is already taken!' % (move._x, move._y))
		
		#Shift piece
		if move._prevX != None:
			#Check that move is within range
			if move._prevX < 0 or move._prevY < 0 or move._prevX > self._sizex or move._prevY > self._sizey:
				raise InvalidMoveException('This space is out of bounds!')
			#Check that the piece being moved belongs to the current player
			if self._spaces[move._prevY][move._prevX] != (-1 if self._turn % 2 == 0 else 1):
				raise InvalidMoveException('That is not your piece!')
			#Check that the destination space is within range
			if abs(move._prevY - move._y) > 1 or abs(move._prevX - move._x) > 1:
				raise InvalidMoveException('Pieces can only move 1 spaces vertically, diagonally, or horizontally!')
			#Check that game has not run out of piece shifts
			if self._shiftsLeft < 1:
				raise InvalidMoveException('No more piece shifts remain!')
				
			#Else make move (we already checked above if the destination is free and within bounds)
			self._spaces[move._y][move._x] = self._spaces[move._prevY][move._prevX]
			self._spaces[move._prevY][move._prevX] = 0
			self._shiftsLeft -= 1
			
		#Else place piece
		else:
			if self._turn % 2 == 0:
				if self._xPiecesLeft < 1:
					raise InvalidMoveException('No more pieces remain!')
				self._spaces[move._y][move._x] = -1
				self._xPiecesLeft -= 1
			else:
				if self._oPiecesLeft < 1:
					raise InvalidMoveException('No more pieces remain!')
				self._spaces[move._y][move._x] = 1
				self._oPiecesLeft -= 1
				
		self.__turnStack.append(move)	
		self._turn += 1
			
	def undoMove(self):
		#If stack of moves is empty, do nothing
		if len(self.__turnStack) == 0:
			return None
			
		prevTurn = self.__turnStack.pop()
		self._turn -= 1
		
		if prevTurn._prevX != None:
			self._spaces[prevTurn._prevY][prevTurn._prevX] = self._spaces[prevTurn._y][prevTurn._x]
			self._spaces[prevTurn._y][prevTurn._x] = 0
			self._shiftsLeft += 1
			return
			
		if self._turn % 2 == 0:
			self._spaces[prevTurn._y][prevTurn._x] = 0
			self._xPiecesLeft += 1
		else:
			self._spaces[prevTurn._y][prevTurn._x] = 0
			self._oPiecesLeft += 1
			
	def getWinner(self):	
		winner = None
		#Iterate over possible middle spaces
		for y in range(1,(self._sizey - 1)):
			for x in range(1,(self._sizex - 1)):
				#Check for X centered around middle space
				if self._spaces[y][x] != 0 and 4 * self._spaces[y][x] == self._spaces[y - 1][x - 1] + self._spaces[y + 1][x + 1] + self._spaces[y - 1][x + 1] + self._spaces[y + 1][x - 1] and self._spaces[y][x - 1] + self._spaces[y][x + 1] != -2 * self._spaces[y][x]:
					#If more than one X was formed by the last move, the winner is the last to move
					if winner == -self._spaces[y][x]:
						return 1 if self._turn % 2 == 0 else -1
					winner = self._spaces[y][x]
		#If a winning x was found, return winner
		if winner != None:
			return winner
			
		#If out of moves, return draw
		if self._shiftsLeft == 0 and (self._xPiecesLeft == self._oPiecesLeft == 0):
			return 0
		
		#Else, game is not over
		return None
		
#===================================#
#               Main                #
#===================================#
def h1(gameState):
	h = 0

	# Iterate over spaces
	for y in range(1, gameState._sizey - 1):
		for x in range(2, gameState._sizex - 2):
			if gameState._spaces[y][x] != 0:
				# Get value of piece
				nodeValue = 0
				factor = 1.0
				if -gameState._spaces[y][x] == gameState._spaces[y][x + 1] == gameState._spaces[y][x - 1]:
					continue
				for i in range(-1, 2):
					if i != 0 and (
							gameState._spaces[y + i][x - 1] == -gameState._spaces[y][x] or gameState._spaces[y + i][
						x + 1] == -gameState._spaces[y][x]):
						continue
					nodeValue += gameState._spaces[y + i][x - 2] + gameState._spaces[y + i][x + 2]
					nodeValue += 0.5 * (gameState._spaces[y + i][x - 1] + gameState._spaces[y + i][x + 1])
				h += factor * nodeValue

	# Get number of pieces
	h = h - gameState._xPiecesLeft + gameState._oPiecesLeft

	return h

def h2(gameState):

	h = 0

	# Iterate over spaces
	for y in range(1, gameState._sizey - 1):
		for x in range(2, gameState._sizex - 2):
			if gameState._spaces[y][x] != 0:
				nodeValue = 0
				for i in range(-1, 2):
					nodeValue += gameState._spaces[y + i][x - 2] + gameState._spaces[y + i][x + 2]
					nodeValue += 0.75 * (gameState._spaces[y + i][x - 1] + gameState._spaces[y + i][x + 1])
				h += nodeValue
	return h

gamesPlayed = 0
oWinCount = 0
xWinCount = 0
tieCount = 0
weirdCount = 0

for x in range(100):

	#Initialize variables
	players = [Player('X', MiniMaxAB(h1)), Player('O', MiniMaxAB(h2))]

	game = GameState()
	winner = None

	#Game loop
	while(winner == None):
		#Update display
		game.printState()
		#Do turn
		crrtPlayer = game._turn % 2
		if players[crrtPlayer].canMove(game):
			players[game._turn % 2].makeMove(game)
		else:
			print("Current player can't move!")
			game._turn += 1
		#Check for winner
		winner = game.getWinner()

	#Print final game state
	game.printState()
	gamesPlayed += 1
	#Print winner
	if winner == 0:
		print("It's a tie!")
		tieCount += 1
	elif winner == -1:
		print("%s wins!" % GameState.translate[winner])
		xWinCount += 1
	elif winner == 1:
		print("%s wins!" % GameState.translate[winner])
		oWinCount += 1
	else:
		weirdCount += 1


print(f"games played {gamesPlayed}\no win count: {oWinCount}\nx win count: {oWinCount}\ntie count: {tieCount}\nweird count: {weirdCount}")