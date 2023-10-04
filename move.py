from setup import rank2, rank7, pieceColour, pieceOffset, moveLimit

def generateMoves(board: list, activeColour: str, enPassantSquare: str):
    moves: list = []
    opponentColour = "b" if activeColour == "w" else "w"
    
    # Convert en passant square to board index
    # enPassantIndex = positionLookup[enPassantSquare]
    
    for position, square in enumerate(board):
        if square == "." or square == 'x': continue
        if pieceColour[square] != activeColour: continue
        
        for offset in pieceOffset[square]:
            targetPosition = position
            
            for move in range(moveLimit[square]):
                targetPosition += offset
                targetSquare = board[targetPosition]
                
                # If the target square is off the board, don't consider this offset
                if targetSquare == 'x': break
                
                # If the target square contains a friendly piece, don't consider this offset
                if pieceColour[targetSquare] == activeColour: break
                
                # If the current piece is a pawn and the offset is diagonal, only
                # allow a single move in this direction if the target square is occupied
                # by an opponents piece or that square can be captured with en Passant
                if square in "Pp" and offset in [-11, -9, 9, 11] and \
                    (pieceColour[targetSquare] != opponentColour): break
                
                # If the piece is a pawn, it can only move twice if it is on it's
                # starting square
                if square == "P" and offset == 20 and square not in rank2: break
                if square == "p" and offset == -20 and square not in rank7: break
                
                # If moving to an enpassant square is possible, record the captured
                # piece as the one in front of the en passant square.
                
                moves.append({
                    "StartingPosition": position, "TargetPosition": targetPosition,
                    "MovingPiece": square, "CapturedPiece": targetSquare
                })
                
    return moves
        
def makeMove(board: list, move: map):
        
    board[move["TargetPosition"]] = board[move["StartingPosition"]]
    board[move["StartingPosition"]] = "."

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