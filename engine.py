from board import displayBoard, populateBoardFromFEN, formatAttackSquares
from setup import gameState
from move import generateMoves, makeMove, calculateKingAttacks
from user import userMove
from evaluate import bestMove

playing: bool = True
gameState["board"] = populateBoardFromFEN()
gameState["attackedSquares"] = formatAttackSquares()
gameState["attacksOnKing"] = calculateKingAttacks(gameState)
previousState: list = []
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
    
    previousState.append(gameState)
    gameState = makeMove(gameState, move)