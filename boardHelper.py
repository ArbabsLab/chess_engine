from dataclasses import dataclass
from typing import List, Tuple


@dataclass(frozen=True)
class Coord:
    file_index: int
    rank_index: int

    def is_light_square(self) -> bool:
        return (self.file_index + self.rank_index) % 2 != 0

    def is_valid_square(self) -> bool:
        return 0 <= self.file_index < 8 and 0 <= self.rank_index < 8

    def square_index(self) -> int:
        return BoardHelper.index_from_coord(self)

    def __add__(self, other):
        return Coord(self.file_index + other.file_index, self.rank_index + other.rank_index)

    def __sub__(self, other):
        return Coord(self.file_index - other.file_index, self.rank_index - other.rank_index)

    def __mul__(self, multiplier: int):
        return Coord(self.file_index * multiplier, self.rank_index * multiplier)


class BoardHelper:
    ROOK_DIRECTIONS = [Coord(-1, 0), Coord(1, 0), Coord(0, 1), Coord(0, -1)]
    BISHOP_DIRECTIONS = [Coord(-1, 1), Coord(1, 1), Coord(1, -1), Coord(-1, -1)]

    FILE_NAMES = "abcdefgh"
    RANK_NAMES = "12345678"

    @staticmethod
    def rank_index(square_index: int) -> int:
        return square_index >> 3

    @staticmethod
    def file_index(square_index: int) -> int:
        return square_index & 0b111

    @staticmethod
    def index_from_coord(coord: Coord) -> int:
        return coord.rank_index * 8 + coord.file_index

    @staticmethod
    def index_from_file_and_rank(file_index: int, rank_index: int) -> int:
        return rank_index * 8 + file_index

    @staticmethod
    def coord_from_index(square_index: int) -> Coord:
        return Coord(BoardHelper.file_index(square_index), BoardHelper.rank_index(square_index))

    @staticmethod
    def is_light_square(file_index: int, rank_index: int) -> bool:
        return (file_index + rank_index) % 2 != 0

    @staticmethod
    def square_name_from_coordinate(file_index: int, rank_index: int) -> str:
        return f"{BoardHelper.FILE_NAMES[file_index]}{rank_index + 1}"

    @staticmethod
    def square_name_from_index(square_index: int) -> str:
        coord = BoardHelper.coord_from_index(square_index)
        return BoardHelper.square_name_from_coordinate(coord.file_index, coord.rank_index)

    @staticmethod
    def square_name_from_coordinate_obj(coord: Coord) -> str:
        return BoardHelper.square_name_from_coordinate(coord.file_index, coord.rank_index)

    @staticmethod
    def square_index_from_name(name: str) -> int:
        file_name = name[0]
        rank_name = name[1]
        file_index = BoardHelper.FILE_NAMES.index(file_name)
        rank_index = BoardHelper.RANK_NAMES.index(rank_name)
        return BoardHelper.index_from_file_and_rank(file_index, rank_index)

    @staticmethod
    def is_valid_coordinate(x: int, y: int) -> bool:
        return 0 <= x < 8 and 0 <= y < 8

    @staticmethod
    def create_diagram(board, black_at_top: bool = True, include_fen: bool = True, include_zobrist_key: bool = True) -> str:
        result = []
        last_move_square = board.all_game_moves[-1].target_square if board.all_game_moves else -1

        for y in range(8):
            rank_index = 7 - y if black_at_top else y
            result.append("+---" * 8 + "+")

            for x in range(8):
                file_index = x if black_at_top else 7 - x
                square_index = BoardHelper.index_from_file_and_rank(file_index, rank_index)
                highlight = square_index == last_move_square
                piece = board.squares[square_index]
                if highlight:
                    result.append(f"|({board.piece_symbol(piece)})")
                else:
                    result.append(f"| {board.piece_symbol(piece)} ")

                if x == 7:
                    result.append(f"| {rank_index + 1}\n")

        result.append("+---" * 8 + "+")
        file_names = "  a   b   c   d   e   f   g   h  " if black_at_top else "  h   g   f   e   d   c   b   a  "
        result.append(file_names + "\n")

        if include_fen:
            result.append(f"Fen         : {board.current_fen()}\n")
        if include_zobrist_key:
            result.append(f"Zobrist Key : {board.zobrist_key}\n")

        return "".join(result)



