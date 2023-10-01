from setup import startingPosition, pieceSymbol, boardLookup

def displayBoard(board: list, playerColour: str):
    
    # Strip away the border symbols when displaying the board
    boardDisplay: list = [ square for index, square in enumerate(board) if index in boardLookup]    
    
    # If the the human player is white, we should display the board with the 
    # white pieces at the bottom
    # If playerColour == "w": ...
    for index, square in enumerate(boardDisplay):
        if index % 8 == 0 and index != 0: print()
        print(pieceSymbol[square], end=" ")
        
    print()
        
def populateBoardFromFEN(board: list):
    
    lookupPosition = 0
    position = startingPosition.replace("/", "")[::-1]
    
    for piece in position:
        boardPosition = boardLookup[lookupPosition]
        if piece.isnumeric():
            for square in range(int(piece)):
                board[boardPosition] = "."
                lookupPosition += 1
                boardPosition = boardLookup[lookupPosition]
        else:
            board[boardPosition] = piece
            lookupPosition += 1
    
    return board