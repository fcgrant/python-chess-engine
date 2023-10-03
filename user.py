from setup import positionLookup
# Take user input, which is either a move or a resign and return the move, which
# is empty if the move is invalid
def userMove(validMoves: list):
    
    files = "abcdefgh"
    ranks = "12345678"
    userMove: str = input("Move: ")
    
    if userMove == "resign":
        print("User resigned, engine wins")
        exit(0)
    
    if len(userMove) != 4: 
        print("Invalid move")
        return {}
    
    startingFile = userMove[0]
    startingRank = userMove[1]
    targetFile = userMove[2]
    targetRank = userMove[3]
    
    if startingFile not in files or targetFile not in files:
        print("Invalid move")
        return {}
    if startingRank not in ranks or targetRank not in ranks:
        print("Invalid move")
        return {}
    
    for move in validMoves:
        startingPosition = positionLookup[startingFile + startingRank]
        targetPosition = positionLookup[targetFile + targetRank]
        
        if move["StartingPosition"] == startingPosition and move["TargetPosition"] == targetPosition:
            return move
      
    print("Invalid move")
    return {}