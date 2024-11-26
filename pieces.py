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

        self.White = 0
        self.Black = 8

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


    def makePiece(self, type, color):
        return type | color
    
    def isWhite(self, piece):
        return (piece & 0b1000) == self.White and piece != 0
    
    def pieceColor(self, piece):
        return (piece & 0b1000)
    
    def pieceType(self, piece):
        return (piece & 0b0111)
    
    def getSymbol(self, piece):
        pieceType = self.pieceType(piece)
        if pieceType == "rook":
            symbol = 'R'
        elif pieceType == "knight":
            symbol = 'N'
        elif pieceType == "bishop":
            symbol = 'B'
        elif pieceType == "queen":
            symbol = 'Q'
        elif pieceType == "king":
            symbol = 'K'
        elif pieceType == "pawn":
            symbol = 'P'
        else:
            symbol = ' '
        if not self.isWhite(piece): 
            symbol = symbol.lower()

        return symbol
    
    def getPiece(self, sym):
        sym = sym.upper()
        if sym == 'R':
            return 'rook'
        elif sym == 'N':
            return 'knight'
        elif sym == 'B':
            return 'bishop'
        elif sym == 'Q':
            return 'queen'
        elif sym == 'K':
            return 'king'
        elif sym == 'P':
            return 'pawn'
        else:
            return ' '
    
    def IsOrthogonalSlider(self, piece):
        if self.pieceType(piece) == 'queen' or self.pieceType(piece) == 'rook':
            return True
        else:
            return False
        
    def IsDiagonalSlider(self, piece):
        if self.pieceType(piece) == 'queen' or self.pieceType(piece) == 'bishop':
            return True
        else:
            return False
    
    def IsSlidingSlider(self, piece):
        if self.pieceType(piece) == 'queen' or self.pieceType(piece) == 'bishop' or self.pieceType(piece) == 'rook':
            return True
        else:
            return False


    