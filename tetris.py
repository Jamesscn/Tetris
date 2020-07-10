import pygame

def updateBoard(matrix, prevTetris):
	newMatrix = []
	emptyRow = []
	clearedRows = 0
	score = 0
	tetris = False
	for tile in matrix[0]:
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
		tetris = True
		if prevTetris:
			score = 1200
		else:
			score = 800
	else:
		score = clearedRows * 100
	return [newMatrix, score, tetris]

pygame.init()
matrixWidth = 10
matrixHeight = 40
viewWidth = 10
viewHeight = 20
tileSize = 32
gridlineSize = 1
filledTileColour = [0, 100, 0]
emptyTileColour = [0, 0, 0]
gridlineColour = [200, 200, 200]
screenWidth = viewWidth * (tileSize + gridlineSize) - gridlineSize
screenHeight = viewHeight * (tileSize + gridlineSize) - gridlineSize
matrix = []
for y in range(matrixHeight):
	row = []
	for x in range(matrixWidth):
		row.append(0)
	matrix.append(row)
filledTile = pygame.surface.Surface([tileSize, tileSize])
filledTile.fill(filledTileColour)
emptyTile = pygame.surface.Surface([tileSize, tileSize])
emptyTile.fill(emptyTileColour)
screen = pygame.display.set_mode([screenWidth, screenHeight])
pygame.display.set_caption("Tetris")
board = pygame.Surface(screen.get_size())
board = board.convert()
board.fill(gridlineColour)
clock = pygame.time.Clock()
while True:
	clock.tick(60)
	for y in range(viewHeight):
		for x in range(viewWidth):
			if matrix[y + (matrixHeight - viewHeight)][x] == 1:
				board.blit(filledTile, [x * (tileSize + gridlineSize), y * (tileSize + gridlineSize)])
			else:
				board.blit(emptyTile, [x * (tileSize + gridlineSize), y * (tileSize + gridlineSize)])
	screen.blit(board, [0, 0])
	pygame.display.flip()