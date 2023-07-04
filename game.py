class Othello:
    def __init__(self, player1, player2):
        self.__Board = Board()
        self.__Player1 = player1
        self.__Player2 = player2
        self.__Turn = 1
        self.__movedirections = [[-1,1], [0,1], [1,1], [1,0], [1,-1], [0,-1], [-1,-1], [-1,0]]

    def playGame(self):
        self.setupGame(1, 2)
        self.__Board.displayBoard()
        print("Black is 1 and White is 2")
        while True:
            if self.checkgameover():
                self.calculateWinner()
            if self.__Turn % 2 == 1:
                print(f"Black's ({self.__Player1.getName()}) turn")
                validmove = False
                # get the players move
                while not validmove:
                    column = int(input("Enter a column: ")) - 1
                    row = int(input("Enter a row: ")) - 1
                    if self.isvalidmove(1, column, row):
                        self.__Board.setBoard(column, row, BoardPiece(self.__Player1.getPieceColour()))
                        validmove = True
                    else:
                        print("Invalid move, try again")
            else:
                print(f"White's ({self.__Player2.getName()}) turn")

                # get the players move
                while not validmove:
                    column = int(input("Enter a column: ")) - 1
                    row = int(input("Enter a row: ")) - 1
                    if self.isvalidmove(2, column, row):
                        self.__Board.setBoard(column, row, BoardPiece(self.__Player1.getPieceColour()))
                        validmove = True
                    else:
                        print("Invalid move, try again")

            self.__Turn += 1
            self.__Board.displayBoard()


    def setupGame(self, colour1, colour2):
        # sets the board up with starting pieces
        self.__Board.fillBoard()

        #sets the players piece colour
        self.__Player1.setPieceColour(colour1)
        self.__Player2.setPieceColour(colour2)

    def willflip(self, colour, move, dir):
        i = 1
        while True:
            nextcol = move[1] + dir[1] * i
            nextrow = move[0] + dir[0] * i
            if self.coordvalid(nextcol, nextrow):
                # if the next piece is the same colour, break
                if self.__Board.getBoardPiece(nextcol, nextrow) == colour:
                    break
                # if the next piece is empty, return false
                elif self.__Board.getBoardPiece(nextcol, nextrow) == 0:
                    return False
                # if the next piece is the opposite colour, continue
                else:
                    i += 1
        return i > 1
    
    def isvalidmove(self, colour, col, row):

        for mov in self.__movedirections:
            if self.willflip(colour, [row, col], mov):
                return True
        return False

    def coordvalid(self, col, row):
        if col > 0 and col < 8 and row > 0 and row < 8:
            return True
        return False              

    def checkgameover(self):
        if self.__Board.isFull():
            return True
        return False

    def calculateWinner(self):                 
        if self.__Board.getBlackScore() > self.__Board.getWhiteScore():
            print(f"{self.__Player1.getName()} wins!")
        elif self.__Board.getBlackScore() < self.__Board.getWhiteScore():
            print(f"{self.__Player2.getName()} wins!")
        else:
            print("It's a tie!")


        
class Board:
    def __init__(self):
        self.__Board = [[None for x in range(8)] for y in range(8)]
    
    def getBoard(self):
        return self.__Board
    
    def displayBoard(self):
        print("  1 2 3 4 5 6 7 8")
        for i in range(8):
            print(i+1, end = " ")
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
        for i in range(8):
            for j in range(8):
                if self.__Board[i][j] == 2:
                    count += 1

        return count

    def getBlackScore(self):
        count = 0
        for i in range(8):
            for j in range(8):
                if self.__Board[i][j] == 1:
                    count += 1

        return count
class BoardPiece:
    def __init__(self, value):
        self.__Value = value #black is 1 and white is 2
    
    
    def getValue(self):
        return self.__Value
    
    def setValue(self, value):
        self.__Value = value

class Player:
    def __init__(self, name):
        self.__Name = name
        self.__pieceColour = None

    def getName(self):
        return self.__Name

    def getPieceColour(self):
        return self.__pieceColour
    
    def setPieceColour(self, colour):
        self.__pieceColour = colour

if __name__ == "__main__":
    
    game = Othello(Player(input("Player 1 enter your name: ")), Player(input("Player 2 enter your name: ")))
    game.playGame()
