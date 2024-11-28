class Piece:
    """
    Encodes pieces as binary numbers:
    - Most significant bit indicates color (Black/White)
    - Least significant bits indicate piece type
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

        # Define individual pieces
        self.WhitePawn = self.Pawn | self.White
        self.WhiteKnight = self.Knight | self.White
        self.WhiteBishop = self.Bishop | self.White
        self.WhiteRook = self.Rook | self.White
        self.WhiteQueen = self.Queen | self.White
        self.WhiteKing = self.King | self.White

        self.BlackPawn = self.Pawn | self.Black
        self.BlackKnight = self.Knight | self.Black
        self.BlackBishop = self.Bishop | self.Black
        self.BlackRook = self.Rook | self.Black
        self.BlackQueen = self.Queen | self.Black
        self.BlackKing = self.King | self.Black

    def make_piece(self, type, color):
        return type | color

    def is_white(self, piece):
        return (piece & 0b1000) == self.White and piece != self.Empty

    def piece_color(self, piece):
        return piece & 0b1000

    def piece_type(self, piece):
        return piece & 0b0111

    def get_symbol(self, piece):
        piece_type = self.piece_type(piece)
        symbols = {self.Pawn: "P", self.Knight: "N", self.Bishop: "B",
                   self.Rook: "R", self.Queen: "Q", self.King: "K"}
        symbol = symbols.get(piece_type, " ")
        return symbol.lower() if not self.is_white(piece) else symbol

    def is_orthogonal_slider(self, piece):
        return self.piece_type(piece) in {self.Queen, self.Rook}

    def is_diagonal_slider(self, piece):
        return self.piece_type(piece) in {self.Queen, self.Bishop}

    def is_sliding_piece(self, piece):
        return self.piece_type(piece) in {self.Queen, self.Rook, self.Bishop}
