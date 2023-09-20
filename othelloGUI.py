import tkinter as tk
from abc import ABC, abstractmethod
from othello import Othello
from player import Player

class UI(ABC):
    @abstractmethod
    def run(self):
        raise NotImplementedError
    
class GUI(UI):
    def __init__(self):
        self.timerentry = -1
        self.help_win = None
        self._game_win = None
        root = tk.Tk()
        root.title("Othello")


        tk.Button(root, text="Play", command=self.options).grid(row=0, column=0)
        tk.Button(root, text="Quit", command=root.quit).grid(row=0, column=1)


        self._root = root
    
    def play(self):
        if self._game_win:
            return
        self._timer = self.timerentry.get()
        self._player1 = self.player1entry.get()
        self._player2 = self.player2entry.get()

        self._game = Othello(self._player1, self._player2, self._timer, 1)
        self._game.setupGame(None)
        print(self._game.getBoard())
        self._finished = False

        game_win = tk.Toplevel(self._root)
        game_win.title("Othello")
        #game_win.geometry("500x500")

        tk.Grid.rowconfigure(game_win, 0, weight=1)
        tk.Grid.columnconfigure(game_win, 0, weight=1)
        self.c = tk.Canvas(game_win, width=800, height=800, bg="dark green")
        self.c.grid(row = 0, column = 0, padx= 5, pady=5, sticky=tk.N+tk.S+tk.E+tk.W)
        self.c.bind("<Button-1>", self.move)
        self.displayBoard(game_win)

    def displayBoard(self, window):
        ratio = 800/8
        for i in range(8):
            self.c.create_line(0, i*ratio, 800, i*ratio)
            self.c.create_line(i*ratio, 0, i*ratio, 800)

        board = self._game.getBoard()
        for row in range(8):
            for col in range(8):
                if board[row][col]:
                    if board[row][col] == 1:
                        self.c.create_oval(col*ratio, row*ratio, (col+1)*ratio, (row+1)*ratio, fill="black")
                    else:
                        self.c.create_oval(col*ratio, row*ratio, (col+1)*ratio, (row+1)*ratio, fill="white")



        

    def gameClose(self):
        self._game_win.destroy()
        self._game_win = None

    def move(self, event):
        if self._game.getTurn()%2 == 1:
            colour = 1
        else:
            colour = 2
        x,y = event.x, event.y
        ratio = 800/8
        try:
            x = int(x//ratio)
            y = int(y//ratio)
        except Exception as e:
            print(e)
        valid, dir = self._game.isvalidmove(self._game.getBoard(), x, y, colour)
        self._game.playGame(self._game.getBoard(), x, y, colour, dir)
        self._game.setTurn(1)
        self.displayBoard(self._game_win)
    
    def run(self):
        self._root.mainloop()

    def options(self):
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
        
        timerlabel = tk.Label(newwindow, text="timer (-1): ")
        timerlabel.grid(row=2, column=0)
        self.timerentry = tk.Entry(newwindow, width = 60)
        self.timerentry.grid(row=2, column=1)

        nextbutton = tk.Button(newwindow, text="Next", command=self.play)
        nextbutton.grid(row=3, column=0, columnspan=2)
        #timerlabel.grid(row=0, column=0)
        #timerentry.grid(row=0, column=1)
        #nextbutton.grid(row=1, column=0, columnspan=2)

        



ui = GUI()
ui.run()