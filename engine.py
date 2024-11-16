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
    #parse square into bit position
        square = 2 ** square

        for piece, pos in self.pieces.items():
            check = bool(self.board_state & pos & square)
            if check:
                return piece
            
    #TODO: move piece from a to b
    #get piece at a, move to b

    def moveHandle(self, a, b):
        pass

    
    #TODO update board and pieces dict
    #may have to alter for capturing since xor wont work in that case
    def updateBoard(self, a, b, piece_to_update):
        self.board_state = self.board_state ^ (2**a)
        self.board_state = self.board_state | (2**b)
        self.pieces[piece_to_update] = self.pieces[piece_to_update] ^ (2**a) | (2**b)


state = State()
state.showBoard()  # Show initial board
state.updateBoard(8, 24, "white_pawns")  # Move white pawn from A2 to A4
state.showBoard()  # Show updated board

    

    


        




    