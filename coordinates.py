class Coord:

    def __init__(self):
        self.fileIndex = 0
        self.rankIndex = 0

    def isLightSquare(self, square):
        return (self.fileIndex + self.rankIndex) % 2 != 0
        
    def coordCompare(self, square):
        return (0 if self.fileIndex == square.fileIndex and self.rankIndex == square.rankIndex else 1)
    
    