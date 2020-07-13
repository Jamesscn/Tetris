import pygame, random, os, time

matrixWidth = 10
matrixHeight = 20
minoSpawnX = 3
minoSpawnY = 1
minoSize = 32
gridlineSize = 1
filledMinoColour = [0, 100, 0]
emptyMinoColour = [0, 0, 0]
gridlineColour = [200, 200, 200]
prevTetris = False

class Mino:
	def __init__(self, x, y): #add colour
		self.x = x
		self.y = y

class Tetromino:
	def __init__(self, dx1, dy1, dx2, dy2, dx3, dy3, dx4, dy4):
		self.minos = [
			Mino(minoSpawnX + dx1, minoSpawnY + dy1),
			Mino(minoSpawnX + dx2, minoSpawnY + dy2),
			Mino(minoSpawnX + dx3, minoSpawnY + dy3),
			Mino(minoSpawnX + dx4, minoSpawnY + dy4)
		]

	def createCopy(self):
		copy = Tetromino(0, 0, 0, 0, 0, 0, 0, 0)
		copy.minos = [
			Mino(self.minos[0].x, self.minos[0].y),
			Mino(self.minos[1].x, self.minos[1].y),
			Mino(self.minos[2].x, self.minos[2].y),
			Mino(self.minos[3].x, self.minos[3].y)
		]
		return copy

	def tryMove(self, matrix, dx, dy):
		canMove = True
		for mino in self.minos:
			newX = mino.x + dx
			newY = mino.y + dy
			if newX < 0 or newX >= matrixWidth or newY >= matrixHeight:
				canMove = False
				break
			if matrix[newY][newX] == 1:
				canMove = False
				break
		if canMove:
			for mino in self.minos:
				mino.x += dx
				mino.y += dy
		return canMove

tetrominos = [
	Tetromino(1, 0, 2, 0, 1, -1, 2, -1), #O
	Tetromino(0, 0, 1, 0, 2, 0, 3, 0), #I
	Tetromino(0, 0, 1, 0, 2, 0, 1, -1), #T
	Tetromino(0, 0, 1, 0, 2, 0, 2, -1), #J
	Tetromino(0, 0, 1, 0, 2, 0, 0, -1), #L
	Tetromino(0, 0, 1, 0, 1, -1, 2, -1), #S
	Tetromino(1, 0, 2, 0, 0, -1, 1, -1) #Z
]

def updateBoard(matrix):
	newMatrix = []
	emptyRow = []
	clearedRows = 0
	score = 0
	tetris = False
	for tile in matrixWidth:
		emptyRow.append(0)
	for row in matrix:
		clear = 1
		for tile in row:
			clear &= tile
		if clear == 0:
			newMatrix.append(row)
		else:
			newMatrix.insert(0, emptyRow)
			clearedRows += 1
	if clearedRows == 4:
		if prevTetris:
			score = 1200
		else:
			score = 800
		prevTetris = True
	else:
		score = clearedRows * 100
		prevTetris = False
	return [newMatrix, score, tetris]

os.environ["SDL_VIDEO_CENTERED"] = "1"
pygame.init()
screenWidth = matrixWidth * (minoSize + gridlineSize) - gridlineSize
screenHeight = matrixHeight * (minoSize + gridlineSize) - gridlineSize
matrix = []
for y in range(matrixHeight):
	row = []
	for x in range(matrixWidth):
		row.append(0)
	matrix.append(row)
filledMino = pygame.surface.Surface([minoSize, minoSize])
filledMino.fill(filledMinoColour)
emptyMino = pygame.surface.Surface([minoSize, minoSize])
emptyMino.fill(emptyMinoColour)
screen = pygame.display.set_mode([screenWidth, screenHeight])
pygame.display.set_caption("Tetris")
board = pygame.Surface(screen.get_size())
board = board.convert()
board.fill(gridlineColour)
clock = pygame.time.Clock()
currentTetromino = None
running = True
gameOver = False
while running:
	for event in pygame.event.get():
		if event.type == pygame.QUIT:
			running = False
	clock.tick(60)
	if gameOver:
		continue
	if currentTetromino == None:
		tetrominoIndex = random.randrange(len(tetrominos))
		currentTetromino = tetrominos[tetrominoIndex].createCopy()
		for mino in currentTetromino.minos:
			if matrix[mino.y][mino.x] == 1:
				print("Game over")
				gameOver = True
				break
		if gameOver:
			continue
	else:
		for mino in currentTetromino.minos:
				matrix[mino.y][mino.x] = 0
		if currentTetromino.tryMove(matrix, 0, 1) == False:
			for mino in currentTetromino.minos:
				matrix[mino.y][mino.x] = 1
			currentTetromino = None
	if currentTetromino != None:
		for mino in currentTetromino.minos:
			matrix[mino.y][mino.x] = 2
	for y in range(matrixHeight):
		for x in range(matrixWidth):
			if matrix[y][x] > 0:
				board.blit(filledMino, [x * (minoSize + gridlineSize), y * (minoSize + gridlineSize)])
			else:
				board.blit(emptyMino, [x * (minoSize + gridlineSize), y * (minoSize + gridlineSize)])
	time.sleep(0.1)
	screen.blit(board, [0, 0])
	pygame.display.flip()
pygame.quit()