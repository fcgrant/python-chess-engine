import json
class Chess():
    def __init__(self, filename):
        # Setup for starting board config and class properties
        with open(filename, encoding='utf8') as file:
            self.__dict__ = json.loads(file.read())

            self.activeColour = 0 if self.fen.split()[1] == 'w' else 1
            self.printBoard(self.fen.split()[0])

    def printBoard(self, fenNotation: str):
        boardList = list()
        fenNotation = fenNotation.replace('/', '\n')
        for char in fenNotation:
            # Append a space before each square for display
            boardList.append(' ')
            
            # Replace the numbers in FEN notation with that many dots
            if char.isdigit():
                # Replace the numbers in FEN notation with that many dots
                for i in range(int(char)):
                    boardList.append('.' + ' ')
            else:
                # Replace piece letters with their unicode symbol
                boardList.append(self.pieces[char])

        # Join the board list into a multi-line string
        board = ''.join(boardList)
        print(board)

chess = Chess("settings.json")