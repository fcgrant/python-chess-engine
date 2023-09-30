
# Contains code pertinent to displaying, formatting, and changing the properties
# off the chess board

def displayBoard(board: list, pieceSymbol: map, lookup: list, activeColour: str):
    
    boardDisplay: list = [ square for index, square in enumerate(board) if index in lookup]    
    
    if activeColour == "w": boardDisplay.reverse()
    
    for index, square in enumerate(boardDisplay):
        if index % 8 == 0 and index != 0: print()
        print(pieceSymbol[square], end=" ")
        
    print()
        
def populateBoardFromFEN(board: list, FEN: str, lookup: list):
    lookupPosition = 0
    FEN = FEN.replace("/", "")[::-1]
    for piece in FEN:
        boardPosition = lookup[lookupPosition]
        if piece.isnumeric():
            for position in range(int(piece)):
                board[boardPosition] = "." 
                lookupPosition += 1
                boardPosition = lookup[lookupPosition]
        else:
            board[boardPosition] = piece
            lookupPosition += 1
    
    return board