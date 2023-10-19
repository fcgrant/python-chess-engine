board: list = ["x"] * 120
attackedSquares: dict = {
    "w": ["x"] * 120,
    "b": ["x"] * 120,
}
# Stores the index for each position in the 120 size array at the positions they
# would be in a 64 size array
boardLookup64: list = [
    21, 22, 23, 24, 25, 26, 27, 28,
    31, 32, 33, 34, 35, 36, 37, 38,
    41, 42, 43, 44, 45, 46, 47, 48,
    51, 52, 53, 54, 55, 56, 57, 58,
    61, 62, 63, 64, 65, 66, 67, 68,
    71, 72, 73, 74, 75, 76, 77, 78,
    81, 82, 83, 84, 85, 86, 87, 88,
    91, 92, 93, 94, 95, 96, 97, 98
]
# Stores the index for each position in the 64 size array at the positions they
# have in the 120 size array
positionLookup: dict = {
    "a1": 21, "b1": 22, "c1": 23, "d1": 24, "e1": 25, "f1": 26, "g1": 27, "h1": 28,
    "a2": 31, "b2": 32, "c2": 33, "d2": 34, "e2": 35, "f2": 36, "g2": 37, "h2": 38,
    "a3": 41, "b3": 42, "c3": 43, "d3": 44, "e3": 45, "f3": 46, "g3": 47, "h3": 48,
    "a4": 51, "b4": 52, "c4": 53, "d4": 54, "e4": 55, "f4": 56, "g4": 57, "h4": 58,
    "a5": 61, "b5": 62, "c5": 63, "d5": 64, "e5": 65, "f5": 66, "g5": 67, "h5": 68,
    "a6": 71, "b6": 72, "c6": 73, "d6": 74, "e6": 75, "f6": 76, "g6": 77, "h6": 78,
    "a7": 81, "b7": 82, "c7": 83, "d7": 84, "e7": 85, "f7": 86, "g7": 87, "h7": 88,
    "a8": 91, "b8": 92, "c8": 93, "d8": 94, "e8": 95, "f8": 96, "g8": 97, "h8": 98,
    "-": 0
}
# Directions for each piece to move
pieceOffset: dict = {
    "P": [10, 20, 9, 11],
    "N": [-19, -21, 21, 19, -8, -12, 12, 8],
    "B": [-9, -11, 11, 9],
    "R": [-10, 1, 10, -1],
    "Q": [-10, 1, 10, -1, -9, -11, 11, 9],
    "K": [-10, 1, 10, -1, -9, -11, 11, 9, 2, -2],
    "p": [-10, -20, -9, -11],
    "n": [-19, -21, 21, 19, -8, -12, 12, 8],
    "b": [-9, -11, 11, 9],
    "r": [-10, 1, 10, -1],
    "q": [-10, 1, 10, -1, -9, -11, 11, 9],
    "k": [-10, 1, 10, -1, -9, -11, 11, 9, 2, -2]
}
pieceSymbol: dict = {
    "p": "♙", "n": "♘", "b": "♗", "r": "♖", "q": "♕", "k": "♔",
    "P": "♟", "N": "♞", "B": "♝", "R": "♜", "Q": "♛", "K": "♚",
    ".": "·", " ": " "
}
pieceColour: dict = {
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
    ".": "No Colour",
    "": "No Colour"
}
captureList: dict = {
    "w": [],
    "b": []
}
attacksOnKing: dict = {
    "w": [],
    "b": []
}
# Track the indexes for the 2nd and 7th rank to see if a pawn can move twice
rank2: list = [31, 32, 33, 34, 35, 36, 37, 38]
rank7: list = [81, 82, 83, 84, 85, 86, 87, 88]

FEN: str = "rnbqkbnr/pppppppp/8/8/8/8/PPPPPPPP/RNBQKBNR w KQkq - 0 1"
startingPosition: str = FEN.split(" ")[0]
gameState: dict = {
    "board": board,
    "activeColour": FEN.split(" ")[1],
    "castlingRights": FEN.split(" ")[2],
    "enPassantSquare": positionLookup[FEN.split(" ")[3]],
    "halfMoveClock": int(FEN.split(" ")[4]),
    "fullMoveCounter": int(FEN.split(" ")[5]),
    "captureList": captureList,
    "attackedSquares": attackedSquares,
    "attacksOnKing": attacksOnKing
}
