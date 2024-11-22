import pygame

pygame.init()
WIDTH, HEIGHT = 640, 640
SQUARE = WIDTH // 8
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Chess")

class Board:
    def __init__(self):
        self.colorLight = (255, 255, 255)
        self.colorDark = (0, 0, 0)

        self.WhiteToMove = True

    def createBoard(self):
        lightSquare = True
        for i in range(8):
            for j in range(8):
                if lightSquare:
                    squareColor = self.colorLight
                else:
                    squareColor = self.colorDark
                x = j * SQUARE
                y = i * SQUARE
                pygame.draw.rect(screen, squareColor, (x, y, SQUARE, SQUARE))
                lightSquare = not lightSquare
            lightSquare = not lightSquare


chess = Board()

run = True
while run:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            run= False
    
    chess.createBoard()
    pygame.display.flip()

pygame.quit()
exit()