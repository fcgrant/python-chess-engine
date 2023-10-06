from setup import rank2, rank7, pieceColour, pieceOffset

def generateMoves(gameState: map):
    moves: list = []
    opponentColour = "b" if gameState["activeColour"] == "w" else "w"
    
    # Convert en passant square to board index
    # enPassantIndex = positionLookup[enPassantSquare]
    
    for position, square in enumerate(gameState["board"]):
        if square == "." or square == 'x': continue
        if pieceColour[square] != gameState["activeColour"]: continue
        
        for offset in pieceOffset[square]:
            targetPosition = position

            # Should iterate through offsets only once if the piece is a King,
            # pawn or knight
            if square in "KkPpNn": moveLimit = 1
            else: moveLimit = 7

            for moveLength in range(moveLimit):
                targetPosition += offset
                targetSquare = gameState["board"][targetPosition]

                move = {
                    "StartingPosition": position, "TargetPosition": targetPosition,
                    "MovingPiece": square, "CapturedPiece": targetSquare
                }

                # OFF BOARD MOVE
                # If the target square is off the board, don't consider this offset
                if targetSquare == 'x': break

                # TARGET SQUARE OCCUPIED BY FRIENDLY
                # If the target square contains a friendly piece, don't consider this offset
                if pieceColour[targetSquare] == gameState["activeColour"]: break
                
                # DIAGONAL PAWN CAPTURE
                # If the current piece is a pawn and the offset is diagonal, only
                # allow a single move in this direction if the target square is occupied
                # by an opponents piece or that square can be captured with en Passant
                if square in "Pp" and offset in [-11, -9, 9, 11] and \
                    (pieceColour[targetSquare] != opponentColour or targetPosition != gameState["enPassantSquare"]): break

                # DOUBLE PAWN PUSHES
                # If the piece is a pawn, it can only move twice if it is on it's
                # starting square
                if square == "P" and offset == 20 and position not in rank2: break
                if square == "p" and offset == -20 and position not in rank7: break
                
                # If the pawn is making a double move, ensure the square the pawn
                # is moving over is not occupied
                if square in "Pp" and offset in [20, -20] and gameState["board"][targetPosition + int(offset / 2)] != '.': break
                
                # PAWN FORWARD MOVEMENT
                # Make sure the pawn cannot move forward if the square ahead is
                # blocked by an opponents piece
                if square in "Pp" and offset in [10, -10, 20, -20] and pieceColour[targetSquare] == opponentColour: break
                
                # CAPTURE VIA ENPASSANT
                # If moving to an enpassant square is possible, record the captured
                # piece as the one in front of the en passant square.
                if square in "Pp" and offset in [-11, -9, 9, 11] and targetPosition == gameState["enPassantSquare"]:
                    if gameState["activeColour"] == "w": enPassantOffset = 10
                    else: enPassantOffset = -10
                    move["CapturedPiece"] = gameState["board"][targetPosition + enPassantOffset]

                # CASTLING KING SIDE AS WHITE
                if square == "K" and offset == 2 and "K" in gameState["castlingRights"]:
                    # Check that the path between the king and the kings rook is
                    # unobstructed
                    if gameState["board"][targetPosition + 1] != "." or gameState["board"][targetPosition + 2] != ".": break
                    # Check that the king is not in check
                    
                    # Check that squares between the rook and king are not attacked
                    
                    moves.append(move)
                    break
                
                # Check castling rights for the white king to castle queen side
                if square == "K" and offset == -2 and "Q" in gameState["castlingRights"]:
                    # Check that the queens rook is on it's original square
                    if gameState["board"][position + 4] != "R": break
                    # Check that the king is not in check
                    # Check that squares between the rook and king are not attacked
                    moves.append(move)
                    break

                moves.append(move)

    return moves
        
def makeMove(gameState: map, move: map):
        
    board: list = gameState["board"]
    activeColour = gameState["activeColour"]
    castlingRights: str = gameState["castlingRights"]
    enPassantSquare: str = gameState["enPassantSquare"]
    halfMoveClock: int = gameState["halfMoveClock"]
    fullMoveCounter: int = gameState["fullMoveCounter"]
    captureList: map = gameState["captureList"]
    
    offset = move["TargetPosition"] - move["StartingPosition"]
    
    # Add enPassant square if the move is a double pawn push
    if move["MovingPiece"] in "Pp" and offset in [20, -20]:
        enPassantSquare = move["TargetPosition"] - int(offset / 2)
    else: enPassantSquare = 0
    
    # If the piece moving is a rook, revoke the castling rights for that side of the 
    # current player
    if move["MovingPiece"] == "R":
        if board[move["StartingPosition"] - 3] == "K": castlingRights.replace("K", "") # White king side castle
        if board[move["StartingPosition"] + 4] == "K": castlingRights.replace("Q", "") # White queen side castle
    elif move["MovingPiece"] == "r":
        if board[move["StartingPosition"] - 3] == "k": castlingRights.replace("k", "") # Black king side castle
        if board[move["StartingPosition"] + 4] == "k": castlingRights.replace("q", "") # Black queen side castle
        
    # If the piece being taken is a rook, revoke the castling rights for that side
    # of the opponent
    if move["CapturedPiece"] == "R":
        if board[move["TargetPosition"] - 3] == "K": castlingRights = castlingRights.replace("K", "") # White king side castle
        if board[move["TargetPosition"] + 4] == "K": castlingRights = castlingRights.replace("Q", "") # White queen side castle
    elif move["CapturedPiece"] == "r":
        if board[move["TargetPosition"] - 3] == "k": castlingRights = castlingRights.replace("k", "") # Black king side castle
        if board[move["TargetPosition"] + 4] == "k": castlingRights = castlingRights.replace("q", "") # Black queen side castle
        
    # If the moving piece is a king, check if they are intending to castle and 
    # revoke all castling rights for that player
    if move["MovingPiece"] == "K": 
        castlingRights = castlingRights.replace("KQ", "")
        
        if offset == -2:
            # Queen side castle
            board[move["TargetPosition"] + 1] = "R"
            board[move["TargetPosition"] - 2] = "."
        if offset == 2:
            # King side castle
            board[move["TargetPosition"] - 1] = "R"
            board[move["TargetPosition"] + 1] = "."            
            
    if move["MovingPiece"] == "k":
        castlingRights = castlingRights.replace("kq", "")
        if offset == -2:
            # Queen side castle
            board[move["TargetPosition"] + 1] = "R"
            board[move["TargetPosition"] - 2] = "."
        if offset == 2:
            # King side castle
            board[move["TargetPosition"] - 1] = "R"
            board[move["TargetPosition"] + 1] = "."
            

    # Move the moving piece to the target position and clear the starting position
    board[move["TargetPosition"]] = board[move["StartingPosition"]]
    board[move["StartingPosition"]] = "."

    # Add the captured piece to the current players capture list
    if move["CapturedPiece"] != ".": captureList[activeColour].append(move["CapturedPiece"])

    # Increment the full move counter if the moving piece is black
    if activeColour == "b": fullMoveCounter += 1

    # Increment the half move counter if the piece moved was not a pawn and no
    # piece was captured
    if move["MovingPiece"] not in "Pp" and move["CapturedPiece"] == ".":
        halfMoveClock += 1
    else: halfMoveClock = 0

    # Change the active colour once the move is made
    if activeColour == "w": activeColour = "b"
    else: activeColour = "w"

    gameState["board"] = board
    gameState["activeColour"] = activeColour
    gameState["castlingRights"] = castlingRights
    gameState["enPassantSquare"] = enPassantSquare
    gameState["halfMoveClock"] = halfMoveClock
    gameState["fullMoveCounter"] = fullMoveCounter
    gameState["captureList"] = captureList

    return gameState

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