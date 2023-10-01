from setup import rank2, rank7, pieceColour, pieceOffset, moveLimit, positionLookup
from random import randint

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
                
                moves.append({
                    "StartingPosition": position, "TargetPosition": targetPosition,
                    "MovingPiece": square, "CapturedPiece": targetSquare
                })
                
    return moves

def makeUserMove(board: list, validMoves: list):
    
    files = "abcdefgh"
    ranks = "12345678"
    userMove: str = input("Move: ")
    
    if len(userMove) != 4: 
        print("Invalid move")
        return
    
    startingFile = userMove[0]
    startingRank = userMove[1]
    targetFile = userMove[2]
    targetRank = userMove[3]
    
    if startingFile not in files or targetFile not in files:
        print("Invalid move")
        return board
    if startingRank not in ranks or targetRank not in ranks:
        print("Invalid move")
        return board
    
    for move in validMoves:
        startingPosition = positionLookup[startingFile + startingRank]
        targetPosition = positionLookup[targetFile + targetRank]
        
        if move["StartingPosition"] == startingPosition and move["TargetPosition"] == targetPosition:
            board[targetPosition] = board[startingPosition]
            board[startingPosition] = "."
            return board
      
    print("Invalid move")
    return board
        
def makeEngineMove(board: list, validMoves: list):
    
    # Pick a random move from the moves list
    index = randint(0, len(validMoves) - 1)
    move = validMoves[index]
    
    targetPosition = ""
    startingPosition = ""
    
    board[move["TargetPosition"]] = board[move["StartingPosition"]]
    board[move["StartingPosition"]] = "."
    
    for position in positionLookup:
        if positionLookup[position] == move["TargetPosition"]:
            targetPosition = position
        elif positionLookup[position] == move["StartingPosition"]:
            startingPosition = position

    print("Engine moved " + startingPosition + " to " + targetPosition)

    return board

def displayMoves(moves: list):
    
    print("Total moves: " + str(len(moves)))
    
    for move in moves:
        startingPosition = move["StartingPosition"]
        targetPosition = move["TargetPosition"]
        piece = move["MovingPiece"]
        print(str(piece) + ": " + str(startingPosition) + " to " + str(targetPosition))