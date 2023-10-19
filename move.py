from setup import rank2, rank7, pieceColour, pieceOffset

def generateMoves(gameState: map):
    moves: list = []
    board = gameState["board"]
    enPassantSquare = gameState["enPassantSquare"]
    activeColour = gameState["activeColour"]
    attackedSquares = gameState["attackedSquares"]
    attacksOnKing = gameState["attacksOnKing"]
    
    opponentColour = "b" if activeColour == "w" else "w"
    
    for position, square in enumerate(board):
        if square == "." or square == 'x': continue
        if pieceColour[square] != activeColour: continue
        
        for offset in pieceOffset[square]:
            targetPosition = position

            # Should iterate through offsets only once if the piece is a King,
            # pawn or knight
            if square in "KkPpNn": moveLimit = 1
            else: moveLimit = 7

            for moveLength in range(moveLimit):
                targetPosition += offset
                targetSquare = board[targetPosition]

                move = {
                    "StartingPosition": position, "TargetPosition": targetPosition,
                    "MovingPiece": square, "CapturedPiece": targetSquare
                }

                # OFF BOARD MOVE
                # If the target square is off the board, don't consider this offset
                if targetSquare == 'x': break

                # TARGET SQUARE OCCUPIED BY FRIENDLY
                # If the target square contains a friendly piece, don't consider this offset
                if pieceColour[targetSquare] == activeColour: break

                # DIAGONAL PAWN CAPTURE
                # If the current piece is a pawn and the offset is diagonal, only
                # allow a single move in this direction if the target square is occupied
                # by an opponents piece or that square can be captured with en Passant
                if square in "Pp" and offset in [-11, -9, 9, 11] and \
                        (pieceColour[targetSquare] != opponentColour or targetPosition != enPassantSquare):
                    # Although the move is not allowed unless an opponents piece
                    # occupies the target square, we still need to add this square
                    # to the attacked squares list
                    attackedSquares[activeColour][targetPosition] += square
                    break

                # DOUBLE PAWN PUSHES
                # If the piece is a pawn, it can only move twice if it is on it's
                # starting square
                if square == "P" and offset == 20 and position not in rank2: break
                if square == "p" and offset == -20 and position not in rank7: break

                # If the pawn is making a double move, ensure the square the pawn
                # is moving over is not occupied
                if square in "Pp" and offset in [20, -20] and board[targetPosition + int(offset / 2)] != '.': break

                # PAWN FORWARD MOVEMENT
                # Make sure the pawn cannot move forward if the square ahead is
                # blocked by an opponents piece
                if square in "Pp" and offset in [10, -10, 20, -20] and pieceColour[targetSquare] == opponentColour: break

                # CAPTURE VIA ENPASSANT
                # If moving to an enpassant square is possible, record the captured
                # piece as the one in front of the en passant square.
                if square in "Pp" and offset in [-11, -9, 9, 11] and targetPosition == enPassantSquare:
                    if activeColour == "w": enPassantOffset = 10
                    else: enPassantOffset = -10
                    move["CapturedPiece"] = board[targetPosition + enPassantOffset]

                # CASTLING
                if square in "Kk" and offset in [2, -2] and not castleAllowed(move, offset, gameState): break

                # Append the move to the attack squares, unless the move is 
                # castling or a pawn moving forward
                if not ((square in "Pp" and offset in [10, 20, -20, -10]) or (square in "Kk" and offset in [-2, 2])):
                    attackedSquares[activeColour][targetPosition] += square

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

def undoMove(previousState: list):
    return previousState[len(previousState) - 1]

def displayMoves(moves: list):
    print("Total moves: " + str(len(moves)))

    for move in moves:
        startingPosition = move["StartingPosition"]
        targetPosition = move["TargetPosition"]
        piece = move["MovingPiece"]

        print(str(piece) + ": " + str(startingPosition) + " to " + str(targetPosition))


def castleAllowed(move: map, offset: int, gameState: map):
    castlingRights = gameState["castlingRights"]
    board = gameState["board"]
    opponentColour = "b" if gameState["activeColour"] == "w" else "w"
    attackedSquares = gameState["attackedSquares"][opponentColour]
    piece = move["MovingPiece"]
    startingPosition = move["StartingPosition"]
    # If the king is in check, cannot castle
    if isInCheck(gameState): return False

    # If the moving piece is not a king, cannot castle#
    if piece not in "Kk": return False

    # If the offset is not a castling move, cannot castle
    if offset not in [2, -2]: return False

    # If king side castle is attempted, but rights are revoked, cannot castle
    if offset == 2 and piece not in castlingRights: return False

    # If queen side castle is attempted, but rights are revoked, cannot castle
    if piece == "K" and offset == -2 and "Q" not in castlingRights: return False
    if piece == "k" and offset == -2 and "q" not in castlingRights: return False

    # If squares between the king and target square are obstructed, cannot castle
    if board[startingPosition + int(offset / 2)] != '.' or board[startingPosition + offset] != '.': return False

    # If squares between king and target square are attacked by opponent, cannot castle 
    if attackedSquares[startingPosition + int(offset / 2)] != "" or attackedSquares[
        startingPosition + offset] != "": return False

    return True


def isInCheck(gameState: map):
    activeColour: str = gameState["activeColour"]
    activeKing = "K" if activeColour == "w" else "k"
    opponentColour: str = "b" if activeColour == "w" else "w"
    attackedSquares: list = gameState["attackedSquares"][opponentColour]
    board: list = gameState["board"]

    for index, square in enumerate(board):
        if square == activeKing: kingSquare = index

    attackingPieces = attackedSquares[kingSquare]
    if attackingPieces == 'x' or attackingPieces == '': return False

    for piece in attackingPieces:
        if pieceColour[piece] == opponentColour: return True

    return False


def calculateKingAttacks(gameState: dict):
    board: list = gameState["board"]
    activeColour: str = gameState["activeColour"]
    attacksOnKing: list = gameState["attacksOnKing"][activeColour]
    opponentColour: str = "b" if activeColour == "w" else "w"
    kingSquare = -1

    # Find the king square for the given active colour
    for index, square in enumerate(board):
        if square in "Kk" and pieceColour[square] == activeColour:
            kingSquare = index

    if kingSquare == -1:
        return

    bishop, queen, rook = "b", "q", "r"

    if opponentColour == "w":
        bishop = bishop.upper()
        queen = queen.upper()
        rook = rook.upper()

    bishopOffsets = pieceOffset[bishop]
    rookOffsets = pieceOffset[rook]
    # Check bishop offsets for bishop/queen attacks on king
    for offset in bishopOffsets:
        bishopAttacks = []
        targetSquare = kingSquare

        # Add each square in this offset to an attack list, and if you find an
        # opponent bishop or queen at some point in this offset add all squares
        # the the king attack list
        for length in range(8):
            targetSquare += offset
            if board[targetSquare] == "x": break

            # Append the list of all attacked squares in this offset to the king
            # attacks list
            if board[targetSquare] == bishop or board[targetSquare] == queen:
                attacksOnKing.extend(bishopAttacks)
                break

            if pieceColour[board[targetSquare]] == opponentColour: break

            bishopAttacks.append(targetSquare)

    # Check rook offsets for rook/queen attacks on king
    for offset in rookOffsets:
        rookAttacks = []
        targetSquare = kingSquare

        # Add each square in this offset to an attack list, and if you find an
        # opponent rook or queen at some point in this offset add all squares
        # the the king attack list
        for length in range(8):
            targetSquare += offset
            if board[targetSquare] == "x": break

            # Append the list of all attacked squares in this offset to the king
            # attacks list
            if board[targetSquare] == rook or board[targetSquare] == queen:
                attacksOnKing.extend(rookAttacks)
                break

            if pieceColour[board[targetSquare]] == opponentColour: break

            rookAttacks.append(targetSquare)

    return attacksOnKing
