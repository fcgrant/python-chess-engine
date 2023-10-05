from setup import rank2, rank7, pieceColour, pieceOffset

def generateMoves(gameConfig: map):
    moves: list = []
    opponentColour = "b" if gameConfig["activeColour"] == "w" else "w"
    
    # Convert en passant square to board index
    # enPassantIndex = positionLookup[enPassantSquare]
    
    for position, square in enumerate(gameConfig["board"]):
        if square == "." or square == 'x': continue
        if pieceColour[square] != gameConfig["activeColour"]: continue
        
        for offset in pieceOffset[square]:
            targetPosition = position

            # Should iterate through offsets only once if the piece is a King,
            # pawn or knight
            if square in "KkPpNn": moveLimit = 1
            else: moveLimit = 7

            for move in range(moveLimit):
                targetPosition += offset
                targetSquare = gameConfig["board"][targetPosition]

                # If the target square is off the board, don't consider this offset
                if targetSquare == 'x': break

                # If the target square contains a friendly piece, don't consider this offset
                if pieceColour[targetSquare] == gameConfig["activeColour"]: break
                
                # If the current piece is a pawn and the offset is diagonal, only
                # allow a single move in this direction if the target square is occupied
                # by an opponents piece or that square can be captured with en Passant
                if square in "Pp" and offset in [-11, -9, 9, 11] and \
                    (pieceColour[targetSquare] != opponentColour or targetPosition == gameConfig["enPassantSquare"]): break
                
                # If the piece is a pawn, it can only move twice if it is on it's
                # starting square
                if square == "P" and offset == 20 and position not in rank2: break
                if square == "p" and offset == -20 and position not in rank7: break
                
                # Make sure the pawn cannot move forward if the square ahead is
                # blocked by an opponents piece
                if square in "Pp" and offset in [10, -10, 20, -20] and pieceColour[targetSquare] == opponentColour: break
                
                # If the pawn is making a double move, ensure the square the pawn
                # is moving over is not occupied
                if square in "Pp" and offset in [20, -20] and gameConfig["board"][targetPosition + int(offset / 2)] != '.': break
                
                # If moving to an enpassant square is possible, record the captured
                # piece as the one in front of the en passant square.
                
                # Check castling rights for the king to castle king side
                if square in "Kk" and offset == -2 and square in gameConfig["castlingRights"]:
                    # Check that the kings rook is on it's original square
                    if gameConfig["board"][position - 3] != "R": break
                    # Check that the king is not in check
                    
                    # Check that squares between the rook and king are not attacked
                    moves.append({
                        "StartingPosition": position, "TargetPosition": targetPosition,
                        "MovingPiece": square, "CapturedPiece": targetSquare
                    })
                    break
                
                # Check castling rights for the white king to castle queen side
                if square == "K" and offset == 2 and "Q" in gameConfig["castlingRights"]:
                    # Check that the queens rook is on it's original square
                    if gameConfig["board"][position + 4] != "R": break
                    # Check that the king is not in check
                    # Check that squares between the rook and king are not attacked
                    moves.append({
                        "StartingPosition": position, "TargetPosition": targetPosition,
                        "MovingPiece": square, "CapturedPiece": targetSquare
                    })
                    break
                
                
                moves.append({
                    "StartingPosition": position, "TargetPosition": targetPosition,
                    "MovingPiece": square, "CapturedPiece": targetSquare
                })
                
    return moves
        
def makeMove(gameConfig: map, move: map):
        
    board: list = gameConfig["board"]
    activeColour = gameConfig["activeColour"]
    castlingRights: str = gameConfig["castlingRights"]
    enPassantSquare: str = gameConfig["enPassantSquare"]
    halfMoveClock: int = gameConfig["halfMoveClock"]
    fullMoveCounter: int = gameConfig["fullMoveCounter"]
    
    offset = move["TargetPosition"] - move["StartingPosition"]
    
    # Add enPassant square if the move is a double pawn push
    if move["MovingPiece"] in "Pp" and offset in [20, -20]:
        enPassantSquare = move["TargetPosition"] - int(offset / 2)
    else: enPassantSquare = 0
    
    # If the piece moving is a rook, revoke the castling rights for that side of the 
    # current player
    if move["MovingPiece"] == "R":
        if board[move["StartingPosition"] + 3] == "K": castlingRights.replace("K", "") # White king side castle
        if board[move["StartingPosition"] - 4] == "K": castlingRights.replace("Q", "") # White queen side castle
    elif move["MovingPiece"] == "r":
        if board[move["StartingPosition"] - 3] == "k": castlingRights.replace("k", "") # Black king side castle
        if board[move["StartingPosition"] + 4] == "k": castlingRights.replace("q", "") # Black queen side castle
        
    # If the piece being taken is a rook, revoke the castling rights for that side
    # of the opponent
    if move["CapturedPiece"] == "R":
        if board[move["TargetPosition"] + 3] == "K": castlingRights = castlingRights.replace("K", "") # White king side castle
        if board[move["TargetPosition"] - 4] == "K": castlingRights = castlingRights.replace("Q", "") # White queen side castle
    elif move["CapturedPiece"] == "r":
        if board[move["TargetPosition"] - 3] == "k": castlingRights = castlingRights.replace("k", "") # Black king side castle
        if board[move["TargetPosition"] + 4] == "k": castlingRights = castlingRights.replace("q", "") # Black queen side castle
        
    # If the moving piece is a king, revoke all castling rights for that player
    if move["MovingPiece"] == "K": castlingRights = castlingRights.replace("KQ", "")
    if move["MovingPiece"] == "k": castlingRights = castlingRights.replace("kq", "")
        
    # Move the moving piece to the target position and add the captured piece
    # to the current players list of captured pieces
    board[move["TargetPosition"]] = board[move["StartingPosition"]]
    board[move["StartingPosition"]] = "."
    
    # Increment the full move counter if the moving piece is black
    if activeColour == "b": fullMoveCounter += 1
    
    # Increment the half move counter if the piece moved was not a pawn and no
    # piece was captured
    if move["MovingPiece"] not in "Pp" and move["CapturedPiece"] == ".":
        halfMoveClock += 1
    
    # Change the active colour once the move is made
    if activeColour == "w": activeColour = "b"
    else: activeColour = "w"
    
    
    gameConfig["board"] = board
    gameConfig["activeColour"] = activeColour
    gameConfig["castlingRights"] = castlingRights
    gameConfig["enPassantSquare"] = enPassantSquare
    gameConfig["halfMoveClock"] = halfMoveClock
    gameConfig["fullMoveCounter"] = fullMoveCounter
    
    return gameConfig

def undoMove(board: list, move: map):
    
    originalPosition = move["StartingPosition"]
    currentPosition = move["TargetPosition"]
    capturedPiece = move["CapturedPiece"]
    movedPiece = board[currentPosition]
    
    board[originalPosition] = movedPiece
    board[currentPosition] = capturedPiece
    
    return board

def displayMoves(moves: list):
    
    print("Total moves: " + str(len(moves)))
    
    for move in moves:
        startingPosition = move["StartingPosition"]
        targetPosition = move["TargetPosition"]
        piece = move["MovingPiece"]
        print(str(piece) + ": " + str(startingPosition) + " to " + str(targetPosition))