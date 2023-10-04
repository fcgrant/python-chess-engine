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
        
    board = gameConfig["board"]
    enPassantSquare = gameConfig["enPassantSquare"]
    board[move["TargetPosition"]] = board[move["StartingPosition"]]
    board[move["StartingPosition"]] = "."
    
    offset = move["TargetPosition"] - move["StartingPosition"]
    
    # Add en Passant square if the move is a double pawn push
    if move["MovingPiece"] in "Pp" and (offset == 20 or offset == -20):
        enPassantSquare = move["TargetPosition"] + (offset / 2)
    # If the piece being taken is a rook or the piece moving is a rook, revoke the
    # castling rights for that side of the opponent

    return board

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