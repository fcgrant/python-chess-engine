from board import displayBoard, populateBoardFromFEN
from setup import activeColour, enPassantSquare
from move import generateMoves, makeMove, displayMoves
from user import userMove
from evaluate import bestMove

playing = True
board = populateBoardFromFEN()
playerColour = input("Playing as w or b: ")

if playerColour not in ["w", "b"]: exit(1)
if playerColour == "w": engineColour = "b" 
else: engineColour = "w"

while playing:
    
    displayBoard(board, activeColour)

    moves = generateMoves(board, activeColour, enPassantSquare)

    if activeColour == playerColour:
        move = userMove(moves)
        while move != {}:
            move = userMove(moves)
        activeColour = engineColour
    else: 
        move = bestMove(moves)
        activeColour = playerColour
        
    board = makeMove(board, move)
    
    displayMoves([move])