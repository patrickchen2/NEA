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
        self.help_win = None
        self._game_win = None
        root = tk.Tk()
        root.title("Othello")
        frame = tk.Frame(root)
        frame.pack()

        tk.Button(frame, text="Play", command=self.options).pack(fill=tk.X)
        tk.Button(frame, text="Quit", command=root.quit).pack(fill=tk.X)

        scroll = tk.Scrollbar(frame)
        console = tk.Text(frame, height=4, width=50)
        scroll.pack(side=tk.RIGHT, fill=tk.Y)
        console.pack(side=tk.LEFT, fill=tk.Y)

        scroll.config(command=console.yview)
        console.config(yscrollcommand=scroll.set)

        self._root = root
        self._console = console
    
    def play(self):
        if self._game_win:
            return
        
        self._game = Othello()
        self._finished = False

        game_win = tk.Toplevel(self._root)
        game_win.title("Othello")
        frame = tk.Frame(game_win)

        tk.Grid.rowconfigure(game_win, 0, weight=1)
        tk.Grid.columnconfigure(game_win, 0, weight=1)
        frame.grid(row=0, column=0, sticky=tk.N+tk.S+tk.E+tk.W)

        self._buttons = [[None for _ in range(8)] for  _ in range(8)]

        for row in range(8):
            for col in range(8):
                b = tk.StringVar()
                b.set(self._game.getPieceAt(row, col))

                cmd = lambda r=row, c=col: self._move(r, c)

                tk.Button(frame, textvariable=b, command=cmd, bg="green").grid(row=row, column=col, sticky=tk.N+tk.S+tk.E+tk.W)

                self._buttons[row][col] = b
        
        for i in range(8):
            tk.Grid.rowconfigure(frame, i, weight=1)
            tk.Grid.columnconfigure(frame, i, weight=1)

        tk.Button(game_win, text="Dismiss", command=self.gameClose).grid(row=1, column=0)
        self._game_win = game_win

    def gameClose(self):
        self._game_win.destroy()
        self._game_win = None

    def move(self, row, col):
        
        if self._finished:
            return None
        
        if self._game.getTurn()%2 == 1:
            colour = 1
        else:
            colour = 2
        valid, flip = self._game.isvalidmove(self._game.getBoard(), col, row, 2)
        if valid:
            self._game.playGame(None, col, row, colour, flip)
        
        for row in range(8):
            for col in range(8):
                self._buttons[row][col].set(self._game.getPieceAt(row, col))

        w = self._game.checkgameover(self._game.getBoard())
        if w:
            self._finished = True
            self._console.insert(tk.END, "Game Over!\n")
            if self._game.getWhiteScore() > self._game.getBlackScore():
                self._console.insert(tk.END, "White Wins!")
            elif self._game.getWhiteScore() < self._game.getBlackScore():
                self._console.insert(tk.END, "Black Wins!")

    def run(self):
        self._root.mainloop()

    def options(self):
        timerlabel = tk.Label(self._root, text="timer (-1): ")
        timerentry = tk.Entry(self._root)
        nextbutton = tk.Button(self._root, text="Next", command=self.play)
        timerlabel.grid(row=0, column=0)
        timerentry.grid(row=0, column=1)

        nextbutton.grid(row=1, column=0, columnspan=2)
        self.__timer = timerentry.get()
        
        timerentry.delete(0, tk.END)


ui = GUI()
ui.run()