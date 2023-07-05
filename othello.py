from board import Board
from boardpiece import BoardPiece
from player import Player

class Othello:
    '''
        Class: Othello
        Attributes:
            Board: a class Board that represents the board
            Player1: a class Player that represents player 1
            Player2: a class Player that represents player 2
            Turn: an integer that represents the turn
            movedirections: a list of lists that represents all the directions from a piece

        Methods:
            playGame
            setupGame
            willflip
            isvalidmove
            getvalidmoves
            coordvalid
            checkgameover
            calculateWinner
    '''

    def __init__(self, player1, player2):
        '''
            Initialises all the attributes of othello
            takes the two players as parameters
        '''

        self.__Board = Board()
        self.__Player1 = player1
        self.__Player2 = player2
        self.__Turn = 1
        self.__movedirections = [[-1,1], [0,1], [1,1], [1,0], [1,-1], [0,-1], [-1,-1], [-1,0]]

    def playGame(self):
        '''
            Method: playGame
            Parameters: None
            Returns: None

            Does: Sets up the game and plays the game until the game is over
        '''

        self.setupGame(1, 2)
        self.__Board.displayBoard()
        print("Black is 1 and White is 2")
        while True:
            if self.checkGameOver():
                self.calculateWinner()
            if self.__Turn % 2 == 1:
                print(f"Black's ({self.__Player1.getName()}) turn")
                validmove = False
                # get the players move
                while not validmove:
                    column = int(input("Enter a column: ")) - 1
                    row = int(input("Enter a row: ")) - 1

                    # check if the move is valid
                    if self.isValidMove(1, column, row) and not self.__Board.isFull():
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

                    # check if the move is valid
                    if self.isValidMove(2, column, row) and not self.__Board.isFull(): # also check if the board doesn't have any moves
                        self.__Board.setBoard(column, row, BoardPiece(self.__Player1.getPieceColour()))
                        validmove = True
                    else:
                        print("Invalid move, try again")

            self.__Turn += 1
            self.__Board.displayBoard()


    def setupGame(self, colour1, colour2):
        '''
            Method: setupGame
            Parameters: colour1, colour2
            Returns: None
            
            Does: Sets up the game with the starting pieces and sets the players piece colour
        '''

        # sets the board up with starting pieces
        self.__Board.fillBoard()

        #sets the players piece colour
        self.__Player1.setPieceColour(colour1)
        self.__Player2.setPieceColour(colour2)

    def willFlip(self, colour, move, dir):
        '''
            Method: willflip
            Parameters: colour, move, dir
            Returns: True or False
            
            Does: Checks if the move will flip any pieces
        '''    

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
    
    def isValidMove(self, colour, col, row):
        '''
            Method: isvalidmove
            Parameters: colour, col, row
            Returns: True or False
            
            Does: Checks if the move is valid
        ''' 

        for mov in self.__movedirections:
            if self.willFlip(colour, [row, col], mov):
                return True
        return False

    def getValidMoves(self,colour):
        '''
            Method: getvalidmoves
            Parameters: colour
            Returns: moves
            
            Does: Gets all the valid moves for a player
        '''
        moves = []
        for i in range(8):
            for j in range(8):
                if self.isValidMove(colour, i, j):
                    moves.append([i,j])
        return moves
    
    def coordValid(self, col, row):
        '''
            Method: coordvalid
            Parameters: col, row
            Returns: True or False
            
            Does: Checks if the coordinates are valid (between 0 and 7)
        '''
        
        if col > 0 and col < 8 and row > 0 and row < 8:
            return True
        return False              

    def checkGameOver(self):
        '''
            Method: checkgameover
            Parameters: None
            Returns: True or False
            
            Does: Checks if the game is over
        '''

        if self.__Board.isFull() and len(self.getValidMoves(1)) == 0 and len(self.getValidMoves(2)) == 0:
            return True
        return False

    def calculateWinner(self): 
        '''
            Method: calculateWinner
            Parameters: None
            Returns: None
        '''

        if self.__Board.getBlackScore() > self.__Board.getWhiteScore():
            print(f"{self.__Player1.getName()} wins!")
        elif self.__Board.getBlackScore() < self.__Board.getWhiteScore():
            print(f"{self.__Player2.getName()} wins!")
        else:
            print("It's a tie!")
        


if __name__ == "__main__":
    
    game = Othello(Player(input("Player 1 enter your name: ")), Player(input("Player 2 enter your name: ")))
    game.playGame()
