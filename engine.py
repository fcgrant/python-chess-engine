from board import displayBoard, populateBoardFromFEN
from setup import activeColour, enPassantSquare, castlingRights, halfMoveClock, fullMoveCounter
from move import generateMoves, makeMove, displayMoves
from user import userMove
from evaluate import bestMove

playing = True
board = populateBoardFromFEN()
gameConfig: map = {
    "board": board,
    "activeColour": activeColour,
    "castlingRights": castlingRights,
    "enPassantSquare": enPassantSquare,
    "halfMoveClock": halfMoveClock,
    "fullMoveCounter": fullMoveCounter
}
playerColour = input("Playing as w or b: ")

if playerColour not in ["w", "b"]: exit(1)
if playerColour == "w": engineColour = "b" 
else: engineColour = "w"

while playing:
    
    displayBoard(gameConfig)

    moves = generateMoves(gameConfig)

    if gameConfig["activeColour"] == playerColour:
        move = userMove(moves)
        while move == {}:
            move = userMove(moves)
    else: 
        move = bestMove(moves)

    gameConfig = makeMove(gameConfig, move)