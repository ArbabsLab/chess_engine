class State():
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
