import pygame
import numpy as np
import math
import time

# Loading all_images
white_pawn = pygame.image.load('images/white.png')
white_pawn = pygame.transform.scale(white_pawn, (64, 64))
black_pawn = pygame.image.load('images/black.png')
black_pawn = pygame.transform.scale(black_pawn, (64, 64))
board_icon = pygame.image.load('images/board.png')
board_icon = pygame.transform.scale(board_icon, (300, 300))
even_block = pygame.image.load('images/even_block.jpg')
even_block = pygame.transform.scale(even_block, (100, 100))
odd_block = pygame.image.load('images/odd_block.jpg')
odd_block = pygame.transform.scale(odd_block, (100, 100))

# Moves
moves = [{-1: 'straight', 0: 'l_diagonal', -2: 'r_diagonal', }, {1: 'straight', 2: 'l_diagonal', 0: 'r_diagonal', }]

# py_game initialization
width = 300
height = 300
pygame.init()
screen = pygame.display.set_mode((width, height))
pygame.display.set_caption("Hexapawn by TwoZero")
game_over = False
current = []
new = []
turn = 1
click = False
result = ''


# Creating Numpy Board
def createBoard():
	return np.zeros((3, 3))


# Creating Chess Board

def drawBoard():
	screen.blit(board_icon, (0, 0))


# Drawing Pawns

def drawPawn():
	for i in range(3):
		for j in range(3):
			if board[i][j] == 1:
				screen.blit(white_pawn, (j * 100 + 20, i * 100 + 20))
			elif board[i][j] == 2:
				screen.blit(black_pawn, (j * 100 + 20, i * 100 + 20))


# Moving pawn with Mouse

def move_pawn(c):
	global turn
	to_draw = ''
	to_pick = ''
	while c:
		for e in pygame.event.get():
			if e.type == pygame.MOUSEMOTION:
				if (current[0] + current[1]) % 2 == 0:
					to_draw = even_block
				else:
					to_draw = odd_block
				if board[current[0]][current[1]] == 1:
					to_pick = white_pawn
				elif board[current[0]][current[1]] == 2:
					to_pick = black_pawn
			if e.type == pygame.MOUSEBUTTONUP:
				c = False
				x1 = round(math.floor(e.pos[0] / 100))
				y1 = round(math.floor(e.pos[1] / 100))
				new.append(y1)
				new.append(x1)
				if is_validMove(current, new, turn):
					board[new[0]][new[1]] = board[current[0]][current[1]]
					board[current[0]][current[1]] = 0
					turn += 1
					turn %= 2
				new.clear()
			drawBoard()
			drawPawn()
			screen.blit(to_draw, (current[1] * 100, current[0] * 100))
			screen.blit(to_pick, (e.pos[0]-32, e.pos[1]-32))
			pygame.display.update()


# Check for valid Moves
def is_validMove(c, n, t):
	row_jump = c[0] - n[0]
	col_jump = abs(c[1] - n[1])
	if t and row_jump != 1 and col_jump != 2:
		return False
	if not t and row_jump != -1 and col_jump != 2:
		return False
	if board[c[0]][c[1]] != t + 1:
		return False
	d = c[0] - n[0] + c[1] - n[1]
	if d in moves[t].keys():
		if moves[t][d] == 'straight' and board[n[0]][n[1]] != 0:
			return False
		elif (moves[t][d] == 'l_diagonal' or moves[t][d] == 'r_diagonal') and board[c[0]][c[1]] == board[n[0]][n[1]]:
			return False
		elif (moves[t][d] == 'l_diagonal' or moves[t][d] == 'r_diagonal') and board[n[0]][n[1]] not in [1, 2]:
			return False
	return True


# Scoring the players
player = ['White', 'Black']
scores = {
	'White': -10,
	'Black': 10
}


# Checking for winner

def checkWinner():
	winner = ''
	for i in range(3):
		if board[0][i] == 2:
			winner = 'Black'
			return winner
		if board[2][i] == 1:
			winner = 'White'
			return winner
	count = 0
	for i in range(3):
		for j in range(3):
			if board[i][j] != turn + 1:
				count += 1
	if count == 9:
		return player[not turn]

	for i in range(3):
		for j in range(3):
			if board[i][j] == 1:
				if board[i + 1][j] == 0:
					return winner
			elif board[i][j] == 2:
				if board[i - 1][j] == 0:
					return winner
	winner = player[not turn]
	return winner


# MiniMax Function

def miniMax(isMinimiser):
	global turn
	winner = checkWinner()
	if winner != '':
		if winner == 'White':
			turn += 1
			turn %= 2
		return scores[winner]
	if isMinimiser:
		bestScore = 9999999999
		for i in range(2, -1, -1):
			for j in range(2, -1, -1):
				possible_moves = []
				if board[i][j] == 1:
					if j == 0:
						possible_moves.append([i + 1, j])
						possible_moves.append([i + 1, j + 1])
					elif j == 2:
						possible_moves.append([i + 1, j])
						possible_moves.append([i + 1, j - 1])
					else:
						possible_moves.append([i + 1, j])
						possible_moves.append([i + 1, j + 1])
						possible_moves.append([i + 1, j - 1])
					for move in possible_moves:
						if is_validMove([i, j], move, 0):
							turn += 1
							turn %= 2
							if abs(move[1] - j):
								board[move[0]][move[1]] = 1
								board[i][j] = 0
							else:
								board[i][j], board[move[0]][move[1]] = board[move[0]][move[1]], board[i][j]
							score = miniMax(False)
							bestScore = min(score, bestScore)
							if abs(move[1] - j):
								board[move[0]][move[1]] = 2
								board[i][j] = 1
							else:
								board[i][j], board[move[0]][move[1]] = board[move[0]][move[1]], board[i][j]
							return bestScore
	else:
		bestScore = -9999999999
		for i in range(3):
			for j in range(3):
				possible_moves = []
				if board[i][j] == 2:
					if j == 0:
						possible_moves.append([i - 1, j])
						possible_moves.append([i - 1, j + 1])
					elif j == 2:
						possible_moves.append([i - 1, j])
						possible_moves.append([i - 1, j - 1])
					else:
						possible_moves.append([i - 1, j])
						possible_moves.append([i - 1, j + 1])
						possible_moves.append([i - 1, j - 1])
					for move in possible_moves:
						if is_validMove([i, j], move, 1):
							turn += 1
							turn %= 2
							if abs(move[1] - j):
								board[move[0]][move[1]] = 2
								board[i][j] = 0
							else:
								board[i][j], board[move[0]][move[1]] = board[move[0]][move[1]], board[i][j]
							score = miniMax(True)
							bestScore = max(score, bestScore)
							if abs(move[1] - j):
								board[move[0]][move[1]] = 1
								board[i][j] = 2
							else:
								board[i][j], board[move[0]][move[1]] = board[move[0]][move[1]], board[i][j]
							return bestScore


# A.I. Moves

def aiMove():
	global turn
	bestScore = 9999999999
	old_pos = []
	new_move = []
	for i in range(2, -1, -1):
		for j in range(2, -1, -1):
			possible_moves = []
			if board[i][j] == 1:
				if j == 0:
					possible_moves.append([i + 1, j])
					possible_moves.append([i + 1, j + 1])
				elif j == 2:
					possible_moves.append([i + 1, j])
					possible_moves.append([i + 1, j - 1])
				else:
					possible_moves.append([i + 1, j])
					possible_moves.append([i + 1, j + 1])
					possible_moves.append([i + 1, j - 1])
				for move in possible_moves:
					if is_validMove([i, j], move, 0):
						turn += 1
						turn %= 2
						if abs(move[1] - j):
							board[move[0]][move[1]] = 1
							board[i][j] = 0
						else:
							board[i][j], board[move[0]][move[1]] = board[move[0]][move[1]], board[i][j]
						score = miniMax(False)
						if score < bestScore:
							bestScore = score
							old_pos = [i, j]
							new_move = move.copy()
						if abs(move[1] - j):
							board[move[0]][move[1]] = 2
							board[i][j] = 1
						else:
							board[i][j], board[move[0]][move[1]] = board[move[0]][move[1]], board[i][j]
	if abs(new_move[1] - old_pos[1]):
		board[new_move[0]][new_move[1]] = 1
		board[old_pos[0]][old_pos[1]] = 0
	else:
		board[old_pos[0]][old_pos[1]], board[new_move[0]][new_move[1]] = board[new_move[0]][new_move[1]], \
			board[old_pos[0]][old_pos[1]]
	turn += 1
	turn %= 2


board = createBoard()
board[0] = [1] * 3
board[2] = [2] * 3
distance = 0
while not game_over:
	for event in pygame.event.get():
		if event.type == pygame.QUIT:
			game_over = True
			pygame.quit()
			quit()
		if turn:
			if event.type == pygame.MOUSEBUTTONDOWN:
				x = round(math.floor(event.pos[0] / 100))
				y = round(math.floor(event.pos[1] / 100))
				current.append(y)
				current.append(x)
				click = True
				if board[y][x] != 0:
					move_pawn(click)
					result = checkWinner()
					if result != '':
						game_over = True
		else:
			aiMove()
			result = checkWinner()
			if result != '':
				game_over = True
		current.clear()
		drawBoard()
		drawPawn()
		pygame.display.update()
font = pygame.font.SysFont("freesansbold.ttf", 50)
res = font.render(f"{result} Win", True, (255, 255, 255))
screen.blit(res, (80, 100))
pygame.display.update()
time.sleep(2)