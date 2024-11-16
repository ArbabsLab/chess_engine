#piece direction

pieces = {
    "white_pawns":0xFF00,
    "white_king":0x10,
    "white_queen":0x8,
    "white_rook":0x81,
    "white_knight": 0x42,
    "white_bishop": 0x24,
    "black_pawns":0xFF000000000000,
    "black_king": 0x1000000000000000,  
    "black_queen": 0x0800000000000000,  
    "black_rook": 0x8100000000000000,  
    "black_knight": 0x4200000000000000,  
    "black_bishop": 0x2400000000000000,
}
       
board_state = 0x0 
for piece, position in pieces.items():
    board_state = board_state | position

print(f"{board_state:064b}")

def getBoard():
    board = []
    for i in range(63, -1, -1):
        board.append(int(bool(board_state & (1 << i))))
    return board

def showBoard():
    board = getBoard()
    for i in range(64):
        if i % 8 == 0:
            print("\n")
            print(board[i], end=" ")
        else:
            print(board[i], end=" ")
    print("\n")
    
        

showBoard()