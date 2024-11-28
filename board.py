from pieces import Piece
from boardHelper import BoardHelper
from state import GameState
from engine import Move

class Board:
    WhiteIndex = 0
    BlackIndex = 1

    def __init__(self):
        self.Square = [None] * 64  # Board squares (64 squares)
        self.KingSquare = [None, None]  # Kings' positions for white and black
        self.PieceBitboards = [0] * 12  # 12 piece bitboards (6 for each color)
        self.ColourBitboards = [0] * 2  # 2 bitboards for white and black pieces
        self.AllPiecesBitboard = 0
        self.FriendlyOrthogonalSliders = 0
        self.FriendlyDiagonalSliders = 0
        self.EnemyOrthogonalSliders = 0
        self.EnemyDiagonalSliders = 0
        self.TotalPieceCountWithoutPawnsAndKings = 0
        self.Rooks = [[], []]
        self.Bishops = [[], []]
        self.Queens = [[], []]
        self.Knights = [[], []]
        self.Pawns = [[], []]
        self.IsWhiteToMove = True
        self.RepetitionPositionHistory = []
        self.PlyCount = 0
        self.CurrentGameState = None
        self.ZobristKey = None
        self.AllGameMoves = []

        # Private stuff
        self.allPieceLists = []
        self.gameStateHistory = []
        self.StartPositionInfo = None
        self.cachedInCheckValue = False
        self.hasCachedInCheckValue = False

    def MakeMove(self, move, inSearch=False):
        startSquare = move.StartSquare
        targetSquare = move.TargetSquare
        moveFlag = move.MoveFlag
        isPromotion = move.IsPromotion
        isEnPassant = moveFlag == Move.EnPassantCaptureFlag

        movedPiece = self.Square[startSquare]
        movedPieceType = Piece.PieceType(movedPiece)
        capturedPiece = self.Square[targetSquare] if not isEnPassant else Piece.MakePiece(Piece.Pawn, self.OpponentColour)
        capturedPieceType = Piece.PieceType(capturedPiece)

        prevCastleState = self.CurrentGameState.castlingRights
        prevEnPassantFile = self.CurrentGameState.enPassantFile
        newZobristKey = self.CurrentGameState.zobristKey
        newCastlingRights = self.CurrentGameState.castlingRights
        newEnPassantFile = 0

        # Update bitboard of moved piece
        self.MovePiece(movedPiece, startSquare, targetSquare)

        # Handle captures
        if capturedPieceType != Piece(None):
            if isEnPassant:
                captureSquare = targetSquare + (-8 if self.IsWhiteToMove else 8)
                self.Square[captureSquare] = Piece(None)
            if capturedPieceType != Piece.Pawn:
                self.TotalPieceCountWithoutPawnsAndKings -= 1

            # Remove captured piece from bitboards/piece list
            self.allPieceLists[capturedPiece].RemovePieceAtSquare(captureSquare)
            BitBoardUtility.ToggleSquare(self.PieceBitboards[capturedPiece], captureSquare)
            BitBoardUtility.ToggleSquare(self.ColourBitboards[self.OpponentColourIndex], captureSquare)
            newZobristKey ^= Zobrist.piecesArray[capturedPiece, captureSquare]

        # Handle king
        if movedPieceType == Piece.King:
            self.KingSquare[self.MoveColourIndex] = targetSquare
            newCastlingRights &= 0b1100 if self.IsWhiteToMove else 0b0011

            # Handle castling
            if moveFlag == Move.CastleFlag:
                rookPiece = Piece.MakePiece(Piece.Rook, self.MoveColour)
                kingside = targetSquare == BoardHelper.g1 or targetSquare == BoardHelper.g8
                castlingRookFromIndex = targetSquare + 1 if kingside else targetSquare - 2
                castlingRookToIndex = targetSquare - 1 if kingside else targetSquare + 1

                # Update rook position
                BitBoardUtility.ToggleSquares(self.PieceBitboards[rookPiece], castlingRookFromIndex, castlingRookToIndex)
                BitBoardUtility.ToggleSquares(self.ColourBitboards[self.MoveColourIndex], castlingRookFromIndex, castlingRookToIndex)
                self.allPieceLists[rookPiece].MovePiece(castlingRookFromIndex, castlingRookToIndex)
                self.Square[castlingRookFromIndex] = Piece(None)
                self.Square[castlingRookToIndex] = Piece.Rook | self.MoveColour

                newZobristKey ^= Zobrist.piecesArray[rookPiece, castlingRookFromIndex]
                newZobristKey ^= Zobrist.piecesArray[rookPiece, castlingRookToIndex]

        # Handle promotion
        if isPromotion:
            self.TotalPieceCountWithoutPawnsAndKings += 1
            promotionPieceType = {
                Move.PromoteToQueenFlag: Piece.Queen,
                Move.PromoteToRookFlag: Piece.Rook,
                Move.PromoteToKnightFlag: Piece.Knight,
                Move.PromoteToBishopFlag: Piece.Bishop,
            }.get(moveFlag, 0)

            promotionPiece = Piece.MakePiece(promotionPieceType, self.MoveColour)

            # Remove pawn from promotion square and add promoted piece instead
            BitBoardUtility.ToggleSquare(self.PieceBitboards[movedPiece], targetSquare)
            BitBoardUtility.ToggleSquare(self.PieceBitboards[promotionPiece], targetSquare)
            self.allPieceLists[movedPiece].RemovePieceAtSquare(targetSquare)
            self.allPieceLists[promotionPiece].AddPieceAtSquare(targetSquare)
            self.Square[targetSquare] = promotionPiece

        # Handle en-passant
        if moveFlag == Move.PawnTwoUpFlag:
            file = BoardHelper.FileIndex(startSquare) + 1
            newEnPassantFile = file
            newZobristKey ^= Zobrist.enPassantFile[file]

        # Update castling rights
        if prevCastleState != 0:
            if targetSquare == BoardHelper.h1 or startSquare == BoardHelper.h1:
                newCastlingRights &= GameState.ClearWhiteKingsideMask
            elif targetSquare == BoardHelper.a1 or startSquare == BoardHelper.a1:
                newCastlingRights &= GameState.ClearWhiteQueensideMask
            elif targetSquare == BoardHelper.h8 or startSquare == BoardHelper.h8:
                newCastlingRights &= GameState.ClearBlackKingsideMask
            elif targetSquare == BoardHelper.a8 or startSquare == BoardHelper.a8:
                newCastlingRights &= GameState.ClearBlackQueensideMask

        # Update zobrist key with new piece position and side to move
        newZobristKey ^= Zobrist.sideToMove
        newZobristKey ^= Zobrist.piecesArray[movedPiece, startSquare]
        newZobristKey ^= Zobrist.piecesArray[self.Square[targetSquare], targetSquare]
        newZobristKey ^= Zobrist.enPassantFile[prevEnPassantFile]

        if newCastlingRights != prevCastleState:
            newZobristKey ^= Zobrist.castlingRights[prevCastleState]
            newZobristKey ^= Zobrist.castlingRights[newCastlingRights]

        # Change side to move
        self.IsWhiteToMove = not self.IsWhiteToMove

        self.PlyCount += 1
        newFiftyMoveCounter = self.CurrentGameState.fiftyMoveCounter + 1

        # Update extra bitboards
        self.AllPiecesBitboard = self.ColourBitboards[self.WhiteIndex] | self.ColourBitboards[self.BlackIndex]
        self.UpdateSliderBitboards()

        # Pawn moves and captures reset the fifty move counter and clear 3-fold repetition history
        if movedPieceType == Piece.Pawn or capturedPieceType != Piece(None):
            if not inSearch:
                self.RepetitionPositionHistory.clear()
            newFiftyMoveCounter = 0

        newState = GameState(capturedPieceType, newEnPassantFile, newCastlingRights, newFiftyMoveCounter, newZobristKey)
        self.gameStateHistory.append(newState)
        self.CurrentGameState = newState
        self.hasCachedInCheckValue = False

        if not inSearch:
            self.RepetitionPositionHistory.append(newState.zobristKey)
            self.AllGameMoves.append(move)

    def UnmakeMove(self, move, inSearch=False):
        self.IsWhiteToMove = not self.IsWhiteToMove
        undoingWhiteMove = self.IsWhiteToMove

        movedFrom = move.StartSquare
        movedTo = move.TargetSquare
        moveFlag = move.MoveFlag

        undoingEnPassant = moveFlag == Move.EnPassantCaptureFlag
        undoingPromotion = move.IsPromotion
        undoingCapture = self.CurrentGameState.capturedPieceType != Piece(None)

        movedPiece = Piece.MakePiece(Piece.Pawn, self.MoveColour) if undoingPromotion else self.Square[movedTo]
        movedPieceType = Piece.PieceType(movedPiece)
        capturedPieceType = self.CurrentGameState.capturedPieceType

        if undoingPromotion:
            promotedPiece = self.Square[movedTo]
            pawnPiece = Piece.MakePiece(Piece.Pawn, self.MoveColour)
            self.TotalPieceCountWithoutPawnsAndKings -= 1

            self.allPieceLists[promotedPiece].RemovePieceAtSquare(movedTo)
            self.allPieceLists[pawnPiece].AddPieceAtSquare(movedTo)
            self.Square[movedTo] = pawnPiece

        self.UnmoveCapturedPiece(capturedPieceType, moveFlag, movedFrom, movedTo)
        
        return True
