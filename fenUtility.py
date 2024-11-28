from pieces import Pieces
from boardHelper import BoardHelper
from typing import List


class FenUtility:
    START_POSITION_FEN = "rnbqkbnr/pppppppp/8/8/8/8/PPPPPPPP/RNBQKBNR w KQkq - 0 1"

    @staticmethod
    def position_from_fen(fen: str):
        return FenUtility.PositionInfo(fen)

    @staticmethod
    def current_fen(board, always_include_ep_square=True) -> str:
        fen = ""

        # Piece positions
        for rank in range(7, -1, -1):
            empty_files = 0
            for file in range(8):
                i = rank * 8 + file
                piece = board.squares[i]
                if piece != 0:
                    if empty_files > 0:
                        fen += str(empty_files)
                        empty_files = 0
                    fen += Pieces().get_symbol(piece)
                else:
                    empty_files += 1
            if empty_files > 0:
                fen += str(empty_files)
            if rank > 0:
                fen += "/"

        # Side to move
        fen += " "
        fen += "w" if board.white_to_move else "b"

        # Castling rights
        fen += " "
        castling = ""
        if board.castling_rights & 1:
            castling += "K"
        if board.castling_rights & 2:
            castling += "Q"
        if board.castling_rights & 4:
            castling += "k"
        if board.castling_rights & 8:
            castling += "q"
        fen += castling if castling else "-"

        # En passant
        fen += " "
        ep_file = board.en_passant_file - 1
        ep_rank = 5 if board.white_to_move else 2
        if ep_file >= 0:
            fen += BoardHelper.square_name_from_coordinate(ep_file, ep_rank)
        else:
            fen += "-"

        # 50-move rule counter
        fen += f" {board.fifty_move_counter}"

        # Full-move count
        fen += f" {((board.ply_count // 2) + 1)}"

        return fen

    @staticmethod
    def flip_fen(fen: str) -> str:
        sections = fen.split(" ")
        board_fen = sections[0]
        flipped_board = "/".join(reversed(FenUtility.invert_case(rank) for rank in board_fen.split("/")))

        flipped_side = "b" if sections[1] == "w" else "w"
        flipped_castling = "".join(FenUtility.invert_case(c) for c in "kqKQ" if c in sections[2])
        flipped_castling = flipped_castling if flipped_castling else "-"

        ep_square = sections[3]
        flipped_ep = "-" if ep_square == "-" else ep_square[0] + ("3" if ep_square[1] == "6" else "6")

        return f"{flipped_board} {flipped_side} {flipped_castling} {flipped_ep} {sections[4]} {sections[5]}"

    @staticmethod
    def invert_case(c: str) -> str:
        return c.lower() if c.isupper() else c.upper()

    class PositionInfo:
        def __init__(self, fen: str):
            self.fen = fen
            self.squares = FenUtility.parse_squares(fen)

        @staticmethod
        def parse_squares(fen: str) -> List[int]:
            board, *_ = fen.split(" ")
            squares = []
            for char in board:
                if char.isdigit():
                    squares.extend([0] * int(char))
                elif char != "/":
                    squares.append(Pieces().make_piece(Pieces().get_piece(char.lower()), 
                                                       Pieces().Black if char.islower() else Pieces().White))
            return squares
