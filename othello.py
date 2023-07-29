from board import Board
from boardpiece import BoardPiece
from player import Player
import time
import random
from computer import Computer
import copy

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

        self.__Board = Board([[None for x in range(8)] for y in range(8)])
        self.__Player1 = player1
        self.__Player2 = player2
        self.__Turn = turn
        self.__movedirections = [[-1,1], [0,1], [1,1], [1,0], [1,-1], [0,-1], [-1,-1], [-1,0]]
        self.__isTimer = False
        self.__p1time = timer
        self.__p2time = timer

    def twoPlayerGame(self):
        '''
            Method: playGame
            Parameters: None
            Returns: None

            Does: Sets up the game and plays the game until the game is over for two players
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
                if self.__p1time <= 0:
                    canplay = False
                    self.calculateWinner()
                    break
                #display the menu
                if canplay:
                    self.displayMenu()
                    choice = 0
                    while choice not in [1,2,3,4]:
                        choice = int(input("Enter your choice (1,2,3,4): "))
                        if choice not in [1,2,3,4]:
                            print("Invalid choice, try again")
                    if choice == 1:
                        self.playMove(1)
                    elif choice == 2:
                        print("This will override the current game, would you like to continue? (y/n)")
                        inp = input()
                        if inp == "y":
                            self.loadGame()
                    elif choice == 3:
                        self.saveGame()
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
                if self.__p2time <= 0:
                    canplay = False
                    self.calculateWinner()
                    break
                #display the menu
                if canplay:
                    self.displayMenu()
                    choice = 0
                    while choice not in [1,2,3,4]:
                        choice = int(input("Enter your choice (1,2,3,4): "))
                        if choice not in [1,2,3,4]:
                            print("Invalid choice, try again")
                    if choice == 1:
                        self.playMove(2)
                    elif choice == 2:
                        print("This will override the current game, would you like to continue? (y/n)")
                        inp = input()
                        if inp == "y":
                            self.loadGame()
                    elif choice == 3:
                        self.saveGame()
                    elif choice == 4:
                        print("Quitting game")
                        quit = True

            self.__Turn += 1
            self.__Board.displayBoard()

    def onePlayerGame(self):
        ''' 
            Method: playGame
            Parameters: None
            Returns: None

            Does: Sets up the game and plays the game until the game is over for one player
        '''
        self.setupGame(1, 2, True)
        self.__Board.displayBoard()
        print("Your are black (1) and the computer is white (2)")
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
                if self.__p1time <= 0:
                    canplay = False
                    self.calculateWinner()
                    break
                #display the menu
                if canplay:
                    self.displayMenu()
                    choice = 0
                    while choice not in [1,2,3,4]:
                        choice = int(input("Enter your choice (1,2,3,4): "))
                        if choice not in [1,2,3,4]:
                            print("Invalid choice, try again")
                    if choice == 1:
                        self.playMove(1)
                    elif choice == 2:
                        print("This will override the current game, would you like to continue? (y/n)")
                        inp = input()
                        if inp == "y":
                            self.loadGame()
                        self.__Turn -= 1
                    elif choice == 3:
                        self.saveGame()
                        self.__Turn -= 1
                    elif choice == 4:
                        print("Quitting game")
                        quit = True
            else:
                print("Computer's turn")

                canplay = True
                move = self.getValidMoves(2)
                if len(move) == 0:
                    print("No valid moves, skipping turn")
                    self.__Turn += 1
                    canplay = False
                if canplay:
                    if self.__Player2.getDifficulty() == 1:
                        #choose a random move from the list of valid moves
                        computermove = random.choice(move)
                    if self.__Player2.getDifficulty() == 2:
                        #choose the move which flips the most pieces
                        same = copy.deepcopy(self.__Board.getBoard())
                        print(same)
                        maxflips = 0
                        computermove = random.choice(move)
                        for mov in move:
                            curr_score = self.__Board.getWhiteScore()
                            self.doMove(2, mov[0], mov[1], mov[2])
                            score_diff = self.__Board.getWhiteScore() - curr_score
                            if score_diff > maxflips:
                                maxflips = score_diff
                                computermove = mov
                            for row in range(8):
                                for col in range(8):
                                    self.__Board.setBoard(col, row, same[row][col])
                    if self.__Player2.getDifficulty() == 3:
                        computermove, score = self.minimax(self.__Board.boardAsList(), 3, True)
                        print(f"minimax score: {score}")
                

                    print(f"computer move: row: {computermove[0]}, col: {computermove[1]}")
                    self.doMove(2, computermove[0], computermove[1], computermove[2])


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
        if self.__isTimer:
            print(f"you have {self.__p1time if colour == 1 else self.__p2time} seconds left")
            currtime = time.time()

        # get the players move
        validmove = False
        while not validmove:
            column = int(input("Enter a column: "))
            row = int(input("Enter a row: "))

            # check if the move is valid
            valid = self.isValidMove(colour, column, row)[0]

            if valid and not self.__Board.isFull():
                flips = self.isValidMove(colour, column, row)[1]
                self.doMove(colour, column, row, flips)
                validmove = True
            else:
                print("Invalid move, try again")
        if self.__isTimer:
            if colour == 1:
                self.__p1time -= time.time() - currtime
            elif colour == 2:
                self.__p2time -= time.time() - currtime

    def setupGame(self, colour1, colour2, singleplayer = False):
        '''
            Method: setupGame
            Parameters: colour1, colour2
            Returns: None
            
            Does: Sets up the game with the starting pieces and sets the players piece colour
        '''
        if not singleplayer:
            # sets the board up with starting pieces
            self.__Board.fillBoard()

            #sets the players piece colour
            self.__Player1.setPieceColour(colour1)
            self.__Player2.setPieceColour(colour2)
            if input("Would you like to play with a timer? (y/n): ") == "y":
                self.__isTimer = True
        else:
            self.__Board.fillBoard()
            self.__Player1.setPieceColour(colour1)
            self.__Player2 = Computer("computer")
            self.__Player2.setPieceColour(colour2)
            if input("Would you like to play with a timer? (y/n): ") == "y":
                self.__isTimer = True
            print("""Select the difficulty of the computer
            1. Easy
            2. Medium
            3. Hard""")
            choice = int(input("Enter your choice (1,2,3): "))
            self.__Player2.setDifficulty(choice)

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
            
            Does: Checks if the move is valid and in what direction
        ''' 
        moves = []
        for mov in self.__movedirections:
            if self.willFlip(colour, [row, col], mov) and self.__Board.getBoardPiece(col, row) == 0:
                moves.append(mov)
        return len(moves) > 0, moves

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
                if self.isValidMove(colour, i, j)[0]:
                    moves.append([i,j, self.isValidMove(colour, i, j)[1]])
        return moves
    
    def coordValid(self, col, row):
        '''
            Method: coordvalid
            Parameters: col, row
            Returns: True or False
            
            Does: Checks if the coordinates are valid (between 0 and 7)
        '''
        
        if 0 <= col <= 7 and 0 <= row <= 7:
            return True
        else:
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
    
    def doMove(self, colour, col, row, dir):
        '''
            Method: doMove
            Parameters: colour, col, row, dir
            Returns: None
            
            Does: Plays the move for a player
        '''
        if colour == 1:
            piece = BoardPiece(self.__Player1.getPieceColour())
        else:
            piece = BoardPiece(self.__Player2.getPieceColour())
        self.__Board.setBoard(col, row, piece)
        # search for next piece of the same color and flip anything between
        for direction in dir:
            i = 1
            while True:
                nextcol = col + direction[1] * i
                nextrow = row + direction[0] * i
                if self.coordValid(nextcol, nextrow):
                    #if next piece is the same colour, break
                    if self.__Board.getBoardPiece(nextcol, nextrow) == colour or self.__Board.getBoardPiece(nextcol, nextrow) == 0:
                        break
                        
                    #if next piece is different colour, flip it
                    else:
                        self.__Board.setBoard(nextcol, nextrow, piece)
                        i += 1
                else:
                    break

    def saveGame(self):
        '''
            Method: saveGame
            Parameters: None
            Returns: None

            Does: Saves the game to a file
            file format:
                player1 name
                player2 name
                turn
                player1 time
                player2 time
                board(8x8)
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
            
        with open(f"game{choice}.txt", "w") as f:
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
            file format:
                player1 name
                player2 name
                turn
                player1 time
                player2 time
                board(8x8)
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
        
        with open(f"game{choice}.txt", "r") as f:
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
 
    def playGame(self, singleplayer = False):
        '''
            Method: playGame
            Parameters: None
            Returns: None
            
            Does: Plays the game
        '''
        if singleplayer:
            self.onePlayerGame()
        else:
            self.twoPlayerGame()

    def calculateScore(self, board, colour):
        '''
            Method: calculateScore
            Parameters: board, colour, row, col
            Returns: score

            Does: Calculates the score of the board for a certain player
        '''

        matrix = [[100, -10, 11, 6, 6, 11, -10, 100],
                  [-10, -20, 1, 2, 2, 1, -20, -10],
                  [11, 1, 5, 4, 4, 5, 1, 11],
                  [6, 2, 4, 2, 2, 4, 2, 6],
                  [6, 2, 4, 2, 2, 4, 2, 6],
                  [11, 1, 5, 4, 4, 5, 1, 11],
                  [-10, -20, 1, 2, 2, 1, -20, -10],
                  [100, -10, 11, 6, 6, 11, -10, 100]]
        score = 0
        for row in range(8):
            for col in range(8):
                if board[row][col] == colour:
                    score += matrix[row][col]
                elif board[row][col] == 0:
                    pass
                else:
                    score -= matrix[row][col]
        print(score)
        return score
    
    def getValidMovesList(self, board, colour):
        '''
            Method: getValidMovesList
            Parameters: board, colour
            Returns: moves

            Does: Gets all the valid moves for a player
        '''
        moves = []
        for i in range(8):
            for j in range(8):
                if self.isValidMoveList(board, colour, i, j)[0] and board[i][j] == 0:
                    moves.append([i,j, self.isValidMoveList(board, colour, i, j)[1]])
        return moves

    def isValidMoveList(self, board, colour, col, row):
        '''
            Method: isvalidmove
            Parameters: colour, col, row
            Returns: True or False

            Does: Checks if the move is valid and in what direction
        '''
        moves = []
        for mov in self.__movedirections:
            if self.willFlipList(board, colour, [row, col], mov):
                moves.append(mov)
        return len(moves) > 0, moves
    
    def willFlipList(self, board, colour, move, dir):
        i = 1
        while True:
            nextcol = move[1] + dir[1] * i
            nextrow = move[0] + dir[0] * i
            if self.coordValid(nextcol, nextrow):
                # if the next piece is the same colour, break
                if board[nextrow][nextcol] == colour:
                    break
                # if the next piece is empty, return false
                elif board[nextrow][nextcol] == 0:
                    return False
                # if the next piece is the opposite colour, continue
                else:
                    i += 1
            else:
                break
        return i > 1
    
    def doMoveList(self, colour, board, col, row, dir): 
        if colour == 1:
            piece = 1
        else:
            piece = 2
        board[row][col] = piece
        # search for next piece of the same color and flip anything between
        for direction in dir:
            i = 1
            while True:
                nextcol = col + direction[1] * i
                nextrow = row + direction[0] * i
                if self.coordValid(nextcol, nextrow):
                    #if next piece is the same colour, break
                    if board[nextrow][nextcol] == colour or board[nextrow][nextcol] == 0:
                        break
                        
                    #if next piece is different colour, flip it
                    else:
                        board[nextrow][nextcol] = piece
                        i += 1
                else:
                    break

    def minimax(self, board, depth, ismaximising):
        '''
            Method: minimax
            Parameters: board, depth, ismaximising
            Returns: score
            
            Does: Calculates the score of the board
        '''
        validlocations = self.getValidMovesList(board, 2)
        isfinished = (len(self.getValidMovesList(board, 1)) == 0) and (len(self.getValidMovesList(board, 2)) == 0)
        if depth == 0 or isfinished:
            if isfinished:
                # calculate who won that simulation
                blackcount = 0
                whitecount = 0
                for row in range(8):
                    for col in range(8):
                        if board[row][col] == 1:
                            blackcount += 1
                        elif board[row][col] == 2:
                            whitecount += 1
                
                if whitecount > blackcount:
                    return None, 100000000000000
                elif blackcount > whitecount:
                    return None, -10000000000000
                else:
                    return None, 0
            else:
                return None, self.calculateScore(board, 2)
            
        if ismaximising:
            value = -100000000000000
            move = random.choice(validlocations)
            for mov in validlocations:
                b = copy.deepcopy(board)
                self.doMoveList(2, b, mov[0], mov[1], mov[2])
                new_score = self.minimax(b, depth - 1, False)[1]
                if new_score > value:
                    value = new_score
                    move = mov
            return move, value
        else:
            value = 100000000000000
            col = random.choice(validlocations)
            for mov in validlocations:
                b = copy.deepcopy(board)
                self.doMoveList(1, b, mov[0], mov[1], mov[2])
                new_score = self.minimax(b, depth - 1, True)[1]
                if new_score < value:
                    value = new_score
                    col = mov
            return col, value



if __name__ == "__main__":
    a = input("single player? (y/n): ")
    if a == "y":
        game = Othello(Player(input("Player 1 enter your name: ")), Player("computer"), 180, 1)
        game.playGame(True)
    else:
        game = Othello(Player(input("Player 1 enter your name: ")), Player(input("Player 2 enter your name: ")), 180, 1)
        game.playGame(False)
