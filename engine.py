from board import displayBoard, populateBoardFromFEN
from setup import activeColour, enPassantSquare, castlingRights, halfMoveClock, fullMoveCounter, captureList
from move import generateMoves, makeMove
from user import userMove
from evaluate import bestMove

playing: bool = True
board: list = populateBoardFromFEN()
previousState: list = []
gameState: map = {
    "board": board,
    "activeColour": activeColour,
    "castlingRights": castlingRights,
    "enPassantSquare": enPassantSquare,
    "halfMoveClock": halfMoveClock,
    "fullMoveCounter": fullMoveCounter,
    "captureList": captureList
}
playerColour: str = input("Playing as w or b: ")

if playerColour not in ["w", "b"]: exit(1)
if playerColour == "w": engineColour = "b" 
else: engineColour = "w"

while playing:
    
    displayBoard(gameState)

    moves = generateMoves(gameState)

    if gameState["activeColour"] == playerColour:
        move = userMove(moves)
        while move == {}:
            move = userMove(moves)
    else: 
        move = bestMove(moves)

    gameState = makeMove(gameState, move)