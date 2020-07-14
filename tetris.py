import pygame, random, os

#Parameters
matrixWidth = 10
matrixHeight = 20
minoSpawnX = 3
minoSpawnY = 1
minoSize = 32
gridlineSize = 1
sidebarWidth = minoSize * 6
sidebarMinoX = 1
sidebarMinoY = 6
emptyMinoColour = [27, 27, 27]
gridlineColour = [0, 0, 0]
textColour = [255, 255, 255]
sidebarColour = [18, 18, 18]

#Classes
class Tile:
	def __init__(self, filled, colour):
		self.filled = filled
		self.colour = colour

class Mino:
	def __init__(self, x, y): #add colour
		self.x = x
		self.y = y

class Tetromino:
	def __init__(self, dx1, dy1, dx2, dy2, dx3, dy3, dx4, dy4, cornerX, cornerY, size, colour):
		self.x = minoSpawnX
		self.y = minoSpawnY
		self.colour = colour
		self.minos = [
			Mino(dx1, dy1),
			Mino(dx2, dy2),
			Mino(dx3, dy3),
			Mino(dx4, dy4)
		]
		self.cornerX = cornerX
		self.cornerY = cornerY
		self.size = size

	def createCopy(self):
		copy = Tetromino(0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, [0, 0, 0])
		copy.x = self.x
		copy.y = self.y
		copy.cornerX = self.cornerX
		copy.cornerY = self.cornerY
		copy.size = self.size
		copy.colour = self.colour
		copy.minos = [
			Mino(self.minos[0].x, self.minos[0].y),
			Mino(self.minos[1].x, self.minos[1].y),
			Mino(self.minos[2].x, self.minos[2].y),
			Mino(self.minos[3].x, self.minos[3].y)
		]
		return copy

	def tryMove(self, moveMatrix, dx, dy):
		canMove = True
		for mino in self.minos:
			newX = self.x + mino.x + dx
			newY = self.y + mino.y + dy
			if newX < 0 or newX >= matrixWidth or newY >= matrixHeight:
				canMove = False
				break
			if moveMatrix[newY][newX].filled:
				canMove = False
				break
		if canMove:
			self.x += dx
			self.y += dy
		return canMove

	def tryTurnLeft(self, moveMatrix):
		canRotate = True
		for mino in self.minos:
			currX = mino.x - self.cornerX
			currY = mino.y - self.cornerY
			newX = self.x + currY + self.cornerX
			newY = self.y + self.size - currX - 1 + self.cornerY
			if newX < 0 or newX >= matrixWidth or newY >= matrixHeight:
				canRotate = False
				break
			if moveMatrix[newY][newX].filled:
				canRotate = False
				break
		if canRotate:
			for mino in self.minos:
				currX = mino.x - self.cornerX
				currY = mino.y - self.cornerY
				mino.x = currY + self.cornerX
				mino.y = self.size - currX - 1 + self.cornerY

	def tryTurnRight(self, moveMatrix):
		canRotate = True
		for mino in self.minos:
			currX = mino.x - self.cornerX
			currY = mino.y - self.cornerY
			newX = self.x + self.size - currY - 1 + self.cornerX
			newY = self.y + currX + self.cornerY
			if newX < 0 or newX >= matrixWidth or newY >= matrixHeight:
				canRotate = False
				break
			if moveMatrix[newY][newX].filled:
				canRotate = False
				break
		if canRotate:
			for mino in self.minos:
				currX = mino.x - self.cornerX
				currY = mino.y - self.cornerY
				mino.x = self.size - currY - 1 + self.cornerX
				mino.y = currX + self.cornerY

def shuffle(array):
	newArray = []
	while len(array) > 0:
		newArray.append(array.pop(random.randrange(len(array))))
	return newArray

tetrominos = [
	Tetromino(1, 0, 2, 0, 1, -1, 2, -1, 0, -2, 4, [192, 192, 0]), #O
	Tetromino(0, 0, 1, 0, 2, 0, 3, 0, 0, -1, 4, [0, 192, 192]), #I
	Tetromino(0, 0, 1, 0, 2, 0, 1, -1, 0, -1, 3, [80, 0, 150]), #T
	Tetromino(0, 0, 1, 0, 2, 0, 2, -1, 0, -1, 3, [200, 100, 0]), #J
	Tetromino(0, 0, 1, 0, 2, 0, 0, -1, 0, -1, 3, [0, 80, 200]), #L
	Tetromino(0, 0, 1, 0, 1, -1, 2, -1, 0, -1, 3, [0, 127, 0]), #S
	Tetromino(1, 0, 2, 0, 0, -1, 1, -1, 0, -1, 3, [192, 0, 0]) #Z
]

#Initialization
os.environ["SDL_VIDEO_CENTERED"] = "1"
pygame.init()
pygame.mixer.music.load('remix.mp3')
pygame.mixer.music.play(-1)
screenWidth = matrixWidth * (minoSize + gridlineSize) - gridlineSize + sidebarWidth
screenHeight = matrixHeight * (minoSize + gridlineSize) - gridlineSize
matrix = []
for y in range(matrixHeight):
	row = []
	for x in range(matrixWidth):
		row.append(Tile(False, [0, 0, 0]))
	matrix.append(row)
filledMino = pygame.surface.Surface([minoSize, minoSize])
emptyMino = pygame.surface.Surface([minoSize, minoSize])
emptyMino.fill(emptyMinoColour)
sidebar = pygame.surface.Surface([sidebarWidth, screenHeight])
sidebar.fill(sidebarColour)
screen = pygame.display.set_mode([screenWidth, screenHeight])
pygame.display.set_caption("Tetris")
board = pygame.Surface(screen.get_size())
board = board.convert()
board.fill(gridlineColour)
clock = pygame.time.Clock()

#Variables
currentTetromino = None
nextTetromino = None
tetrominoBag = []
running = True
gameOver = False
paused = False
ticksSinceFall = 0
score = 0
lines = 0
prevTetris = False

#Loop
while running:
	descend = False
	drop = False
	moveLeft = False
	moveRight = False
	turnLeft = False
	turnRight = False

	#Input
	for event in pygame.event.get():
		if event.type == pygame.QUIT:
			running = False
		if event.type == pygame.KEYDOWN:
			if event.key == pygame.K_UP:
				turnRight = True
			if event.key == pygame.K_z:
				turnLeft = True
			if event.key == pygame.K_SPACE:
				drop = True
				
	keys = pygame.key.get_pressed()
	if keys[pygame.K_DOWN]:
		descend = True
	if keys[pygame.K_LEFT]:
		moveLeft = True
	if keys[pygame.K_RIGHT]:
		moveRight = True

	clock.tick(60)
	if gameOver or paused:
		pygame.mixer.music.fadeout(5000)
		continue

	#Tetromino Logic
	if currentTetromino != None:
		if turnLeft:
			currentTetromino.tryTurnLeft(matrix)
		if turnRight:
			currentTetromino.tryTurnRight(matrix)
		if drop:
			while currentTetromino.tryMove(matrix, 0, 1):
				score += 1
		if ticksSinceFall % 6 == 0:
			if descend:
				if currentTetromino.tryMove(matrix, 0, 1):
					score += 1
			if moveLeft:
				currentTetromino.tryMove(matrix, -1, 0)
			if moveRight:
				currentTetromino.tryMove(matrix, 1, 0)

	if ticksSinceFall >= 36:
		ticksSinceFall = 0
		if currentTetromino == None:
			if len(tetrominoBag) == 0:
				for index in range(len(tetrominos)):
					tetrominoBag.append(index)
				tetrominoBag = shuffle(tetrominoBag)
			if nextTetromino == None:
				nextTetromino = tetrominos[tetrominoBag.pop()].createCopy()
			currentTetromino = nextTetromino
			nextTetromino = tetrominos[tetrominoBag.pop()].createCopy()
			for mino in currentTetromino.minos:
				if matrix[currentTetromino.y + mino.y][currentTetromino.x + mino.x].filled:
					gameOver = True
					break
		else:
			if currentTetromino.tryMove(matrix, 0, 1) == False:
				for mino in currentTetromino.minos:
					matrix[currentTetromino.y + mino.y][currentTetromino.x + mino.x].filled = True
					matrix[currentTetromino.y + mino.y][currentTetromino.x + mino.x].colour = currentTetromino.colour
				currentTetromino = None
				newMatrix = []
				clearedRows = 0
				tetris = False
				for row in matrix:
					clear = True
					for tile in row:
						if not tile.filled:
							clear = False
							break
					if clear:
						emptyRow = []
						for emptyTile in range(matrixWidth):
							emptyRow.append(Tile(False, [0, 0, 0]))
						newMatrix.insert(0, emptyRow)
						clearedRows += 1
						lines += 1
					else:
						newMatrix.append(row)
				if clearedRows == 4:
					if prevTetris:
						score += 1200
					else:
						score += 800
					prevTetris = True
				else:
					score += clearedRows * 100
					prevTetris = False
				matrix = newMatrix
	
	#Screen Display
	for y in range(matrixHeight):
		for x in range(matrixWidth):
			if matrix[y][x].filled:
				filledMino.fill(matrix[y][x].colour)
				board.blit(filledMino, [x * (minoSize + gridlineSize), y * (minoSize + gridlineSize)])
			else:
				board.blit(emptyMino, [x * (minoSize + gridlineSize), y * (minoSize + gridlineSize)])
	if currentTetromino != None:
		for mino in currentTetromino.minos:
			filledMino.fill(currentTetromino.colour)
			board.blit(filledMino, [(currentTetromino.x + mino.x) * (minoSize + gridlineSize), (currentTetromino.y + mino.y) * (minoSize + gridlineSize)])
	screen.blit(board, [sidebarWidth, 0])
	screen.blit(sidebar, [0, 0])
	if nextTetromino != None:
		for mino in nextTetromino.minos:
			filledMino.fill(nextTetromino.colour)
			offsetX = 0
			if nextTetromino.size == 3:
				offsetX = round(minoSize / 2)
			screen.blit(filledMino, [(sidebarMinoX + mino.x) * (minoSize + gridlineSize) + offsetX, (sidebarMinoY + mino.y) * (minoSize + gridlineSize)])
	if pygame.font:
		font = pygame.font.Font(None, 36)
		scoreText = font.render("Score: " + str(score), 1, textColour)
		linesText = font.render("Lines: " + str(lines), 1, textColour)
		nextText = font.render("Next", 1, textColour)
		gameoverText = font.render("Game Over", 1, textColour)
		screen.blit(scoreText, [20, 20])
		screen.blit(linesText, [20, 50])
		screen.blit(nextText, [72, 120])
		if gameOver:
			screen.blit(gameoverText, [30, 270])
	pygame.display.flip()
	ticksSinceFall += 1

pygame.quit()