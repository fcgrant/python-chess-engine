board: list = ["x"] * 120
# Stores the index for each position in the 120 size array at the positions they
# would be in a 64 size array
boardLookup: list = [
    21, 22, 23, 24, 25, 26, 27, 28,
    31, 32, 33, 34, 35, 36, 37, 38,
    41, 42, 43, 44, 45, 46, 47, 48,
    51, 52, 53, 54, 55, 56, 57, 58,
    61, 62, 63, 64, 65, 66, 67, 68, 
    71, 72, 73, 74, 75, 76, 77, 78, 
    81, 82, 83, 84, 85, 86, 87, 88,
    91, 92, 93, 94, 95, 96, 97, 98
]
# Directions for each piece to move
pieceOffset: map = {
    "P": [10, 20, 9, 11],
    "N": [-19, -21, 21, 19, -8, -12, 12, 8],
    "B": [-9, -11, 11, 9],
    "R": [-10, 1, 10, -1],
    "Q": [-10, 1, 10, -1, -9, -11, 11, 9],
    "K": [-10, 1, 10, -1, -9, -11, 11, 9],
    "p": [-10, -20, -9, -11],
    "n": [-19, -21, 21, 19, -8, -12, 12, 8],
    "b": [-9, -11, 11, 9],
    "r": [-10, 1, 10, -1],
    "q": [-10, 1, 10, -1, -9, -11, 11, 9],
    "k": [-10, 1, 10, -1, -9, -11, 11, 9]
}
# The maximum number of squares a piece can traverse in one direction
moveLimit: map = {
    "P": 2,
    "N": 1,
    "B": 7,
    "R": 7,
    "Q": 7,
    "K": 1,
    "p": 2,
    "n": 1,
    "b": 7,
    "r": 7,
    "q": 7,
    "k": 1
}
pieceSymbol: map = {
    "p": "♙", "n": "♘", "b": "♗", "r": "♖", "q": "♕", "k": "♔",
    "P": "♟", "N": "♞", "B": "♝", "R": "♜", "Q": "♛", "K": "♚",
    ".": "·", " ": " "
}
pieceColour: map = {
    "P": "w",
    "N": "w",
    "B": "w",
    "R": "w",
    "Q": "w",
    "K": "w",
    "p": "b",
    "n": "b",
    "b": "b",
    "r": "b",
    "q": "b",
    "k": "b",
    ".": "No Colour"
}
# Track the indexes for the 2nd and 7th rank to see if a pawn can move twice
rank2: list = [31, 32, 33, 34, 35, 36, 37, 38]
rank7: list = [81, 82, 83, 84, 85, 86, 87, 88]

startingFEN: str = "rnbqkbnr/pppppppp/8/8/8/8/PPPPPPPP/RNBQKBNR w KQkq - 0 1".split(" ")
currentPosition: str = startingFEN[0]
activeColour: str = startingFEN[1]
castlingRights: str = startingFEN[2]
enPassantSquare: str = startingFEN[3]
halfMoveClock: int = int(startingFEN[4])
fullMoveCounter: int = int(startingFEN[5])

