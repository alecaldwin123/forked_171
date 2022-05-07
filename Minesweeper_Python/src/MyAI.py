# ==============================CS-199==================================
# FILE:			MyAI.py
#
# AUTHOR: 		Justin Chung
#
# DESCRIPTION:	This file contains the MyAI class. You will implement your
#				agent in this file. You will write the 'getAction' function,
#				the constructor, and any additional helper functions.
#
# NOTES: 		- MyAI inherits from the abstract AI class in AI.py.
#
#				- DO NOT MAKE CHANGES TO THIS FILE.
# ==============================CS-199==================================

from AI import AI
from Action import Action
import numpy as np
import random
import time


class MyAI( AI ):

	def __init__(self, rowDimension, colDimension, totalMines, startX, startY):

		
		self.row = rowDimension
		self.col = colDimension
		self.numOfMines = totalMines
		self.numOfFlag = 0 #should be one by the end 
		self.numUncoveredtiles = 1
		#self.unTiles = []
		#self.flag = []

		### New Attempt
		# there are 3 type of tiles

		## 1. Uncovered tile
		## 2. flagged tile
		## 3. untouched tile

		self.label = np.full((rowDimension, colDimension), -1)
		self.elabel = np.full((rowDimension, colDimension), -1)
		self.refLabel = np.full((rowDimension, colDimension), "") # this creates a reference board, an empty string indicates the tile has not been touched yet
		# we can label each tile as a flagged and uncovered

		self.amove = Action(AI.Action.UNCOVER, startX, startY) #uncovers the first move tile 
		self.time_elapsed = 0.0

		

		

		

		########################################################################
		#							YOUR CODE ENDS							   #
		########################################################################

		
	def getAction(self, number: int):

		#Note: The max time I'm putting rn is arbitrary since idk how much time there really is
		MAX_TIME = 1000
		remaining_time = MAX_TIME - self.time_elapsed

		if(remaining_time < 3):
			random_coords = self.chooseRandom()
			print("hi")
			return Action(AI.Action.UNCOVER, random_coords[0],random_coords[1])
		else:
			print("Action start!")
			ts = time.time()
		########################################################################
		#							YOUR CODE BEGINS						   #
		########################################################################
		
			#win condition= uncovered all except one tile 
			if (self.row * self.col) - self.numOfMines == self.numUncoveredtiles:
				print('Done')
				return Action(AI.Action.LEAVE)

			#check which tiles are uncovered relative to the current position
			#uncovered = [] #tiles uncovered relative to start position
			
			if number >= 0: # if the number is non negative then we work on the board

				self.refLabel[self.amove.getX(), self.amove.getY()] = 'U' # u indicates uncovered
				self.label[self.amove.getX(), self.amove.getY()] = number # the number of adjacent bombs

				numFlagged, numNoFlagged = self.markedOrUnmarked(self.amove.getX(), self.amove.getY())

				# EffectiveLabel(x) = Label(x) – NumMarkedNeighbors(x)
			
				self.elabel[self.amove.getX(), self.amove.getY()] = self.label[self.amove.getX(), self.amove.getY()] - numFlagged

				
				if self.elabel[self.amove.getX(), self.amove.getY()] == numNoFlagged: # mark all unmarked neighbors
					
					print('a')
					
					print(self.elabel[self.amove.getX(), self.amove.getY()])


					self.coverAll(self.amove.getX(), self.amove.getY(),ts)
					

				if self.elabel[self.amove.getX(), self.amove.getY()] == 0: # uncover all unmarked neighbors
					
					print('b')
					
					print(self.elabel[self.amove.getX(), self.amove.getY()])

					result = self.unCoverAll(self.amove.getX(), self.amove.getY(),ts)
					if(result == None):
						print("Returned nothing")
						coordinates = self.chooseRandom()
						self.amove = Action(AI.Action.UNCOVER, coordinates[0], coordinates[1])

						return self.amove

					else:
						return result
					

				# make a random guess
				if not self.elabel[self.amove.getX(), self.amove.getY()] == 0 and not self.elabel[self.amove.getX(), self.amove.getY()] == numNoFlagged:
					print("random guess")
					coordinates = self.chooseRandom()
					self.amove = Action(AI.Action.UNCOVER, coordinates[0], coordinates[1])

					return self.amove

				
			
				print('c')
				print(self.numUncoveredtiles)
				print(self.amove.getX(), self.amove.getY())
				print(self.elabel[self.amove.getX(), self.amove.getY()])
				print("oh we're leaving now?")
				return Action(AI.Action.LEAVE)
			else:
				print("The number is negative and we don't know what to do! Number: ", number)


			






		
		
		
		########################################################################
		#							YOUR CODE ENDS							   #
		########################################################################


	def updateELabel(self, x, y):
		#left
		self.elabel[x - 1, y] -= 1
		self.elabel[x - 1, y + 1] -= 1
		self.elabel[x - 1, y - 1] -= 1

		# right
		self.elabel[x + 1, y] -= 1
		self.elabel[x + 1, y - 1] -= 1
		self.elabel[x + 1, y + 1] -= 1

		#top
		self.elabel[x, y + 1] -= 1

		#bottom
		self.elabel[x, y - 1] -= 1
		
		return
	def coverAll(self, x, y, ts):
		# left side
		## left
		print("Hi, we're covering stuff now")
		if self.tileinBounds(x - 1, y) and self.refLabel[x - 1, y] == '':  # if coordinates is valid and it is not touched yet
			self.refLabel[x - 1, y] = 'F'
			print("hi, welcome to the left!")
			self.amove = Action(AI.Action.FLAG, x - 1, y)

			print('printing elabel before')
			print(self.elabel[x - 1, y])
			self.updateELabel(x - 1, y)
			print('fin')
			

			#time now
			tE = time.time()
			dt = tE-ts
			self.time_elapsed += dt


			return self.amove
	
		## top left
		if self.tileinBounds(x - 1, y + 1) and self.refLabel[x - 1, y + 1] == '':  
			
			print("Hi welcome to the top left!")
			self.refLabel[x - 1, y + 1] = 'F'
			self.amove = Action(AI.Action.FLAG, x - 1, y + 1)

			print('printing elabel before')
			print(self.elabel[x - 1, y + 1])
			self.updateELabel(x - 1, y + 1)
			print('fin')


			tE = time.time()
			dt = tE-ts
			self.time_elapsed += dt

			return self.amove
		
		## bottom left
		if self.tileinBounds(x - 1, y - 1) and self.refLabel[x - 1, y - 1] == '': 
			
			print("hi welcome to the bottom left")
			self.refLabel[x - 1, y 	- 1] = 'F'
			self.amove = Action(AI.Action.FLAG, x - 1, y - 1)


			print('printing elabel before')
			print(self.elabel[x - 1, y - 1])
			self.updateELabel(x - 1, y - 1)
			print('fin')

			tE = time.time()
			dt = tE-ts
			self.time_elapsed += dt

			return self.amove
		

		# right side


		## right
		if self.tileinBounds(x + 1, y) and self.refLabel[x + 1, y] == '':  
			
			
			print("hi welcome to the right!")
			self.refLabel[x + 1, y] = 'F'
			self.amove = Action(AI.Action.FLAG, x + 1, y)

			print('printing elabel before')
			print(self.elabel[x + 1, y])
			self.updateELabel(x + 1, y)
			print('fin')

			tE = time.time()
			dt = tE-ts
			self.time_elapsed += dt

			return self.amove
		
		## top right
		if self.tileinBounds(x + 1, y + 1)  and self.refLabel[x + 1, y + 1] == '':  
			
			print("hi welcome to the top right")

			self.refLabel[x + 1, y + 1] = 'F'
			self.amove = Action(AI.Action.FLAG, x + 1, y + 1)

			print('printing elabel before')
			print(self.elabel[x + 1, y + 1])
			self.updateELabel(x + 1, y + 1)
			print('fin')

			tE = time.time()
			dt = tE-ts
			self.time_elapsed += dt

			return self.amove
		
		## bottom right
		if self.tileinBounds(x + 1, y - 1) and self.refLabel[x + 1, y - 1] == '':

			print("hi welcome to the bottom right")
			self.refLabel[x + 1, y - 1] = 'F'
			self.amove = Action(AI.Action.FLAG, x + 1, y - 1)

			print('printing elabel before')
			print(self.elabel[x + 1, y - 1])
			self.updateELabel(x + 1, y - 1)
			print('fin')


			tE = time.time()
			dt = tE - ts
			self.time_elapsed += dt

			return self.amove
		

		#top 
		if self.tileinBounds(x, y + 1) and self.refLabel[x, y + 1] == '': 
			
			print("hi welcome to top")
			self.refLabel[x, y + 1] = 'F'
			self.amove = Action(AI.Action.FLAG, x, y + 1)

			print('printing elabel before')
			print(self.elabel[x, y + 1])
			self.updateELabel(x, y + 1)
			print('fin')

			tE = time.time()
			dt = tE-ts
			self.time_elapsed += dt

			return self.amove

		#bottom 
		if self.tileinBounds(x, y - 1) and self.refLabel[x, y - 1] == '':  
			
			print("hi welcome bottom")
			self.refLabel[x, y - 1] = 'F'

			self.amove = Action(AI.Action.FLAG, x, y - 1)


			print('printing elabel before')
			print(self.elabel[x, y - 1])
			self.updateELabel(x, y - 1)
			print('fin')

			tE = time.time()
			dt = tE - ts
			self.time_elapsed += dt

			return self.amove





	def unCoverAll(self, x, y,ts):
		
		print('we at uncover now')
		# left side
		## left

		print("Checking left condition")
		if self.tileinBounds(x - 1, y) and self.refLabel[x - 1, y] == '':  # if coordinates is valid and it is not touched yet
			print("hi, welcome to the left!")

			self.refLabel[x - 1, y] = 'U'
			

			self.amove = Action(AI.Action.UNCOVER, x - 1, y)
			
			
			
			

			#time now
			tE = time.time()
			dt = tE-ts
			self.time_elapsed += dt


			return self.amove
	
		print("Checking top left condition")
		## top left
		if self.tileinBounds(x - 1, y + 1) and self.refLabel[x - 1, y + 1] == '':  
			
			print("Hi welcome to the top left!")
			self.refLabel[x - 1, y + 1] = 'U'
			self.amove = Action(AI.Action.UNCOVER, x - 1, y + 1)

			


			tE = time.time()
			dt = tE-ts
			self.time_elapsed += dt

			return self.amove
		
		print("Checking bottom left condition")
		## bottom left
		if self.tileinBounds(x - 1, y - 1) and self.refLabel[x - 1, y - 1] == '': 
			
			print("hi welcome to the bottom left")
			self.refLabel[x - 1, y 	- 1] = 'U'
			self.amove = Action(AI.Action.UNCOVER, x - 1, y - 1)


			tE = time.time()
			dt = tE-ts
			self.time_elapsed += dt

			return self.amove
		

		# right side


		## right
		print("Checking right condition")
		if self.tileinBounds(x + 1, y) and self.refLabel[x + 1, y] == '':  
			
			
			print("hi welcome to the right!")
			self.refLabel[x + 1, y] = 'U'
			self.amove = Action(AI.Action.UNCOVER, x + 1, y)

			

			tE = time.time()
			dt = tE-ts
			self.time_elapsed += dt

			return self.amove
		
		## top right
		print("Checking top right condition")
		if self.tileinBounds(x + 1, y + 1)  and self.refLabel[x + 1, y + 1] == '':  
			
			print("hi welcome to the top right")

			self.refLabel[x + 1, y + 1] = 'U'
			self.amove = Action(AI.Action.UNCOVER, x + 1, y + 1)

			

			tE = time.time()
			dt = tE-ts
			self.time_elapsed += dt

			return self.amove
		
		## bottom right
		print("Checking bottom right condition")
		if self.tileinBounds(x + 1, y - 1) and self.refLabel[x + 1, y - 1] == '':

			print("hi welcome to the bottom right")
			self.refLabel[x + 1, y - 1] = 'U'
			self.amove = Action(AI.Action.UNCOVER, x + 1, y - 1)



			tE = time.time()
			dt = tE - ts
			self.time_elapsed += dt

			return self.amove
		

		#top 
		print("Checking top condition")
		if self.tileinBounds(x, y + 1) and self.refLabel[x, y + 1] == '': 
			
			print("hi welcome to top")
			self.refLabel[x, y + 1] = 'U'
			self.amove = Action(AI.Action.UNCOVER, x, y + 1)

			

			tE = time.time()
			dt = tE-ts
			self.time_elapsed += dt

			return self.amove

		#bottom 
		print("Checking bottom  condition")
		if self.tileinBounds(x, y - 1) and self.refLabel[x, y - 1] == '':  
			
			print("hi welcome bottom")
			self.refLabel[x, y - 1] = 'U'

			self.amove = Action(AI.Action.UNCOVER, x, y - 1)


			

			tE = time.time()
			dt = tE - ts
			self.time_elapsed += dt

			return self.amove
		print("None of the conditions were satisfied")

	def markedOrUnmarked(self, x, y):
		i = 0 # marked with a flag
		j = 0 # not marked with a flag
		# left side
		## left


		if self.tileinBounds(x - 1, y) and self.refLabel[x - 1, y] == 'F': # if valid move and flagged and not touched yet 
			i +=1 
		
		if self.tileinBounds(x - 1, y) and self.refLabel[x - 1, y] == '': # if valid move and not touched yet 
			j +=1 


		## top left
		if self.tileinBounds(x - 1, y + 1) and self.refLabel[x - 1, y + 1] == 'F':
			i +=1 
		
		if self.tileinBounds(x - 1, y + 1) and self.refLabel[x - 1, y + 1] == '': 
			j +=1 


		## bottom left
		if self.tileinBounds(x - 1, y - 1) and self.refLabel[x - 1, y - 1] == 'F':
			i +=1 

		if self.tileinBounds(x - 1, y - 1) and self.refLabel[x - 1, y - 1] == '':
			j +=1 

		# right side

		## right
		if self.tileinBounds(x + 1, y) and self.refLabel[x + 1, y] == 'F':
			i +=1 
		if self.tileinBounds(x + 1, y) and self.refLabel[x + 1, y] == '':
			j +=1 
		
		## top right
		if self.tileinBounds(x + 1, y + 1) and self.refLabel[x + 1, y + 1] == 'F':
			i +=1 
		if self.tileinBounds(x + 1, y + 1) and self.refLabel[x + 1, y + 1] == '':
			j +=1 

		## bottom right
		if self.tileinBounds(x + 1, y - 1) and self.refLabel[x + 1, y - 1] == 'F':
			i +=1 
		if self.tileinBounds(x + 1, y - 1) and self.refLabel[x + 1, y - 1] == '':
			j +=1 


		#top 
		if self.tileinBounds(x, y + 1) and self.refLabel[x, y + 1] == 'F':
			i +=1 

		if self.tileinBounds(x, y + 1) and self.refLabel[x, y + 1] == '':
			j +=1 

		#bottom 
		if self.tileinBounds(x, y - 1) and self.refLabel[x, y - 1] == 'F':
			i +=1 

		if self.tileinBounds(x, y - 1) and self.refLabel[x, y - 1] == '':
			j +=1 

		return i, j

	
	



	#check if tile is in Bounds or not 
	def tileinBounds(self, x, y):
		if (x >= 0 and x < self.row) and (y >= 0 and y < self.col) :
			return True
		else:
			print("Tile is in bounds")
			return False

	def chooseRandom(self):
		
		

		explore = []
		for x in range(0, self.row):
			for y in range(0, self.col):
				if self.refLabel[x, y] == '': # if empty string then we explore
					explore.append((x, y))

		coords = random.choice(explore)

		
		
		
		
		
		return coords
		#self.action = Action(AI.Action.UNCOVER, randx, randy)