
def makeNewBoard():
    board = []
    for i in range(8):
        board.append([])
        for j in range(8):
            if i==1 or i==6:
                board[i].append('P')
            elif i==0 or i==7:
                if j == 0 or j == 7:
                    board[i].append('R')
                elif j == 1 or j == 6:
                    board[i].append('N')
                elif j == 2 or j == 5:
                    board[i].append('B')
                elif j == 3:
                    board[i].append('Q')
                elif j == 4:
                    board[i].append('K')
            else:
                board[i].append('-')
            
    return board

print(makeNewBoard())

