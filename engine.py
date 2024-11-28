from pieces import Piece

class Move:
    # Flags
    NoFlag = 0b0000
    EnPassantCaptureFlag = 0b0001
    CastleFlag = 0b0010
    PawnTwoUpFlag = 0b0011

    PromoteToQueenFlag = 0b0100
    PromoteToKnightFlag = 0b0101
    PromoteToRookFlag = 0b0110
    PromoteToBishopFlag = 0b0111

    # Masks
    startSquareMask = 0b0000000000111111
    targetSquareMask = 0b0000111111000000
    flagMask = 0b1111000000000000

    def __init__(self, move_value=None, start_square=None, target_square=None, flag=None):
        if move_value is not None:
            self.move_value = move_value
        elif start_square is not None and target_square is not None:
            self.move_value = (start_square | (target_square << 6))
        elif start_square is not None and target_square is not None and flag is not None:
            self.move_value = (start_square | (target_square << 6) | (flag << 12))
        else:
            self.move_value = 0

    @property
    def value(self):
        return self.move_value

    @property
    def is_null(self):
        return self.move_value == 0

    @property
    def start_square(self):
        return self.move_value & self.startSquareMask

    @property
    def target_square(self):
        return (self.move_value & self.targetSquareMask) >> 6

    @property
    def is_promotion(self):
        return self.move_flag >= self.PromoteToQueenFlag

    @property
    def move_flag(self):
        return self.move_value >> 12

    @property
    def promotion_piece_type(self):
        if self.move_flag == self.PromoteToRookFlag:
            return Piece.Rook
        elif self.move_flag == self.PromoteToKnightFlag:
            return Piece.Knight
        elif self.move_flag == self.PromoteToBishopFlag:
            return Piece.Bishop
        elif self.move_flag == self.PromoteToQueenFlag:
            return Piece.Queen
        else:
            return Piece.None

    @staticmethod
    def null_move():
        return Move(0)

    @staticmethod
    def same_move(a, b):
        return a.move_value == b.move_value
