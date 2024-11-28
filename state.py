class GameState():
    def __init__(self) -> None:
        self.capturedPieceType = 0
        self.enpassantFile = 0
        self.castlingRights = 0
        self.fiftyMoveCounter = 0

    def State(self, capturedPieceType, enPassantFile, castlingRights, fiftyMoveCounter):
        self.capturedPieceType = capturedPieceType
        self.enPassantFile = enPassantFile
        self.castlingRights = castlingRights
        self.fiftyMoveCounter = fiftyMoveCounter
    
    def canCastleKing(self, white):
        mask = 1 if white else 4
        return (self.castlingRights & mask) != 0
    
    def canCastleQueen(self, white):
        mask = 2 if white else 8
        return (self.castlingRights & mask) != 0
