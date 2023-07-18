from board import Board
from boardpiece import BoardPiece
from player import Player
import time

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

    def __init__(self, player1, player2, timer, turn):
        '''
            Initialises all the attributes of othello
            takes the two players as parameters
        '''

        self.__Board = Board()
        self.__Player1 = player1
        self.__Player2 = player2
        self.__Turn = turn
        self.__movedirections = [[-1,1], [0,1], [1,1], [1,0], [1,-1], [0,-1], [-1,-1], [-1,0]]
        self.__p1time = timer
        self.__p2time = timer

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
        quit = False
        while True:
            if self.checkGameOver():
                self.calculateWinner()
                break
            if quit == True:
                break

            if self.__Turn % 2 == 1:
                print(f"Black's ({self.__Player1.getName()}) turn")

                # if there are no valid moves, then skip their turn
                canplay = True
                move = self.getValidMoves(1)
                if len(move) == 0:
                    print("No valid moves, skipping turn")
                    self.__Turn += 1
                    canplay = False
                
                #display the menu
                if canplay:
                    self.displayMenu()
                    choice = int(input("Enter your choice (1,2,3,4): "))
                    if choice == 1:
                        self.playMove(1)
                    elif choice == 2:
                        print("This will override the current game, would you like to continue? (y/n)")
                        inp = input()
                        if inp == "y":
                            self.loadGame()
                    elif choice == 3:
                        self.saveGame
                    elif choice == 4:
                        print("Quitting game")
                        quit = True
            else:
                print(f"White's ({self.__Player2.getName()}) turn")

                # if there are no valid moves, then skip their turn
                canplay = True
                move = self.getValidMoves(2)
                if len(move) == 0:
                    print("No valid moves, skipping turn")
                    self.__Turn += 1
                    canplay = False
                
                #display the menu
                if canplay:
                    self.displayMenu()
                    choice = int(input("Enter your choice (1,2,3,4): "))
                    if choice == 1:
                        self.playMove(2)
                    elif choice == 2:
                        print("This will override the current game, would you like to continue? (y/n)")
                        inp = input()
                        if inp == "y":
                            self.loadGame()
                    elif choice == 3:
                        self.saveGame
                    elif choice == 4:
                        print("Quitting game")
                        quit = True

            self.__Turn += 1
            self.__Board.displayBoard()

    def playMove(self, colour):
        '''
            Method: playMove
            Parameters: colour
            Returns: None
            
            Does: Plays a move for a player
        '''
        #display how much time they have left
        print(f"you have {self.__p1time if colour == 1 else self.__p2time} seconds left")
        currtime = time.time()

        # get the players move
        validmove = False
        while not validmove:
            column = int(input("Enter a column: ")) - 1
            row = int(input("Enter a row: ")) - 1

            # check if the move is valid
            if self.isValidMove(colour, column, row) and not self.__Board.isFull():
                if colour == 1:
                    self.__Board.setBoard(column, row, BoardPiece(self.__Player1.getPieceColour()))
                elif colour == 2:
                    self.__Board.setBoard(column, row, BoardPiece(self.__Player2.getPieceColour()))
                validmove = True
            else:
                print("Invalid move, try again")
        if colour == 1:
            self.__p1time -= time.time() - currtime
        elif colour == 2:
            self.__p2time -= time.time() - currtime


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
            if self.coordValid(nextcol, nextrow):
                # if the next piece is the same colour, break
                if self.__Board.getBoardPiece(nextcol, nextrow) == colour:
                    break
                # if the next piece is empty, return false
                elif self.__Board.getBoardPiece(nextcol, nextrow) == 0:
                    return False
                # if the next piece is the opposite colour, continue
                else:
                    i += 1
            else:
                break
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

    def checkGameOver(self,):
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

            Does: Calculates the winner of the game
        '''

        if self.__Board.getBlackScore() > self.__Board.getWhiteScore():
            print(f"{self.__Player1.getName()} wins!")
        elif self.__Board.getBlackScore() < self.__Board.getWhiteScore():
            print(f"{self.__Player2.getName()} wins!")
        else:
            print("It's a tie!")

    def saveGame(self):
        '''
            Method: saveGame
            Parameters: None
            Returns: None

            Does: Saves the game to a file
        '''

        validchoice = False
        while not validchoice:
            choice = int(input("choose which file you want to save to (1, 2, 3, 4 to cancel): "))
            if choice in [1,2,3]:
                validchoice = True
            elif choice == 4:
                return None
            else:
                print("Invalid choice, try again")
            
        with open(f"save{choice}.txt", "w") as f:
            f.write(f"{self.__Player1.getName()}\n")
            f.write(f"{self.__Player2.getName()}\n")
            f.write(f"{self.__Turn}\n")
            f.write(f"{self.__p1time}\n")
            f.write(f"{self.__p2time}\n")
            for row in range(8):
                for col in range(8):
                    f.write(f"{self.__Board.getBoardPiece(col, row)}")
                f.write("\n")
            print("Game saved")

    def loadGame(self):
        '''
            Method: loadGame
            Parameters: None
            Returns: None
            
            Does: Loads the game from a file
        '''

        validchoice = False
        while not validchoice:
            choice = int(input("choose which file you want to save to (1, 2, 3, 4 to cancel): "))
            if choice in [1,2,3]:
                validchoice = True
            elif choice == 4:
                return None
            else:
                print("Invalid choice, try again")
        
        with open(f"save{choice}.txt", "r") as f:
            self.__Player1.setName(f.readline().strip())
            self.__Player2.setName(f.readline().strip())
            self.__Turn = int(f.readline().strip())
            self.__p1time = int(f.readline().strip())
            self.__p2time = int(f.readline().strip())
            for row in range(8):
                line = f.readline().strip()
                for col in range(8):
                    self.__Board.setBoard(col, row, BoardPiece(int(line[col])))
            print("Game loaded")

    def displayMenu(self):
        '''
            Method: displayMenu
            Parameters: None
            Returns: None
            
            Does: Displays the menu
        '''

        print("1. Play game")
        print("2. Load game")
        print("3. Save game")
        print("4. Quit")
        


if __name__ == "__main__":
    
    game = Othello(Player(input("Player 1 enter your name: ")), Player(input("Player 2 enter your name: ")), 180, 1)
    game.playGame()
