#Will handle all states of the game and state updates

#initialize starting board
class State:
    def __init__(self):
        self.pieces = {
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
       
        self.board_state = 0x0 
        for piece, position in self.pieces.items():
            self.board_state = self.board_state | position
        
        #initial flags and checks
        self.whiteMove = True
        self.blackMove = False
        self.move_log = []
        self.in_check = False
        self.in_stalemate = False
        self.in_mate = False
    
    
    def getBoard(self):
        board = []
        for i in range(63, -1, -1):
            board.append(int(bool(self.board_state & (1 << i))))
        return board
    
    def showBoard(self):
        board = self.getBoard()
        for i in range(64):
            if i % 8 == 0:
                print("\n")
                print(board[i], end=" ")
            else:
                print(board[i], end=" ")
        print("\n")

    def toggleTurn(self):
        self.blackMove = not self.whiteMove
        self.whiteMove = not self.blackMove
    
    def getPiece(self, square):
        for piece, pos in self.pieces.items():
            


    def moveHandle(self, a, b):
        #check whose turn it is
        #validate appropriate color piece is on a
        #check if move is valid
        #update self.board_state
        #toggle turn
        
        if self.whiteMove:
            moving_piece = self.getPiece(a)
            # Validate if it's a white piece
            if moving_piece == "w":
                self.updateBoard(a, b, moving_piece)
                self.toggleTurn()
                self.move_log.append((a, b, moving_piece))
        elif self.blackMove:
            moving_piece = self.getPiece(a)
            # Validate if it's a black piece
            if moving_piece == "b":
                self.updateBoard(a, b, moving_piece)
                self.toggleTurn()
                self.move_log.append((a, b, moving_piece))
    
    def updateBoard(self, a, b, piece_color):
    
        self.board_state = self.board_state & ~(1 << a)  
        self.board_state = self.board_state | (1 << b)     # Set the to square
        self.pieces[piece_color] |= (1 << b)


state = State()
state.showBoard()  # Show initial board
state.moveHandle(8, 16)  # Move white pawn from E2 to E4
state.showBoard()  # Show updated board

    

    


        




    