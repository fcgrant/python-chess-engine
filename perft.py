from setup import board, activeColour, enPassantSquare, castlingRights, halfMoveClock, fullMoveCounter, captureList, attackedSquares
from board import populateBoardFromFEN
from move import generateMoves, makeMove, undoMove

# Performance test, indicates how many moves are available after a given depth
# for debugging purposes
board = populateBoardFromFEN()
gameState: map = {
    "board": board,
    "activeColour": activeColour,
    "castlingRights": castlingRights,
    "enPassantSquare": enPassantSquare,
    "halfMoveClock": halfMoveClock,
    "fullMoveCounter": fullMoveCounter,
    "captureList": captureList,
    "attackedSquares": attackedSquares
}

previousState: list = []

def perft(depth: int, gameState: map, previousState: list):
    
    nodes = generateMoves(gameState)
    moveCounter = len(nodes)
    
    if depth == 1:
        return moveCounter
    
    for i in range(len(nodes)):
        gameState = makeMove(gameState, nodes[i])
        previousState.append(gameState)
        
        moveCounter += perft(depth - 1, gameState, previousState)
        
        gameState = undoMove(previousState)
          
    return moveCounter

perft(2, gameState, previousState)