from setup import board, activeColour, enPassantSquare
from board import populateBoardFromFEN
from move import generateMoves

# Performance test, indicates how many moves are available after a given depth
# for debugging purposes
board = populateBoardFromFEN()
def perft(depth: int):
    
    nodes = generateMoves(board, activeColour, enPassantSquare)
    return
perft(0)