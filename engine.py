from board import displayBoard, populateBoardFromFEN
from setup import currentPosition, board, pieceSymbol, activeColour, boardLookup, pieceColour, pieceOffset, moveLimit
from move import generateMoves, displayMoves

board = populateBoardFromFEN(board, currentPosition, boardLookup)

displayBoard(board, pieceSymbol, boardLookup, activeColour)

moves = generateMoves(board, activeColour, pieceOffset, pieceColour, moveLimit)

displayMoves(moves)