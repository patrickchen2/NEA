from player import Player
import time
import random
from computer import Computer
import copy

class Othello:
    def __init__(self, player1, player2, timer, turn):


        self.__Board = [[0 for i in range(8)] for j in range(8)]
        self.__Player1 = player1
        self.__Player2 = player2
        self.__Turn = turn
        self.__movedirections = [[-1,1], [0,1], [1,1], [1,0], [1,-1], [0,-1], [-1,-1], [-1,0]]
        self.__isTimer = False
        self.__p1time = timer
        self.__p2time = timer

    def twoPlayerGame(self):
        '''
            Method: twoPlayerGame
            Parameters: None
            Returns: None
            Does: Runs the game for two players
        '''
        self.setupGame(self.__Board)
        while not self.checkgameover(self.__Board):
            self.displayBoard(self.__Board)
            choice = input("""
1. Play
2. Save
3. Load
4. Quit

""")
            if choice == "1":
                if self.__Turn % 2 == 1:
                    print("White turn")
                    currtime = time.time()
                    valid = False
                    while not valid:
                        column = int(input("enter a column between 0 and 7: "))
                        row = int(input("enter a row between 0 and 7: "))
                        valid, dir = self.isvalidmove(self.__Board, column, row, 1)
                        if not valid:
                            print("Invalid move")
                    self.playGame(self.__Board, column, row, 1, dir)
                    if self.__isTimer:
                        self.__p1time -= time.time() - currtime
                        if self.__p1time <= 0:
                            print("Player 1 ran out of time")
                            print("Player 2 wins!")
                            return None
                else:
                    print("Black turn")
                    currtime = time.time()
                    valid = False
                    while not valid:
                        column = int(input("enter a column between 0 and 7: "))
                        row = int(input("enter a row between 0 and 7: "))
                        valid, dir = self.isvalidmove(self.__Board, column, row, 2)
                        if not valid:
                            print("Invalid move")
                    self.playGame(self.__Board, column, row, 2, dir)
                    if self.__isTimer:
                        self.__p2time -= time.time() - currtime
                        if self.__p2time <= 0:
                            print("Player 2 ran out of time")
                            print("Player 1 wins!")
                            return None

                self.__Turn += 1
            elif choice == "2":
                self.saveGame()
            elif choice == "3":
                self.loadGame()
            elif choice == "4":
                return None
        self.calculateWinner()

    def onePlayerGame(self):
        self.setupGame(self.__Board)
        self.__Player2 = Computer("Computer")
        self.__Player2.setDifficulty(int(input("Enter the difficulty of the computer (1-4): ")))
        while not self.checkgameover(self.__Board):
            self.displayBoard(self.__Board)
            if self.__Turn % 2 == 1:
                print("White turn")
                choice = input("""
1. Play
2. Save
3. Load
4. Quit

""")
                if choice == "1":
                    valid = False
                    while not valid:
                        column = int(input("enter a column between 0 and 7: "))
                        row = int(input("enter a row between 0 and 7: "))
                        valid, dir = self.isvalidmove(self.__Board, column, row, 1)
                        if not valid:
                            print("Invalid move")
                    self.playGame(self.__Board, column, row, 1, dir)
                    self.__Turn += 1
            else:
                print("Computer turn")
                move = self.getValidMoves(self.__Board, 2)
                if self.__Player2.getDifficulty() == 1:
                    #choose a random move from the list of valid moves
                    computermove = random.choice(move)
                if self.__Player2.getDifficulty() == 2:
                    #choose the move which flips the most pieces
                    same = copy.deepcopy(self.__Board)
                    print(same)
                    maxflips = 0
                    computermove = random.choice(move)
                    for mov in move:
                        curr_score = self.getWhiteScore(same)
                        self.playGame(same, mov[0][0], mov[0][1], 2, mov[1])
                        score_diff = self.getWhiteScore(same) - curr_score
                        if score_diff > maxflips:
                            maxflips = score_diff
                            computermove = mov
                        
                if self.__Player2.getDifficulty() == 3:
                    computermove, score = self.minimax(self.__Board, 3, True)
                    print(f"minimax score: {score}")
                self.playGame(self.__Board, computermove[0][0], computermove[0][1], 2, computermove[1])
                self.__Turn += 1
    def setupGame(self,board):
        '''
            Method: setupGame
            Parameters: None
            Returns: None
            Does: Sets up the game by placing the initial pieces
        '''
        board[3][3] = 1
        board[4][4] = 1
        board[3][4] = 2
        board[4][3] = 2
        if self.__p1time == -1:
            self.__isTimer = False
        else:
            self.__isTimer = True

    def getWhiteScore(self, board):
        count = 0
        for row in range(8):
            for col in range(8):
                if board[row][col] == 1:
                    count += 1

        return count
    
    def getBlackScore(self, board):
        count = 0
        for row in range(8):
            for col in range(8):
                if board[row][col] == 2:
                    count += 1
        
        return count

    def playGame(self, board,  col, row, colour, direction):
        if board:
            for dir in direction:
                i = 1
                while True:
                    nextrow = row + i*dir[0]
                    nextcol = col + i*dir[1]
                    if board[nextrow][nextcol] == colour or board[nextrow][nextcol] == 0:
                        break
                    else:
                        board[nextrow][nextcol] = colour
                        i+=1
            board[row][col] = colour
        else:
            for dir in direction:
                i = 1
                while True:
                    nextrow = row + i*dir[0]
                    nextcol = col + i*dir[1]
                    if self.__Board[nextrow][nextcol] == colour or board[nextrow][nextcol] == 0:
                        break
                    else:
                        self.__Board[nextrow][nextcol] = colour
                        i+=1
            self.__Board[row][col] = colour

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
    
    def checkgameover(self, board):
        for row in range(8):
            for col in range(8):
                if board[row][col] == 0:
                    return False
        return True
    
    def calculateWinner(self):
        white = 0
        black = 0
        for row in range(8):
            for col in range(8):
                if self.__Board[row][col] == 1:
                    white += 1
                elif self.__Board[row][col] == 2:
                    black += 1

        if white > black:
            print("White wins!")
        elif black > white:
            print("Black wins!")
        else:
            print("It's a tie!")

    def isvalidmove(self, board, col, row, colour):
        valid = False
        moves = []
        for direction in self.__movedirections:
            if self.willFlip(board, col, row, direction, colour):
                moves.append(direction)
        return len(moves) > 0, moves
    
    def willFlip(self, board, col, row, direction, colour):
        i = 1
        while True:
            newcol = col + i*direction[1]
            newrow = row + i*direction[0]
            if 0<=newcol<=7 and 0<=newrow<=7:
                if board[newrow][newcol] == 0:
                    return False
                elif board[newrow][newcol] == colour:
                    break
                else:
                    i += 1
            else:
                break
        return i > 1
    
    def getValidMoves(self, board, colour):
        moves = []
        for row in range(8):
            for col in range(8):
                if board[row][col] == 0:
                    valid, dir = self.isvalidmove(board, col, row, colour)
                    if valid:
                        moves.append([[col, row], dir])
        return moves
    
    def displayBoard(self, board):
        print("  0 1 2 3 4 5 6 7")
        for i in range(8):
            print(i, end = " ")
            for j in range(8):
                print(board[i][j], end = " ")
            print()

    def saveGame(self):
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
                    f.write(f"{self.__Board[row][col]}")
                f.write("\n")
            print("Game saved")             

    def loadGame(self):
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
                    self.__Board[row][col] = int(line[col])

    def minimax(self, board, depth, ismaximising):
        '''
            Method: minimax
            Parameters: board, depth, ismaximising
            Returns: score
            
            Does: Calculates the score of the board
        '''
        validlocations = self.getValidMoves(board, 2)
        isfinished = (len(self.getValidMoves(board, 1)) == 0) and (len(self.getValidMoves(board, 2)) == 0)
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
                self.playGame(b, mov[0], mov[1], 2, mov[2])
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
                self.playGame(b, mov[0], mov[1], 1, mov[2])
                new_score = self.minimax(b, depth - 1, True)[1]
                if new_score < value:
                    value = new_score
                    col = mov
            return col, value
        
    def startGame(self):
        x = input("1. 2 Player Game\n2. 1 Player Game\n3. Quit\n")
        if x == "2":
            self.twoPlayerGame()
        elif x == "1":
            self.onePlayerGame()
        elif x == "3":
            return None
        
    def getPieceAt(self, col, row):
        self.__Board[row][col]

    def getBoard(self):
        return self.__Board 

    def getTurn(self):
        return self.__Turn
