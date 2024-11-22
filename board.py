import pygame

pygame.init()
WIDTH, HEIGHT = 640, 640
SQUARE = WIDTH // 8
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Chessboard")


colorLight = (255, 255, 255)
colorDark = (0, 0, 0)

def createBoard():
    lightSquare = True
    for i in range(8):
        for j in range(8):
            if lightSquare:
                squareColor = colorLight
            else:
                squareColor = colorDark
            x = j * SQUARE
            y = i * SQUARE
            pygame.draw.rect(screen, squareColor, (x, y, SQUARE, SQUARE))
            lightSquare = not lightSquare
        lightSquare = not lightSquare


run = True
while run:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            run= False
    
    createBoard()
    pygame.display.flip()

pygame.quit()
exit()