
class SquareManipulator:
    def __init__(self):
        self.squareOccupied = [0]*16
        self.map = [0]*64
        self.pieceCount = 0

    def AddPieceAtSquare(self, square):
        self.squareOccupied[self.pieceCount] = square
        self.map[square] = self.pieceCount
        pieceCount += 1

    def RemovePieceAtSquare(self, square):
        i = self.map[square]
        self.squareOccupied[i] = self.squareOccupied[self.pieceCount - 1]
        self.map[self.squareOccupied[i]] = i
        self.pieceCount -= 1

    def MovePiece(self, a, b):
        i = self.map[a]
        self.squareOccupied[i] = self.squareOccupied[self.pieceCount - 1]
        self.map[self.squareOccupied[i]] = b
        self.pieceCount -= 1
    

    
