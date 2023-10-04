from random import randint

def bestMove(moves: list):
    
    # Call evaluate function here
    bestMove = moves[randint(0, len(moves) - 1)]
    
    return bestMove