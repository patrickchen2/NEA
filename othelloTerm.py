from othello import Othello
from player import Player
from computer import Computer
import random
import copy
from othelloGUI import UI

class terminal(UI):
    def __init__(self, player1, player2):
        super().__init__()
        self.__game = Othello(Player(player1), Player(player2), 1)
    def twoPlayerGame(self):
        """
            Method: twoPlayerGame
            Parameters: None
            Returns: None
            Does: Runs the game for two players
        """
        self.__game.setGamemode(2)
        self.__game.setupGame()

        while not self.__game.checkgameover(self.__game.getBoard()):
            self.__game.displayBoard(self.__game.getBoard())
            choice = input("""
1. Play
2. Save
3. Load
4. Quit
                           """)
            if choice == "1":
                if self.__game.getTurn() % 2 == 1:
                    print(f"Black ({self.__game.getPlayer1Name()}) turn")
                    valid = False
                    while not valid:
                        column = int(input("enter a column between 0 and 7: "))
                        row = int(input("enter a row between 0 and 7: "))
                        valid, dir = self.__game.isvalidmove(self.__game.getBoard(), column, row, 1)
                        print(valid, dir)
                        if not valid:
                            print("Invalid move")
                    self.__game.playGame(None, column, row, 1, dir)
                    print(self.__game.getBoard())
                else:
                    print(f"White ({self.__game.getPlayer2Name()}) turn")
                    valid = False
                    while not valid:
                        column = int(input("enter a column between 0 and 7: "))
                        row = int(input("enter a row between 0 and 7: "))
                        valid, dir = self.__game.isvalidmove(self.__game.getBoard(), column, row, 2)
                        if not valid:
                            print("Invalid move")
                    self.__game.playGame(None, column, row, 2, dir)
                self.__game.setTurn(1)
            elif choice == "2":
                self.__game.saveGame()
            elif choice == "3":
                self.__game.loadGame()
            elif choice == "4":
                return None
        white, black = self.__game.calculateWinner()
        print(f"Black: {white}\nWhite: {black}")
        if white > black:
            print(f"{self.__game.getPlayer1Name()} wins!")
        elif black > white:
            print(f"{self.__game.getPlayer2Name()} wins!")
        else:
            print("Tie!")

    def onePlayerGame(self):
        '''
            Method: onePlayerGame
            Parameters: None
            Returns: None
            Does: Runs the game for one player and one computer
        '''
        self.__game.setGamemode(1)
        self.__game.setupGame()
        while not self.__game.checkgameover(self.__game.getBoard()):
            self.__game.displayBoard(self.__game.getBoard())
            if self.__game.getTurn() % 2 == 1:
                print(f"Black ({self.__game.getPlayer1Name()}) turn")
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
                        valid, dir = self.__game.isvalidmove(self.__game.getBoard(), column, row, 1)
                        if not valid:
                            print("Invalid move")
                    self.__game.playGame(None, column, row, 1, dir)
                    self.__game.setTurn(1)
                elif choice == "2":
                    self.__game.saveGame()
                elif choice == "3":
                    self.__game.loadGame()
                elif choice == "4":
                    return None
            else:
                print("Computer turn")
                move = self.__game.getValidMoves(self.__game.getBoard(), 2)
                #print(self.__game.getDifficulty())
                if self.__game.getDifficulty() == 1:
                    #choose a random move from the list of valid moves
                    computermove = random.choice(move)
                if self.__game.getDifficulty() == 2:
                    #choose the move which flips the most pieces
                    same = copy.deepcopy(self.__game.getBoard())
                    print(same)
                    maxflips = 0
                    computermove = random.choice(move)
                    for mov in move:
                        curr_score = self.__game.getWhiteScore(same)
                        self.__game.playGame(same, mov[0][0], mov[0][1], 2, mov[1])
                        score_diff = self.__game.getWhiteScore(same) - curr_score
                        if score_diff > maxflips:
                            maxflips = score_diff
                            computermove = mov
                        
                if self.__game.getDifficulty() == 3:
                    computermove, score = self.__game.minimax(self.__game.getBoard(), 3, True, 2, -100000, 100000)
                    print(f"minimax score: {score}")

                if self.__game.getDifficulty() == 4:
                    computermove, score = self.__game.minimax(self.__game.getBoard(), 5, True, 2, -100000, 100000)
                    print(f"minimax score: {score}")
                self.__game.playGame(None, computermove[0][1], computermove[0][0], 2, computermove[1])
                self.__game.setTurn(1)

        white, black = self.__game.calculateWinner()
        print(f"Black: {white}\nWhite: {black}")
        if white > black:
            print(f"{self.__game.getPlayer1Name()} wins!")
        elif black > white:
            print(f"Computer wins!")
        else:
            print("Tie!")

    def run(self):
        '''
            Method: startGame
            Parameters: None
            Returns: None
            Does: Starts the game
        '''
        x = input("1. 1 Player Game\n2. 2 Player Game\n3. Load Game\n4. Quit\n")
        if x == "2":
            self.twoPlayerGame()
        elif x == "1":
            self.onePlayerGame()
        elif x == "3":
            self.__game.loadGame()
            if self.__game.getGamemode() == 1:
                self.onePlayerGame()
            elif self.__game.getGamemode() == 2:
                self.twoPlayerGame()
            else:
                print("Invalid gamemode")
            return None
        elif x == "4":
            return None
