from boardpiece import BoardPiece
class Board:
    def __init__(self, board):
        self.__Board = board
    
    def getBoard(self):
        return self.__Board
    
    def boardAsList(self):
        boardList = []
        for row in range(8):
            rowlist = []
            for col in range(8):
                if self.__Board[row][col]:
                    rowlist.append(self.__Board[row][col].getValue())
                else:
                    rowlist.append(0)
            boardList.append(rowlist)
        return boardList
    def displayBoard(self):
        print("  0 1 2 3 4 5 6 7")
        for i in range(8):
            print(i, end = " ")
            for j in range(8):
                if self.__Board[i][j]:
                    print(self.__Board[i][j].getValue(), end = " ")
                else:
                    print("0", end = " ")
            print()

    def setBoard(self, col, row, value):
        self.__Board[row][col] = value

    def fillBoard(self):
        for i in range(8):
            for j in range(8):
                if i == j == 3 or i == 4 == j:
                    self.__Board[i][j] = BoardPiece(1)
                elif i == 3 and j == 4 or i == 4 and j == 3:
                    self.__Board[i][j] = BoardPiece(2)
    
    def isFull(self):
        for i in range(8):
            for j in range(8):
                if not self.__Board[i][j]:
                    return False
        return True

    def getBoardPiece(self, col, row):
        if self.__Board[row][col]:
            return self.__Board[row][col].getValue()
        else:
            return 0

    def getWhiteScore(self):
        count = 0
        for row in range(8):
            for col in range(8):
                if self.__Board[row][col]:
                    if self.__Board[row][col].getValue() == 2:
                        count += 1

        return count

    def getBlackScore(self):
        count = 0
        for i in range(8):
            for j in range(8):
                if self.__Board[i][j].getValue() == 1:
                    count += 1

        return count