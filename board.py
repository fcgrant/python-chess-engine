from setup import startingPosition, pieceSymbol, boardLookup, board

def displayBoard(gameConfig: map):
    
    # Strip away the border symbols when displaying the board
    boardDisplay: list = [ square for index, square in enumerate(gameConfig["board"]) if index in boardLookup]    
    
    # If the the human player is white, we should display the board with the 
    # white pieces at the bottom
    # If playerColour == "w": ...
    for index, square in enumerate(boardDisplay):
        if index % 8 == 0 and index != 0: print()
        print(pieceSymbol[square], end=" ")
        
    print()
        
def populateBoardFromFEN():
    
    # Start at h1 to run through the array and populate with the fen values
    lookupPosition = 0
    position = startingPosition.split("/")
    position.reverse()
    position = ''.join(position)
    
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