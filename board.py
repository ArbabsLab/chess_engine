import pygame

lightSquare = False
colorLight = "white"
colorDark = "black"

def createBoard():
    for i in range(8):
        for j in range(8):
            if lightSquare:
                squareColor = colorLight
            else:
                squareColor = colorDark
            lightSquare = not lightSquare

            #find position of square
            #draw square
                