from setup import startingPosition, pieceSymbol, boardLookup64, board

def displayBoard(gameState: map):
    # Strip away the border symbols when displaying the board
    boardDisplay: list = [ square for index, square in enumerate(gameState["board"]) if index in boardLookup64]
    
    # If the the human player is white, we should display the board with the 
    # white pieces at the bottom
    # If playerColour == "w": ...
    for index, square in enumerate(boardDisplay):
        if index % 8 == 0 and index != 0: print()
        print(pieceSymbol[square], end=" ")
        
    print()
    
    for colour in gameState["captureList"]:
        captureList: list = gameState["captureList"][colour]
        if len(captureList) == 0: break
        print("Captured by " + colour + ": ", end="")
        for piece in captureList:
            print(pieceSymbol[piece], end=" ")
    print()
        
def populateBoardFromFEN():
    
    lookupPosition = 0
    
    # The FEN string starts with black pieces then works down the ranks, but to
    # populate the board array starting with white pieces we need to put the FEN 
    # string into the correct order, starting at a1
    position = startingPosition.split("/")
    position.reverse()
    position = ''.join(position)
    
    for piece in position:
        boardPosition = boardLookup64[lookupPosition]
        if piece.isnumeric():
            for square in range(int(piece)):
                board[boardPosition] = "."
                lookupPosition += 1
                boardPosition = boardLookup64[lookupPosition]
        else:
            board[boardPosition] = piece
            lookupPosition += 1
    
    return board