import json
class Chess():
    def __init__(self, filename):
        # Setup for starting board config and class properties
        with open(filename, encoding='utf8') as file:
            self.__dict__ = json.loads(file.read())

            self.activeColour = 0 if self.fen.split()[1] == 'w' else 1
            self.FormatBoard(self.fen.split()[0])

    def PrintBoard(self):
        boardList = list()
        file = 0
        for char in self.board:
            # Append a space before each square for display purposes
            boardList.append(' ')
            
            # Print the unicode symbol for each square
            boardList.append(self.pieces[char])
                
            # Append a newline character if you've reached the end of the file
            if (file % 7 == 0 and file != 0):
                boardList.append('\n')
                file = 0
            else:
                file += 1

        print(''.join(boardList))
        
    def FormatBoard(self, fenNotation: str):
        board = list()

        fenNotation = fenNotation.replace('/', '')
        
        for char in fenNotation:
            if char.isdigit():
                # Replace the numbers in FEN notation with that many dots
                for i in range(int(char)):
                    board.append('.')
            else:
                board.append(char)

        self.board = ''.join(board)
        
    def GenerateMoveList(self):
        moveList = []
        for square in range(len(self.board)):
            piece = self.board[square]
            # Only consider pieces of the current players colour
            if piece != '.' and self.colours[piece] == self.activeColour:
                print(square)
                for offset in self.directions[piece]:
                    targetSquare = square
                    while True:
                        targetSquare += offset 
                        capturedPiece = self.board[targetSquare]
                        
                        # If the target square contains a piece of the current
                        # players colour, then this offset can no longer be 
                        # traversed
                        if self.colours[capturedPiece] == self.activeColour: break
                        
                        # Check that the target square is actually on the board
                        if 
                    # Break if the target square is occupied by a piece of the players
                    # colour
                    
        return moveList
    
    def Play(self):
        self.GenerateMoveList()

chess = Chess('settings.json')
chess.PrintBoard()
chess.Play()