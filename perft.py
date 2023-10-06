from setup import board, activeColour, enPassantSquare, castlingRights, halfMoveClock, fullMoveCounter, captureList
from board import populateBoardFromFEN
from move import generateMoves

gameState: map = {
    "board": board,
    "activeColour": activeColour,
    "castlingRights": castlingRights,
    "enPassantSquare": enPassantSquare,
    "halfMoveClock": halfMoveClock,
    "fullMoveCounter": fullMoveCounter,
    "captureList": captureList
}
# Performance test, indicates how many moves are available after a given depth
# for debugging purposes
board = populateBoardFromFEN()
def perft(depth: int):
    
    if depth == 0:
        return
    
    nodes = generateMoves(gameState)
    for i in range(len(nodes)):
        nodes
    return nodes

perft(0)