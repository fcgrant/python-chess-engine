from board import displayBoard, populateBoardFromFEN
from setup import startingFEN, board, pieceSymbols, activeColour

board = populateBoardFromFEN(board, startingFEN[0], activeColour)

displayBoard(board, pieceSymbols)