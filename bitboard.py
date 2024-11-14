
A1, H1 = 0, 7
A8, H8 = 56, 63

empty_board = 0

print(f"{empty_board:064b}")

#initialize starting board
white_pawns = 0x0000FF00
black_pawns = 0x00FF000000000000
curr_board = empty_board | white_pawns | black_pawns
print(f"{curr_board:064b}")