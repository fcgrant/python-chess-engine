board: list = ["."] * 64
pieceOffsets: map = {
    "P": [ 7, 8, 9],
    "N": [ -15, -6, 10, 17, 15, 6, -10, -17],
    "B": [ -9, -7, 7, 9],
    "R": [ -8, -1, 1, -8],
    "Q": [ -9, -8, -7, -1, 1, 7, 8, 9],
    "K": [ -9, -8, -7, -1, 1, 7, 8, 9],
    "p": [ -7, -8, -9],
    "n": [ -15, -6, 10, 17, 15, 6, -10, -17],
    "b": [ -9, -7, 7, 9],
    "r": [ -8, -1, 1, -8],
    "q": [ -9, -8, -7, -1, 1, 7, 8, 9],
    "k": [ -9, -8, -7, -1, 1, 7, 8, 9]
}
pieceSymbols: map = {
    "p": "♙", "n": "♘", "b": "♗", "r": "♖", "q": "♕", "k": "♔",
    "P": "♟", "N": "♞", "B": "♝", "R": "♜", "Q": "♛", "K": "♚",
    ".": "·", " ": " "
}
startingFEN: str = "rnbqkbnr/pppppppp/8/8/8/8/PPPPPPPP/RNBQKBNR w KQkq - 0 1".split(" ")
currentPosition: str = startingFEN[0]
activeColour: str = startingFEN[1]
castlingRights: str = startingFEN[2]
enPassantSquare: str = startingFEN[3]
halfMoveClock: int = int(startingFEN[4])
fullMoveCounter: int = int(startingFEN[5])

