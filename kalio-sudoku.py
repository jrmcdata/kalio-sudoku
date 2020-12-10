#!/usr/bin/env python3
'''
##############################################
###
### LIBRARIES
###
##############################################
'''
import copy, itertools
from collections import deque
import time

'''
##############################################
###
### SUDOKU CLASS
###
##############################################
'''
class sudoku:
	'''
	+--------------------------------------------------------------------
	|
	| GLOBAL CONSTANTS
	|
	+--------------------------------------------------------------------
	'''
	ROW = [ [ nn for nn in range(0,81) if nn // 9 == ii ] for ii in range(0,9) ]
	COL = [ [ nn for nn in range(0,81) if nn %  9 == ii ] for ii in range(0,9) ]
	DOM = [ [ nn for nn in range(0,81) if (nn//9)//3 == ii//3 and (nn%9)//3 == ii % 3 ] for ii in range(0,9) ]
	
	'''
	+--------------------------------------------------------------------
	|
	| __init__( self, myArray ):
	| Initialize puzzle based on list of values [myArray], and generate initial neighbors
	|
	+--------------------------------------------------------------------
	'''
	def __init__( self, myArray = None ):
		
		## INITIALIZE neighbors
		self.nei = [ set(range(1,9+1)) for xx in range(0,81) ]
		
		
		## CHOICE: no arguments
		if   not myArray:
			
			# Load clean array
			self.val = [0]*9*9
			
		## CHOICE: has arguments
		else:
			
			## CHOICE: from array
			if   type(myArray) == type([0]):
				
				# Load value array
				self.val = copy.deepcopy( myArray )
				
				# Update neighbors
				self.update('val')
				
			## CHOICE: from old sudoku
			elif type(myArray) == type(sudoku()):
				
				# Load value array
				self.val = copy.deepcopy( myArray.val )
				
				# Copy neighbors
				self.nei = copy.deepcopy( myArray.nei )
	
	'''
	+--------------------------------------------------------------------
	|
	| __str__(self):
	| Outputs string formatted for properly displaying board
	|
	+--------------------------------------------------------------------
	'''
	def __str__( self):
		
		# Initalize output variable
		outText = ''
		
		# Print every row of board
		for ii in range(0,9):
			
			# Top frame
			if ii == 0:
				outText += '+-------+-------+-------+\n'
				
			# Every data row
			row = [ str(xx) if xx != 0 else '*' for xx in self.val[ ii*9: 9 + ii*9 ] ]
			outText += '| ' + ' '.join(row[0:3]) + ' | ' + ' '.join(row[3:6]) + ' | ' + ' '.join(row[6:9]) + ' |\n'
			
			# Print bottom frame every three rows
			if ii in [2,5,8]:
				outText += '+-------+-------+-------+'
				
				if ii != 8:
					outText += '\n'
		
		return outText
	
	'''
	+--------------------------------------------------------------------
	|
	| __eq__( self, other):
	| Compares two boards, true if the values are the same
	|
	+--------------------------------------------------------------------
	'''
	def __eq__( self, other):
		return ( self.val == other.val ) and ( self.nei == other.nei )
	
	'''
	+--------------------------------------------------------------------
	|
	| get( self, myFlag, myIndex):
	| Retrieves copy of n-th [myIndex = nth] row, column, or domain [ myFlag = 'row', 'col', 'dom' ];
	| otherwise, for myFlag = 'idx' outputs rows, columns and doms for a given index.
	|
	+--------------------------------------------------------------------
	'''
	def get( self, myFlag, myIndex ):
		
		# Get index to work within puzzle
		wIndex = int(myIndex) % 9**2 if str(myFlag).lower() == 'idx' else int(myIndex) % 9
		
		# Send data out, otherwise send empty list
		if   str(myFlag).lower() == 'row':
			return [ self.val[xx] for xx in sudoku.ROW[wIndex] ], \
			       [ self.nei[xx] for xx in sudoku.ROW[wIndex] ]
		elif str(myFlag).lower() == 'col':
			return [ self.val[xx] for xx in sudoku.COL[wIndex] ], \
			       [ self.nei[xx] for xx in sudoku.COL[wIndex] ]
		elif str(myFlag).lower() == 'dom':
			return [ self.val[xx] for xx in sudoku.DOM[wIndex] ], \
			       [ self.nei[xx] for xx in sudoku.DOM[wIndex] ]
		elif str(myFlag).lower() == 'idx':
			return [ self.val[xx] for xx in sudoku.ROW[wIndex // 9] ], \
			       [ self.val[xx] for xx in sudoku.COL[wIndex %  9] ], \
			       [ self.val[xx] for xx in sudoku.DOM[ 3*((wIndex // 9 ) // 3) + ( wIndex % 9 ) // 3 ] ]
		else:
			return []
	
	'''
	+--------------------------------------------------------------------
	|
	| update( self, myFlag):
	| Update board keeping values (neighbors) [ myFlag = 'val', 'nei' ] fixed
	|
	+--------------------------------------------------------------------
	'''
	def update( self, myFlag):
		
		#############################################
		###
		### Run through all board elements
		###
		#############################################
		for ii in range(0,81):
			
			# Keep values fixed
			if   myFlag.lower() == 'val':
				
				# On unoccupied spaces
				if self.val[ii] == 0:
					# Unoccupied cells
					self.nei[ii] = set(self.nei[ii]) - set([]).union(*self.get('idx',ii))
				# On occupied spaces
				else:
					self.nei[ii] = set( [self.val[ii]] )
			
			# Keep neighbors fixed
			elif myFlag.lower() == 'nei':
				self.val[ii] = list(self.nei[ii])[0] if len(self.nei[ii]) == 1 else 0
	
	'''
	+--------------------------------------------------------------------
	|
	| put( self, myGrid, myFlag, myIndex, myList):
	| Put list [myList] into n-th [myIndex] row, column, domain [myFlag] for
	| values, neighbors [myGrid]
	|
	+--------------------------------------------------------------------
	'''
	def put( self, myGrid, myFlag, myIndex, myList):
		
		# Get index of element
		wIndex = int(myIndex) % 9
		
		# Push elements into board
		for nn in range(0,9):
			if   str(myGrid).lower() == 'val':
				if   str(myFlag).lower() == 'row':
					self.val[ sudoku.ROW[wIndex][nn] ] = myList[nn]
				elif str(myFlag).lower() == 'col':
					self.val[ sudoku.COL[wIndex][nn] ] = myList[nn]
				elif str(myFlag).lower() == 'dom':
					self.val[ sudoku.DOM[wIndex][nn] ] = myList[nn]
			elif str(myGrid).lower() == 'nei':
				if   str(myFlag).lower() == 'row':
					self.nei[ sudoku.ROW[wIndex][nn] ] = myList[nn]
				elif str(myFlag).lower() == 'col':
					self.nei[ sudoku.COL[wIndex][nn] ] = myList[nn]
				elif str(myFlag).lower() == 'dom':
					self.nei[ sudoku.DOM[wIndex][nn] ] = myList[nn]
		
		# Update board
		if   str(myGrid).lower() == 'val':
			self.update( 'val' )
		elif str(myGrid).lower() == 'nei':
			self.update( 'nei' )
	
	'''
	+--------------------------------------------------------------------
	|
	| solveSimple():
	| Solve board by eliminating all single solution occupancy cells
	|
	+--------------------------------------------------------------------
	'''
	def solveSimple( self ):
		
		# Generate new boards
		lastBoard = sudoku()
		nextBoard = sudoku( self )
		
		# Run until all single neighbor cells are gone
		while lastBoard != nextBoard:
			
			# Update old board with new board
			lastBoard = sudoku( nextBoard )
			
			# Remove single neighbor cells
			nextBoard.update('nei')
			nextBoard.update('val')
		
		# Output results
		self.val = copy.deepcopy( nextBoard.val )
		self.nei = copy.deepcopy( nextBoard.nei )
	
	'''
	+--------------------------------------------------------------------
	|
	| status( self ):
	| Returns -1 if no solution, 1 if complete, 0 if incomplete
	|
	+--------------------------------------------------------------------
	'''
	def status( self ):
		
		# Obtain grid with all numbers, return if any are bad
		solGrid = [ [ xx for xx in sorted(self.get(dd, nn)[0]) if xx != 0 ] for nn in range(0,9) for dd in ['row','col','dom'] ]
		txtGrid = set([ ''.join(list(map(str,xx))) for xx in solGrid ])
		isBroken = 0 in [ 1 if len(set(xx)) == len(xx) else 0 for xx in solGrid ]
		
		# Exit if inconsistent solution
		if ( set() in self.nei ) or isBroken:
			return -1
		
		# Check if solved
		if txtGrid == set( [ ''.join(list(map(str,range(1,9+1)))) ] ):
			return 1
		else:
			return 0
	
	'''
	+--------------------------------------------------------------------
	|
	| solvePairs( self ):
	| Solve board by eliminating all repeated pairs in element
	|
	+--------------------------------------------------------------------
	'''
	def solvePairs( self ):
		
		# Initialize boards
		pastBoard = sudoku()
		nextBoard = sudoku( self )
		
		# Parse until board remains static
		while pastBoard != nextBoard:
			
			# Save old board
			pastBoard = sudoku ( nextBoard )
			
			# Parse through all elements and positions
			for item in itertools.product( ['row', 'col', 'dom'], range(0,9) ):
				
				# Get element: row, col, domain
				myElem = item[0]
				# Get index: 0 ... 8
				myIndx = item[1]
				
				
				# Obtain element values and neighbors
				getVal = nextBoard.get( myElem , myIndx )[0]
				getNei = nextBoard.get( myElem , myIndx )[1]
				
				# Sort out all neighbors, and get only pairs that are repeated twice
				srtNei = sorted(getNei, key = lambda xx: sorted(list(xx)) )
				repNei = [ yy[0] for yy in [ [ xx[0], len(list(xx[1])) ] for xx in itertools.groupby( srtNei ) ] if yy[1] == 2 and len(yy[0]) == 2 ]
				
				# If pairs are found
				if len(repNei) != 0:
					
					# Remove them from all neighbors
					for item in repNei:
						getNei = [ ( item if xx == item else xx - item )  for xx in getNei ]
					
					# Send neighbors upstream
					nextBoard.put( 'nei', myElem, myIndx, getNei )
		
		# Output final values to 'self'
		self.val = copy.deepcopy( nextBoard.val )
		self.nei = copy.deepcopy( nextBoard.nei )
	
	'''
	+--------------------------------------------------------------------
	|
	| solveUnique( self ):
	| Solve board by eliminating all unique elements
	|
	+--------------------------------------------------------------------
	'''
	def solveUnique( self ):
		
		# Initialize boards
		self.update('nei')
		pastBoard = sudoku()
		nextBoard = sudoku( self )
		
		# Parse until board remains static
		while pastBoard != nextBoard:
			
			# Save old board
			pastBoard = sudoku( nextBoard )
			
			# Parse through all elements and positions
			for item in itertools.product( ['row', 'col', 'dom'], range(0,9) ):
				
				# Get element: row, col, domain
				myElem = item[0]
				# Get index: 0 ... 8
				myIndx = item[1]
				
				# Obtain element values and neighbors
				getVal = nextBoard.get( myElem , myIndx )[0]
				getNei = nextBoard.get( myElem , myIndx )[1]
				
				# Is cell empty
				isEmpty = [ 1 if nn not in getVal else 0 for nn in range(1,9+1) ]
				# Is cell uniquely occupied
				isUnique = [ 1 if sum([ 1 if nn in tt else 0 for tt in getNei ]) == 1 else 0 for nn in range(1,9+1) ]
				# Is there a singleton?
				isSingle = [ xx[2] for xx in zip( isEmpty, isUnique, range(1,9+1) ) if xx[0] * xx[1] * xx[2] != 0 ]
				
				# If pairs are found
				if len(isSingle) != 0:
					
					# Remove them from all neighbors
					for item in isSingle:
						getNei = [ set([item]) if item in xx else xx for xx in getNei ]
					
					# Send neighbors upstream
					nextBoard.put( 'nei', myElem, myIndx, getNei )
		
		# Output final values to 'self'
		self.val = copy.deepcopy( nextBoard.val )
		self.nei = copy.deepcopy( nextBoard.nei )
	
	'''
	+--------------------------------------------------------------------
	|
	| solveTwins( self ):
	| Solve board by eliminating all pairs of pairs that appear twice
	|
	+--------------------------------------------------------------------
	'''
	def solveTwins( self ):
		
		# Initialize boards
		self.update('nei')
		pastBoard = sudoku()
		nextBoard = sudoku( self )
		
		# Parse until board remains static
		while pastBoard != nextBoard:
			
			# Save old board
			pastBoard = sudoku( nextBoard )
			
			# Parse through all elements and positions
			for item in itertools.product( ['row', 'col', 'dom'], range(0,9) ):
				
				# Get element: row, col, domain
				myElem = item[0]
				# Get index: 0 ... 8
				myIndx = item[1]
				
				# Obtain element values and neighbors
				getVal = nextBoard.get( myElem , myIndx )[0]
				getNei = nextBoard.get( myElem , myIndx )[1]
				
				# Missing elements
				getMissing = list(set(range(1,9+1)) - set(getVal))
				getSoloCandidates = [ jj for jj in getMissing if sum([ 1 if jj in xx else 0 for xx in getNei ]) == 2 ]
				
				# Only if you have 2 candidates
				if len(getSoloCandidates) >= 2:
					
					# Get all possible pairs
					getPairCandidates = [ set(xx) for xx in itertools.combinations( getSoloCandidates, 2 ) ]
					
					# For every pair
					for item in getPairCandidates:
						
						# How many times has the pair happened
						getHappen = sum([ 1 if item.issubset(yy) else 0 for yy in getNei])
						
						# If pair is uniquely paired
						if getHappen == 2:
							
							# Update board by compressing pairs
							getNew = [ item if item.issubset(yy) else yy for yy in getNei]
							nextBoard.put( 'nei', myElem, myIndx, getNew )
							
						
		# Output final values to 'self'
		self.val = copy.deepcopy( nextBoard.val )
		self.nei = copy.deepcopy( nextBoard.nei )
	
	'''
	+--------------------------------------------------------------------
	|
	| solve( self ):
	| Solve board by eliminating all pairs of pairs that appear twice
	|
	+--------------------------------------------------------------------
	'''
	def solve( self ):
		
		# Initialize boards
		self.update('nei')
		pastBoard = sudoku()
		nextBoard = sudoku( self )
		
		# Repeat loop until no changes made
		while pastBoard != nextBoard:
			
			# Copy past board
			pastBoard = sudoku(nextBoard)
			
			# Main solve section
			nextBoard.solveSimple()
			nextBoard.solveTwins()
			nextBoard.solveUnique()
			nextBoard.solveTwins()
		
		# Output results
		self.val = copy.deepcopy( nextBoard.val )
		self.nei = copy.deepcopy( nextBoard.nei )
	
	'''
	+--------------------------------------------------------------------
	|
	| solveRandom( self ):
	| Solve board by randomly picking elements, and eliminating impossible boards
	|
	+--------------------------------------------------------------------
	'''
	def solveRandom(self):
		
		# Start board queue / initialize isIncomplete (exit loop flag)
		boardQue = deque()
		boardQue.append( sudoku(self) )
		remainsUnfound = True
		
		# Continue while items are on queue AND loop is not over
		while len(boardQue) > 0 and remainsUnfound:
			
			# Grab unsolved board
			bigBoard = sudoku( boardQue.popleft() )
			
			# Get the candidate with the shortest lenght and the largest number of sites
			candidateSite = min( \
			[ xx for xx in zip( bigBoard.nei, range(0,81) ) if len(xx[0]) != 1 ]  \
			, key = lambda zz: 100*len(zz[0]) - len([ xx for xx in itertools.chain( *bigBoard.get( 'idx', zz[1] ) ) if xx == 0 ]) )
			
			# For all items in the candidate
			for myChoice in list(candidateSite[0]):
				
				# Initialize new board, set the value to pick and solve
				lilBoard = sudoku( bigBoard )
				lilBoard.nei[ candidateSite[1] ] = set([myChoice])
				lilBoard.solve()
				
				# Check board status
				exitCode = lilBoard.status()
				
				
				if   exitCode == 0:
					# If board is incomplete, push it to the queue
					boardQue.append( lilBoard )
				elif exitCode == 1:
					# If board has been solved, exit loop send quit signal
					remainsUnfound = False
					break
		
		# Update the original board with solution
		if not remainsUnfound:
			self.val = copy.deepcopy(lilBoard.val)
			self.nei = copy.deepcopy(lilBoard.nei)




'''
##############################################
###
### TESTING CODE
###
##############################################
'''

'''
# File names
testNames = [ 'puzzle_easy_1.txt', 'puzzle_easy_2.txt', 'puzzle_easy_3.txt', 'puzzle_easy_4.txt', 'puzzle_easy_5.txt', 'puzzle_easy_6.txt', 'puzzle_easy_7.txt', 'puzzle_easy_8.txt', 'puzzle_medium_1.txt', 'puzzle_medium_2.txt', 'puzzle_medium_3.txt', 'puzzle_medium_4.txt', 'puzzle_medium_5.txt', 'puzzle_medium_6.txt', 'puzzle_medium_7.txt', 'puzzle_medium_8.txt',  'puzzle_hard_1.txt', 'puzzle_hard_2.txt', 'puzzle_hard_3.txt', 'puzzle_hard_4.txt', 'puzzle_hard_5.txt', 'puzzle_hard_6.txt', 'puzzle_hard_7.txt', 'puzzle_hard_8.txt', 'puzzle_evil_1.txt', 'puzzle_evil_2.txt', 'puzzle_evil_3.txt', 'puzzle_evil_4.txt', 'puzzle_evil_5.txt', 'puzzle_evil_6.txt', 'puzzle_evil_7.txt', 'puzzle_evil_8.txt', 'puzzle_evil_9.txt', 'puzzle_evil_10.txt', 'puzzle_evil_11.txt', 'puzzle_evil_12.txt',  'puzzle_impossible_1.txt', 'puzzle_impossible_2.txt', 'puzzle_impossible_3.txt', 'puzzle_impossible_4.txt', 'puzzle_impossible_5.txt', 'puzzle_impossible_6.txt', 'puzzle_impossible_7.txt', 'puzzle_impossible_8.txt', 'puzzle_impossible_9.txt', 'puzzle_impossible_10.txt', 'puzzle_impossible_11.txt', 'puzzle_impossible_12.txt']

# Initial boards
runTest = []
for fileName in testNames:
	with open('test/' + fileName ,'r') as myFile:
		fileData = myFile.read()
	
	tempGrid = [ int(xx) if xx != '*' else 0 for xx in fileData if xx in set(['*']).union(set(map(str,range(0,9+1)))) ]
	
	runTest.append( sudoku(tempGrid) )

solTest = []
timeTest = []
for xx in runTest:
	
	inTime = time.time()
	yy = sudoku(xx)
	yy.solve()
	
	if yy.status() == 0:
		yy.solveRandom()
	
	solTest.append(yy)
	
	outTime = time.time()
	
	timeTest.append( outTime - inTime )


count = 0
for xx in reversed(range(0, len(solTest))):
	if solTest[xx].status() == 0:
		print('BOARD ' + testNames[xx].split('.')[0] + ', number ' + str(xx) )
		print( runTest[xx] )
		print( solTest[xx] )
		count += 1

'''
