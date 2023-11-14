import tkinter as tk
from abc import ABC, abstractmethod
from othello import Othello
from player import Player
from computer import Computer
import tkinter.messagebox as messagebox
import copy
import random
import time
class UI(ABC):
    @abstractmethod
    def run(self):
        raise NotImplementedError
    
class GUI(UI):
    def __init__(self):
        self.help_win = None
        self._game_win = None
        self.__boards = []
        root = tk.Tk()
        root.title("Othello")
        root.geometry("300x300")

        tk.Button(root, text="Multi Player", command=self.options1).grid(row=0, column=0, padx=5, pady=5, columnspan = 5)
        tk.Button(root, text="Single Player", command=self.options2).grid(row=1, column=0, padx=5, pady=5, columnspan = 5)
        tk.Button(root, text="Quit", command=root.quit).grid(row=2, column=0, padx=5, pady=5, columnspan = 5)


        self._root = root
    
    def play1(self):
        if self._game_win:
            return
        self._player1 = self.player1entry.get()
        self._player2 = self.player2entry.get()

        self._game = Othello(self._player1, self._player2, 1)
        self._game.setupGame()
        self.__boards.append(copy.deepcopy(self._game.getBoard()))
        self._finished = False

        self._game_win = tk.Toplevel(self._root)
        self._game_win.title("Othello")
        #game_win.geometry("500x500")
        
        self.canvassize = 700
        tk.Grid.rowconfigure(self._game_win, 0, weight=1)
        tk.Grid.columnconfigure(self._game_win, 0, weight=1)
        self.c = tk.Canvas(self._game_win, width=self.canvassize, height=self.canvassize, bg="dark green")
        self.c.grid(row = 0, column = 0, padx= 5, pady=5, sticky=tk.N+tk.S+tk.E+tk.W)
        self.c.bind("<Button-1>", self.move)

        self.indicator = tk.Label(self._game_win, text="Black's Turn")
        self.indicator.grid(row = 0, column = 2, padx= 5, pady=5, sticky=tk.N+tk.S+tk.E+tk.W)

        self.t = tk.Text(self._game_win, height=2, width=30)
        self.t.grid(row = 0, column = 1, padx= 5, pady=5, sticky=tk.N+tk.S+tk.E+tk.W)

        self.u = tk.Button(self._game_win, text = "Undo", command = self.undo)
        self.u.grid(row=1, column=0, columnspan=5)
        self.quitbutton = tk.Button(self._game_win, text="Quit", command=self.gameClose)
        self.quitbutton.grid(row=2, column=0, columnspan=5)
        self.displayBoard(self._game_win)

    def displayBoard(self, window):
        ratio = self.canvassize/8
        self.c.delete("all")
        for i in range(8):
            self.c.create_line(0, i*ratio, self.canvassize, i*ratio)
            self.c.create_line(i*ratio, 0, i*ratio, self.canvassize)
        #getting the borders of the board
        self.c.create_line(0, self.canvassize, self.canvassize, self.canvassize)
        self.c.create_line(0, 0, 0, self.canvassize)
        self.c.create_line(self.canvassize, 0, self.canvassize, self.canvassize)
        self.c.create_line(0, 0, self.canvassize, 0)

        board = self._game.getBoard()
        for row in range(8):
            for col in range(8):
                if board[row][col]:
                    if board[row][col] == 1:
                        self.c.create_oval(col*ratio, row*ratio, (col+1)*ratio, (row+1)*ratio, fill="black")
                    else:
                        self.c.create_oval(col*ratio, row*ratio, (col+1)*ratio, (row+1)*ratio, fill="white")

        #display valid moves
        if self.validbutton.cget("text") == "Enabled":  
            if self._game.getTurn()%2 == 1: # black
                validlocations = self._game.getValidMoves(board, 1)
            else:
                validlocations = self._game.getValidMoves(board, 2)
            for location in validlocations:
                self.c.create_oval(location[0][1]*ratio, location[0][0]*ratio, (location[0][1]+1)*ratio, (location[0][0]+1)*ratio, fill="grey")

    def gameClose(self):
        self._game_win.quit()

    def undo(self):
        if len(self.__boards) > 1:
            self.__boards.pop()
            self._game.setBoard(copy.deepcopy(self.__boards[-1]))
            self._game.setTurn(-1)
            if self._game.getGamemode() == 1:
                self._game.setTurn(-1)
            if self._game.getTurn()%2 == 1:
                self.indicator.config(text="Black's Turn")
            else:
                self.indicator.config(text="White's Turn")
            self.c.delete("all")
            self.displayBoard(self._game_win)
        else:
            pass

    def move(self, event):
        if self._game.getTurn()%2 == 1:
            colour = 1
        else:
            colour = 2
        x,y = event.x, event.y
        ratio = self.canvassize/8
        try:
            x = int(x//ratio)
            y = int(y//ratio)
        except Exception as e:
            print(e)
        valid, dir = self._game.isvalidmove(self._game.getBoard(), x, y, colour)
        if valid:
            self._game.playGame(None, x, y, colour, dir)
            if colour == 1:
                self.t.insert(tk.END, self._player1 + ": " + str(x) + "," + str(y) + "\n")
                self.indicator.config(text="White's Turn")
            elif colour == 2:
                self.t.insert(tk.END, self._player2 + ": " + str(x) + "," + str(y) + "\n")
                self.indicator.config(text="Black's Turn")
            self.__boards.append(copy.deepcopy(self._game.getBoard()))
            self._game.setTurn(1)
        else:
            #messagebox.showinfo("Invalid Move", "Invalid Move")
            pass
        if self._game.checkgameover(self._game.getBoard()):
            self.displayBoard(self._game_win)
            self.gameClose()
            game_win = None
            messagebox.showinfo("Game Over", "Game Over")    
        self.displayBoard(self._game_win)
    
    def run(self):
        self._root.mainloop()

    def options1(self):
        newwindow = tk.Toplevel(self._root)
        newwindow.title("Options")
        newwindow.geometry("300x300")
        
        player1label = tk.Label(newwindow, text="Player 1: ")
        player1label.grid(row=0, column=0)
        self.player1entry = tk.Entry(newwindow, width = 60)
        self.player1entry.grid(row=0, column=1)

        player2label = tk.Label(newwindow, text="Player 2: ")
        player2label.grid(row=1, column=0)
        self.player2entry = tk.Entry(newwindow, width = 60)
        self.player2entry.grid(row=1, column=1)

        self.validlabel = tk.Label(newwindow, text="Valid Moves: ")
        self.validlabel.grid(row=2, column=0)
        self.validbutton = tk.Button(newwindow, text="Disabled", command=self.valids, bg="red")
        self.validbutton.grid(row=2, column=1, columnspan=2)

        nextbutton = tk.Button(newwindow, text="Next", command=self.play1)
        nextbutton.grid(row=3, column=0, columnspan=2)

    def options2(self):
        option2 = tk.Toplevel(self._root)
        option2.title("Options")
        option2.geometry("300x300")

        player1label = tk.Label(option2, text="Player 1: ")
        player1label.grid(row=0, column=0)
        self.player1entry = tk.Entry(option2, width = 60)
        self.player1entry.grid(row=0, column=1)

        difficultlabel = tk.Label(option2, text="Difficulty: ")
        difficultlabel.grid(row=1, column=0)
        self.difficultentry = tk.Entry(option2, width = 60)
        self.difficultentry.grid(row=1, column=1)

        self.validlabel = tk.Label(option2, text="Valid Moves: ")
        self.validlabel.grid(row=2, column=0)
        self.validbutton = tk.Button(option2, text="Disabled", command=self.valids, bg="red")
        self.validbutton.grid(row=2, column=1, columnspan=2)

        self.hintlabel = tk.Label(option2, text="Hint: ")
        self.hintlabel.grid(row=3, column=0)
        self.hintbutton = tk.Button(option2, text="Disabled", command=self.hints, bg="red")
        self.hintbutton.grid(row=3, column=1, columnspan=2)

        nextbutton = tk.Button(option2, text="Next", command=self.play2)
        nextbutton.grid(row=4, column=0, columnspan=2)

    def valids(self):
        if self.validbutton.cget("text") == "Disabled":
            self.validbutton.config(text="Enabled", bg="green")
        else:
            self.validbutton.config(text="Disabled", bg="red")

    def hints(self):
        if self.hintbutton.cget("text") == "Disabled":
            self.hintbutton.config(text="Enabled", bg="green")
        else:
            self.hintbutton.config(text="Disabled", bg="red")
    
    def play2(self):
        if self._game_win:
            return
        self._player1 = self.player1entry.get()
        self._player2 = "Computer"
        try:
            self._difficulty = int(self.difficultentry.get())
        except:
            self._difficulty = 1
        
        self._game = Othello(self._player1, Computer(self._player2), 1)
        self._game.setDifficult(self._difficulty)
        self._game.setupGame()
        self._game.setGamemode(1)
        self.__boards.append(copy.deepcopy(self._game.getBoard()))
        self._finished = False

        self._game_win = tk.Toplevel(self._root)
        self._game_win.title("Othello")
        #game_win.geometry("500x500")
        
        self.canvassize = 700
        tk.Grid.rowconfigure(self._game_win, 0, weight=1)
        tk.Grid.columnconfigure(self._game_win, 0, weight=1)
        self.c = tk.Canvas(self._game_win, width=self.canvassize, height=self.canvassize, bg="dark green")
        self.c.grid(row = 0, column = 0, padx= 5, pady=5, sticky=tk.N+tk.S+tk.E+tk.W)
        self.c.bind("<Button-1>", self.move2)

        self.indicator = tk.Label(self._game_win, text="Player 1 Turn")
        self.indicator.grid(row = 0, column = 2, padx= 5, pady=5, sticky=tk.N+tk.S+tk.E+tk.W)

        self.t = tk.Text(self._game_win, height=2, width=30)
        self.t.grid(row = 0, column = 1, padx= 5, pady=5, sticky=tk.N+tk.S+tk.E+tk.W)

        self.u = tk.Button(self._game_win, text = "Undo", command = self.undo)
        self.u.grid(row=1, column=0, columnspan=5)

        self.quitbutton = tk.Button(self._game_win, text="Quit", command=self.gameClose)
        self.quitbutton.grid(row=2, column=0, columnspan=5)

        self.savebutton = tk.Button(self._game_win, text="Save", command=self.saveGame)
        self.savebutton.grid(row=1, column=1, columnspan=2)

        self.loadbutton = tk.Button(self._game_win, text="Load", command=self.loadGame)
        self.loadbutton.grid(row=1, column=3, columnspan=2)
        self.displayBoard(self._game_win)

    def saveGame(self):
        savewindow = tk.Toplevel(self._game_win)
        savewindow.title("Save Game")
        savewindow.geometry("300x300")
        

    def move2(self, event):
        if self._game.getTurn()%2 == 1:
            colour = 1
        else:
            colour = 2
        x,y = event.x, event.y
        ratio = self.canvassize/8
        try:
            x = int(x//ratio)
            y = int(y//ratio)
        except Exception as e:
            print(e)
        valid, dir = self._game.isvalidmove(self._game.getBoard(), x, y, colour)
        if valid:
            self._game.playGame(None, x, y, colour, dir)

            self.t.insert(tk.END, self._player1 + ": " + str(x) + "," + str(y) + "\n")
            self.indicator.config(text="Computer Turn")

            self.displayBoard(self._game_win)

            self._root.update()
            self._root.update_idletasks()
            #computer's turn
            if colour == 1:
                computercolour = 2
            else:
                computercolour = 1
            computermove = self.computermove()
            print(computermove)
            self._game.playGame(None, computermove[0][1], computermove[0][0], computercolour, computermove[1])
            self.__boards.append(copy.deepcopy(self._game.getBoard()))
            
            if self._game.getDifficulty() == 1:
                time.sleep(0.5)

            self.t.insert(tk.END, self._player2 + ": " + str(x) + "," + str(y) + "\n")
            self.indicator.config(text="Player 1 Turn")
            self._game.setTurn(2)
            self.displayBoard(self._game_win)
        else:
            #messagebox.showinfo("Invalid Move", "Invalid Move")
            pass
        if self._game.checkgameover(self._game.getBoard()):
            self.displayBoard(self._game_win)
            self.gameClose()
            game_win = None
            messagebox.showinfo("Game Over", "Game Over")      
    
    def computermove(self):
        move = self._game.getValidMoves(self._game.getBoard(), 2)
        #print(self.__game.getDifficulty())
        if self._game.getDifficulty() == 1:
            #choose a random move from the list of valid moves
            computermove = random.choice(move)
        if self._game.getDifficulty() == 2:
            #choose the move which flips the most pieces
            same = copy.deepcopy(self._game.getBoard())
            maxflips = 0
            computermove = random.choice(move)
            for mov in move:
                curr_score = self._game.getWhiteScore(same)
                self._game.playGame(same, mov[0][0], mov[0][1], 2, mov[1])
                score_diff = self._game.getWhiteScore(same) - curr_score
                if score_diff > maxflips:
                    maxflips = score_diff
                    computermove = mov
                
        if self._game.getDifficulty() == 3:
            computermove, score = self._game.minimax(self._game.getBoard(), 3, True, 2, -100000, 100000)
            print(f"minimax score: {score}")
        return computermove

ui = GUI()
ui.run()