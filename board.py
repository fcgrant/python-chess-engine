
# Contains code pertinent to displaying, formatting, and changing the properties
# off the chess board

def displayBoard(board: list, pieceSymbols: map):
    for index, square in enumerate(board):
        if index % 8 == 0 and index != 0: print()
        print(pieceSymbols[square], end=" ")
    
def populateBoardFromFEN(board: list, FEN: str, activeColour: str):
    boardPosition = 0
    FEN = FEN.replace("/", "")
    if activeColour == "b": FEN = FEN[::-1]
    for piece in FEN:
        if piece.isnumeric():
            for position in range(int(piece)):
                board[boardPosition] = "." 
                boardPosition += 1
        else:
            board[boardPosition] = piece
            boardPosition += 1
    
    return board