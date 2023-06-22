class Game:
    def __init__(self, player1, player2):
        self.__Board = Board()
        self.__Player1 = player1
        self.__Player2 = player2

class Board:
    def __init__(self):
        self.__Board = [[BoardPiece() for x in range(8)] for y in range(8)]
    
    def getBoard(self):
        return self.__Board
    
    def displayBoard(self):
        print("  1 2 3 4 5 6 7 8")
        for i in range(8):
            print(i+1, end = " ")
            for j in range(8):
                print(self.__Board[i][j].getValue(), end = " ")
            print()

    def setBoard(self, col, row, value):
        self.__Board[row][col] = value

class BoardPiece:
    def __init__(self):
        self.__Color = None
        self.__Value = 0
    
    def getColor(self):
        return self.__Color
    
    def setColor(self, color):
        self.__Color = color
    
    def getValue(self):
        return self.__Value
    
    def setValue(self, value):
        self.__Value = value

class Player:
    pass


