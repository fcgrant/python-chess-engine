from board import displayBoard, populateBoardFromFEN
from setup import board, activeColour, enPassantSquare
from move import generateMoves, makeUserMove, makeEngineMove

playing = True
board = populateBoardFromFEN(board)
playerColour = input("Playing as w or b: ")

if playerColour not in ["w", "b"]: exit(1)
if playerColour == "w": engineColour = "b" 
else: engineColour = "w"

while playing:
    
    displayBoard(board, activeColour)

    moves = generateMoves(board, activeColour, enPassantSquare)

    if activeColour == playerColour:
        board = makeUserMove(board, moves)
        activeColour = engineColour
    else: 
        board = makeEngineMove(board, moves)
        activeColour = playerColour