import random
import time
import pygame
import math
from connect4 import connect4

class connect4Player(object):
	def __init__(self, position, seed=0):
		self.position = position
		self.opponent = None
		self.seed = seed
		random.seed(seed)

	def play(self, env, move):
		move = [-1]

class human(connect4Player):

	def play(self, env, move):
		move[:] = [int(input('Select next move: '))]
		while True:
			if int(move[0]) >= 0 and int(move[0]) <= 6 and env.topPosition[int(move[0])] >= 0:
				break
			move[:] = [int(input('Index invalid. Select next move: '))]

class human2(connect4Player):

	def play(self, env, move):
		done = False
		while(not done):
			for event in pygame.event.get():
				if event.type == pygame.QUIT:
					sys.exit()

				if event.type == pygame.MOUSEMOTION:
					pygame.draw.rect(screen, BLACK, (0,0, width, SQUARESIZE))
					posx = event.pos[0]
					if self.position == 1:
						pygame.draw.circle(screen, RED, (posx, int(SQUARESIZE/2)), RADIUS)
					else: 
						pygame.draw.circle(screen, YELLOW, (posx, int(SQUARESIZE/2)), RADIUS)
				pygame.display.update()

				if event.type == pygame.MOUSEBUTTONDOWN:
					posx = event.pos[0]
					col = int(math.floor(posx/SQUARESIZE))
					move[:] = [col]
					done = True

class randomAI(connect4Player):

	def play(self, env, move):
		possible = env.topPosition >= 0
		indices = []
		for i, p in enumerate(possible):
			if p: indices.append(i)
		move[:] = [random.choice(indices)]

class stupidAI(connect4Player):

	def play(self, env, move):
		possible = env.topPosition >= 0
		indices = []
		for i, p in enumerate(possible):
			if p: indices.append(i)
		if 3 in indices:
			move[:] = [3]
		elif 2 in indices:
			move[:] = [2]
		elif 1 in indices:
			move[:] = [1]
		elif 5 in indices:
			move[:] = [5]
		elif 6 in indices:
			move[:] = [6]
		else:
			move[:] = [0]
            
def check_terminal(board, moves, p1, p2): #was having issues with gameOver() so needed to make a separate function
	return check_win(board, p1) or check_win(board, p2) or len(moves) == 0
    
def check_win(board, player): #was having issues with gameOver() so needed to make a separate function
	for c in range(COLUMN_COUNT - 3):
		for r in range(ROW_COUNT):
			if board[r][c] == player and board[r][c+1] == player and board[r][c+2] == player and board[r][c+3] == player:
				return True
		
	for c in range(COLUMN_COUNT):
		for r in range(ROW_COUNT - 3):
			if board[r][c] == player and board[r+1][c] == player and board[r+2][c] == player and board[r+3][c] == player:
				return True
                
	for c in range(COLUMN_COUNT - 3):
		for r in range(3, ROW_COUNT):
			if board[r][c] == player and board[r-1][c+1] == player and board[r-2][c+2] == player and board[r-3][c+3] == player:
				return True
                
	for c in range(COLUMN_COUNT - 3):
		for r in range(ROW_COUNT - 3):
			if board[r][c] == player and board[r+1][c+1] == player and board[r+2][c+2] == player and board[r+3][c+3] == player:
				return True
                
def get_score(board, player):
	score = 0
	center_array = [int(i) for i in list(board[:,3])]
	center_count = center_array.count(player)
	score += center_count * 3
    
	for r in range(ROW_COUNT):
		row_array = [int(i) for i in list(board[r,:])]
		for c in range(COLUMN_COUNT - 3):
			area = row_array[c:c+4]
			score += score_area(area, player)
        
	for c in range(COLUMN_COUNT):
		col_array = [int(i) for i in list(board[:,c])]
		for r in range(ROW_COUNT - 3):
			area = col_array[r:r+4]
			score += score_area(area, player)
            
	for r in range(3, ROW_COUNT):
		for c in range(COLUMN_COUNT - 3):
			area = [board[r-i][c+i] for i in range(4)]
			score += score_area(area, player)
          
	for r in range(ROW_COUNT - 3):
		for c in range(COLUMN_COUNT - 3):
			area = [board[r+i][c+i] for i in range(4)]
			score += score_area(area, player)
            
	return score
        
def score_area(area, player):
	score = 0
	if player == 1:
		opp = 2
	else:
		opp = 1

	if area.count(player) == 4:
		score += 100
	elif area.count(player) == 3 and area.count(0) == 1:
		score += 5
	elif area.count(player) == 2 and area.count(0) == 2:
		score += 2
	if area.count(opp) == 3 and area.count(0) == 1:
		score -= 4
        
	return score

def get_moves(board): #Was having a lot of issues with env not updating so needed to make a separate function
	indices = []
	for col in range(COLUMN_COUNT):
		if board[0][col] == 0:
			indices.append(col)
	return indices
    
def get_row(board, col): #Was having a lot of issues with env not updating so needed to make a separate function
	for r in range(ROW_COUNT - 1, -1, -1):
		if board[r][col] == 0:
			return r

class minimaxAI(connect4Player):

	def minimax(self, board, depth, maxPlayer):
		mmax = self.position
		opp = self.opponent.position
		indices = get_moves(board)
		terminal = check_terminal(board, indices, mmax, opp)
        
		if depth == 0 or terminal:
			if terminal:
				if check_win(board, mmax):
					return (None, 1000)
				elif check_win(board, opp):
					return (None, -1000)
				else:
					return (None, 0)
			else: 
				return (None, get_score(board, mmax))	
            
		if maxPlayer:
			value = -math.inf
			best_move = random.choice(indices)
			for s in indices:
				board_copy = board.copy()
				row = get_row(board_copy, s)
				board_copy[row][s] = mmax
				new_val = self.minimax(board_copy, depth - 1, False)[1]
				if new_val > value:
					value = new_val
					best_move = s
			return best_move, value
            
		else:
			value = math.inf
			best_move = random.choice(indices)
			for s in indices:
				board_copy = board.copy()
				row = get_row(board_copy, s)
				board_copy[row][s] = opp
				new_val = self.minimax(board_copy, depth - 1, True)[1]
				if new_val < value:
					value = new_val
					best_move = s
			return best_move, value

	def play(self, env, move):
		board = env.getBoard()
		move[:] = [self.minimax(board, 3, True)[0]]

class alphaBetaAI(connect4Player):

	def alphabeta(self, board, depth, alpha, beta, maxPlayer):
		mmax = self.position
		opp = self.opponent.position
		indices = get_moves(board)
		#indices = self.successor(indices)
		terminal = check_terminal(board, indices, mmax, opp)
        
		if depth == 0 or terminal:
			if terminal:
				if check_win(board, mmax):
					return (None, 10000)
				elif check_win(board, opp):
					return (None, -10000)
				else:
					return (None, 0)
			else: 
				return (None, get_score(board, mmax))
            
		if maxPlayer:
			value = -math.inf
			best_move = random.choice(indices)
			for s in indices:
				board_copy = board.copy()
				row = get_row(board_copy, s)
				board_copy[row][s] = mmax
				new_val = self.alphabeta(board_copy, depth - 1, alpha, beta, False)[1]
				if new_val > value:
					value = new_val
					best_move = s
				alpha = max(alpha, value)
				if alpha >= beta:
					break
			return best_move, value
            
		else:
			value = math.inf
			best_move = random.choice(indices)
			for s in indices:
				board_copy = board.copy()
				row = get_row(board_copy, s)
				board_copy[row][s] = opp
				new_val = self.alphabeta(board_copy, depth - 1, alpha, beta, True)[1]
				if new_val < value:
					value = new_val
					best_move = s
				beta = min(beta, value)
				if alpha >= beta:
					break
			return best_move, value
   
	def successor(self, indices): #successor function
		new_index = []
		if 3 in indices:
			new_index.append(3)
		if 2 in indices:
				new_index.append(2)
		if 4 in indices:
			new_index.append(4)
		if 1 in indices:
				new_index.append(1)
		if 5 in indices:
			new_index.append(5)
		if 0 in indices:
				new_index.append(0)
		if 6 in indices:
			new_index.append(6)
		return new_index

	def play(self, env, move):
		board = env.getBoard()
		move[:] = [self.alphabeta(board, 5, -math.inf, math.inf, True)[0]]


SQUARESIZE = 100
BLUE = (0,0,255)
BLACK = (0,0,0)
RED = (255,0,0)
YELLOW = (255,255,0)

ROW_COUNT = 6
COLUMN_COUNT = 7

pygame.init()

SQUARESIZE = 100

width = COLUMN_COUNT * SQUARESIZE
height = (ROW_COUNT+1) * SQUARESIZE

size = (width, height)

RADIUS = int(SQUARESIZE/2 - 5)

screen = pygame.display.set_mode(size)




