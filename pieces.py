class Pieces:
    """
    most significant and 2nd most significant bits are color representations
    3 least significant bits are for pieces
    """
    def __init__(self):
        self.Empty = 0
        self.King = 1
        self.Queen = 2
        self.Rook = 3
        self.Knight = 4
        self.Bishop = 5
        self.Pawn = 6

        self.White = 8
        self.Black = 16

        self.WhitePawn = self.Pawn | self.White
        self.WhiteKnight = self.Knight | self.White
        self.WhiteBishop = self.Bishop | self.White
        self.WhiteRook = self.Rook | self.White
        self.WhiteQueen = self.Queen | self.White
        self.WhiteKing = self.King | self.White

        self.BlackPawn = self.Pawn |self.Black
        self.BlackKnight = self.Knight |self.Black
        self.BlackBishop = self.Bishop |self.Black
        self.BlackRook = self.Rook |self.Black
        self.BlackQueen = self.Queen |self.Black
        self.BlackKing = self.King |self.Black
